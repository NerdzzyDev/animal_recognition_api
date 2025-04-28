from PIL import Image
import base64
import io
import logging
from app.utils.exceptions import ImageProcessingError

class ImageProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.allowed_content_types = {"image/jpeg", "image/png", "image/jpg"}

    def image_to_base64(self, image_data: bytes, content_type: str) -> str:
        try:
            if content_type not in self.allowed_content_types:
                raise ImageProcessingError(
                    message="Invalid content type",
                    details={"error": f"Content type {content_type} is not supported"}
                )
            image = Image.open(io.BytesIO(image_data))
            buffered = io.BytesIO()
            image_format = "PNG" if content_type == "image/png" else "JPEG"
            image.save(buffered, format=image_format)
            base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return f"data:{content_type};base64,{base64_string}"
        except ImageProcessingError as e:
            raise
        except Exception as e:
            self.logger.error(f"Failed to convert image to base64: {str(e)}")
            raise ImageProcessingError(
                message="Failed to process image",
                details={"error": str(e)}
            )

    def decode_base64_image(self, base64_image: str) -> Image.Image:
        try:
            # Если строка начинается с data:image, извлекаем base64-часть
            if base64_image.startswith("data:image"):
                base64_string = base64_image.split(",")[1]
            else:
                base64_string = base64_image
            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data))
            return image
        except (base64.binascii.Error, IndexError):
            raise ImageProcessingError(
                message="Invalid base64 data",
                details={"error": "Failed to decode base64 string"}
            )
        except Exception as e:
            self.logger.error(f"Failed to decode base64 image: {str(e)}")
            raise ImageProcessingError(
                message="Failed to decode image",
                details={"error": str(e)}
            )