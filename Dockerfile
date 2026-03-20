# syntax=docker/dockerfile:1.7
FROM ghcr.io/astral-sh/uv:0.8.15-python3.11-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv export --frozen --no-dev --no-hashes -o requirements.txt
RUN grep -v '^-e \.$' requirements.txt > requirements.runtime.txt
RUN python -m pip install --no-cache-dir --target /install -r requirements.runtime.txt
RUN python -m pip install --no-cache-dir --no-deps --upgrade --target /install .

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY --from=builder /install /app

ENTRYPOINT ["/usr/bin/python3", "-m", "jeff_dean_bot"]
