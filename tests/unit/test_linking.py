import pytest
from app.services.linking import generate_internal_links, generate_external_references
from app.models.schemas import SERPItem


def test_generate_internal_links():
    keywords = {
        "primary": "productivity tools",
        "secondary": ["remote", "collaboration", "management", "software", "teams"]
    }
    sections = [
        {"level": 2, "heading": "Introduction", "content": "Some content"},
        {"level": 2, "heading": "Features", "content": "More content"}
    ]
    
    links = generate_internal_links(keywords, sections)
    
    assert isinstance(links, list)
    assert len(links) > 0
    assert len(links) <= 5
    
    for link in links:
        assert hasattr(link, 'anchor_text')
        assert hasattr(link, 'suggested_target')
        assert hasattr(link, 'context')


def test_generate_external_references():
    serp_items = [
        SERPItem(
            rank=1,
            url="https://harvard.edu/research",
            title="Harvard Research on Productivity",
            snippet="Academic research on productivity"
        ),
        SERPItem(
            rank=2,
            url="https://example.com/blog",
            title="Blog Post",
            snippet="Regular blog content"
        ),
        SERPItem(
            rank=3,
            url="https://wikipedia.org/productivity",
            title="Wikipedia: Productivity",
            snippet="Encyclopedia entry"
        )
    ]
    
    references = generate_external_references(serp_items)
    
    assert isinstance(references, list)
    assert len(references) > 0
    assert len(references) <= 4
    
    for ref in references:
        assert hasattr(ref, 'url')
        assert hasattr(ref, 'title')
        assert hasattr(ref, 'citation_context')
        assert hasattr(ref, 'placement_suggestion')


def test_generate_external_references_prioritizes_authority():
    serp_items = [
        SERPItem(
            rank=1,
            url="https://example.com/blog",
            title="Regular Blog",
            snippet="Blog content"
        ),
        SERPItem(
            rank=2,
            url="https://mit.edu/research",
            title="MIT Research",
            snippet="Academic research"
        )
    ]
    
    references = generate_external_references(serp_items)
    
    authority_refs = [r for r in references if '.edu' in r.url or '.gov' in r.url]
    assert len(authority_refs) > 0

