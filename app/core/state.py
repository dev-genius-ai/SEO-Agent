from typing import TypedDict, Optional, Annotated
from operator import add


class AgentState(TypedDict):
    topic: str
    target_word_count: int
    language: str
    job_id: str
    
    serp_results: Optional[list[dict]]
    keywords: Optional[dict]
    outline: Optional[dict]
    sections: Optional[list[dict]]
    
    article_html: Optional[str]
    article_text: Optional[str]
    word_count: Optional[int]
    
    seo_metadata: Optional[dict]
    internal_links: Optional[list[dict]]
    external_references: Optional[list[dict]]
    validation_report: Optional[list[dict]]
    
    status: str
    error: Optional[str]
    messages: Annotated[list[str], add]

