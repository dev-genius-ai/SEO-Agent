import httpx
import json
from pathlib import Path
from app.models.schemas import SERPItem
from app.config import get_settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()


async def fetch_serp_results(query: str) -> list[SERPItem]:
    if not settings.serpapi_key:
        logger.warning("No SERPAPI_KEY found, using mock data")
        return load_mock_serp()
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://serpapi.com/search",
                params={
                    "q": query,
                    "api_key": settings.serpapi_key,
                    "num": 10,
                    "engine": "google"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            results = []
            for idx, item in enumerate(data.get("organic_results", [])[:10], 1):
                results.append(SERPItem(
                    rank=idx,
                    url=item["link"],
                    title=item["title"],
                    snippet=item.get("snippet", "")
                ))
            
            if not results:
                logger.warning("No SERP results found, falling back to mock")
                return load_mock_serp()
            
            return results
            
    except Exception as e:
        logger.error(f"SERP API failed: {str(e)}, falling back to mock")
        return load_mock_serp()


def load_mock_serp() -> list[SERPItem]:
    mock_path = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "mock_serp.json"
    
    if not mock_path.exists():
        return create_default_mock()
    
    try:
        data = json.loads(mock_path.read_text())
        return [SERPItem(**item) for item in data]
    except Exception as e:
        logger.error(f"Failed to load mock SERP: {str(e)}")
        return create_default_mock()


def create_default_mock() -> list[SERPItem]:
    return [
        SERPItem(
            rank=i,
            url=f"https://example.com/article-{i}",
            title=f"Best Productivity Tools for Remote Teams - Article {i}",
            snippet=f"Discover top productivity tools that help remote teams collaborate effectively. Features include project management, communication, and time tracking."
        )
        for i in range(1, 11)
    ]

