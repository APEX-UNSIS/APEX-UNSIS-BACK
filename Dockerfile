# Backend APEX-UNSIS (FastAPI + PostgreSQL client)
FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables de entorno se inyectan en tiempo de ejecución (docker-compose / .env)
# No incluir .env con datos reales en la imagen
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
