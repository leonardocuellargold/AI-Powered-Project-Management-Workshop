FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/ /app/

RUN pip install --no-cache-dir \
    python-dotenv==1.0.1 requests==2.32.3 \
    httpx==0.27.2 \
    openai==1.40.0 anthropic==0.34.2 google-generativeai==0.7.2

ENV PYTHONUNBUFFERED=1
