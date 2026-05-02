# E-Commerce MLOps Pipeline — General Retail

Production-grade MLOps system for general retail: real-time recommendations,
demand forecasting, dynamic pricing, and inventory management.

## Architecture

```
User Events (clicks, purchases, searches)
        |
        v Kafka Event Stream
Session Feature Engineering + Product Embeddings
        |
        v Redis Feature Store
Recommendation Engine (ALS + Two-Tower + LightGBM Ranker)
        |
        v FastAPI (<50ms P99)
Personalised Recommendations + Similar Items
        |
        v Impression + Conversion Logging
A/B Testing Framework + Statistical Significance
        |
        v Demand Forecasting (Prophet + XGBoost)
Dynamic Pricing + Inventory Alerts + Auto-Reorder
        |
        v Evidently Drift Detection
Airflow DAG → Auto Retrain → Canary Deploy
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Event Streaming | Apache Kafka |
| Features | Redis, RFM, Product2Vec |
| Recommendations | ALS, Two-Tower (PyTorch), LightGBM Ranker |
| Forecasting | Prophet, XGBoost |
| Serving | FastAPI (<50ms P99) |
| A/B Testing | Custom framework + z-test |
| Drift Detection | Evidently AI |
| Orchestration | Apache Airflow |
| Monitoring | Prometheus, Grafana |

## Quick Start

```bash
docker compose up -d
make simulate    # Start e-commerce event simulation
make serve       # Start recommendation API
```

## License
MIT
