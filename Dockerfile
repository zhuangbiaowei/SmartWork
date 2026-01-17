FROM node:18-alpine AS frontend-builder

WORKDIR /app/smartwork/src/frontend
COPY src/frontend/package*.json ./
RUN npm ci

COPY src/frontend/ .
RUN npm run build

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/smartwork

COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend/ .

COPY --from=frontend-builder /app/smartwork/src/frontend/dist ./static/

RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app/smartwork
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]