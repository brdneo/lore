#!/usr/bin/env python3
"""
FastAPI Server - Lore N.A.
==========================

Servidor API para persistência e gerenciamento de agentes neurais.

Autor: Lore N.A. Genesis Team
Data: 27 de Junho de 2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import json
import os
from datetime import datetime

app = FastAPI(
    title="Lore N.A. Neural Agents API",
    description="API para gerenciamento de agentes neurais com vida artificial",
    version="1.0.0"
)

# CORS middleware para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Storage (em produção usar PostgreSQL/MongoDB)
AGENTS_FILE = "data/agents.json"
EVOLUTION_FILE = "data/evolution_history.json"

def load_agents():
    """Carrega agentes do arquivo"""
    if os.path.exists(AGENTS_FILE):
        with open(AGENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_agents(agents):
    """Salva agentes no arquivo"""
    os.makedirs("data", exist_ok=True)
    with open(AGENTS_FILE, 'w') as f:
        json.dump(agents, f, indent=2, default=str)

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Lore N.A. Neural Agents API",
        "status": "operational",
        "version": "1.0.0"
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

if __name__ == "__main__":
    print("🚀 Iniciando Lore N.A. API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
