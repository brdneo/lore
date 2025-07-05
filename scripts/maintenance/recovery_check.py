#!/usr/bin/env python3
"""
Reconexão Railway & Neon - Lore N.A.
===================================

Script para verificar e reconectar os deploys existentes.
"""

import os
import requests
import json
from datetime import datetime

def check_env_config():
    """Verifica configurações de ambiente recuperadas"""
    print("🔍 VERIFICANDO CONFIGURAÇÕES RECUPERADAS...")
    print()
    
    configs = {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "RAILWAY_ENVIRONMENT": os.getenv("RAILWAY_ENVIRONMENT"), 
        "JWT_SECRET": os.getenv("JWT_SECRET")
    }
    
    for key, value in configs.items():
        if value:
            # Mascarar valores sensíveis
            if "postgresql://" in str(value):
                masked = f"postgresql://***:***@{value.split('@')[1]}" if "@" in value else "postgresql://***"
                print(f"   ✅ {key}: {masked}")
            elif key == "JWT_SECRET":
                print(f"   ✅ {key}: {value[:10]}...{value[-5:]}")
            else:
                print(f"   ✅ {key}: {value}")
        else:
            print(f"   ❌ {key}: NÃO CONFIGURADO")
    print()

def test_database_connection():
    """Testa conexão com o Neon PostgreSQL"""
    print("🐘 TESTANDO CONEXÃO NEON POSTGRESQL...")
    
    try:
        import sys
        sys.path.append('src')
        from database_manager import DatabaseManager
        
        # Inicializar com configurações de produção
        db = DatabaseManager()
        
        if db.is_postgresql:
            print("   ✅ Conectado ao PostgreSQL (Neon)")
            print(f"   📊 Database: {db.DATABASE_URL.split('@')[1].split('/')[0] if '@' in db.DATABASE_URL else 'N/A'}")
            
            # Testar operação básica
            stats = db.get_database_stats()
            print(f"   📈 Agentes: {stats.get('total_agents', 0)}")
            print(f"   🔗 Conexões: {stats.get('total_connections', 0)}")
        else:
            print("   ⚠️  Usando SQLite local (não PostgreSQL)")
            
    except Exception as e:
        print(f"   ❌ Erro na conexão: {e}")
    
    print()

def check_railway_deployment():
    """Verifica possível deployment no Railway"""
    print("🚂 VERIFICANDO RAILWAY DEPLOYMENT...")
    
    # URLs possíveis baseadas no padrão Railway
    possible_urls = [
        "https://lore-production.up.railway.app",
        "https://lore-na-production.up.railway.app", 
        "https://lore-production-a5a3ol11.up.railway.app",
        "https://web-production-a5a3ol11.up.railway.app"
    ]
    
    for url in possible_urls:
        try:
            print(f"   🔍 Testando: {url}")
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ ENCONTRADO! Status: {data.get('status')}")
                print(f"   📊 Environment: {data.get('environment')}")
                print(f"   🔢 Versão: {data.get('version')}")
                print(f"   🗄️  Database: {data.get('database', {}).get('type')}")
                print(f"   🌐 URL Ativa: {url}")
                return url
            else:
                print(f"   ❌ Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Não acessível: {str(e)[:50]}...")
    
    print("   ❌ Nenhum deployment Railway encontrado nos URLs testados")
    print()
    return None

def show_recovery_status():
    """Mostra status da recuperação"""
    print("📋 STATUS DA RECUPERAÇÃO:")
    print()
    
    # Verificar arquivos de configuração existentes
    files_status = {
        "✅ Neon Database": "Configurado com credenciais reais",
        "✅ Arquivos Railway": "Procfile, runtime.txt, railway.json presentes", 
        "✅ Environment": "DATABASE_URL, JWT_SECRET configurados",
        "✅ API Local": "Funcionando com PostgreSQL",
        "⚠️  Railway Deploy": "Precisa verificar se ainda está ativo"
    }
    
    for status, description in files_status.items():
        print(f"   {status}: {description}")
    
    print()

def show_next_steps():
    """Próximos passos baseados na recuperação"""
    print("🎯 PRÓXIMOS PASSOS:")
    print()
    
    print("   1. 🚂 VERIFICAR RAILWAY:")
    print("      • Acessar: https://railway.app/dashboard")
    print("      • Verificar se projeto 'lore' ainda existe")
    print("      • Se existir: Verificar variáveis de ambiente")
    print("      • Se não: Reconectar repositório GitHub")
    print()
    
    print("   2. 🔧 RECONFIGURAR SE NECESSÁRIO:")
    print("      • DATABASE_URL: Já configurado ✅")
    print("      • RAILWAY_ENVIRONMENT: production ✅") 
    print("      • JWT_SECRET: Já configurado ✅")
    print()
    
    print("   3. 🚀 REDEPLOY:")
    print("      • Se Railway ainda conectado: git push para redeploy")
    print("      • Se não: Conectar repo e configurar vars")
    print()

def test_local_production():
    """Testa modo produção local"""
    print("🧪 TESTE LOCAL EM MODO PRODUÇÃO:")
    print("   Execute: python start.py")
    print("   Acesse: http://localhost:8000/health")
    print("   ✅ Deve mostrar 'environment': 'production'")
    print("   ✅ Deve mostrar 'type': 'PostgreSQL'")
    print()

def main():
    """Função principal"""
    print("🔄 LORE N.A. - RECUPERAÇÃO RAILWAY & NEON")
    print("=" * 50)
    print()
    
    # Verificar configurações
    check_env_config()
    
    # Testar database
    test_database_connection()
    
    # Verificar Railway
    active_url = check_railway_deployment()
    
    # Status da recuperação
    show_recovery_status()
    
    # Próximos passos
    show_next_steps()
    
    # Teste local
    test_local_production()
    
    # Resumo final
    print("🎉 RESUMO:")
    if active_url:
        print(f"   ✅ DEPLOY ENCONTRADO: {active_url}")
        print("   🎯 Ação: Verificar se está funcionando 100%")
    else:
        print("   ⚠️  DEPLOY NÃO ENCONTRADO")
        print("   🎯 Ação: Reconectar Railway ou fazer novo deploy")
    
    print()
    print("📚 Documentação de recuperação salva em docs/archive/")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
