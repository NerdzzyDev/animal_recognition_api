from app.infrastructure.clip_model import CLIPModelWrapper
from app.infrastructure.qdrant_client import QdrantClientWrapper
from app.infrastructure.ollama_client import OllamaClientWrapper
from app.utils.exceptions import EmbeddingGenerationError, QdrantError, OllamaError, TranslationError, \
    ImageProcessingError
from app.api.models import AnimalResponse
from app.utils.translations import translate_animal_name
from app.infrastructure.image_processor import ImageProcessor
import logging
from datetime import datetime


class AnimalRecognitionService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.clip_model = CLIPModelWrapper()
        self.qdrant_client = QdrantClientWrapper()
        self.ollama_client = OllamaClientWrapper()
        self.image_processor = ImageProcessor()

    def recognize_animal(self, base64_image: str, user_id: str, query: str, timestamp: datetime) -> AnimalResponse:
        try:
            # Декодируем base64-изображение в PIL.Image
            image = self.image_processor.decode_base64_image(base64_image)
            embedding = self.clip_model.generate_embedding(image)
            similar_animals = self.qdrant_client.search_similar(embedding, limit=5)

            if not similar_animals:
                raise QdrantError(message="No similar animals found", details={})

            top_animal = similar_animals[0]
            animal_name = top_animal["metadata"].get("animal_name", "unknown")
            animal_name_translated = translate_animal_name(animal_name, target_language="ru")
            description = self.ollama_client.generate_description(animal_name_translated)

            return AnimalResponse(
                animal=animal_name_translated,
                description=description,
                user_id=user_id,
                answer=f"На изображении, вероятно, {animal_name_translated}.",
                timestamp=timestamp.isoformat(),
                similarities=similar_animals
            )
        except ImageProcessingError as e:
            self.logger.error(f"Image processing failed: {str(e)}")
            raise
        except EmbeddingGenerationError as e:
            self.logger.error(f"Embedding generation failed: {str(e)}")
            raise
        except QdrantError as e:
            self.logger.error(f"Qdrant search failed: {str(e)}")
            raise
        except OllamaError as e:
            self.logger.error(f"Ollama description failed: {str(e)}")
            raise
        except TranslationError as e:
            self.logger.error(f"Translation failed: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in recognize_animal: {str(e)}")
            raise