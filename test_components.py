#!/usr/bin/env python3
"""Quick component test to isolate issues"""

import asyncio
import sys
sys.path.insert(0, '/Users/devs/Documents/seo-agent')

async def test_components():
    print("Testing individual components...")
    
    # Test 1: Config
    print("\n1. Testing config...")
    try:
        from app.config import get_settings
        settings = get_settings()
        print(f"   Config loaded")
        print(f"   - GROQ Model: {settings.groq_model}")
        print(f"   - GROQ API Key: {settings.groq_api_key[:20]}...")
    except Exception as e:
        print(f"   Config failed: {e}")
        return
    
    # Test 2: SERP Service
    print("\n2. Testing SERP service...")
    try:
        from app.services.serp import fetch_serp_results
        results = await fetch_serp_results("test query")
        print(f"   SERP service works - got {len(results)} results")
    except Exception as e:
        print(f"   SERP failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: LLM Service
    print("\n3. Testing LLM service...")
    try:
        from app.services.llm import get_llm_client
        llm = get_llm_client()
        print(f"   LLM client created")
        print(f"   - Model: {llm.model}")
        
        # Try a simple generation
        response = await llm.generate("Say 'test successful' in 3 words", max_tokens=20)
        print(f"   LLM generation works: {response[:50]}")
    except Exception as e:
        print(f"   LLM failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Agent State
    print("\n4. Testing agent graph...")
    try:
        from app.core.graph import get_agent_graph
        graph = get_agent_graph()
        print(f"   Agent graph created")
    except Exception as e:
        print(f"   Agent graph failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*50)
    print("Component tests complete!")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_components())

