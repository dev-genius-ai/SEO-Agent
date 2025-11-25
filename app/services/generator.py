from app.services.llm import get_llm_client
from app.models.schemas import SERPItem, ArticleSection
from app.utils.logger import setup_logger
from app.utils.html import sections_to_html, sections_to_text
import json

logger = setup_logger(__name__)


async def create_outline(topic: str, keywords: dict, serp_items: list[SERPItem]) -> dict:
    llm = get_llm_client()
    
    serp_titles = "\n".join([f"- {item.title}" for item in serp_items[:5]])
    
    prompt = f"""Create an SEO-optimized article outline for the topic: "{topic}"

Primary keyword: {keywords['primary']}
Secondary keywords: {', '.join(keywords['secondary'][:8])}

Top-ranking article titles:
{serp_titles}

Create a detailed outline with:
1. A compelling H1 title (include the primary keyword naturally)
2. 5-7 H2 section headings that cover the topic comprehensively
3. For each H2, suggest 2-3 H3 subheadings

Format as JSON:
{{
    "h1": "Main Title Here",
    "sections": [
        {{
            "h2": "Section Title",
            "h3s": ["Subsection 1", "Subsection 2"]
        }}
    ]
}}

Make it natural and valuable for readers, not keyword-stuffed."""

    try:
        response = await llm.generate(prompt, max_tokens=1500, temperature=0.7)
        response = response.strip()
        
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        
        outline = json.loads(response.strip())
        return outline
        
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON outline: {e}, using fallback")
        return create_fallback_outline(topic, keywords)
    except Exception as e:
        logger.error(f"Outline generation failed: {e}")
        return create_fallback_outline(topic, keywords)


def create_fallback_outline(topic: str, keywords: dict) -> dict:
    return {
        "h1": topic.title(),
        "sections": [
            {"h2": f"What is {keywords['primary'].title()}?", "h3s": []},
            {"h2": f"Benefits of {keywords['primary'].title()}", "h3s": []},
            {"h2": f"Top {keywords['secondary'][0].title()} Options", "h3s": []},
            {"h2": f"How to Choose {keywords['primary'].title()}", "h3s": []},
            {"h2": "Best Practices", "h3s": []},
            {"h2": "Conclusion", "h3s": []}
        ]
    }


async def generate_sections(outline: dict, keywords: dict, target_word_count: int) -> list[dict]:
    llm = get_llm_client()
    sections = []
    
    num_sections = len(outline["sections"])
    words_per_section = max(150, target_word_count // num_sections)
    
    intro_prompt = f"""Write an engaging introduction for an article titled "{outline['h1']}".

Primary keyword to include naturally: {keywords['primary']}

Write {min(200, words_per_section)} words that:
- Hook the reader
- Introduce the topic
- Preview what the article will cover
- Include the primary keyword naturally in the first paragraph

Write only the introduction text, no headings."""

    try:
        intro_content = await llm.generate(intro_prompt, max_tokens=500, temperature=0.7)
        sections.append({
            "level": 2,
            "heading": "Introduction",
            "content": intro_content.strip()
        })
    except Exception as e:
        logger.error(f"Failed to generate introduction: {e}")
        sections.append({
            "level": 2,
            "heading": "Introduction",
            "content": f"In this comprehensive guide, we'll explore {keywords['primary']} and provide valuable insights."
        })
    
    for section_data in outline["sections"]:
        h2 = section_data["h2"]
        h3s = section_data.get("h3s", [])
        
        section_prompt = f"""Write a detailed section for "{h2}" in an article about {outline['h1']}.

Keywords to include naturally: {', '.join(keywords['secondary'][:5])}

{"Subsections to cover: " + ', '.join(h3s) if h3s else ""}

Write approximately {words_per_section} words that:
- Provide valuable, actionable information
- Use natural language (not robotic or keyword-stuffed)
- Include examples or specific details
- Are well-structured with clear paragraphs

Write only the content, no headings."""

        try:
            content = await llm.generate(section_prompt, max_tokens=words_per_section * 2, temperature=0.7)
            sections.append({
                "level": 2,
                "heading": h2,
                "content": content.strip()
            })
            
            if h3s and len(h3s) <= 2:
                for h3 in h3s[:2]:
                    h3_prompt = f"""Write a focused subsection for "{h3}" under the section "{h2}".

Write 100-150 words of practical, valuable information. Be specific and actionable."""

                    try:
                        h3_content = await llm.generate(h3_prompt, max_tokens=300, temperature=0.7)
                        sections.append({
                            "level": 3,
                            "heading": h3,
                            "content": h3_content.strip()
                        })
                    except Exception as e:
                        logger.warning(f"Failed to generate H3 '{h3}': {e}")
                        
        except Exception as e:
            logger.error(f"Failed to generate section '{h2}': {e}")
            sections.append({
                "level": 2,
                "heading": h2,
                "content": f"This section covers important aspects of {h2.lower()}."
            })
    
    return sections


def compile_article(h1: str, sections: list[dict]) -> dict:
    html = sections_to_html(sections, h1)
    plain_text = sections_to_text(sections, h1)
    
    word_count = len(plain_text.split())
    
    return {
        "h1": h1,
        "html": html,
        "plain_text": plain_text,
        "word_count": word_count,
        "sections": sections
    }

