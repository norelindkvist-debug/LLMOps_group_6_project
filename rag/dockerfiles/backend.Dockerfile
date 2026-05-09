FROM python:3.13-slim

WORKDIR /app/rag/backend

COPY data/ /app/rag/data
COPY backend/ /app/rag/backend

ENV PYTHONPATH=/app

RUN pip install uv
RUN uv sync --no-dev

CMD ["uv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]