#!/usr/bin/env python3
"""
Railway Deploy Reactivation Guide
Guia e instruções para reativar o deploy Railway
"""

import os
import subprocess
import json


def check_railway_cli():
    """Verifica se o Railway CLI está instalado"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Railway CLI instalado: {result.stdout.strip()}")
            return True
        else:
            print("❌ Railway CLI não encontrado")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI não encontrado")
        return False


def show_reactivation_guide():
    """Mostra guia de reativação"""

    print("🚂 GUIA DE REATIVAÇÃO DO RAILWAY DEPLOY")
    print("=" * 60)
    print()

    # Dados do projeto
    railway_data = {
        "projectId": "e20bef32-6bb9-4670-8a79-c60fa4939e71",
        "serviceId": "e5b3e063-be8f-409a-8c78-26dc34fbfa51",
        "environmentId": "9c86a94e-8c19-47e6-a5e0-5c6a9e27b4b8",
        "publicDomain": "lore-na-production.up.railway.app",
        "sshConnection": "ssh root@containers-us-west1.railway.app -p 30625"
    }

    print("## 📋 DADOS DO PROJETO")
    for key, value in railway_data.items():
        print(f"- {key}: {value}")
    print()

    print("## 🔧 INSTRUÇÕES DE REATIVAÇÃO")
    print()

    # Verificar se CLI está instalado
    cli_installed = check_railway_cli()
    print()

    if not cli_installed:
        print("### 1. INSTALAR RAILWAY CLI")
        print("```bash")
        print("# Método 1 - NPM")
        print("npm install -g @railway/cli")
        print()
        print("# Método 2 - Curl")
        print("curl -fsSL https://railway.app/install.sh | sh")
        print()
        print("# Método 3 - Homebrew (macOS)")
        print("brew install railway")
        print("```")
        print()

    print("### 2. LOGIN NO RAILWAY")
    print("```bash")
    print("railway login")
    print("```")
    print()

    print("### 3. CONECTAR AO PROJETO")
    print("```bash")
    print(f"railway link {railway_data['projectId']}")
    print("```")
    print()

    print("### 4. VERIFICAR STATUS")
    print("```bash")
    print("railway status")
    print("railway ps")
    print("```")
    print()

    print("### 5. REDEPLOYAR SE NECESSÁRIO")
    print("```bash")
    print("# Redeploy do último commit")
    print("railway up")
    print()
    print("# Ou forçar novo deploy")
    print("railway up --detach")
    print("```")
    print()

    print("### 6. VERIFICAR LOGS")
    print("```bash")
    print("railway logs")
    print("railway logs --follow")
    print("```")
    print()

    print("### 7. CONFIGURAR VARIÁVEIS (SE NECESSÁRIO)")
    print("```bash")
    print("railway variables")
    print("railway variables set DATABASE_URL='sua_url_neon'")
    print("railway variables set JWT_SECRET='seu_jwt_secret'")
    print("```")
    print()

    print("### 8. ACESSO SSH (SE NECESSÁRIO)")
    print("```bash")
    print(f"{railway_data['sshConnection']}")
    print("```")
    print()

    print("## 🎯 CHECKLIST DE VERIFICAÇÃO")
    print("- [ ] Railway CLI instalado e logado")
    print("- [ ] Projeto linkado corretamente")
    print("- [ ] Variáveis de ambiente configuradas")
    print("- [ ] Deploy ativo e funcionando")
    print("- [ ] Health check respondendo em /health")
    print("- [ ] Logs sem erros críticos")
    print()

    print("## 🆘 TROUBLESHOOTING")
    print()
    print("### Deploy não inicia")
    print("1. Verificar Procfile está correto")
    print("2. Verificar requirements.txt atualizado")
    print("3. Verificar main.py como ponto de entrada")
    print("4. Verificar variáveis de ambiente")
    print()

    print("### 404 Error")
    print("1. Deploy pode estar pausado por inatividade")
    print("2. Domínio pode ter mudado")
    print("3. Serviço pode ter sido removido")
    print()

    print("### Database Connection Error")
    print("1. Verificar DATABASE_URL do Neon")
    print("2. Verificar se Neon database está ativo")
    print("3. Verificar conexão de rede")
    print()


def create_reactivation_script():
    """Cria script automatizado de reativação"""

    script_content = """#!/bin/bash
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
"""

    with open("/home/brendo/lore/reactivate_railway.sh", "w") as f:
        f.write(script_content)

    # Tornar executável
    os.chmod("/home/brendo/lore/reactivate_railway.sh", 0o755)

    print("📝 Script de reativação criado: reactivate_railway.sh")


if __name__ == "__main__":
    show_reactivation_guide()
    create_reactivation_script()
