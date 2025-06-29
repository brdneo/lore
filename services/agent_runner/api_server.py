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
from fastapi.responses import HTMLResponse
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
    # Estatísticas básicas
    stats = {}
    agent_count = 0
    
    if db:
        try:
            db_stats = db.get_stats()
            agent_count = db_stats.get('total_agents', 0)
            stats = {
                "agents": db_stats.get('total_agents', 0),
                "generation": db_stats.get('current_generation', 0),
                "connections": db_stats.get('total_connections', 0),
                "evolutions": db_stats.get('total_evolutions', 0)
            }
        except:
            stats = {"error": "Unable to fetch stats"}
    
    return {
        "message": "🧠 Lore N.A. - Neural Agents Universe",
        "description": "Sistema de agentes neurais autônomos em execução 24/7",
        "status": "operational",
        "version": cloud_config["app"]["version"],
        "environment": "production" if is_production else "development",
        "stats": stats,
        "endpoints": {
            "dashboard": "/dashboard - Interface visual do sistema",
            "health": "/health - Status detalhado do sistema",
            "agents": "/agents - Lista todos os agentes",
            "create_agent": "POST /agents - Criar novo agente",
            "agent_detail": "/agents/{id} - Detalhes de um agente",
            "population": "/population/stats - Estatísticas da população"
        },
        "database": {
            "type": "PostgreSQL (Neon)" if db and db.is_postgresql else "SQLite (Local)",
            "status": "connected" if db else "disconnected"
        },
        "docs": "/docs" if not is_production else "https://github.com/brdneo/lore",
        "repository": "https://github.com/brdneo/lore"
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

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Dashboard HTML simples para visualização no navegador"""
    # Buscar estatísticas
    stats = {}
    agents = []
    
    if db:
        try:
            db_stats = db.get_stats()
            stats = {
                "agents": db_stats.get('total_agents', 0),
                "generation": db_stats.get('current_generation', 0),
                "connections": db_stats.get('total_connections', 0),
                "evolutions": db_stats.get('total_evolutions', 0)
            }
            
            # Buscar alguns agentes para mostrar
            all_agents = load_agents()
            agents = list(all_agents.values())[:5]  # Primeiros 5 agentes
            
        except Exception as e:
            stats = {"error": str(e)}
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lore N.A. - Neural Agents Universe</title>
        <meta charset="UTF-8">
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .header h1 {{ font-size: 3em; margin-bottom: 10px; }}
            .subtitle {{ font-size: 1.2em; opacity: 0.8; }}
            .stats-grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-bottom: 40px; 
            }}
            .stat-card {{ 
                background: rgba(255,255,255,0.1); 
                padding: 20px; 
                border-radius: 10px; 
                text-align: center;
                backdrop-filter: blur(10px);
            }}
            .stat-number {{ font-size: 2.5em; font-weight: bold; color: #4CAF50; }}
            .stat-label {{ font-size: 0.9em; opacity: 0.8; }}
            .agents-section {{ 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px; 
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
            }}
            .agent-card {{ 
                background: rgba(255,255,255,0.1); 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 8px; 
                border-left: 4px solid #4CAF50;
            }}
            .endpoints {{ 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }}
            .endpoint-item {{ 
                margin: 10px 0; 
                padding: 10px; 
                background: rgba(255,255,255,0.05); 
                border-radius: 5px; 
            }}
            .endpoint-url {{ color: #81C784; font-family: monospace; }}
            .status-good {{ color: #4CAF50; }}
            .status-warning {{ color: #FF9800; }}
            a {{ color: #81C784; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Lore N.A.</h1>
                <div class="subtitle">Neural Agents Universe - Sistema Autônomo 24/7</div>
                <div class="subtitle">
                    <span class="status-good">● Online</span> | 
                    PostgreSQL (Neon) | 
                    Versão 2.0.0
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{stats.get('agents', 0)}</div>
                    <div class="stat-label">Agentes Ativos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('generation', 0)}</div>
                    <div class="stat-label">Geração Atual</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('connections', 0)}</div>
                    <div class="stat-label">Conexões Neurais</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{stats.get('evolutions', 0)}</div>
                    <div class="stat-label">Evoluções</div>
                </div>
            </div>
            
            <div class="agents-section">
                <h2>🤖 Agentes Recentes</h2>
                {generate_agents_html(agents)}
            </div>
            
            <div class="endpoints">
                <h2>🔗 Endpoints da API</h2>
                <div class="endpoint-item">
                    <strong>GET <span class="endpoint-url">/health</span></strong><br>
                    Status detalhado do sistema e banco de dados
                </div>
                <div class="endpoint-item">
                    <strong>GET <span class="endpoint-url">/agents</span></strong><br>
                    Lista todos os agentes neurais do sistema
                </div>
                <div class="endpoint-item">
                    <strong>POST <span class="endpoint-url">/agents</span></strong><br>
                    Criar um novo agente neural (JSON: name, dna, personality)
                </div>
                <div class="endpoint-item">
                    <strong>GET <span class="endpoint-url">/agents/{{id}}</span></strong><br>
                    Detalhes específicos de um agente
                </div>
                <div class="endpoint-item">
                    <strong>GET <span class="endpoint-url">/population/stats</span></strong><br>
                    Estatísticas da população e métricas de evolução
                </div>
                
                <h3 style="margin-top: 30px;">📚 Links Úteis</h3>
                <div class="endpoint-item">
                    <a href="https://github.com/brdneo/lore" target="_blank">📁 Repositório GitHub</a><br>
                    Código fonte completo do projeto
                </div>
                <div class="endpoint-item">
                    <a href="/health" target="_blank">💓 Health Check</a><br>
                    Verificar status do sistema em tempo real
                </div>
                <div class="endpoint-item">
                    <a href="/agents" target="_blank">🤖 API de Agentes</a><br>
                    Visualizar dados JSON dos agentes
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def generate_agents_html(agents):
    """Gera HTML para mostrar agentes"""
    if not agents:
        return '<p style="opacity: 0.7;">Nenhum agente encontrado. Use POST /agents para criar o primeiro agente.</p>'
    
    html = ""
    for agent in agents:
        # Formatar DNA como string legível
        dna_str = ""
        if agent.get('dna'):
            dna_items = [f"{k}: {v:.2f}" for k, v in agent['dna'].items()]
            dna_str = " | ".join(dna_items)
        
        created_date = agent.get('created_at', '')
        if created_date:
            # Formatar data se possível
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                created_date = dt.strftime("%d/%m/%Y %H:%M")
            except:
                pass
        
        html += f"""
        <div class="agent-card">
            <strong>{agent.get('name', 'Unknown')}</strong> 
            <span style="opacity: 0.7;">({agent.get('id', 'no-id')})</span><br>
            <div style="font-size: 0.9em; margin-top: 5px;">
                <strong>DNA:</strong> {dna_str}<br>
                <strong>Personalidade:</strong> {agent.get('personality', 'N/A')}<br>
                <strong>Criado:</strong> {created_date}
            </div>
        </div>
        """
    
    return html

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
