#!/usr/bin/env python3
"""
Script para gerar secrets seguros para o projeto Lore
Gera chaves JWT, API keys e outros secrets criptograficamente seguros
"""
import secrets
import string
import hashlib
import base64
import json
from datetime import datetime
import os


def generate_secure_key(length=64):
    """Gera uma chave segura usando secrets module"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_jwt_secret():
    """Gera um secret JWT de 256 bits (32 bytes)"""
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')


def generate_api_key():
    """Gera uma API key no formato padrão"""
    prefix = "lore"
    random_part = secrets.token_urlsafe(32)
    return f"{prefix}_{random_part}"


def generate_database_password():
    """Gera uma senha robusta para o banco"""
    # 20 caracteres com mix de letras, números e símbolos seguros
    alphabet = string.ascii_letters + string.digits + "!@#$%&*+-="
    return ''.join(secrets.choice(alphabet) for _ in range(20))


def main():
    print("🔐 Gerando secrets seguros para o projeto Lore...")

    # Gerar todos os secrets
    secrets_data = {
        "generated_at": datetime.now().isoformat(),
        "jwt_secrets": {
            "agent_genesis": generate_jwt_secret(),
            "agent_trader": generate_jwt_secret(),
            "agent_collector": generate_jwt_secret(),
            "master_key": generate_jwt_secret()
        },
        "database": {
            "postgres_password": generate_database_password(),
            "postgres_user": "postgres_admin",
            "postgres_db": "lore_production"
        },
        "api_keys": {
            "supabase_anon": generate_api_key(),
            "supabase_service": generate_api_key(),
            "admin_api": generate_api_key()
        },
        "encryption": {
            "secret_key_base": generate_secure_key(128),
            "encryption_key": generate_jwt_secret(),
            "session_secret": generate_secure_key(64)
        }
    }

    # Salvar em arquivo seguro
    secrets_file = "secrets.json"
    with open(secrets_file, 'w') as f:
        json.dump(secrets_data, f, indent=2)

    # Definir permissões restritas (apenas owner pode ler)
    os.chmod(secrets_file, 0o600)

    print(f"✅ Secrets gerados e salvos em {secrets_file}")
    print("⚠️  IMPORTANTE: Adicione 'secrets.json' ao .gitignore!")
    print("⚠️  IMPORTANTE: Faça backup seguro deste arquivo!")

    # Gerar template do .env com placeholders
    env_template = """# Lore N.A. - Configuração de Segurança
# ATENÇÃO: Nunca commitar este arquivo com valores reais!

# === BANCO DE DADOS ===
POSTGRES_USER={postgres_user}
POSTGRES_PASSWORD={postgres_password}
POSTGRES_DB={postgres_db}
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgres://{postgres_user}:{postgres_password}@db:5432/{postgres_db}

# === JWT AUTHENTICATION ===
JWT_SECRET={master_key}
SUPABASE_JWT_SECRET={master_key}

# === KONG JWT SECRETS ===
KONG_JWT_ISS_GENESIS=agent_genesis
KONG_JWT_SECRET_GENESIS={agent_genesis}
KONG_JWT_ISS_TRADER=agent_trader
KONG_JWT_SECRET_TRADER={agent_trader}
KONG_JWT_ISS_COLLECTOR=agent_collector
KONG_JWT_SECRET_COLLECTOR={agent_collector}

# === API KEYS ===
ANON_KEY={supabase_anon}
SERVICE_ROLE_KEY={supabase_service}
ADMIN_API_KEY={admin_api}

# === ENCRYPTION ===
SECRET_KEY_BASE={secret_key_base}
ENCRYPTION_KEY={encryption_key}
SESSION_SECRET={session_secret}

# === POSTGREST ===
PGRST_DB_URI=postgres://{postgres_user}:{postgres_password}@db:5432/{postgres_db}
PGRST_DB_SCHEMAS=public,storage,auth
PGRST_DB_ANON_ROLE=anon
PGRST_JWT_SECRET={master_key}

# === APLICAÇÃO ===
APP_NAME=LoreNA
API_EXTERNAL_URL=https://api.lore.local
API_BASE_URL=https://api.lore.local/rest/v1
KONG_INTERNAL_URL=http://kong:8000

# === AGENTE ===
AGENT_NAME=Agente Gênesis
TICK_INTERVAL_SECONDS=15
""".format(
        postgres_user=secrets_data["database"]["postgres_user"],
        postgres_password=secrets_data["database"]["postgres_password"],
        postgres_db=secrets_data["database"]["postgres_db"],
        master_key=secrets_data["jwt_secrets"]["master_key"],
        agent_genesis=secrets_data["jwt_secrets"]["agent_genesis"],
        agent_trader=secrets_data["jwt_secrets"]["agent_trader"],
        agent_collector=secrets_data["jwt_secrets"]["agent_collector"],
        supabase_anon=secrets_data["api_keys"]["supabase_anon"],
        supabase_service=secrets_data["api_keys"]["supabase_service"],
        admin_api=secrets_data["api_keys"]["admin_api"],
        secret_key_base=secrets_data["encryption"]["secret_key_base"],
        encryption_key=secrets_data["encryption"]["encryption_key"],
        session_secret=secrets_data["encryption"]["session_secret"]
    )

    with open(".env.production", 'w') as f:
        f.write(env_template)

    os.chmod(".env.production", 0o600)

    print("✅ Template .env.production criado")
    print("\n🔑 Resumo dos secrets gerados:")
    print(f"  - JWT Secrets: {len(secrets_data['jwt_secrets'])} chaves")
    print(f"  - API Keys: {len(secrets_data['api_keys'])} chaves")
    print(f"  - Encryption Keys: {len(secrets_data['encryption'])} chaves")
    print(f"  - Database: Senha robusta de {len(secrets_data['database']['postgres_password'])} caracteres")


if __name__ == "__main__":
    main()
