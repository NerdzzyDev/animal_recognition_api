from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.routes import router as api_router
from app.scripts.populate_qdrant import populate_qdrant
import logging

app = FastAPI(title="Animal Recognition API", version="1.0.0")

# Подключаем роутер без префикса для корневого маршрута
app.include_router(api_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Animal Recognition API",
        version="1.0.0",
        routes=app.routes,
        tags=[{"name": "animals", "description": "Animal recognition endpoints"}]
    )
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger(__name__)
    logger.info("Starting application")
    try:
        populate_qdrant(data_dir="/app/data/animals-10/raw-img", batch_size=100, max_workers=4)
        logger.info("Qdrant initialization completed")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant: {str(e)}")
        raise
