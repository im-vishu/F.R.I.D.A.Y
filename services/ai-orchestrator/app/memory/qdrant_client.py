from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config.settings import settings
from app.memory.embeddings import VECTOR_SIZE


COLLECTION_NAME = "friday_memories"


qdrant = QdrantClient(url=settings.QDRANT_URL)


def ensure_memory_collection():
    collections = qdrant.get_collections().collections
    existing = [collection.name for collection in collections]

    if COLLECTION_NAME not in existing:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )