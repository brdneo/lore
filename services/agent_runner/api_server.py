#!/usr/bin/env python3
"""
FastAPI Server - Lore N.A.
==========================

Servidor API para persistência e gerenciamento de agentes neurais.
Preparado para deploy 24/7 na nuvem (Railway + Neon).

Autor: Lore N.A. Genesis Team
Data: 31 de Dezembro de 2024
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import json
import os
from datetime import datetime

# Importar configurações cloud e database
try:
    from cloud_deployment_config import CloudConfig, HealthCheck
    from database_manager import LoREDatabase
    cloud_config = CloudConfig.get_full_config()
    is_production = CloudConfig.is_production()
    
    # Inicializar database
    db = LoREDatabase()
    
except ImportError as e:
    # Fallback para desenvolvimento local
    print(f"⚠️ Aviso: {e}")
    cloud_config = {
        "app": {
            "title": "Lore N.A. Neural Agents API",
            "description": "API para agentes neurais autônomos",
            "version": "2.0.0",
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "cors_origins": ["*"]
        }
    }
    is_production = False
    db = None

app = FastAPI(
    title=cloud_config["app"]["title"],
    description=cloud_config["app"]["description"],
    version=cloud_config["app"]["version"],
    docs_url=cloud_config["app"].get("docs_url"),
    redoc_url=cloud_config["app"].get("redoc_url")
)

# CORS middleware configurado para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=cloud_config["app"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AgentCreate(BaseModel):
    name: str
    dna: Dict
    personality: str

class AgentResponse(BaseModel):
    id: str
    name: str
    full_name: str
    personality: str
    generation: int
    fitness_scores: Dict
    created_at: datetime

class PopulationStats(BaseModel):
    total_agents: int
    current_generation: int
    average_fitness: float
    top_performers: List[AgentResponse]

# Storage usando database
AGENTS_FILE = "data/agents.json"  # Fallback file
EVOLUTION_FILE = "data/evolution_history.json"  # Fallback file

def load_agents():
    """Carrega agentes do database"""
    if db:
        agents = db.get_all_agents()
        return {agent['id']: agent for agent in agents}
    
    # Fallback para arquivo se database não disponível
    if os.path.exists(AGENTS_FILE):
        with open(AGENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_agents(agents):
    """Salva agentes no database"""
    if db:
        for agent_id, agent_data in agents.items():
            agent_data['id'] = agent_id  # Garantir que o ID está presente
            db.save_agent(agent_data)
        return True
    
    # Fallback para arquivo se database não disponível
    os.makedirs("data", exist_ok=True)
    with open(AGENTS_FILE, 'w') as f:
        json.dump(agents, f, indent=2, default=str)
    return True

@app.get("/")
async def root():
    """Endpoint raiz com informações do sistema"""
    return {
        "message": cloud_config["app"]["title"],
        "status": "operational",
        "version": cloud_config["app"]["version"],
        "environment": "production" if is_production else "development",
        "docs": "/docs" if not is_production else "disabled_in_production"
    }

@app.get("/agents", response_model=List[AgentResponse])
async def get_agents():
    """Lista todos os agentes"""
    agents = load_agents()
    return list(agents.values())

@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Obtém um agente específico"""
    agents = load_agents()
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents[agent_id]

@app.post("/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    """Cria um novo agente"""
    agents = load_agents()
    
    agent_id = f"agent_{len(agents) + 1:05d}"
    
    new_agent = {
        "id": agent_id,
        "name": agent.name,
        "full_name": agent.name,  # Será expandido pela lógica do sistema
        "personality": agent.personality,
        "dna": agent.dna,
        "generation": 0,
        "fitness_scores": {"overall": 0.5},
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    agents[agent_id] = new_agent
    save_agents(agents)
    
    return new_agent

@app.put("/agents/{agent_id}/fitness")
async def update_fitness(agent_id: str, fitness_scores: Dict[str, float]):
    """Atualiza scores de fitness de um agente"""
    agents = load_agents()
    
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agents[agent_id]["fitness_scores"] = fitness_scores
    agents[agent_id]["updated_at"] = datetime.now()
    
    save_agents(agents)
    return {"message": "Fitness updated", "agent_id": agent_id}

@app.get("/population/stats", response_model=PopulationStats)
async def get_population_stats():
    """Estatísticas da população"""
    agents = load_agents()
    
    if not agents:
        return PopulationStats(
            total_agents=0,
            current_generation=0,
            average_fitness=0.0,
            top_performers=[]
        )
    
    agent_list = list(agents.values())
    total_agents = len(agent_list)
    current_generation = max(a.get("generation", 0) for a in agent_list)
    average_fitness = sum(a.get("fitness_scores", {}).get("overall", 0) for a in agent_list) / total_agents
    
    # Top 5 performers
    top_performers = sorted(
        agent_list, 
        key=lambda x: x.get("fitness_scores", {}).get("overall", 0), 
        reverse=True
    )[:5]
    
    return PopulationStats(
        total_agents=total_agents,
        current_generation=current_generation,
        average_fitness=average_fitness,
        top_performers=top_performers
    )

@app.post("/evolution/run")
async def run_evolution():
    """Executa uma rodada de evolução"""
    # Aqui seria integrado com o PopulationManager
    return {"message": "Evolution cycle completed", "new_generation": "TBD"}

@app.get("/neural-web/connections/{agent_id}")
async def get_agent_connections(agent_id: str):
    """Obtém conexões neurais de um agente"""
    # Integração com NeuralWeb
    return {"agent_id": agent_id, "connections": []}

# Health Check Endpoints para Railway
@app.get("/health")
async def health_check():
    """Health check endpoint para monitoring"""
    try:
        # Verificar sistema básico
        agents = load_agents()
        
        # Verificar database
        db_status = {"status": "not_configured"}
        if db:
            try:
                stats = db.get_stats()
                db_status = {
                    "status": "connected",
                    "type": "PostgreSQL" if db.is_postgresql else "SQLite",
                    "stats": stats
                }
            except Exception as e:
                db_status = {"status": "error", "error": str(e)}
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "environment": "production" if is_production else "development",
            "agents_count": len(agents),
            "database": db_status,
            "version": cloud_config["app"]["version"]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now()
        }

if __name__ == "__main__":
    # Configuração para desenvolvimento e produção
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"  # Necessário para Railway
    
    print(f"🚀 Iniciando Lore N.A. API Server")
    print(f"🌐 Ambiente: {'Produção' if is_production else 'Desenvolvimento'}")
    print(f"🔗 Servidor: http://{host}:{port}")
    
    if db:
        print(f"💾 Database: {'PostgreSQL (Neon)' if db.is_postgresql else 'SQLite (Local)'}")
    else:
        print(f"⚠️ Database: Não disponível (usando arquivos)")
    
    if not is_production:
        print(f"📖 Documentação: http://{host}:{port}/docs")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info" if is_production else "debug"
    )
