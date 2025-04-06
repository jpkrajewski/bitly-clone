FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV="/venv"

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV

WORKDIR /app

ENV PYTHONPATH="/app:$PYTHONPATH"

COPY pyproject.toml ./

COPY src/ ./src

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "urlshortner.app:app", "--host", "0.0.0.0", "--port", "8000"]
