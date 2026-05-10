from fastapi import APIRouter

from app.schemas.memory_schema import StoreMemoryRequest, SearchMemoryRequest
from app.memory.memory_service import memory_service

router = APIRouter(prefix="/memory", tags=["memory"])


@router.post("/store")
def store_memory(payload: StoreMemoryRequest):
    return memory_service.store_memory(payload)


@router.post("/search")
def search_memory(payload: SearchMemoryRequest):
    return memory_service.search_memory(payload)