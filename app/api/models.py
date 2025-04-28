from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class AnimalRequest(BaseModel):
    user_id: UUID = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    query: str = Field(..., example="Какое это животное?")
    timestamp: str = Field(..., example="2025-04-25T13:59:27.740855")
    image: str = Field(..., example="data:image/png;base64,iVBORw0KGgo...")

class AnimalResponse(BaseModel):
    animal: str = Field(..., example="кошка")
    description: str = Field(..., example="Маленькое пушистое животное.")
    user_id: UUID = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    answer: str = Field(..., example="На изображении, вероятно, кошка.")
    timestamp: str = Field(..., example="2025-04-25T13:59:27.740855")
    similarities: list[dict] = Field(..., example=[{"metadata": {"animal_name": "cat"}, "score": 0.9}])

class ImageToBase64Response(BaseModel):
    base64_image: str = Field(..., example="data:image/png;base64,iVBORw0KGgo...")