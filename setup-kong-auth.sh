#!/bin/bash
# setup-kong-auth.sh
# Configura o consumer e as credenciais JWT no Kong

set -e

KONG_ADMIN_URL="http://localhost:8001"
CONSUMER_USERNAME="agent_genesis"
JWT_KEY="agent_genesis"
JWT_SECRET="MinhaChaveSecretaSuperSegura123"

echo "Configurando autenticação JWT no Kong..."

# Verifica se Kong está rodando
echo "Verificando se Kong está acessível..."
until curl -sSf "$KONG_ADMIN_URL" > /dev/null; do
  echo "Aguardando Kong ficar disponível..."
  sleep 2
done

# Cria o consumer
echo "1. Criando consumer '$CONSUMER_USERNAME'..."
CONSUMER_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/consumer_response.json -X POST "$KONG_ADMIN_URL/consumers" \
  --data "username=$CONSUMER_USERNAME")

if [ "$CONSUMER_RESPONSE" = "201" ] || [ "$CONSUMER_RESPONSE" = "409" ]; then
    echo "Consumer criado ou já existente."
else
    echo "Erro ao criar consumer. Código: $CONSUMER_RESPONSE"
    cat /tmp/consumer_response.json
    exit 1
fi

# Associa credencial JWT
echo "2. Associando credencial JWT..."
JWT_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/jwt_response.json -X POST "$KONG_ADMIN_URL/consumers/$CONSUMER_USERNAME/jwt" \
  --data "key=$JWT_KEY" \
  --data "secret=$JWT_SECRET")

if [ "$JWT_RESPONSE" = "201" ] || [ "$JWT_RESPONSE" = "409" ]; then
    echo "Credencial JWT criada ou já existente."
else
    echo "Erro ao criar credencial JWT. Código: $JWT_RESPONSE"
    cat /tmp/jwt_response.json
    exit 1
fi

echo ""
echo "✅ Configuração JWT concluída com sucesso!"
echo "Consumer: $CONSUMER_USERNAME"
echo "JWT Key (iss): $JWT_KEY"
echo ""
echo "Para testar, use:"
echo "curl -H 'Authorization: Bearer <TOKEN>' http://localhost:8000/rest/v1/agents"

# Cleanup
rm -f /tmp/consumer_response.json /tmp/jwt_response.json
