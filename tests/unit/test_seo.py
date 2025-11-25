import pytest
from app.services.seo import (
    generate_seo_title,
    generate_meta_description,
    generate_structured_data,
    validate_article
)


def test_generate_seo_title():
    title = generate_seo_title("Best Productivity Tools", "productivity tools")
    
    assert len(title) <= 60
    assert "productivity tools" in title.lower() or "Best Productivity Tools".lower() in title.lower()
    assert isinstance(title, str)


def test_generate_meta_description():
    desc = generate_meta_description("productivity tools", "Best Productivity Tools for Remote Teams")
    
    assert len(desc) <= 160
    assert "productivity tools" in desc.lower()
    assert isinstance(desc, str)


def test_generate_structured_data():
    data = generate_structured_data(
        "Best Productivity Tools",
        "A comprehensive guide to productivity tools",
        1500
    )
    
    assert data["@context"] == "https://schema.org"
    assert data["@type"] == "Article"
    assert data["headline"] == "Best Productivity Tools"
    assert data["wordCount"] == 1500


def test_validate_article_success():
    article = """# Best Productivity Tools

Productivity tools are essential for remote teams to collaborate effectively.

## Introduction
Modern productivity tools help teams stay organized.

## Features
Key features include task management and collaboration.

## Conclusion
Choosing the right productivity tools is crucial."""

    report = validate_article(
        "Best Productivity Tools",
        article,
        "productivity tools",
        100
    )
    
    assert isinstance(report, list)
    assert len(report) > 0
    assert all("check" in item and "pass" in item for item in report)
    
    title_check = next((r for r in report if r["check"] == "title_contains_keyword"), None)
    assert title_check is not None
    assert title_check["pass"] is True


def test_validate_article_missing_keyword():
    article = "This is an article without the target keyword."
    
    report = validate_article(
        "Random Title",
        article,
        "productivity tools",
        50
    )
    
    title_check = next((r for r in report if r["check"] == "title_contains_keyword"), None)
    assert title_check["pass"] is False

