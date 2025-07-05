#!/usr/bin/env python3
"""
Próximos Passos - Deploy Lore N.A.
=================================

Script interativo para guiar o deploy em produção.
"""

import os
import json
import subprocess
from datetime import datetime

def print_header():
    print("🚀 LORE N.A. - DEPLOY PARA PRODUÇÃO")
    print("=" * 40)
    print()

def check_current_status():
    """Verifica status atual do projeto"""
    print("📊 VERIFICANDO STATUS ATUAL...")
    
    checks = {
        "🏗️  Estrutura do projeto": os.path.exists("src/api_server.py"),
        "📝  Documentação": os.path.exists("docs/reports/STATUS-PRODUCAO.md"),
        "⚙️   Config Railway": os.path.exists("config/railway.json"),
        "🐍  Procfile": os.path.exists("Procfile"),
        "📦  Requirements": os.path.exists("requirements.txt"),
        "🔧  Cloud config": os.path.exists("src/cloud_deployment_config.py"),
        "🗄️   Database manager": os.path.exists("src/database_manager.py"),
    }
    
    all_good = True
    for check, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {check}")
        if not status:
            all_good = False
    
    print()
    if all_good:
        print("🎉 PROJETO 100% PRONTO PARA DEPLOY!")
    else:
        print("⚠️  Alguns arquivos estão faltando")
    
    return all_good

def check_environment():
    """Verifica variáveis de ambiente"""
    print("🔍 VERIFICANDO ENVIRONMENT...")
    
    env_vars = {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "JWT_SECRET": os.getenv("JWT_SECRET"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
        "PORT": os.getenv("PORT", "8000")
    }
    
    for var, value in env_vars.items():
        if value:
            masked_value = value[:20] + "..." if len(value) > 20 else value
            print(f"   ✅ {var}: {masked_value}")
        else:
            print(f"   ❌ {var}: NÃO CONFIGURADO")
    
    print()

def create_env_template():
    """Cria template .env para produção"""
    print("📝 CRIANDO TEMPLATE .env...")
    
    env_content = f"""# Lore N.A. - Configuração de Produção
# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# =================
# RAILWAY CONFIG
# =================
PORT=8000
ENVIRONMENT=production

# =================
# NEON DATABASE
# =================
DATABASE_URL=postgresql://username:password@hostname/database?sslmode=require

# =================
# SECURITY
# =================
JWT_SECRET=your-super-secure-jwt-secret-here-at-least-64-characters-long
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# =================
# API CONFIG
# =================
API_TITLE=Lore N.A. API
API_VERSION=2.0.0
API_DESCRIPTION=Sistema de Vida Artificial

# =================
# LOGGING
# =================
LOG_LEVEL=INFO
"""
    
    with open(".env.production", "w") as f:
        f.write(env_content)
    
    print("   ✅ Arquivo .env.production criado")
    print("   📋 Copie e configure as variáveis conforme necessário")
    print()

def show_deployment_steps():
    """Mostra próximos passos para deploy"""
    print("📋 PRÓXIMOS PASSOS PARA PRODUÇÃO:")
    print()
    
    steps = [
        {
            "title": "1. 🐘 CONFIGURAR NEON POSTGRESQL",
            "actions": [
                "• Acessar: https://neon.tech/",
                "• Criar conta gratuita",
                "• Criar database: 'lore-na-universe'",
                "• Copiar connection string",
                "• Adicionar no .env como DATABASE_URL"
            ]
        },
        {
            "title": "2. 🚂 CONFIGURAR RAILWAY",
            "actions": [
                "• Acessar: https://railway.app/",
                "• Conectar com GitHub",
                "• Importar este repositório",
                "• Configurar variáveis de ambiente",
                "• Fazer primeiro deploy"
            ]
        },
        {
            "title": "3. 🔐 CONFIGURAR SEGURANÇA",
            "actions": [
                "• Gerar JWT_SECRET seguro",
                "• Configurar CORS para domínio",
                "• Adicionar rate limiting",
                "• Configurar SSL/HTTPS"
            ]
        },
        {
            "title": "4. 📊 CONFIGURAR MONITORAMENTO",
            "actions": [
                "• Ativar logs no Railway",
                "• Configurar health checks",
                "• Adicionar alertas de erro",
                "• Monitorar métricas de uso"
            ]
        }
    ]
    
    for step in steps:
        print(f"   {step['title']}")
        for action in step['actions']:
            print(f"     {action}")
        print()

def test_local_api():
    """Testa API local"""
    print("🧪 TESTANDO API LOCAL...")
    
    try:
        # Tentar fazer uma requisição local
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ API local funcionando")
            data = response.json()
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🔢 Versão: {data.get('version')}")
        else:
            print(f"   ❌ API retornou status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ⚠️  API local não está rodando")
        print("   💡 Execute: python start.py")
    except ImportError:
        print("   ⚠️  requests não instalado")
    except Exception as e:
        print(f"   ❌ Erro ao testar API: {e}")
    
    print()

def show_costs():
    """Mostra estimativa de custos"""
    print("💰 ESTIMATIVA DE CUSTOS:")
    print()
    print("   🆓 TIER GRATUITO (Recomendado):")
    print("      • Railway: $500 créditos grátis (~100 meses)")
    print("      • Neon: 0.5GB PostgreSQL grátis")
    print("      • Total: $0/mês por ~8 meses")
    print()
    print("   💰 TIER PAGO (Quando necessário):")
    print("      • Railway Pro: $5/mês")
    print("      • Neon Pro: $19/mês")
    print("      • Total: ~$25/mês")
    print()

def main():
    """Função principal"""
    print_header()
    
    # Status atual
    project_ready = check_current_status()
    
    # Environment check
    check_environment()
    
    # Criar template .env
    create_env_template()
    
    # Testar API local
    test_local_api()
    
    # Próximos passos
    show_deployment_steps()
    
    # Custos
    show_costs()
    
    # Resumo final
    print("🎯 RESUMO:")
    if project_ready:
        print("   ✅ Projeto PRONTO para deploy")
        print("   ⏱️  Tempo estimado: 30 minutos")
        print("   🚀 Próxima ação: Criar contas Neon + Railway")
    else:
        print("   ⚠️  Verificar arquivos faltantes primeiro")
    
    print()
    print("📚 Documentação completa: docs/deployment/DEPLOY-GUIDE.md")
    print("📊 Status detalhado: docs/reports/STATUS-PRODUCAO.md")

if __name__ == "__main__":
    main()
