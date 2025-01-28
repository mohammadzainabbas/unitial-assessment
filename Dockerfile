# Stage 1: Builder
FROM python:3.13-slim as builder

WORKDIR /app
COPY . .

RUN python -m pip install --no-cache-dir uv && \
    uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install --system .

# Stage 2: Runtime
FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app/data /app/data

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]