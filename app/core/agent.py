from app.core.state import AgentState
from app.services import serp, analyzer, generator, seo, linking
from app.models.schemas import SERPItem
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def fetch_serp_node(state: AgentState) -> dict:
    logger.info(f"Fetching SERP results for: {state['topic']}")
    
    try:
        results = await serp.fetch_serp_results(state["topic"])
        
        return {
            "serp_results": [item.model_dump() for item in results],
            "messages": [f"Fetched {len(results)} SERP results"]
        }
    except Exception as e:
        logger.error(f"SERP fetch failed: {e}")
        raise


async def analyze_serp_node(state: AgentState) -> dict:
    logger.info("Analyzing SERP results")
    
    try:
        serp_items = [SERPItem(**item) for item in state["serp_results"]]
        keywords = analyzer.extract_keywords(serp_items)
        
        return {
            "keywords": keywords,
            "messages": [f"Extracted primary keyword: {keywords['primary']}"]
        }
    except Exception as e:
        logger.error(f"SERP analysis failed: {e}")
        raise


async def create_outline_node(state: AgentState) -> dict:
    logger.info("Creating article outline")
    
    try:
        serp_items = [SERPItem(**item) for item in state["serp_results"]]
        outline = await generator.create_outline(
            state["topic"],
            state["keywords"],
            serp_items
        )
        
        return {
            "outline": outline,
            "messages": [f"Created outline with H1: {outline['h1']}"]
        }
    except Exception as e:
        logger.error(f"Outline creation failed: {e}")
        raise


async def generate_content_node(state: AgentState) -> dict:
    logger.info("Generating article content")
    
    try:
        sections = await generator.generate_sections(
            state["outline"],
            state["keywords"],
            state["target_word_count"]
        )
        
        article = generator.compile_article(state["outline"]["h1"], sections)
        
        return {
            "sections": sections,
            "article_html": article["html"],
            "article_text": article["plain_text"],
            "word_count": article["word_count"],
            "messages": [f"Generated article with {article['word_count']} words"]
        }
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise


async def generate_metadata_node(state: AgentState) -> dict:
    logger.info("Generating SEO metadata")
    
    try:
        metadata = seo.generate_seo_metadata(
            state["outline"]["h1"],
            state["topic"],
            state["keywords"],
            state["article_text"],
            state["word_count"]
        )
        
        return {
            "seo_metadata": metadata,
            "messages": ["Generated SEO metadata and structured data"]
        }
    except Exception as e:
        logger.error(f"Metadata generation failed: {e}")
        raise


async def generate_links_node(state: AgentState) -> dict:
    logger.info("Generating internal and external links")
    
    try:
        serp_items = [SERPItem(**item) for item in state["serp_results"]]
        
        internal = linking.generate_internal_links(state["keywords"], state["sections"])
        external = linking.generate_external_references(serp_items)
        
        return {
            "internal_links": [link.model_dump() for link in internal],
            "external_references": [ref.model_dump() for ref in external],
            "messages": [f"Generated {len(internal)} internal and {len(external)} external links"]
        }
    except Exception as e:
        logger.error(f"Link generation failed: {e}")
        raise


async def validate_node(state: AgentState) -> dict:
    logger.info("Validating article SEO")
    
    try:
        report = seo.validate_article(
            state["outline"]["h1"],
            state["article_text"],
            state["keywords"]["primary"],
            state["target_word_count"]
        )
        
        all_passed = all(check["pass"] for check in report)
        status_msg = "All SEO checks passed" if all_passed else "Some SEO checks failed"
        
        return {
            "validation_report": report,
            "status": "completed",
            "messages": [status_msg]
        }
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return {
            "validation_report": [],
            "status": "completed",
            "messages": ["Validation completed with errors"]
        }

