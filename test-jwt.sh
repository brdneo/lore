#!/bin/bash
# test-jwt.sh
# Script para testar a autenticação JWT no Kong

set -e

ISS="agent_genesis"
SECRET="MinhaChaveSecretaSuperSegura123"
API_URL="http://localhost:8000/rest/v1"

echo "Gerando token JWT para teste..."

# Verifica se PyJWT está disponível
if ! python3 -c "import jwt" 2>/dev/null; then
    echo "Erro: PyJWT não está instalado. Instale com: pip install PyJWT"
    exit 1
fi

# Gera o token JWT usando Python
TOKEN=$(python3 << EOF
import jwt
import time

payload = {
    'iss': '$ISS',
    'exp': int(time.time()) + 3600
}

token = jwt.encode(payload, '$SECRET', algorithm='HS256')
print(token)
EOF
)

echo "Token gerado: ${TOKEN:0:50}..."
echo ""

# Testa sem token (deve dar 401)
echo "1. Testando sem token (deve dar 401):"
curl -s -w "\nStatus: %{http_code}\n" "$API_URL/agents" || true
echo ""

# Testa com token (deve dar 200)
echo "2. Testando com token (deve dar 200):"
curl -s -w "\nStatus: %{http_code}\n" -H "Authorization: Bearer $TOKEN" "$API_URL/agents"
echo ""

echo "Teste concluído!"
