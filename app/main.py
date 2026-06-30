import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crm")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.SEED_ON_STARTUP:
        try:
            from app.db.seed import run_seed

            run_seed()
            logger.info("Seed-данные загружены")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Seed пропущен: %s", exc)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description=(
        "CRM-система для малого бизнеса: клиенты, сотрудники, услуги, записи, "
        "роли и история действий. Документация — Swagger UI ниже."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Служебное"], summary="Проверка работоспособности")
def health() -> dict[str, str]:
    return {"status": "ok"}
