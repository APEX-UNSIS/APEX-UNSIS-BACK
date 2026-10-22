# Backend APEX-UNSIS (FastAPI + PostgreSQL client)
FROM python:3.11-slim

WORKDIR /app

# psycopg2-binary trae wheels precompilados -> no requiere gcc ni libpq-dev.
# (Además, el egress de los contenedores está bloqueado en esta red, así que
#  depender de apt-get durante el build es frágil: se usa `network: host`.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usuario no-root con el uid/gid del host (1000) para que el bind mount de
# desarrollo sea escribible por el proceso de uvicorn --reload.
ARG UID=1000
ARG GID=1000
RUN groupadd --gid ${GID} appuser \
    && useradd --uid ${UID} --gid ${GID} --create-home appuser \
    && chown -R ${UID}:${GID} /app
USER appuser

# Variables de entorno se inyectan en tiempo de ejecución (docker-compose / .env)
# No incluir .env con datos reales en la imagen
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
