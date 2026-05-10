from uuid import uuid4
from datetime import datetime, timezone

from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

from app.memory.embeddings import create_mock_embedding
from app.memory.qdrant_client import COLLECTION_NAME, qdrant, ensure_memory_collection
from app.schemas.memory_schema import StoreMemoryRequest, SearchMemoryRequest


class MemoryService:
    def __init__(self):
        ensure_memory_collection()

    def store_memory(self, payload: StoreMemoryRequest):
        memory_id = str(uuid4())
        vector = create_mock_embedding(payload.text)

        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=memory_id,
                    vector=vector,
                    payload={
                        "memory_id": memory_id,
                        "user_id": payload.user_id,
                        "session_id": payload.session_id,
                        "text": payload.text,
                        "metadata": payload.metadata or {},
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
            ],
        )

        return {
            "success": True,
            "message": "Memory stored successfully",
            "memory_id": memory_id,
        }

    def search_memory(self, payload: SearchMemoryRequest):
        query_vector = create_mock_embedding(payload.query)

        results = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=payload.user_id),
                    )
                ]
            ),
            limit=payload.limit,
        )

        memories = []

        for item in results.points:
            memories.append(
                {
                    "score": item.score,
                    "memory_id": item.payload.get("memory_id"),
                    "text": item.payload.get("text"),
                    "session_id": item.payload.get("session_id"),
                    "metadata": item.payload.get("metadata"),
                    "created_at": item.payload.get("created_at"),
                }
            )

        return {
            "success": True,
            "query": payload.query,
            "count": len(memories),
            "memories": memories,
        }


memory_service = MemoryService()