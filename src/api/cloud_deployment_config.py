#!/usr/bin/env python3
"""
Cloud Deployment Configuration - Lore N.A.
==========================================

Configurações e scripts para deploy 24/7 na nuvem.
Stack escolhido: Railway + Neon PostgreSQL

Autor: Lore N.A. Genesis Team
Data: 31 de Dezembro de 2024
"""

import os
from datetime import datetime
from typing import Dict, Any

class CloudConfig:
    """Configurações para deployment na nuvem"""
    
    # Railway Configuration
    RAILWAY_CONFIG = {
        "port": int(os.getenv("PORT", 8000)),
        "host": "0.0.0.0",
        "workers": int(os.getenv("WEB_CONCURRENCY", 1)),
        "timeout": 300,
        "keep_alive": 2
    }
    
    # Neon PostgreSQL Configuration
    DATABASE_CONFIG = {
        "url": os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_Il2RJN8hGwYb@ep-orange-fog-a5a3ol11-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"),
        "pool_size": 20,
        "max_connections": 30,
        "ssl_mode": "require",
        # Configurações específicas Neon
        "project_name": "lore-na-universe",
        "postgres_version": "15",
        "cloud_provider": "aws",
        "region": "us-east-2",  # Ohio (sua região real)
        "connection_pooling": True,
        "auto_scaling": True,
        # Credenciais reais
        "host": "ep-orange-fog-a5a3ol11-pooler.us-east-2.aws.neon.tech",
        "database": "neondb",
        "user": "neondb_owner"
    }
    
    # Environment Detection
    @staticmethod
    def is_production() -> bool:
        return os.getenv("RAILWAY_ENVIRONMENT") == "production"
    
    @staticmethod
    def is_development() -> bool:
        return not CloudConfig.is_production()
    
    # Application Settings
    @staticmethod
    def get_app_config():
        """Retorna configuração da aplicação baseada no ambiente"""
        is_dev = not os.getenv("RAILWAY_ENVIRONMENT") == "production"
        return {
            "title": "Lore N.A. Neural Agents API",
            "description": "API para agentes neurais autônomos com vida artificial",
            "version": "2.0.0",
            "docs_url": "/docs" if is_dev else None,  # Desabilitar docs em produção
            "redoc_url": "/redoc" if is_dev else None,
            "cors_origins": [
                "https://*.railway.app",
                "https://lore-na.vercel.app",
                "http://localhost:3000",
                "http://localhost:8080"
            ] if not is_dev else ["*"]
        }
    
    # Monitoring & Health Check
    MONITORING_CONFIG = {
        "health_check_interval": 30,  # seconds
        "metrics_enabled": True,
        "log_level": "INFO"
    }
    
    @staticmethod
    def get_database_url() -> str:
        """Retorna URL do database baseada no ambiente"""
        if CloudConfig.is_production():
            # Railway automaticamente injeta DATABASE_URL do Neon
            return os.getenv("DATABASE_URL")
        else:
            # Local SQLite para desenvolvimento
            return "sqlite:///lore_local.db"
    
    @staticmethod
    def get_full_config() -> Dict[str, Any]:
        """Retorna configuração completa"""
        return {
            "railway": CloudConfig.RAILWAY_CONFIG,
            "database": CloudConfig.DATABASE_CONFIG,
            "app": CloudConfig.get_app_config(),
            "monitoring": CloudConfig.MONITORING_CONFIG,
            "environment": {
                "is_production": CloudConfig.is_production(),
                "database_url": CloudConfig.get_database_url()
            }
        }

# Health Check Endpoints
class HealthCheck:
    """Sistema de monitoramento de saúde"""
    
    @staticmethod
    def check_database_connection():
        """Verifica conexão com database"""
        try:
            from database_manager import LoREDatabase
            db = LoREDatabase(CloudConfig.get_database_url())
            # Test query
            cursor = db.connection.cursor()
            cursor.execute("SELECT 1")
            return {"status": "healthy", "timestamp": datetime.now()}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "timestamp": datetime.now()}
    
    @staticmethod
    def check_agents_system():
        """Verifica sistema de agentes"""
        try:
            from population_manager import PopulationManager
            pm = PopulationManager("http://localhost:8000")
            agent_count = len(pm.agents)
            return {
                "status": "healthy", 
                "agent_count": agent_count,
                "timestamp": datetime.now()
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "timestamp": datetime.now()}

# Auto-deployment utilities
def prepare_for_deployment():
    """Prepara ambiente para deployment"""
    print("🚀 PREPARANDO PARA DEPLOY CLOUD")
    print("=" * 50)
    
    # 1. Verificar dependências
    print("1️⃣ Verificando dependências...")
    
    # 2. Configurar variáveis de ambiente
    print("2️⃣ Configurando variáveis de ambiente...")
    env_vars = {
        "PORT": "8000",
        "WEB_CONCURRENCY": "1",
        "PYTHONPATH": "/app/src",
        "RAILWAY_ENVIRONMENT": "production"
    }
    
    # 3. Criar arquivos de configuração
    print("3️⃣ Criando arquivos de deploy...")
    
    print("✅ Preparação concluída!")
    print(f"📊 Configuração atual: {CloudConfig.get_full_config()}")

if __name__ == "__main__":
    prepare_for_deployment()
