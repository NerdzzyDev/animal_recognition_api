import clip
import torch
from PIL import Image
from app.utils.exceptions import EmbeddingGenerationError

class CLIPModelWrapper:
    def __init__(self, model_name: str = "ViT-B/32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            self.model, self.preprocess = clip.load(model_name, device=self.device)
        except Exception as e:
            raise EmbeddingGenerationError(
                message="Failed to load CLIP model",
                details={"error": str(e)}
            )

    def generate_embedding(self, image: Image.Image) -> list:
        try:
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                embedding = self.model.encode_image(image_input)
            return embedding.squeeze().cpu().numpy().tolist()
        except Exception as e:
            raise EmbeddingGenerationError(
                message="Failed to generate embedding",
                details={"error": str(e)}
            )
