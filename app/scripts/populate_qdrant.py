
import logging
import os
from pathlib import Path
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Tuple
import pickle
from tqdm import tqdm
from app.infrastructure.clip_model import CLIPModelWrapper
from app.infrastructure.qdrant_client import QdrantClientWrapper
from app.utils.exceptions import QdrantError, EmbeddingGenerationError
from qdrant_client.http.models import PointStruct
import torch

def process_image(image_path: str, animal_name: str, point_id: int) -> Tuple[int, list, dict]:
    """Обрабатывает одно изображение и возвращает данные для Qdrant."""
    logger = logging.getLogger(__name__)
    logger.info(f"Processing image: {image_path}")
    try:
        clip_model = CLIPModelWrapper()
        image = Image.open(image_path).convert("RGB")
        embedding = clip_model.generate_embedding(image)
        logger.info(f"Generated embedding for {image_path}, length: {len(embedding)}")
        return point_id, embedding, {"animal_name": animal_name}
    except Exception as e:
        logger.error(f"Failed to process image {image_path}: {str(e)}")
        return None

def populate_qdrant(data_dir: str = "/app/data/animals-10/raw-img", batch_size: int = 100, max_workers: int = None, limit_images: int = None):
    logger = logging.getLogger(__name__)
    logger.info(f"Starting Qdrant population from {data_dir} with batch_size={batch_size}, max_workers={max_workers}, limit_images={limit_images}")

    use_gpu = torch.cuda.is_available()
    logger.info(f"Using GPU: {use_gpu}")

    max_workers = max_workers or os.cpu_count() or 8
    logger.info(f"Using {max_workers} workers")

    try:
        qdrant_client = QdrantClientWrapper()

        data_path = Path(data_dir)
        if not data_path.exists():
            logger.error(f"Dataset directory {data_dir} does not exist")
            raise FileNotFoundError(f"Directory {data_dir} not found")

        try:
            qdrant_client.create_collection()
            logger.info("Qdrant collection created or already exists")
        except QdrantError as e:
            logger.error(f"Failed to create collection: {str(e)}")
            raise

        try:
            points_count = qdrant_client.client.count(collection_name="animals").count
            expected_count = limit_images or 100
            logger.info(f"Current points in Qdrant: {points_count}, expected: {expected_count}")
            if points_count >= expected_count:
                logger.info(f"Qdrant already contains {points_count} points, skipping population")
                return
        except Exception as e:
            logger.warning(f"Failed to check Qdrant points count: {str(e)}")

        cache_path = Path("/app/data/animals-10/embeddings_cache.pkl")
        image_tasks = []
        if cache_path.exists():
            logger.info("Loading embeddings from cache")
            with cache_path.open("rb") as f:
                image_tasks = pickle.load(f)
            logger.info(f"Loaded {len(image_tasks)} tasks from cache")
        else:
            logger.info(f"No cache found at {cache_path}, collecting images")
            point_id = 1
            for animal_folder in data_path.iterdir():
                if not animal_folder.is_dir():
                    logger.debug(f"Skipping non-directory: {animal_folder}")
                    continue
                animal_name = animal_folder.name.lower()
                logger.info(f"Collecting images for animal: {animal_name}")
                images = list(animal_folder.glob("*.jpeg"))  # Изменено на *.jpeg
                logger.info(f"Found {len(images)} images in {animal_folder}")
                for image_path in images:
                    image_tasks.append((str(image_path), animal_name, point_id))
                    point_id += 1
                    if limit_images and point_id > limit_images:
                        break
                if limit_images and point_id > limit_images:
                    break
            logger.info(f"Collected {len(image_tasks)} images to process")
            with cache_path.open("wb") as f:
                pickle.dump(image_tasks, f)
                logger.info(f"Saved {len(image_tasks)} tasks to cache")

        if not image_tasks:
            logger.error("No images found to process, exiting")
            return

        if limit_images:
            image_tasks = image_tasks[:limit_images]
            logger.info(f"Limited to {len(image_tasks)} images")

        total_points = 0
        for i in tqdm(range(0, len(image_tasks), batch_size), desc="Processing batches"):
            batch = image_tasks[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} with {len(batch)} images")

            points = []
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                future_to_task = {
                    executor.submit(process_image, task[0], task[1], task[2]): task
                    for task in batch
                }
                for future in as_completed(future_to_task):
                    result = future.result()
                    if result:
                        point_id, embedding, metadata = result
                        points.append(PointStruct(id=point_id, vector=embedding, payload=metadata))
                    else:
                        logger.warning(f"Skipping failed image in batch {i//batch_size + 1}")

            if points:
                logger.info(f"Prepared {len(points)} points for upsert")
                try:
                    qdrant_client.upsert(collection_name="animals", points=points)
                    total_points += len(points)
                    logger.info(f"Upserted {len(points)} points in batch {i//batch_size + 1}")
                except QdrantError as e:
                    logger.error(f"Failed to upsert batch: {str(e)}")
                    continue
            else:
                logger.warning(f"No points generated for batch {i//batch_size + 1}")

        logger.info(f"Qdrant population completed. Added {total_points} points")
    except Exception as e:
        logger.error(f"Unexpected error during Qdrant population: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    populate_qdrant()
