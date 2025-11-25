#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the SEO Agent
"""

import httpx
import asyncio
import json
from datetime import datetime


async def generate_article(topic: str, word_count: int = 1500):
    """Generate an SEO-optimized article"""
    
    api_url = "http://localhost:8000/api/v1"
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        print(f"\n{'='*60}")
        print(f"Generating article: {topic}")
        print(f"Target word count: {word_count}")
        print(f"{'='*60}\n")
        
        print("1. Creating job...")
        response = await client.post(
            f"{api_url}/generate",
            json={
                "topic": topic,
                "target_word_count": word_count,
                "language": "en"
            }
        )
        response.raise_for_status()
        
        job_data = response.json()
        job_id = job_data["job_id"]
        print(f"   Job ID: {job_id}")
        print(f"   Status: {job_data['status']}\n")
        
        print("2. Waiting for completion...")
        max_attempts = 60
        
        for attempt in range(1, max_attempts + 1):
            await asyncio.sleep(2)
            
            response = await client.get(f"{api_url}/jobs/{job_id}")
            response.raise_for_status()
            
            job = response.json()
            status = job["status"]
            
            print(f"   Attempt {attempt}/{max_attempts}: {status}")
            
            if status == "completed":
                print("\n✅ Generation completed!\n")
                return job
            elif status == "failed":
                print(f"\n❌ Generation failed: {job.get('error', 'Unknown error')}\n")
                return None
        
        print("\n⏰ Timeout waiting for completion\n")
        return None


def print_article_summary(job: dict):
    """Print a summary of the generated article"""
    
    if not job or not job.get("article"):
        print("No article data available")
        return
    
    article = job["article"]
    
    print(f"\n{'='*60}")
    print("ARTICLE SUMMARY")
    print(f"{'='*60}\n")
    
    print(f"Title: {article['h1']}")
    print(f"Word Count: {article['word_count']}")
    print(f"\nSEO Title: {article['seo_title']}")
    print(f"Meta Description: {article['meta_description']}\n")
    
    keyword_analysis = article["keyword_analysis"]
    print("Keyword Analysis:")
    print(f"  Primary: {keyword_analysis['primary_keyword']}")
    print(f"  Secondary: {', '.join(keyword_analysis['secondary_keywords'][:5])}")
    
    densities = keyword_analysis['keyword_density']
    print(f"\nKeyword Density:")
    for kw, density in list(densities.items())[:3]:
        print(f"  {kw}: {density}%")
    
    print(f"\nInternal Links: {len(article['internal_links'])}")
    for link in article["internal_links"][:3]:
        print(f"  - {link['anchor_text']} → {link['suggested_target']}")
    
    print(f"\nExternal References: {len(article['external_references'])}")
    for ref in article["external_references"]:
        print(f"  - {ref['title']}")
        print(f"    {ref['url']}")
    
    print("\nValidation Report:")
    for check in article["validation_report"]:
        status = "✅" if check["pass"] else "❌"
        print(f"  {status} {check['check']}: {check['message']}")
    
    print(f"\n{'='*60}\n")
    
    print("First 500 characters of article:")
    print("-" * 60)
    print(article["plain_text"][:500] + "...")
    print("-" * 60)


async def main():
    """Main execution"""
    
    print("\n" + "="*60)
    print("SEO AGENT - EXAMPLE USAGE")
    print("="*60)
    
    topics = [
        "best productivity tools for remote teams",
    ]
    
    for topic in topics:
        job = await generate_article(topic, word_count=800)
        
        if job:
            print_article_summary(job)
            
            output_file = f"example_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(job, f, indent=2)
            print(f"\n📄 Full output saved to: {output_file}\n")


if __name__ == "__main__":
    asyncio.run(main())

