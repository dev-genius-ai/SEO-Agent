import pytest
from app.services.analyzer import extract_keywords, calculate_keyword_density, tokenize
from app.models.schemas import SERPItem


def test_tokenize():
    text = "The best productivity tools for remote teams"
    tokens = tokenize(text)
    
    assert "productivity" in tokens
    assert "tools" in tokens
    assert "remote" in tokens
    assert "teams" in tokens
    assert "the" not in tokens
    assert "for" not in tokens


def test_extract_keywords():
    serp_items = [
        SERPItem(
            rank=1,
            url="https://example.com/1",
            title="Best Productivity Tools for Remote Teams",
            snippet="Discover productivity tools that help remote teams collaborate"
        ),
        SERPItem(
            rank=2,
            url="https://example.com/2",
            title="Top Remote Work Productivity Software",
            snippet="Remote work tools for team productivity and collaboration"
        )
    ]
    
    keywords = extract_keywords(serp_items)
    
    assert "primary" in keywords
    assert "secondary" in keywords
    assert len(keywords["secondary"]) > 0
    assert isinstance(keywords["primary"], str)


def test_calculate_keyword_density():
    text = "productivity tools for productivity and remote teams with productivity software"
    keywords = ["productivity", "remote", "tools"]
    
    density = calculate_keyword_density(text, keywords)
    
    assert "productivity" in density
    assert "remote" in density
    assert "tools" in density
    assert density["productivity"] > density["remote"]
    assert all(isinstance(v, float) for v in density.values())

