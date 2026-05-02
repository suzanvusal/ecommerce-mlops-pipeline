#!/usr/bin/env python3
"""Bootstrap ecommerce-mlops-pipeline repo. Run once locally."""
import argparse
import subprocess
from pathlib import Path

DIRS = [
    "src/ingestion", "src/features", "src/recommendations",
    "src/forecasting", "src/pricing", "src/serving",
    "src/monitoring", "src/security", "src/retraining",
    "infra/docker", "infra/k8s", "infra/grafana/dashboards",
    "infra/grafana/provisioning", "infra/prometheus", "infra/airflow",
    "tests/unit", "tests/integration", "tests/load",
    "notebooks", "docs/runbooks", "scripts", "configs",
    ".github/workflows", ".automation_state", "plan", "templates"
]

BASE_FILES = {
"README.md": """\
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
""",

"pyproject.toml": """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "ecommerce-mlops-pipeline"
version = "0.1.0"
description = "E-Commerce MLOps Pipeline: recommendations, forecasting, pricing"
requires-python = ">=3.11"
dependencies = [
    "kafka-python>=2.0.2",
    "redis>=5.0.1",
    "pydantic>=2.5.0",
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "torch>=2.1.0",
    "pytorch-lightning>=2.1.2",
    "implicit>=0.7.2",
    "lightgbm>=4.1.0",
    "prophet>=1.1.5",
    "xgboost>=2.0.2",
    "scikit-learn>=1.3.2",
    "mlflow>=2.9.2",
    "evidently>=0.4.11",
    "apache-airflow>=2.7.3",
    "prometheus-client>=0.19.0",
    "faiss-cpu>=1.7.4",
    "gensim>=4.3.2",
    "chromadb>=0.4.18",
    "numpy>=1.26.2",
    "pandas>=2.1.4",
    "asyncpg>=0.29.0",
    "orjson>=3.9.10",
    "pyyaml>=6.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "pytest-cov>=4.1.0",
    "hypothesis>=6.92.1",
    "black>=23.11.0",
    "ruff>=0.1.7",
    "mypy>=1.7.1",
    "locust>=2.19.1",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
""",

"Makefile": """\
.PHONY: up down test lint serve simulate

up:
\tdocker compose up -d
\t@echo "✓ Stack started"

down:
\tdocker compose down -v

test:
\tpytest tests/ -v --cov=src --cov-report=term-missing

lint:
\truff check src/ tests/ --fix

serve:
\tuvicorn src.serving.api:app --reload --port 8000

simulate:
\tpython -m src.ingestion.simulator --users 10000 --products 50000 --rate 100

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
""",

"configs/base_config.yaml": """\
kafka:
  bootstrap_servers: "localhost:9092"
  topics:
    clicks:    "ecom.events.clicks"
    purchases: "ecom.events.purchases"
    searches:  "ecom.events.searches"
    views:     "ecom.events.views"
  consumer_group: "ecom-feature-consumers"

redis:
  host: "localhost"
  port: 6379
  user_feature_ttl: 86400
  product_feature_ttl: 3600
  recommendation_cache_ttl: 60

mlflow:
  tracking_uri: "http://localhost:5000"
  experiment_name: "ecommerce-recommendations"
  model_name: "product-recommender"

serving:
  host: "0.0.0.0"
  port: 8000
  top_k_recommendations: 20
  p99_target_ms: 50

recommendations:
  als_factors: 128
  two_tower_embedding_dim: 64
  diversity_lambda: 0.3

forecasting:
  horizon_days: 30
  confidence_interval: 0.95

pricing:
  min_margin_pct: 0.15
  max_price_change_pct: 0.20
""",

".env.example": """\
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
REDIS_HOST=localhost
MLFLOW_TRACKING_URI=http://localhost:5000
DATABASE_URL=postgresql://ecom:ecom@localhost/ecom_db
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
""",

".gitignore": """\
__pycache__/
*.py[cod]
.venv/
venv/
.env
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
mlruns/
.mypy_cache/
data/
*.pt
*.faiss
.DS_Store
""",

"src/__init__.py": '"""E-Commerce MLOps Pipeline — General Retail."""\n__version__ = "0.1.0"\n',
"src/ingestion/__init__.py": '"""Event ingestion: Kafka, schemas, simulators."""\n',
"src/features/__init__.py": '"""Feature engineering: user behaviour, product, embeddings."""\n',
"src/recommendations/__init__.py": '"""Recommendation models: ALS, Two-Tower, ensemble ranker."""\n',
"src/forecasting/__init__.py": '"""Demand forecasting: Prophet, XGBoost, inventory management."""\n',
"src/pricing/__init__.py": '"""Dynamic pricing engine with elasticity and competitor tracking."""\n',
"src/serving/__init__.py": '"""FastAPI recommendation and pricing API."""\n',
"src/monitoring/__init__.py": '"""Drift detection, metrics, A/B experiment monitoring."""\n',
"src/security/__init__.py": '"""Security: PII handling, GDPR compliance, audit logging."""\n',
"src/retraining/__init__.py": '"""Automated retraining: Airflow DAGs, validation, canary."""\n',
"tests/__init__.py": "",
"tests/unit/__init__.py": "",
"tests/integration/__init__.py": "",
"tests/load/__init__.py": "",
"templates/__init__.py": "",
".automation_state/.gitkeep": "",

"infra/prometheus/prometheus.yml": """\
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: ecom-serving-api
    static_configs:
      - targets: ["host.docker.internal:8000"]
    metrics_path: /metrics
""",
}


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()

    print("\n🚀 Bootstrapping ecommerce-mlops-pipeline repo...")
    print(f"   Remote: {args.repo}\n")

    print("📁 Creating directories...")
    for d in DIRS:
        Path(d).mkdir(parents=True, exist_ok=True)
    print(f"   ✓ {len(DIRS)} directories created")

    print("📝 Writing base files...")
    for filepath, content in BASE_FILES.items():
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"   ✓ {len(BASE_FILES)} files written")

    print("\n🔧 Initialising Git...")
    if not Path(".git").exists():
        run(["git", "init", "-b", "main"])
    run(["git", "config", "user.name", "MLOps Engineer"])
    run(["git", "config", "user.email", "86911143+suzanvusal@users.noreply.github.com"])
    run(["git", "remote", "remove", "origin"])
    run(["git", "remote", "add", "origin", args.repo])

    print("📦 Making initial commit...")
    run(["git", "add", "-A"])
    run(["git", "commit", "-m",
         "chore: bootstrap ecommerce-mlops-pipeline project\n\n"
         "- Real-time recommendations: ALS + Two-Tower + LightGBM\n"
         "- Demand forecasting: Prophet + XGBoost ensemble\n"
         "- Dynamic pricing engine + inventory auto-reorder\n"
         "- Evidently drift detection + Airflow retraining"])

    print("🚀 Pushing to GitHub...")
    result = run(["git", "push", "-u", "origin", "main"])
    if result.returncode == 0:
        print("   ✓ Pushed successfully!")
    else:
        print(f"   ⚠ Push failed: {result.stderr[:200]}")

    print("\n" + "="*55)
    print("  ✅ Bootstrap complete!")
    print("="*55)
    print("\nNext steps:")
    print("  1. Add AUTOMATION_PAT secret in GitHub repo Settings")
    print("  2. Actions → Run workflow → trigger Day 1")


if __name__ == "__main__":
    main()
