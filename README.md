## URL Shortener

A minimal, extensible URL shortening service built with clean architecture in mind.

### Endpoints

- POST /shorten - Create a shortened version of a long URL
- GET /r/{short_url} - Redirect to the original URL
- GET /telemetry/count/{short_url} - Retrieve access count of the short URL
- GET /telemetry/owner/{short_url} - Retrieve IP and User-Agent of the creator

### Tech Stack

- Falcon – high-performance ASGI web framework
- MongoDB – primary data store
- Docker – for containerized local development

### Getting Started

#### Run with Docker

```bash
docker-compose up --build
```

#### Run Locally (Requires local MongoDB)

```bash
uv venv
source venv/bin/activate
cd backend
uv pip install -e .
uvicorn src.app:app --reload
```

### Run tests
```bash
pytest
```



### Why Use 302 Redirect?

We return HTTP 302 (Found) for redirection:

- Indicates a temporary redirect (the short URL may change later)
- Prevents browsers from caching the redirect permanently
- Maintains flexibility and accurate click tracking
- Should be combined with `Cache-Control: no-store` to fully prevent caching

Using 301 (permanent) could lead to browser-level caching that bypasses future logic or changes in destination.

### Architecture Patterns

- **Service Layer** – business logic lives in services like BasicTelemetryService and BasicLinkService, decoupled from the web framework
- **Repository Pattern** – AbstractLinkRepository abstracts DB access, enabling easy replacement with other data sources
- **Cached Repository** – CachedLinkRepository adds caching to the repository, improving performance
- **Adapter Pattern** – repository acts as an adapter implementing AbstractLinkRepository
- **Dependency Injection** – services and repositories are injected through constructors
- **App Bootstrap / Factory** – all setup is handled in create_app() for modularity and testability
