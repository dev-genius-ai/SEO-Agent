from app.models.schemas import SERPItem, InternalLink, ExternalReference
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def generate_internal_links(keywords: dict, sections: list[dict]) -> list[InternalLink]:
    links = []
    
    secondary_keywords = keywords.get("secondary", [])[:5]
    
    for kw in secondary_keywords:
        slug = kw.lower().replace(" ", "-")
        links.append(InternalLink(
            anchor_text=f"{kw} guide",
            suggested_target=f"/blog/{slug}",
            context=f"Link when discussing {kw} in detail for additional resources"
        ))
    
    primary = keywords.get("primary", "")
    if primary:
        links.append(InternalLink(
            anchor_text=f"complete {primary} tutorial",
            suggested_target=f"/resources/{primary.replace(' ', '-')}",
            context=f"Deep dive resource about {primary}"
        ))
    
    return links[:5]


def generate_external_references(serp_items: list[SERPItem]) -> list[ExternalReference]:
    references = []
    
    authority_domains = [
        ".edu", ".gov", ".org", "wikipedia", "harvard", "stanford",
        "mit.edu", "forbes", "techcrunch", "medium", "blog"
    ]
    
    for item in serp_items[:10]:
        url_lower = str(item.url).lower()
        
        if any(domain in url_lower for domain in authority_domains[:4]):
            references.append(ExternalReference(
                url=str(item.url),
                title=item.title,
                citation_context="Authoritative source for industry standards and research",
                placement_suggestion="Reference in introduction or key statistics section"
            ))
            
            if len(references) >= 4:
                break
    
    if len(references) < 2:
        for item in serp_items[:6]:
            if str(item.url) not in [r.url for r in references]:
                references.append(ExternalReference(
                    url=str(item.url),
                    title=item.title,
                    citation_context="Additional resource and perspective on the topic",
                    placement_suggestion="Reference when providing examples or case studies"
                ))
                
                if len(references) >= 4:
                    break
    
    return references[:4]

