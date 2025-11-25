import asyncio
import traceback
from app.core.graph import get_agent_graph
from app.core.state import AgentState
from app.db.repository import JobRepository
from app.models.database import SessionLocal
from app.models.schemas import ArticleOutput, SEOKeywordAnalysis, InternalLink, ExternalReference
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def run_article_generation(job_id: str, topic: str, target_word_count: int, language: str):
    db = SessionLocal()
    repo = JobRepository(db)
    
    try:
        logger.info(f"Starting article generation for job {job_id}")
        repo.update_status(job_id, "running")
        
        initial_state: AgentState = {
            "topic": topic,
            "target_word_count": target_word_count,
            "language": language,
            "job_id": job_id,
            "serp_results": None,
            "keywords": None,
            "outline": None,
            "sections": None,
            "article_html": None,
            "article_text": None,
            "word_count": None,
            "seo_metadata": None,
            "internal_links": None,
            "external_references": None,
            "validation_report": None,
            "status": "running",
            "error": None,
            "messages": []
        }
        
        logger.info(f"Getting agent graph for job {job_id}")
        graph = get_agent_graph()
        
        config = {"configurable": {"thread_id": job_id}}
        
        logger.info(f"Invoking agent graph for job {job_id}")
        final_state = await graph.ainvoke(initial_state, config)
        logger.info(f"Agent graph completed for job {job_id}")
        
        logger.info(f"Saving results for job {job_id}")
        
        serp_snapshot = []
        for item in final_state["serp_results"]:
            serp_snapshot.append({
                "rank": item["rank"],
                "url": str(item["url"]),
                "title": item["title"],
                "snippet": item["snippet"]
            })
        
        repo.update_field(job_id, "serp_snapshot", serp_snapshot)
        repo.update_field(job_id, "keywords", final_state["keywords"])
        repo.update_field(job_id, "outline", final_state["outline"])
        repo.update_field(job_id, "sections", final_state["sections"])
        
        logger.info(f"Building article output for job {job_id}")
        article_output = build_article_output(final_state)
        repo.update_field(job_id, "article", article_output.model_dump())
        
        repo.update_status(job_id, "completed")
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Job {job_id} failed: {error_msg}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        try:
            db.rollback()
            repo.save_error(job_id, error_msg if error_msg.strip() else traceback.format_exc())
        except Exception as save_error:
            logger.error(f"Failed to save error: {save_error}")
    finally:
        db.close()


def build_article_output(state: AgentState) -> ArticleOutput:
    seo_meta = state["seo_metadata"]
    keyword_analysis = seo_meta["keyword_analysis"]
    
    return ArticleOutput(
        title=state["outline"]["h1"],
        h1=state["outline"]["h1"],
        html=state["article_html"],
        plain_text=state["article_text"],
        word_count=state["word_count"],
        seo_title=seo_meta["seo_title"],
        meta_description=seo_meta["meta_description"],
        keyword_analysis=SEOKeywordAnalysis(**keyword_analysis),
        structured_data=seo_meta["structured_data"],
        internal_links=[InternalLink(**link) for link in state["internal_links"]],
        external_references=[ExternalReference(**ref) for ref in state["external_references"]],
        validation_report=state["validation_report"]
    )


def start_job_async(job_id: str, topic: str, target_word_count: int, language: str):
    asyncio.create_task(run_article_generation(job_id, topic, target_word_count, language))

