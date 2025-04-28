import pytest
from app.infrastructure.image_processor import ImageProcessor
from app.utils.exceptions import ImageProcessingError
from PIL import Image
import io

@pytest.fixture
def image_processor():
    return ImageProcessor()

def test_image_to_base64_success(image_processor, test_image):
    content_type = "image/png"
    base64_image = image_processor.image_to_base64(test_image, content_type)
    assert base64_image.startswith("data:image/png;base64,")

def test_image_to_base64_invalid_content_type(image_processor, test_image):
    content_type = "text/plain"
    with pytest.raises(ImageProcessingError) as exc_info:
        image_processor.image_to_base64(test_image, content_type)
    assert "Invalid content type" in str(exc_info.value)

def test_decode_base64_image_success(image_processor, test_image_base64):
    image = image_processor.decode_base64_image(test_image_base64)
    assert isinstance(image, Image.Image)

def test_decode_base64_image_invalid(image_processor):
    invalid_base64 = "invalid-base64-string"
    with pytest.raises(ImageProcessingError) as exc_info:
        image_processor.decode_base64_image(invalid_base64)
    assert "Invalid base64" in str(exc_info.value)