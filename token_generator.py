# token_generator.py
# Utilitário para gerar as chaves JWT necessárias para a stack Supabase.

import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

def generate_jwt(role: str, secret: str) -> str:
    """Gera um JWT com a role e o segredo especificados."""
    payload = {
        "role": role,
        "iss": "supabase",
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int((datetime.now(timezone.utc) + timedelta(days=365*10)).timestamp())
    }
    try:
        encoded_jwt = jwt.encode(payload, secret, algorithm="HS256")
        return encoded_jwt
    except Exception as e:
        print(f"Erro ao gerar o JWT para a role '{role}': {e}")
        return None

def main():
    """Carrega o ambiente e gera as chaves ANON e SERVICE_ROLE."""
    load_dotenv()
    
    # CORREÇÃO: Lê a variável de ambiente correta usada pela stack do Supabase.
    jwt_secret = os.getenv("JWT_SECRET")
    if not jwt_secret or len(jwt_secret) < 32:
        print("Erro: A variável de ambiente JWT_SECRET não está definida no .env ou é muito curta.")
        return

    print("Gerando chaves JWT para o Supabase...")
    
    anon_key = generate_jwt("anon", jwt_secret)
    service_key = generate_jwt("service_role", jwt_secret)
    
    if anon_key and service_key:
        print("\n--- Chaves Geradas com Sucesso! ---")
        print("Copie as seguintes linhas e adicione-as ao seu arquivo .env:")
        print("\n# --- Chaves da API (Geradas pelo token_generator.py) ---")
        print(f"ANON_KEY={anon_key}")
        print(f"SERVICE_ROLE_KEY={service_key}")
        print("\n------------------------------------")
    else:
        print("\n--- Falha ao gerar as chaves. ---")

if __name__ == "__main__":
    main()
