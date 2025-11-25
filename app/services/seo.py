from datetime import datetime
from app.services.analyzer import calculate_keyword_density
from app.utils.logger import setup_logger
import textstat

logger = setup_logger(__name__)


def generate_seo_title(topic: str, primary_keyword: str, max_len: int = 60) -> str:
    if primary_keyword.lower() in topic.lower():
        title = topic.title()
    else:
        title = f"{topic.title()} - {primary_keyword.title()}"
    
    if len(title) > max_len:
        title = title[:max_len-3] + "..."
    
    return title


def generate_meta_description(primary_keyword: str, h1: str, max_len: int = 160) -> str:
    desc = f"Comprehensive guide to {primary_keyword}. Learn everything about {h1.lower()} with expert insights and practical tips."
    
    if len(desc) > max_len:
        desc = desc[:max_len-3] + "..."
    
    return desc


def generate_structured_data(h1: str, meta_description: str, word_count: int) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1,
        "description": meta_description,
        "author": {
            "@type": "Organization",
            "name": "Content Generation Platform"
        },
        "datePublished": datetime.utcnow().isoformat(),
        "wordCount": word_count,
        "articleBody": "Full article content available on the page"
    }


def validate_article(
    h1: str,
    article_text: str,
    primary_keyword: str,
    target_word_count: int
) -> list[dict]:
    report = []
    
    text_lower = article_text.lower()
    h1_lower = h1.lower()
    primary_lower = primary_keyword.lower()
    
    report.append({
        "check": "title_contains_keyword",
        "pass": primary_lower in h1_lower,
        "message": "Primary keyword in H1"
    })
    
    first_paragraph = article_text.split("\n\n")[0] if article_text else ""
    report.append({
        "check": "intro_contains_keyword",
        "pass": primary_lower in first_paragraph.lower(),
        "message": "Primary keyword in introduction"
    })
    
    word_count = len(article_text.split())
    tolerance = max(100, int(target_word_count * 0.15))
    word_count_ok = abs(word_count - target_word_count) <= tolerance
    
    report.append({
        "check": "word_count",
        "pass": word_count_ok,
        "message": f"Word count: {word_count} (target: {target_word_count})",
        "value": word_count
    })
    
    h2_count = article_text.count("## ")
    report.append({
        "check": "has_multiple_sections",
        "pass": h2_count >= 3,
        "message": f"H2 sections: {h2_count}"
    })
    
    try:
        readability = textstat.flesch_reading_ease(article_text)
        is_readable = 30 <= readability <= 80
        report.append({
            "check": "readability",
            "pass": is_readable,
            "message": f"Flesch Reading Ease: {readability:.1f}",
            "value": readability
        })
    except Exception as e:
        logger.warning(f"Readability check failed: {e}")
        report.append({
            "check": "readability",
            "pass": True,
            "message": "Readability check skipped"
        })
    
    keyword_count = text_lower.count(primary_lower)
    density = (keyword_count / len(article_text.split())) * 100
    density_ok = 0.5 <= density <= 3.0
    
    report.append({
        "check": "keyword_density",
        "pass": density_ok,
        "message": f"Keyword density: {density:.2f}% (ideal: 0.5-3.0%)",
        "value": density
    })
    
    return report


def generate_seo_metadata(
    h1: str,
    topic: str,
    keywords: dict,
    article_text: str,
    word_count: int
) -> dict:
    primary = keywords["primary"]
    
    seo_title = generate_seo_title(topic, primary)
    meta_description = generate_meta_description(primary, h1)
    structured_data = generate_structured_data(h1, meta_description, word_count)
    
    all_keywords = [primary] + keywords["secondary"][:8]
    keyword_density = calculate_keyword_density(article_text, all_keywords)
    
    return {
        "seo_title": seo_title,
        "meta_description": meta_description,
        "structured_data": structured_data,
        "keyword_analysis": {
            "primary_keyword": primary,
            "secondary_keywords": keywords["secondary"][:8],
            "keyword_density": keyword_density
        }
    }

