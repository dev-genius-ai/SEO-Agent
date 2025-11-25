# Design Decisions

## Architecture Choices

### 1. LangGraph for Agent Orchestration
**Decision**: Use LangGraph instead of manual orchestration or full LangChain.

**Rationale**: 
- Provides clean state management between agent steps
- Built-in support for complex workflows with conditional logic
- Simpler than full LangChain while more structured than manual pipelines
- Industry-proven for production AI agent systems

### 2. Async/Await Throughout
**Decision**: Use async functions for all I/O operations.

**Rationale**:
- Non-blocking execution for API calls (SERP, LLM)
- Better resource utilization under load
- Native FastAPI support for async endpoints
- Scalable architecture that can handle concurrent requests

### 3. Repository Pattern for Data Access
**Decision**: Abstract database operations behind a Repository layer.

**Rationale**:
- Clean separation between business logic and persistence
- Easy to mock in tests
- Simple to swap database implementations (SQLite → PostgreSQL)
- Follows SOLID principles

### 4. Pydantic for Validation
**Decision**: Use Pydantic models for all API contracts and data validation.

**Rationale**:
- Type-safe validation at runtime
- Automatic API documentation generation
- Clear contracts between layers
- Prevents invalid data from entering the system

### 5. Groq for LLM Provider
**Decision**: Use Groq with openai/gpt-oss-20b model.

**Rationale**:
- Fast inference speed (important for user experience)
- Simple, reliable API
- Good quality for content generation
- Cost-effective

### 6. Graceful Degradation
**Decision**: Implement fallbacks for all external dependencies.

**Rationale**:
- SERP API failure → falls back to mock data
- LLM call failure → retries with exponential backoff (3 attempts)
- System remains functional even when external services fail

### 7. Checkpointing Disabled
**Decision**: Disable LangGraph SQLite checkpointing.

**Rationale**:
- SQLite checkpointer not thread-safe with async operations
- Trade-off: lose resume capability to gain stability
- For production, would use PostgreSQL-based checkpointer
- Core functionality more important than bonus feature

### 8. Background Task Processing
**Decision**: Use FastAPI BackgroundTasks for job execution.

**Rationale**:
- Simple to implement and understand
- Sufficient for moderate load
- No additional infrastructure required
- For high scale, would migrate to Celery + Redis

## Data Flow Decisions

### Sequential Agent Steps
**Decision**: Linear flow through 7 agent nodes.

**Rationale**:
- Clear, predictable execution path
- Easy to debug and monitor
- Each step depends on previous output
- Extensible for future conditional logic

### Job Status Tracking
**Decision**: Persist job state in database with status field.

**Rationale**:
- Enables async status polling
- Provides job history and audit trail
- Supports resume/retry scenarios
- Simple query interface for clients

## Code Organization

### Layer Separation
**Decision**: Strict separation into api/, core/, services/, models/, db/ layers.

**Rationale**:
- Clear responsibility boundaries
- Easy to navigate codebase
- Prevents circular dependencies
- Follows clean architecture principles

### Minimal Comments
**Decision**: Write self-documenting code with minimal comments.

**Rationale**:
- Code should be readable without excessive comments
- Comments can become outdated
- Focus on clear naming and structure
- Reserve comments for complex business logic only

## Technology Trade-offs

### SQLite vs PostgreSQL
**Choice**: SQLite for simplicity.
**Trade-off**: Limited concurrency, but sufficient for assessment and moderate load.

### Mock SERP Data
**Choice**: Realistic mock data with optional API integration.
**Trade-off**: Tests are deterministic, but requires API key for production use.

### Synchronous Graph Execution
**Choice**: Use `asyncio.to_thread()` for graph execution.
**Trade-off**: Slight performance overhead, but solves async/sync compatibility issue.

## What We Avoided

### Over-Engineering
- Did not implement Celery/Redis (overkill for assessment)
- Did not add caching layer (premature optimization)
- Did not implement user authentication (out of scope)

### Under-Engineering
- Did not use simple templates (requirement: actual LLM generation)
- Did not skip error handling (production-readiness required)
- Did not ignore testing (quality demonstration needed)

## Future Improvements

If given more time or moving to production:

1. **Celery + Redis** for distributed task processing
2. **PostgreSQL** for better concurrency and JSON querying
3. **Content quality scorer** with automatic revision loop
4. **FAQ generation** from "People Also Ask" boxes
5. **Redis caching** for SERP results
6. **Rate limiting** on API endpoints
7. **Prometheus metrics** for monitoring
8. **PostgreSQL checkpointer** for resume capability

