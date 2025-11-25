# SEO Content Generation Agent

An AI-powered backend service that generates SEO-optimized articles at scale using LangGraph and Groq for LLM.

## Features

- **Intelligent Agent System** - Multi-step reasoning agent using LangGraph
- **SERP Analysis** - Analyzes top 10 search results to understand competitive landscape
- **Natural Content Generation** - Uses Groq's LLM for human-like article creation
- **SEO Validation** - Validates articles against SEO best practices
- **Smart Linking** - Generates internal and external link suggestions
- **Job Persistence** - Tracks generation jobs with resume capability
- **Structured Output** - Returns articles with proper HTML, metadata, and JSON-LD

## Architecture

The system uses a **multi-step AI agent** architecture powered by LangGraph:

```
Input (Topic) → SERP Fetcher → Analyzer → Outline Planner → 
Content Generator → SEO Validator → Metadata Generator → Output
```

### Technology Stack

- **Framework**: FastAPI
- **Agent Framework**: LangGraph with SQLite checkpointing
- **LLM**: Groq (openai/gpt-oss-20b)
- **SERP API**: SerpAPI (with mock fallback)
- **Database**: SQLAlchemy + SQLite
- **Testing**: pytest with async support

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd seo-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your API keys. **Required configuration**:

```env
# Groq LLM Configuration (REQUIRED)
# Get your API key from: https://console.groq.com/keys
GROQ_API_KEY=gsk_your_actual_api_key_here
GROQ_MODEL=openai/gpt-oss-20b

# SERP API Configuration (OPTIONAL - uses mock data if not provided)
# Get your API key from: https://serpapi.com/manage-api-key
SERPAPI_KEY=your_serpapi_key_here

# Database Configuration
DATABASE_URL=sqlite:///./seo_agent.db

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
MAX_WORKERS=4
```

**Important**: 
- Replace `gsk_your_actual_api_key_here` with your real Groq API key
- SERPAPI_KEY is optional - the system falls back to realistic mock data if not provided
- Never commit your `.env` file to version control

### 3. Run the Service

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Usage

### Generate an Article

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "best productivity tools for remote teams",
    "target_word_count": 1500,
    "language": "en"
  }'
```

Response:
```json
{
  "job_id": "abc-123-def-456",
  "status": "pending",
  "created_at": "2025-11-24T10:30:00"
}
```

### Check Job Status

```bash
curl http://localhost:8000/api/v1/jobs/abc-123-def-456
```

Response:
```json
{
  "job_id": "abc-123-def-456",
  "status": "completed",
  "topic": "best productivity tools for remote teams",
  "article": {
    "title": "Best Productivity Tools for Remote Teams",
    "h1": "Best Productivity Tools for Remote Teams",
    "html": "<h1>Best Productivity Tools...</h1>",
    "plain_text": "Best Productivity Tools...",
    "word_count": 1502,
    "seo_title": "Best Productivity Tools for Remote Teams",
    "meta_description": "Comprehensive guide to productivity tools...",
    "keyword_analysis": {
      "primary_keyword": "productivity tools",
      "secondary_keywords": ["remote", "teams", "collaboration"],
      "keyword_density": {"productivity tools": 1.8}
    },
    "internal_links": [...],
    "external_references": [...],
    "validation_report": [...]
  }
}
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
seo-agent/
├── app/
│   ├── api/              # FastAPI routes and dependencies
│   ├── core/             # LangGraph agent implementation
│   ├── db/               # Database repository layer
│   ├── models/           # Pydantic schemas and SQLAlchemy models
│   ├── services/         # Business logic (LLM, SERP, SEO, etc.)
│   ├── utils/            # Utilities (logging, HTML generation)
│   └── main.py           # FastAPI application entry point
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test data
├── .env                  # Environment variables (not in git)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_analyzer.py

# Run with verbose output
pytest -v
```

## How It Works

### 1. SERP Analysis
- Fetches top 10 search results for the topic
- Extracts common themes, keywords, and topics
- Identifies what successful content covers

### 2. Outline Generation
- Creates structured outline with H1, H2, and H3 hierarchy
- Ensures coverage of key topics from SERP analysis
- Naturally incorporates target keywords

### 3. Content Generation
- Generates each section using Groq LLM
- Maintains natural, human-like writing
- Avoids keyword stuffing

### 4. SEO Optimization
- Validates keyword placement and density
- Checks readability score (Flesch Reading Ease)
- Ensures proper header hierarchy
- Generates meta tags and structured data

### 5. Link Generation
- Suggests 3-5 internal links to related content
- Identifies 2-4 authoritative external references
- Provides placement context for each link

## SEO Validation Checks

The system validates:
- Primary keyword in H1 title
- Primary keyword in introduction
- Word count within target range (±15%)
- Multiple H2 sections (at least 3)
- Readability score (Flesch Reading Ease: 30-80)
- Keyword density (0.5-3.0%)


## Error Handling

The system gracefully handles:
- **SERP API failures** - Falls back to mock data
- **LLM failures** - Retries with exponential backoff (3 attempts)
- **Invalid responses** - Uses fallback templates
- **Database errors** - Properly tracked in job status

## Resume Capability

Thanks to LangGraph checkpointing, if the process crashes:
1. Job state is automatically saved after each step
2. The agent can resume from the last successful checkpoint
3. No need to re-fetch SERP data or regenerate completed sections

## Performance

- **Average generation time**: 30-60 seconds (depending on word count)
- **SERP fetch**: ~2-3 seconds
- **LLM generation**: ~20-40 seconds (for 1500 words)
- **Validation**: < 1 second

## Troubleshooting

### "No GROQ_API_KEY found"
Make sure your `.env` file exists and contains a valid `GROQ_API_KEY`.

### "SERP API failed, falling back to mock"
Either no `SERPAPI_KEY` is configured, or the API call failed. The system will use realistic mock data.

### Tests failing
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```




