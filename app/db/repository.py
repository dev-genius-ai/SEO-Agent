from sqlalchemy.orm import Session
from app.models.database import Job
from typing import Optional


class JobRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, topic: str, target_word_count: int, language: str) -> Job:
        job = Job(
            topic=topic,
            target_word_count=target_word_count,
            language=language,
            status="pending"
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def get(self, job_id: str) -> Optional[Job]:
        return self.db.query(Job).filter(Job.id == job_id).first()
    
    def update_status(self, job_id: str, status: str) -> None:
        job = self.get(job_id)
        if job:
            job.status = status
            self.db.commit()
    
    def update_field(self, job_id: str, field: str, value: any) -> None:
        job = self.get(job_id)
        if job:
            setattr(job, field, value)
            self.db.commit()
    
    def save_error(self, job_id: str, error: str) -> None:
        job = self.get(job_id)
        if job:
            job.status = "failed"
            job.error = error
            self.db.commit()

