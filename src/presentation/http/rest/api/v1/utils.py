import structlog
from fastapi import APIRouter, Response, Depends
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.infrastructure.database.db import DatabaseAdapter
from src.infrastructure.vector_db.milvus_service import MilvusService
from src.infrastructure.embeddings.ollama_service import OllamaService
from dependency_injector.wiring import inject, Provide
from main.di.container import Container

utils_router = APIRouter()
logger = structlog.get_logger()


@utils_router.get("/metrics")
async def get_metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@utils_router.get("/heatlh")
@inject
async def heatlhchecker(
    db: DatabaseAdapter = Depends(Provide[Container.db_adapter]),
    milvus: MilvusService = Depends(Provide[Container.milvus_service]),
    ollama: OllamaService = Depends(Provide[Container.ollama_service]),
):
    logger.info("Call from heatlh-check api endpoint")
    db = await db.healthcheck()
    milvus = await milvus.healthcheck()
    ollama = await ollama.healthcheck()
    return {"db": db, "milvus": milvus, "ollama": ollama}
