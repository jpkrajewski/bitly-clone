## Project - URL Shortener

### Endpoints

- POST /shorten - shorten the URL
- GET /r/{short_url} - redirect the user to the original URL
- GET /telemetry/count/{short_url} - get the number of times the URL was accessed
- GET /telemetry/owner/{short_url} - get the ip address and user agent of user who created the short URL


### Technologies

- Falcon
- MongoDB
- Docker



### How to rnu 

#### Docker 

```bash
docker-compose up --build
```

#### Local 

```bash
uv venv
source venv/bin/activate
cd backend
uv pip install -e .
uvicorn src.app:app --reload
```