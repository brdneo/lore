#!/bin/bash

# 🚀 Lore N.A. - Script de Instalação Automática
# Este script configura todo o ambiente do projeto

set -e  # Para execução em caso de erro

echo "🧠 Bem-vindo ao Lore N.A. - Setup Automático"
echo "=============================================="
echo ""

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale o Docker primeiro."
    echo "📖 Instruções: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Instale o Docker Compose primeiro."
    echo "📖 Instruções: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker e Docker Compose detectados"

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "⚙️  Criando arquivo .env a partir do template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📝 Arquivo .env criado. IMPORTANTE: Edite as senhas antes de continuar!"
        echo ""
        read -p "Pressione Enter após editar o arquivo .env ou CTRL+C para sair..."
    else
        echo "❌ Arquivo .env.example não encontrado!"
        exit 1
    fi
else
    echo "✅ Arquivo .env já existe"
fi

# Verificar se secrets.json existe
if [ ! -f secrets.json ]; then
    echo "🔐 Gerando arquivo de secrets..."
    if [ -f scripts/generate-secrets.py ]; then
        python3 scripts/generate-secrets.py
    else
        echo "⚠️  Script de geração de secrets não encontrado. Criando arquivo básico..."
        cat > secrets.json << EOF
{
    "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "jwt_secret": "$(openssl rand -base64 64)",
    "api_key": "$(openssl rand -hex 32)",
    "db_encryption_key": "$(openssl rand -base64 32)"
}
EOF
    fi
    echo "✅ Secrets gerados"
else
    echo "✅ Arquivo secrets.json já existe"
fi

echo ""
echo "🐳 Iniciando containers do Docker..."
echo "=================================="

# Parar containers existentes (se houver)
docker-compose down 2>/dev/null || true

# Construir e iniciar services
echo "📦 Construindo containers..."
docker-compose build

echo "🚀 Iniciando serviços..."
docker-compose up -d

# Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

# Verificar status dos containers
echo ""
echo "📊 Status dos containers:"
docker-compose ps

# Verificar conectividade
echo ""
echo "🔍 Testando conectividade..."

# Testar PostgreSQL
if docker-compose exec -T postgres pg_isready -U lore_admin -d lore_na &>/dev/null; then
    echo "✅ PostgreSQL: Conectado"
else
    echo "❌ PostgreSQL: Falha na conexão"
fi

# Testar Kong Admin
if curl -f http://localhost:8001/status &>/dev/null; then
    echo "✅ Kong Admin: Ativo (porta 8001)"
else
    echo "⚠️  Kong Admin: Não responsivo"
fi

# Testar Kong Proxy
if curl -f http://localhost:8080/ &>/dev/null; then
    echo "✅ Kong Proxy: Ativo (porta 8080)"
else
    echo "⚠️  Kong Proxy: Não responsivo"
fi

# Configurar Kong (se necessário)
if [ -f infra/kong.yml ]; then
    echo ""
    echo "⚙️  Configurando Kong..."
    sleep 5  # Dar tempo para Kong inicializar
    
    if curl -f -X POST http://localhost:8001/config -F config=@infra/kong.yml &>/dev/null; then
        echo "✅ Kong configurado com sucesso"
    else
        echo "⚠️  Falha na configuração do Kong (pode já estar configurado)"
    fi
fi

# Testar PostgREST
if curl -f http://localhost:8000/ &>/dev/null; then
    echo "✅ PostgREST: Ativo (porta 8000)"
else
    echo "⚠️  PostgREST: Não responsivo"
fi

echo ""
echo "🧪 Configurando ambiente Python para agentes..."
echo "=============================================="

cd services/agent_runner

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv .venv
fi

# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
echo "📚 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Testar importações básicas
echo "🧪 Testando importações..."
python -c "
try:
    from sentiment_service import SentimentService
    print('✅ SentimentService: OK')
except Exception as e:
    print(f'❌ SentimentService: {e}')

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    print('✅ VADER: OK')
except Exception as e:
    print(f'❌ VADER: {e}')

try:
    from textblob import TextBlob
    print('✅ TextBlob: OK')
except Exception as e:
    print(f'❌ TextBlob: {e}')

try:
    from transformers import pipeline
    print('✅ Transformers: OK')
except Exception as e:
    print(f'❌ Transformers: {e}')
"

cd ../..

echo ""
echo "🎉 INSTALAÇÃO CONCLUÍDA!"
echo "========================"
echo ""
echo "📋 Próximos passos:"
echo "1. Verifique se todos os serviços estão ativos: docker-compose ps"
echo "2. Acesse a API via: http://localhost:8080/api/"
echo "3. Para executar um agente:"
echo "   cd services/agent_runner"
echo "   source .venv/bin/activate"
echo "   python main.py"
echo ""
echo "📊 URLs importantes:"
echo "   - Kong Proxy (API): http://localhost:8080"
echo "   - Kong Admin: http://localhost:8001"
echo "   - PostgREST: http://localhost:8000"
echo "   - PostgreSQL: localhost:5432"
echo ""
echo "📚 Documentação completa no README.md"
echo ""
echo "🚀 Bem-vindo ao Lore N.A.! Que os agentes evoluam! 🧠✨"
