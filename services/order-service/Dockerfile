FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install fastapi uvicorn sqlmodel asyncpg aiokafka

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
