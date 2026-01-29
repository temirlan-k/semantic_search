from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest


metrics_router = APIRouter()


@metrics_router.get("/metrics")
async def get_metrics():
    data = generate_latest()
    print("METRICS")
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
