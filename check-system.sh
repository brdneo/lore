#!/bin/bash

# 🔍 Lore N.A. - Verificação de Sistema
# Script para verificar se todos os componentes estão funcionando

echo "🔍 Lore N.A. - Verificação Completa do Sistema"
echo "=============================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success_count=0
total_checks=0

check_service() {
    local service_name=$1
    local check_command=$2
    local expected_result=$3
    
    total_checks=$((total_checks + 1))
    echo -n "Verificando $service_name... "
    
    if eval "$check_command" &>/dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
        success_count=$((success_count + 1))
    else
        echo -e "${RED}❌ FALHA${NC}"
        if [ ! -z "$expected_result" ]; then
            echo "   Esperado: $expected_result"
        fi
    fi
}

# 1. Verificar Docker
echo "🐳 DOCKER & CONTAINERS"
echo "====================="
check_service "Docker" "docker --version"
check_service "Docker Compose" "docker-compose --version"

# Verificar containers em execução
if docker-compose ps | grep -q "Up"; then
    echo -e "Containers ativos: ${GREEN}✅ OK${NC}"
    success_count=$((success_count + 1))
else
    echo -e "Containers ativos: ${RED}❌ FALHA${NC}"
fi
total_checks=$((total_checks + 1))

echo ""

# 2. Verificar Serviços de Rede
echo "🌐 CONECTIVIDADE DE REDE"
echo "======================="
check_service "PostgreSQL (interno)" "docker-compose exec -T postgres pg_isready -U lore_admin -d lore_na"
check_service "Kong Admin API (8001)" "curl -f http://localhost:8001/status"
check_service "Kong Proxy (8080)" "curl -f http://localhost:8080/"
check_service "PostgREST (8000)" "curl -f http://localhost:8000/"

echo ""

# 3. Verificar Database
echo "🐘 DATABASE"
echo "==========="
check_service "Conexão PostgreSQL" "docker-compose exec -T postgres psql -U lore_admin -d lore_na -c 'SELECT 1'"

# Verificar tabelas essenciais
check_service "Tabela agents" "docker-compose exec -T postgres psql -U lore_admin -d lore_na -c '\dt agents'"
check_service "Tabela limbo" "docker-compose exec -T postgres psql -U lore_admin -d lore_na -c '\dt limbo'"

echo ""

# 4. Verificar Ambiente Python
echo "🐍 AMBIENTE PYTHON"
echo "=================="

if [ -d "services/agent_runner/.venv" ]; then
    cd services/agent_runner
    source .venv/bin/activate
    
    # Verificar imports Python
    python -c "
import sys
modules_to_check = [
    ('sentiment_service', 'SentimentService'),
    ('vaderSentiment.vaderSentiment', 'SentimentIntensityAnalyzer'),
    ('textblob', 'TextBlob'),
    ('transformers', 'pipeline'),
    ('requests', 'requests'),
    ('asyncio', 'asyncio')
]

success = 0
total = len(modules_to_check)

for module, component in modules_to_check:
    try:
        exec(f'from {module} import {component}')
        print(f'✅ {module}: OK')
        success += 1
    except Exception as e:
        print(f'❌ {module}: {e}')

print(f'')
print(f'Módulos Python: {success}/{total} OK')
"
    
    cd ../..
else
    echo -e "Ambiente virtual Python: ${RED}❌ NÃO ENCONTRADO${NC}"
    echo "Execute: cd services/agent_runner && python -m venv .venv"
fi

echo ""

# 5. Verificar Arquivos de Configuração
echo "⚙️  CONFIGURAÇÃO"
echo "==============="
check_service "Arquivo .env" "test -f .env"
check_service "Arquivo secrets.json" "test -f secrets.json"
check_service "Kong config" "test -f infra/kong.yml"
check_service "Requirements.txt" "test -f services/agent_runner/requirements.txt"

echo ""

# 6. Teste de API
echo "🧪 TESTE DE API"
echo "=============="

# Testar endpoint básico
if curl -f http://localhost:8080/api/ &>/dev/null; then
    echo -e "API básica: ${GREEN}✅ OK${NC}"
    success_count=$((success_count + 1))
else
    echo -e "API básica: ${RED}❌ FALHA${NC}"
fi
total_checks=$((total_checks + 1))

# Testar endpoints específicos
check_service "Endpoint /agents" "curl -f http://localhost:8080/api/agents"
check_service "Endpoint /limbo" "curl -f http://localhost:8080/api/limbo"

echo ""

# 7. Resumo Final
echo "📊 RESUMO FINAL"
echo "=============="

percentage=$((success_count * 100 / total_checks))

echo "Total de verificações: $total_checks"
echo "Sucessos: $success_count"
echo "Falhas: $((total_checks - success_count))"
echo ""

if [ $percentage -ge 90 ]; then
    echo -e "Status geral: ${GREEN}🎉 EXCELENTE ($percentage%)${NC}"
    echo "✅ Sistema pronto para uso!"
elif [ $percentage -ge 70 ]; then
    echo -e "Status geral: ${YELLOW}⚠️  BOM ($percentage%)${NC}"
    echo "🔧 Algumas correções podem ser necessárias"
else
    echo -e "Status geral: ${RED}❌ CRÍTICO ($percentage%)${NC}"
    echo "🚨 Vários problemas detectados - verifique logs"
fi

echo ""
echo "📋 PRÓXIMOS PASSOS:"

if [ $percentage -ge 80 ]; then
    echo "1. Execute um agente: cd services/agent_runner && python main.py"
    echo "2. Monitore logs: docker-compose logs -f"
    echo "3. Acesse API: http://localhost:8080/api/"
else
    echo "1. Verifique os serviços com falha acima"
    echo "2. Execute: docker-compose logs [nome_do_servico]"
    echo "3. Reinicie se necessário: docker-compose restart"
fi

echo ""
echo "🧠 Bem-vindo ao Lore N.A.! 🚀"
