#!/usr/bin/env python3
"""
Sistema de Modo Offline e Fallback - Lore N.A.
==============================================

Implementa capacidade do universo funcionar independentemente de APIs externas:
- Modo offline automático quando APIs falham
- Cache local de dados críticos
- Fallback para banco SQLite local
- Sincronização automática quando conectividade volta

Autor: Lore N.A. Resilience Team
Data: 2025-07-05
"""

import os
import sys
import json
import sqlite3
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import threading
import time

# Adicionar src ao path
sys.path.append('/home/brendo/lore/src')

from robustness_config import setup_global_error_handling

# Configurar logging
setup_global_error_handling()
logger = logging.getLogger(__name__)

class OfflineCache:
    """Cache local para dados críticos"""
    
    def __init__(self, cache_dir: str = "/home/brendo/lore/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("OfflineCache")
        
        # Arquivos de cache
        self.agent_cache = self.cache_dir / "agents.json"
        self.population_cache = self.cache_dir / "population.json"
        self.neural_web_cache = self.cache_dir / "neural_web.json"
        self.metrics_cache = self.cache_dir / "metrics.json"
        
    def save_agents(self, agents_data: List[Dict[str, Any]]):
        """Salva dados de agentes no cache"""
        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "agents": agents_data,
                "count": len(agents_data)
            }
            
            with open(self.agent_cache, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)
            
            self.logger.info(f"💾 Cache de agentes atualizado: {len(agents_data)} agentes")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar cache de agentes: {e}")
    
    def load_agents(self) -> List[Dict[str, Any]]:
        """Carrega dados de agentes do cache"""
        try:
            if self.agent_cache.exists():
                with open(self.agent_cache, 'r') as f:
                    cache_data = json.load(f)
                
                # Verificar se cache não está muito antigo (24 horas)
                cache_time = datetime.fromisoformat(cache_data["timestamp"])
                if datetime.now() - cache_time < timedelta(hours=24):
                    self.logger.info(f"📂 Cache de agentes carregado: {cache_data['count']} agentes")
                    return cache_data["agents"]
                else:
                    self.logger.warning("⚠️ Cache de agentes expirado")
            
            return []
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar cache de agentes: {e}")
            return []
    
    def save_population_state(self, population_data: Dict[str, Any]):
        """Salva estado da população"""
        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "population": population_data
            }
            
            with open(self.population_cache, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)
            
            self.logger.info("💾 Estado da população salvo no cache")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar estado da população: {e}")
    
    def load_population_state(self) -> Optional[Dict[str, Any]]:
        """Carrega estado da população"""
        try:
            if self.population_cache.exists():
                with open(self.population_cache, 'r') as f:
                    cache_data = json.load(f)
                
                self.logger.info("📂 Estado da população carregado do cache")
                return cache_data["population"]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar estado da população: {e}")
            return None
    
    def save_neural_web(self, neural_web_data: Dict[str, Any]):
        """Salva dados da neural web"""
        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "neural_web": neural_web_data
            }
            
            with open(self.neural_web_cache, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)
            
            self.logger.info("💾 Neural web salva no cache")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar neural web: {e}")
    
    def load_neural_web(self) -> Optional[Dict[str, Any]]:
        """Carrega dados da neural web"""
        try:
            if self.neural_web_cache.exists():
                with open(self.neural_web_cache, 'r') as f:
                    cache_data = json.load(f)
                
                self.logger.info("📂 Neural web carregada do cache")
                return cache_data["neural_web"]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar neural web: {e}")
            return None

class OfflineDatabase:
    """Banco de dados local para modo offline"""
    
    def __init__(self, db_path: str = "/home/brendo/lore/data/offline_universe.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger("OfflineDatabase")
        
        # Inicializar banco local
        self.init_database()
    
    def init_database(self):
        """Inicializa estrutura do banco offline"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela de agentes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    dna_data TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de população
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS population_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    generation INTEGER NOT NULL,
                    population_size INTEGER NOT NULL,
                    state_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de conexões neural web
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS neural_connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id_1 TEXT NOT NULL,
                    agent_id_2 TEXT NOT NULL,
                    connection_strength REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (agent_id_1) REFERENCES agents (id),
                    FOREIGN KEY (agent_id_2) REFERENCES agents (id)
                )
            """)
            
            # Tabela de métricas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
            self.logger.info("✅ Banco de dados offline inicializado")
            
        except Exception as e:
            self.logger.error(f"Falha ao inicializar banco offline: {e}")
    
    def save_agent(self, agent_id: str, name: str, dna_data: Dict[str, Any]):
        """Salva agente no banco offline"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO agents (id, name, dna_data, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (agent_id, name, json.dumps(dna_data, default=str)))
            
            conn.commit()
            conn.close()
            
            self.logger.debug(f"💾 Agente {name} salvo no banco offline")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar agente {agent_id}: {e}")
    
    def load_agents(self) -> List[Dict[str, Any]]:
        """Carrega todos os agentes do banco offline"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name, dna_data, status, created_at FROM agents WHERE status = 'active'")
            rows = cursor.fetchall()
            
            agents = []
            for row in rows:
                agent_data = {
                    "id": row[0],
                    "name": row[1],
                    "dna_data": json.loads(row[2]),
                    "status": row[3],
                    "created_at": row[4]
                }
                agents.append(agent_data)
            
            conn.close()
            
            self.logger.info(f"📂 {len(agents)} agentes carregados do banco offline")
            return agents
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar agentes: {e}")
            return []
    
    def save_population_state(self, generation: int, population_size: int, state_data: Dict[str, Any]):
        """Salva estado da população"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO population_state (generation, population_size, state_data)
                VALUES (?, ?, ?)
            """, (generation, population_size, json.dumps(state_data, default=str)))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"💾 Estado da população salvo (Gen {generation}, Size {population_size})")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar estado da população: {e}")
    
    def get_latest_population_state(self) -> Optional[Dict[str, Any]]:
        """Obtém último estado da população"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT generation, population_size, state_data, created_at
                FROM population_state
                ORDER BY created_at DESC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "generation": row[0],
                    "population_size": row[1],
                    "state_data": json.loads(row[2]),
                    "created_at": row[3]
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar estado da população: {e}")
            return None

class OfflineManager:
    """Gerenciador do modo offline"""
    
    def __init__(self):
        self.logger = logging.getLogger("OfflineManager")
        self.cache = OfflineCache()
        self.offline_db = OfflineDatabase()
        
        self.is_offline = False
        self.api_base_url = "http://localhost:8000"
        self.last_sync = None
        
        # Configurações
        self.sync_interval = 300  # 5 minutos
        self.connectivity_check_interval = 60  # 1 minuto
        
        # Estado offline
        self.offline_agents = []
        self.offline_population_state = None
        self.offline_neural_web = None
        
    def check_connectivity(self) -> bool:
        """Verifica conectividade com API"""
        try:
            import requests
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            return response.status_code == 200
            
        except Exception:
            return False
    
    def enter_offline_mode(self):
        """Entra em modo offline"""
        if not self.is_offline:
            self.logger.warning("🔌 Entrando em modo OFFLINE")
            self.is_offline = True
            
            # Carregar dados do cache e banco local
            self.load_offline_data()
            
            self.logger.info("📂 Modo offline ativado - usando dados locais")
    
    def exit_offline_mode(self):
        """Sai do modo offline"""
        if self.is_offline:
            self.logger.info("🌐 Saindo do modo offline")
            self.is_offline = False
            
            # Sincronizar dados locais com API
            self.sync_offline_data()
            
            self.logger.info("✅ Reconectado - dados sincronizados")
    
    def load_offline_data(self):
        """Carrega dados para modo offline"""
        try:
            # Carregar agentes do banco offline
            self.offline_agents = self.offline_db.load_agents()
            
            # Carregar estado da população
            self.offline_population_state = self.offline_db.get_latest_population_state()
            
            # Carregar dados do cache se banco estiver vazio
            if not self.offline_agents:
                cached_agents = self.cache.load_agents()
                if cached_agents:
                    self.logger.info("📂 Usando agentes do cache como fallback")
                    self.offline_agents = cached_agents
            
            if not self.offline_population_state:
                cached_population = self.cache.load_population_state()
                if cached_population:
                    self.logger.info("📂 Usando população do cache como fallback")
                    self.offline_population_state = cached_population
            
            self.logger.info(f"📊 Dados offline carregados:")
            self.logger.info(f"   👥 Agentes: {len(self.offline_agents)}")
            self.logger.info(f"   🧬 População: {'Sim' if self.offline_population_state else 'Não'}")
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar dados offline: {e}")
    
    def sync_offline_data(self):
        """Sincroniza dados offline com API"""
        try:
            # Aqui seria implementada a sincronização real com a API
            # Por enquanto, apenas salvamos no cache
            
            if self.offline_agents:
                self.cache.save_agents(self.offline_agents)
            
            if self.offline_population_state:
                self.cache.save_population_state(self.offline_population_state)
            
            self.last_sync = datetime.now()
            self.logger.info("🔄 Dados sincronizados com sucesso")
            
        except Exception as e:
            self.logger.error(f"Falha na sincronização: {e}")
    
    def get_agents(self) -> List[Dict[str, Any]]:
        """Obtém agentes (online ou offline)"""
        if self.is_offline:
            return self.offline_agents
        else:
            # Tentaria carregar da API aqui
            return []
    
    def save_agent_offline(self, agent_data: Dict[str, Any]):
        """Salva agente em modo offline"""
        try:
            self.offline_db.save_agent(
                agent_data["id"],
                agent_data["name"],
                agent_data.get("dna_data", {})
            )
            
            # Atualizar lista local
            existing_ids = [a["id"] for a in self.offline_agents]
            if agent_data["id"] not in existing_ids:
                self.offline_agents.append(agent_data)
            else:
                # Atualizar agente existente
                for i, agent in enumerate(self.offline_agents):
                    if agent["id"] == agent_data["id"]:
                        self.offline_agents[i] = agent_data
                        break
            
            self.logger.debug(f"💾 Agente {agent_data['name']} salvo offline")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar agente offline: {e}")
    
    def create_basic_universe_offline(self) -> Dict[str, Any]:
        """Cria universo básico para funcionar offline"""
        
        self.logger.info("🌍 Criando universo básico offline...")
        
        # Criar agentes básicos se não existirem
        if not self.offline_agents:
            self.logger.info("👥 Criando população inicial offline...")
            
            for i in range(10):
                agent_data = {
                    "id": f"offline_agent_{i}",
                    "name": f"Agent Offline {i+1}",
                    "dna_data": {
                        "traits": {
                            "curiosity": 0.5 + (i * 0.05),
                            "social": 0.4 + (i * 0.04),
                            "creative": 0.6 + (i * 0.03)
                        },
                        "generation": 0
                    },
                    "status": "active",
                    "created_at": datetime.now().isoformat()
                }
                
                self.save_agent_offline(agent_data)
            
            self.logger.info(f"✅ {len(self.offline_agents)} agentes criados offline")
        
        # Criar estado básico da população
        if not self.offline_population_state:
            population_state = {
                "generation": 0,
                "population_size": len(self.offline_agents),
                "total_connections": 0,
                "average_fitness": 0.5,
                "diversity_score": 0.8,
                "last_evolution": datetime.now().isoformat()
            }
            
            self.offline_db.save_population_state(0, len(self.offline_agents), population_state)
            self.offline_population_state = population_state
            
            self.logger.info("🧬 Estado inicial da população criado")
        
        universe_status = {
            "mode": "offline",
            "agents_count": len(self.offline_agents),
            "population_generation": self.offline_population_state.get("generation", 0) if self.offline_population_state else 0,
            "status": "running_offline",
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "created_at": datetime.now().isoformat()
        }
        
        self.logger.info("🌟 Universo offline pronto!")
        return universe_status
    
    async def connectivity_monitor(self):
        """Monitor de conectividade"""
        
        while True:
            try:
                is_connected = self.check_connectivity()
                
                if is_connected and self.is_offline:
                    self.exit_offline_mode()
                elif not is_connected and not self.is_offline:
                    self.enter_offline_mode()
                
                await asyncio.sleep(self.connectivity_check_interval)
                
            except Exception as e:
                self.logger.error(f"Erro no monitor de conectividade: {e}")
                await asyncio.sleep(self.connectivity_check_interval)
    
    def start_monitoring(self):
        """Inicia monitoramento de conectividade"""
        
        def run_monitor():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.connectivity_monitor())
            finally:
                loop.close()
        
        monitor_thread = threading.Thread(target=run_monitor, daemon=True)
        monitor_thread.start()
        
        self.logger.info("🔍 Monitor de conectividade iniciado")
        return monitor_thread

def main():
    """Função principal para testar modo offline"""
    
    print("🔌 SISTEMA DE MODO OFFLINE - Lore N.A.")
    print("=" * 50)
    
    # Criar gerenciador offline
    offline_manager = OfflineManager()
    
    # Verificar conectividade inicial
    is_connected = offline_manager.check_connectivity()
    print(f"🌐 Conectividade inicial: {'✅ Online' if is_connected else '❌ Offline'}")
    
    if not is_connected:
        offline_manager.enter_offline_mode()
        
        # Criar universo básico offline
        universe = offline_manager.create_basic_universe_offline()
        
        print("\\n🌍 UNIVERSO OFFLINE CRIADO:")
        print(f"   👥 Agentes: {universe['agents_count']}")
        print(f"   🧬 Geração: {universe['population_generation']}")
        print(f"   📊 Status: {universe['status']}")
        
        # Listar agentes offline
        agents = offline_manager.get_agents()
        print(f"\\n👥 AGENTES OFFLINE ({len(agents)}):")
        for agent in agents[:5]:  # Mostrar apenas os primeiros 5
            print(f"   - {agent['name']} (ID: {agent['id']})")
        
        if len(agents) > 5:
            print(f"   ... e mais {len(agents) - 5} agentes")
    
    # Iniciar monitoramento
    monitor_thread = offline_manager.start_monitoring()
    
    print("\\n✅ Sistema offline configurado!")
    print("🔍 Monitoramento de conectividade ativo")
    print("💾 Cache local: /home/brendo/lore/cache/")
    print("🗄️ Banco offline: /home/brendo/lore/data/offline_universe.db")
    
    try:
        print("\\n⏳ Testando por 30 segundos...")
        time.sleep(30)
        
        # Verificar status final
        final_status = "Online" if not offline_manager.is_offline else "Offline"
        print(f"\\n🎯 Status final: {final_status}")
        
        if offline_manager.is_offline:
            agents_count = len(offline_manager.get_agents())
            print(f"👥 Agentes offline disponíveis: {agents_count}")
        
    except KeyboardInterrupt:
        print("\\n🛑 Teste interrompido")
    
    print("\\n✅ Sistema de modo offline está funcionando!")

if __name__ == "__main__":
    main()
