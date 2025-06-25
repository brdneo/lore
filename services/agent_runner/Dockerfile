# Usa uma imagem base do Python slim (Debian) com tag específica
FROM python:3.11-slim-bookworm

# Cria usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin -c "App user" appuser

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema, incluindo 'curl' e remove cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Copia o arquivo de dependências e instala as bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip check

# Copia o código da aplicação
COPY --chown=appuser:appuser . .

# Configura permissões
RUN chmod -R 755 /app && \
    chmod 644 /app/*.py

# Muda para usuário não-root
USER appuser

# Configura variáveis de ambiente de segurança
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

# Configura healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# O CMD é um fallback. O entrypoint principal é definido no docker-compose.yml.
CMD ["python", "main.py"]
