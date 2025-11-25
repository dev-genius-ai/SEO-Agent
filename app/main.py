from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.models.database import init_db
from app.utils.logger import setup_logger
from contextlib import asynccontextmanager

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting SEO Agent service")
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down SEO Agent service")


app = FastAPI(
    title="SEO Content Generation Agent",
    description="AI-powered service for generating SEO-optimized articles",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["articles"])


@app.get("/")
def root():
    return {
        "service": "SEO Content Generation Agent",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "seo-agent"}

