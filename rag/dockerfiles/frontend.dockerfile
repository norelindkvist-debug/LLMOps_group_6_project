FROM python:3.13-slim

WORKDIR /app/frontend

RUN pip install --no-cache-dir uv

COPY frontend/pyproject.toml .

RUN uv sync --no-dev

COPY frontend/ .

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
