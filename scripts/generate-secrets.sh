#!/bin/bash
# Script para gerar secrets seguros

echo "🔐 Gerando secrets seguros para o projeto Lore..."

# Função para gerar chaves seguras
generate_key() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
}

# Gerar JWT secrets
JWT_GENESIS=$(generate_key)
JWT_TRADER=$(generate_key)
JWT_COLLECTOR=$(generate_key)
JWT_MASTER=$(generate_key)

# Gerar senha do banco
DB_PASSWORD=$(openssl rand -base64 20 | tr -d "=+/" | cut -c1-16)

# Gerar API keys
API_ANON="lore_$(openssl rand -hex 16)"
API_SERVICE="lore_$(openssl rand -hex 16)"
API_ADMIN="lore_$(openssl rand -hex 16)"

# Gerar encryption keys
SECRET_BASE=$(openssl rand -hex 64)
ENCRYPTION_KEY=$(generate_key)
SESSION_SECRET=$(generate_key)

echo "✅ Secrets gerados com sucesso!"

# Criar arquivo .env.secure
cat > .env.secure << EOF
# Lore N.A. - Configuração de Segurança Produção
# ATENÇÃO: Nunca commitar este arquivo!

# === BANCO DE DADOS ===
POSTGRES_USER=postgres_admin
POSTGRES_PASSWORD=${DB_PASSWORD}
POSTGRES_DB=lore_production
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgres://postgres_admin:${DB_PASSWORD}@db:5432/lore_production

# === JWT AUTHENTICATION ===
JWT_SECRET=${JWT_MASTER}
SUPABASE_JWT_SECRET=${JWT_MASTER}

# === KONG JWT SECRETS ===
KONG_JWT_ISS_GENESIS=agent_genesis
KONG_JWT_SECRET_GENESIS=${JWT_GENESIS}
KONG_JWT_ISS_TRADER=agent_trader
KONG_JWT_SECRET_TRADER=${JWT_TRADER}
KONG_JWT_ISS_COLLECTOR=agent_collector
KONG_JWT_SECRET_COLLECTOR=${JWT_COLLECTOR}

# === API KEYS ===
ANON_KEY=${API_ANON}
SERVICE_ROLE_KEY=${API_SERVICE}
ADMIN_API_KEY=${API_ADMIN}

# === ENCRYPTION ===
SECRET_KEY_BASE=${SECRET_BASE}
ENCRYPTION_KEY=${ENCRYPTION_KEY}
SESSION_SECRET=${SESSION_SECRET}

# === POSTGREST ===
PGRST_DB_URI=postgres://postgres_admin:${DB_PASSWORD}@db:5432/lore_production
PGRST_DB_SCHEMAS=public,storage,auth
PGRST_DB_ANON_ROLE=anon
PGRST_JWT_SECRET=${JWT_MASTER}

# === APLICAÇÃO ===
APP_NAME=LoreNA
API_EXTERNAL_URL=https://api.lore.local
API_BASE_URL=https://api.lore.local/rest/v1
KONG_INTERNAL_URL=http://kong:8000

# === AGENTE ===
AGENT_NAME=Agente Gênesis
TICK_INTERVAL_SECONDS=15
EOF

chmod 600 .env.secure

echo "✅ Arquivo .env.secure criado com permissões restritas"
echo "🔑 Resumo dos secrets:"
echo "  - JWT Master: ${JWT_MASTER:0:8}..."
echo "  - DB Password: ${DB_PASSWORD:0:4}..."
echo "  - API Keys: 3 chaves geradas"
echo "  - Encryption: 3 chaves geradas"
echo ""
echo "⚠️  IMPORTANTE: Adicione '.env.secure' ao .gitignore!"
echo "⚠️  IMPORTANTE: Faça backup seguro deste arquivo!"
