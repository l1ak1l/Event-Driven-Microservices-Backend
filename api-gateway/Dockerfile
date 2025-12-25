FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv pip install --system -r pyproject.toml

# Alternative if skipping uv inside docker slightly for simplicity with standard pip in minimal container context
# taking 'uv' approach as requested:
# Ideally we generate requirements.txt from uv, but for dev speed 'pip install .' or manual install:
RUN pip install fastapi uvicorn httpx

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
