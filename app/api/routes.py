from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.schemas import GenerateRequest, JobResponse, JobDetailResponse
from app.db.repository import JobRepository
from app.core.orchestrator import run_article_generation
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/generate", response_model=JobResponse)
async def generate_article(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.info(f"Received generation request for topic: {request.topic}")
    
    repo = JobRepository(db)
    job = repo.create(request.topic, request.target_word_count, request.language)
    
    background_tasks.add_task(
        run_article_generation,
        job.id,
        request.topic,
        request.target_word_count,
        request.language
    )
    
    return JobResponse(
        job_id=job.id,
        status=job.status,
        created_at=job.created_at
    )


@router.get("/jobs/{job_id}", response_model=JobDetailResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    job = repo.get(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobDetailResponse(
        job_id=job.id,
        status=job.status,
        topic=job.topic,
        target_word_count=job.target_word_count,
        language=job.language,
        article=job.article,
        error=job.error,
        created_at=job.created_at,
        updated_at=job.updated_at
    )

