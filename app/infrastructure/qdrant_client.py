from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import logging
from app.utils.exceptions import QdrantError

class QdrantClientWrapper:
    def __init__(self, host: str = "qdrant", port: int = 6333, collection_name: str = "animals"):
        self.logger = logging.getLogger(__name__)
        self.collection_name = collection_name
        try:
            self.client = QdrantClient(host=host, port=port)
            self.logger.info(f"Connected to Qdrant at {host}:{port}")
        except Exception as e:
            self.logger.error(f"Failed to connect to Qdrant: {str(e)}")
            raise QdrantError(
                message="Failed to initialize Qdrant client",
                details={"error": str(e)}
            )

    def create_collection(self):
        try:
            collections = self.client.get_collections()
            if self.collection_name not in [c.name for c in collections.collections]:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=512, distance=Distance.COSINE)
                )
                self.logger.info(f"Created collection {self.collection_name}")
            else:
                self.logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            self.logger.error(f"Failed to create collection: {str(e)}")
            raise QdrantError(
                message="Failed to create collection",
                details={"error": str(e)}
            )

    def upsert(self, collection_name: str = None, points: list = None):
        if collection_name is None:
            collection_name = self.collection_name
        try:
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            self.logger.info(f"Upserted {len(points)} points to collection {collection_name}")
        except Exception as e:
            self.logger.error(f"Failed to upsert points: {str(e)}")
            raise QdrantError(
                message="Failed to upsert points",
                details={"error": str(e)}
            )

    def search_similar(self, embedding: list, limit: int = 5) -> list:
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=embedding,
                limit=limit,
                with_payload=True
            )
            results = [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "metadata": hit.payload
                }
                for hit in search_result
            ]
            self.logger.info(f"Found {len(results)} similar items")
            return results
        except Exception as e:
            self.logger.error(f"Failed to search similar: {str(e)}")
            raise QdrantError(
                message="Failed to search similar items",
                details={"error": str(e)}
            )
