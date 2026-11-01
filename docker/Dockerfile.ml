# syntax=docker/dockerfile:1.7
# One image for the two services that load models: user_api and worker.
# docker-compose.yml sets the command (and healthcheck) for each of them.
FROM python:3.11-slim

# Empty = default PyPI PyTorch (CUDA build, for GPU servers).
# Local CPU build: https://download.pytorch.org/whl/cpu
ARG TORCH_INDEX_URL=""

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app \
    HF_HOME=/models/huggingface

WORKDIR /app

# Only if PARSER_BACKEND=unstructured, uncomment:
# RUN apt-get update && apt-get install -y --no-install-recommends \
#       poppler-utils tesseract-ocr libgl1 \
#     && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 10001 app \
 && useradd  --system --uid 10001 --gid app --home-dir /app app \
 && mkdir -p /models/huggingface \
 && chown -R app:app /models

COPY pyproject.toml ./
RUN if [ -n "$TORCH_INDEX_URL" ]; then pip install torch --index-url "$TORCH_INDEX_URL"; fi \
 && pip install ".[user,worker]"

COPY --chown=app:app main_user.py ./
COPY --chown=app:app app  ./app
COPY --chown=app:app core ./core

USER app
EXPOSE 8002

# Default is the user API; the worker service overrides this in docker-compose.yml
CMD ["uvicorn", "main_user:app", "--host", "0.0.0.0", "--port", "8002"]
