from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=200)
    target_word_count: int = Field(default=1500, ge=300, le=5000)
    language: str = Field(default="en", max_length=5)


class SERPItem(BaseModel):
    rank: int
    url: HttpUrl
    title: str
    snippet: str


class SEOKeywordAnalysis(BaseModel):
    primary_keyword: str
    secondary_keywords: list[str]
    keyword_density: dict[str, float]


class InternalLink(BaseModel):
    anchor_text: str
    suggested_target: str
    context: str


class ExternalReference(BaseModel):
    url: str
    title: str
    citation_context: str
    placement_suggestion: str


class ArticleSection(BaseModel):
    level: int
    heading: str
    content: str


class ArticleOutput(BaseModel):
    title: str
    h1: str
    html: str
    plain_text: str
    word_count: int
    seo_title: str
    meta_description: str
    keyword_analysis: SEOKeywordAnalysis
    structured_data: dict
    internal_links: list[InternalLink]
    external_references: list[ExternalReference]
    validation_report: list[dict]


class JobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime


class JobDetailResponse(BaseModel):
    job_id: str
    status: str
    topic: str
    target_word_count: int
    language: str
    article: Optional[ArticleOutput] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

