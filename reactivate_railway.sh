#!/bin/bash
# Script de Reativação Automática do Railway

echo "🚂 Iniciando reativação do Railway Deploy..."

# Verificar Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI não encontrado"
    echo "📦 Instalando Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
    export PATH="$HOME/.railway/bin:$PATH"
fi

echo "✅ Railway CLI encontrado"

# Login (se necessário)
echo "🔑 Verificando login..."
railway whoami || railway login

# Conectar ao projeto
echo "🔗 Conectando ao projeto..."
railway link e20bef32-6bb9-4670-8a79-c60fa4939e71

# Verificar status
echo "📊 Verificando status..."
railway status
railway ps

# Verificar variáveis
echo "🔧 Verificando variáveis..."
railway variables

# Tentar redeploy
echo "🚀 Iniciando redeploy..."
railway up --detach

# Verificar logs
echo "📋 Verificando logs..."
railway logs --tail 50

echo "✅ Script de reativação concluído"
echo "🌐 Teste a URL: https://lore-na-production.up.railway.app"
