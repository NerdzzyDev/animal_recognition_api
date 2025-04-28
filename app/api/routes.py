from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from app.api.models import AnimalRequest, AnimalResponse, ImageToBase64Response
from app.services.animal_recognition import AnimalRecognitionService
from app.utils.exceptions import ImageProcessingError, EmbeddingGenerationError, QdrantError, OllamaError, \
    TranslationError
from app.infrastructure.image_processor import ImageProcessor
import logging
from datetime import datetime

router = APIRouter(tags=["animals"])
templates = Jinja2Templates(directory="templates")
image_processor = ImageProcessor()


def get_animal_recognition_service():
    return AnimalRecognitionService()


@router.get("/", response_class=HTMLResponse, tags=["animals"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/image_to_base64", response_model=ImageToBase64Response, tags=["animals"])
async def image_to_base64(image: UploadFile = File(...)):
    try:
        content_type = image.content_type
        image_data = await image.read()
        base64_image = image_processor.image_to_base64(image_data, content_type)
        return {"base64_image": base64_image}
    except ImageProcessingError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error in image_to_base64: {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/what_is_animal", response_model=AnimalResponse, tags=["animals"])
async def what_is_animal(
        request: AnimalRequest,
        service: AnimalRecognitionService = Depends(get_animal_recognition_service)
):
    try:
        # Проверяем, что timestamp - строка, и преобразуем в datetime
        if not isinstance(request.timestamp, str):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Timestamp must be a string in ISO format"
            )
        try:
            timestamp = datetime.fromisoformat(request.timestamp)
        except ValueError as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Invalid timestamp format: {str(e)}"
            )

        response = service.recognize_animal(
            base64_image=request.image,
            user_id=str(request.user_id),
            query=request.query,
            timestamp=timestamp
        )
        return response
    except ImageProcessingError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except (EmbeddingGenerationError, QdrantError, OllamaError, TranslationError) as e:
        logging.error(f"Error in what_is_animal: {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error in what_is_animal: {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

