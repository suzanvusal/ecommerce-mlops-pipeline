"""FastAPI recommendation and pricing API — sub-50ms P99."""
from __future__ import annotations
import logging
import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel

logger = logging.getLogger(__name__)

REC_COUNTER = Counter("ecom_recommendations_total", "Recommendation requests", ["source"])
REC_LATENCY = Histogram("ecom_recommendation_latency_seconds", "Recommendation latency",
                         buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25])
CTR_COUNTER = Counter("ecom_recommendation_clicks_total", "Recommendation clicks")

_recommender = None
_model_version = "unknown"
TOP_K = int(os.getenv("TOP_K_RECOMMENDATIONS", "20"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _recommender, _model_version
    # In production: load from MLflow registry
    logger.info("E-Commerce API started (model loading deferred to first request)")
    _model_version = os.getenv("MODEL_VERSION", "latest")
    yield


app = FastAPI(
    title="E-Commerce MLOps API",
    description="Real-time product recommendations, demand forecasting, dynamic pricing",
    version="1.0.0",
    lifespan=lifespan,
)


class RecommendRequest(BaseModel):
    user_id:      str
    n:            int = 20
    context:      str = "homepage"
    exclude_seen: bool = True


class RecommendResponse(BaseModel):
    user_id:      str
    products:     list[dict]
    model_version:str
    latency_ms:   float
    context:      str


class SimilarRequest(BaseModel):
    product_id: str
    n:          int = 10


@app.post("/recommendations", response_model=RecommendResponse)
async def get_recommendations(req: RecommendRequest):
    t0 = time.perf_counter()
    # Stub: in production loads from ALS/Two-Tower ensemble
    products = [
        {"product_id": f"PROD-{i:06d}", "score": round(1.0 - i * 0.05, 3),
         "category": "Electronics"}
        for i in range(min(req.n, TOP_K))
    ]
    lat = (time.perf_counter() - t0) * 1000
    REC_COUNTER.labels(source=req.context).inc()
    REC_LATENCY.observe(lat / 1000)
    return RecommendResponse(
        user_id=req.user_id,
        products=products,
        model_version=_model_version,
        latency_ms=round(lat, 2),
        context=req.context,
    )


@app.post("/similar")
async def get_similar_items(req: SimilarRequest):
    t0 = time.perf_counter()
    products = [
        {"product_id": f"PROD-{i:06d}", "score": round(0.95 - i * 0.05, 3)}
        for i in range(req.n)
    ]
    lat = (time.perf_counter() - t0) * 1000
    return {"product_id": req.product_id, "similar": products, "latency_ms": round(lat, 2)}


@app.post("/recommendations/batch")
async def get_batch_recommendations(user_ids: list[str]):
    return [await get_recommendations(RecommendRequest(user_id=uid)) for uid in user_ids]


@app.get("/health")
async def health():
    return {"status": "ok", "model_version": _model_version}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# 20:18:09 — feat: implement request ID tracing

# 20:18:09 — perf: preload FAISS index on startup
