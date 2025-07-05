#!/usr/bin/env python3
"""
Universe Autonomous Cycles - Lore N.A.
=====================================

Sistema de ciclos autônomos que faz o universo funcionar sozinho:
- Agentes vivem suas vidas independentemente
- População evolui automaticamente 
- Marketplace se atualiza dinamicamente
- Neural Web cresce organicamente
- Métricas são coletadas continuamente

O universo funciona 24/7 sem intervenção humana!

Autor: Lore N.A. Genesis Team
Data: 2025
"""

import asyncio
import logging
import signal
import sys
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# Configurar environment
os.environ['KONG_JWT_SECRET'] = 'universe-autonomous-secret-key'
os.environ['DATABASE_URL'] = 'sqlite:///autonomous_universe.db'

# Adicionar src ao path
sys.path.append('/home/brendo/lore/src')

from population_manager import PopulationManager
from neural_web import NeuralWeb
from social_agent import SocialAgent
from agent_dna import AgentDNA

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/brendo/lore/logs/universe_autonomous.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutonomousUniverse:
    """Sistema de ciclos autônomos do universo"""
    
    def __init__(self):
        self.neural_web = NeuralWeb()
        self.population_manager = None
        self.agents: Dict[str, SocialAgent] = {}
        self.running = False
        self.cycle_count = 0
        self.start_time = datetime.now()
        
        # Métricas do universo
        self.universe_metrics = {
            'total_cycles': 0,
            'total_connections': 0,
            'total_interactions': 0,
            'population_size': 0,
            'generation_count': 0,
            'uptime_hours': 0
        }
        
        # Configurações de ciclo
        self.cycle_interval = 30  # segundos entre ciclos
        self.save_interval = 300   # salvar estado a cada 5 minutos
        self.metrics_interval = 60 # métricas a cada 1 minuto
        
        # Handlers para graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("🌟 AutonomousUniverse inicializado")
    
    async def initialize_universe(self, initial_population_size: int = 10):
        """Inicializa o universo com população inicial"""
        
        logger.info(f"🧬 Inicializando universo com {initial_population_size} agentes...")
        
        # Criar população inicial se não existe
        if not self.agents:
            await self._create_initial_population(initial_population_size)
        
        # Inicializar population manager
        self.population_manager = PopulationManager(
            neural_web=self.neural_web,
            max_population=20,
            generation_cycles=50  # Evolução a cada 50 ciclos
        )
        
        # Adicionar agentes ao population manager
        for agent in self.agents.values():
            self.population_manager.add_agent(agent)
        
        logger.info("✅ Universo inicializado com sucesso!")
        
        return True
    
    async def _create_initial_population(self, size: int):
        """Cria população inicial de agentes"""
        
        logger.info(f"👶 Criando {size} agentes iniciais...")
        
        for i in range(size):
            # Gerar DNA aleatório
            dna = AgentDNA.generate_random()
            agent_id = f"autonomous_agent_{i+1:03d}"
            
            try:
                # Criar agente social
                agent = SocialAgent(agent_id, dna, self.neural_web)
                self.agents[agent_id] = agent
                
                logger.info(f"  ✓ {agent.identity.full_name} '{agent.identity.nickname}' criado")
                
            except Exception as e:
                logger.error(f"  ❌ Erro criando agente {agent_id}: {e}")
        
        logger.info(f"🎉 {len(self.agents)} agentes criados!")
    
    async def run_autonomous_cycle(self):
        """Executa um ciclo autônomo completo"""
        
        self.cycle_count += 1
        cycle_start = time.time()
        
        logger.info(f"🔄 Ciclo {self.cycle_count} iniciado")
        
        try:
            # 1. Ciclo de vida dos agentes
            await self._run_agent_lifecycles()
            
            # 2. Interações sociais
            await self._run_social_interactions()
            
            # 3. Evolução populacional (se necessário)
            if self.population_manager:
                await self.population_manager.run_population_cycle()
            
            # 4. Atualizar métricas da neural web
            self.neural_web.update_social_metrics()
            
            # 5. Coletar métricas do universo
            self._update_universe_metrics()
            
            cycle_time = time.time() - cycle_start
            logger.info(f"✅ Ciclo {self.cycle_count} concluído em {cycle_time:.2f}s")
            
        except Exception as e:
            logger.error(f"❌ Erro no ciclo {self.cycle_count}: {e}")
    
    async def _run_agent_lifecycles(self):
        """Executa ciclo de vida de todos os agentes"""
        
        if not self.agents:
            return
        
        logger.debug(f"🤖 Executando ciclo de vida de {len(self.agents)} agentes...")
        
        # Executar em paralelo para performance
        tasks = []
        for agent in self.agents.values():
            tasks.append(self._agent_lifecycle(agent))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _agent_lifecycle(self, agent: SocialAgent):
        """Ciclo de vida individual do agente"""
        
        try:
            # Decidir e agir (se implementado)
            if hasattr(agent, 'decide_and_act'):
                await agent.decide_and_act()
            
            # Buscar novas conexões ocasionalmente
            if self.cycle_count % 5 == 0:  # A cada 5 ciclos
                agent.seek_new_connections(self.agents, max_new_connections=1)
            
            # Manter relacionamentos
            if self.cycle_count % 3 == 0:  # A cada 3 ciclos
                agent.maintain_relationships(self.agents)
            
            # Influenciar rede (se for líder)
            if self.cycle_count % 7 == 0:  # A cada 7 ciclos
                agent.influence_network(self.agents)
                
        except Exception as e:
            logger.warning(f"Erro no ciclo do agente {agent.agent_id}: {e}")
    
    async def _run_social_interactions(self):
        """Executa interações sociais entre agentes"""
        
        if len(self.agents) < 2:
            return
        
        logger.debug("🤝 Executando interações sociais...")
        
        # Selecionar alguns agentes para interagir neste ciclo
        active_agents = list(self.agents.values())
        interaction_count = min(5, len(active_agents) // 2)
        
        for _ in range(interaction_count):
            # Escolher dois agentes aleatórios
            if len(active_agents) >= 2:
                import random
                agent1, agent2 = random.sample(active_agents, 2)
                
                # Verificar se podem interagir
                connection = self.neural_web.get_connection(agent1.agent_id, agent2.agent_id)
                
                if connection:
                    # Simular interação
                    await self._simulate_interaction(agent1, agent2, connection)
    
    async def _simulate_interaction(self, agent1: SocialAgent, agent2: SocialAgent, connection):
        """Simula uma interação entre dois agentes"""
        
        try:
            # Agente 1 mantém relacionamento com agente 2
            agent1.maintain_relationships({agent2.agent_id: agent2})
            
            # Ocasionalmente, interação mútua
            if self.cycle_count % 2 == 0:
                agent2.maintain_relationships({agent1.agent_id: agent1})
                
            logger.debug(f"💬 Interação: {agent1.identity.nickname} ↔ {agent2.identity.nickname}")
            
        except Exception as e:
            logger.warning(f"Erro na interação {agent1.agent_id} ↔ {agent2.agent_id}: {e}")
    
    def _update_universe_metrics(self):
        """Atualiza métricas do universo"""
        
        # Métricas básicas
        self.universe_metrics['total_cycles'] = self.cycle_count
        self.universe_metrics['population_size'] = len(self.agents)
        self.universe_metrics['uptime_hours'] = (datetime.now() - self.start_time).total_seconds() / 3600
        
        # Métricas da neural web
        if self.neural_web.connections:
            self.universe_metrics['total_connections'] = len(self.neural_web.connections)
            
            # Contar interações
            total_interactions = 0
            for connection in self.neural_web.connections.values():
                total_interactions += connection.interaction_count
            self.universe_metrics['total_interactions'] = total_interactions
        
        # Métricas da população
        if self.population_manager:
            self.universe_metrics['generation_count'] = self.population_manager.current_generation
    
    async def _save_universe_state(self):
        """Salva estado atual do universo"""
        
        try:
            state = {
                'timestamp': datetime.now().isoformat(),
                'cycle_count': self.cycle_count,
                'metrics': self.universe_metrics,
                'agent_count': len(self.agents),
                'agent_summaries': []
            }
            
            # Adicionar resumos dos agentes
            for agent in list(self.agents.values())[:5]:  # Top 5 para economia de espaço
                try:
                    summary = agent.get_social_summary()
                    state['agent_summaries'].append({
                        'agent_id': agent.agent_id,
                        'name': summary['identity']['full_name'],
                        'nickname': summary['identity']['nickname'],
                        'personality': summary['personality'],
                        'connections': summary['total_connections'],
                        'influences_given': summary['influences_given'],
                        'influences_received': summary['influences_received']
                    })
                except:
                    pass
            
            # Salvar arquivo
            state_file = Path('/home/brendo/lore/logs/universe_state.json')
            state_file.parent.mkdir(exist_ok=True)
            
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
                
            logger.debug(f"💾 Estado do universo salvo (ciclo {self.cycle_count})")
            
        except Exception as e:
            logger.error(f"Erro salvando estado: {e}")
    
    def _log_universe_metrics(self):
        """Log das métricas do universo"""
        
        logger.info("📊 MÉTRICAS DO UNIVERSO:")
        logger.info(f"  🔄 Ciclos executados: {self.universe_metrics['total_cycles']}")
        logger.info(f"  👥 População atual: {self.universe_metrics['population_size']}")
        logger.info(f"  🌐 Conexões totais: {self.universe_metrics['total_connections']}")
        logger.info(f"  💬 Interações totais: {self.universe_metrics['total_interactions']}")
        logger.info(f"  🧬 Geração atual: {self.universe_metrics['generation_count']}")
        logger.info(f"  ⏰ Uptime: {self.universe_metrics['uptime_hours']:.2f}h")
        
        # Métricas da neural web
        if hasattr(self.neural_web, 'get_network_statistics'):
            try:
                net_stats = self.neural_web.get_network_statistics()
                logger.info(f"  📈 Network stats: {net_stats}")
            except:
                pass
    
    async def run_forever(self):
        """Executa o universo autonomamente para sempre"""
        
        logger.info("🚀 INICIANDO UNIVERSO AUTÔNOMO")
        logger.info(f"   Ciclo a cada {self.cycle_interval}s")
        logger.info(f"   Salvando estado a cada {self.save_interval}s")
        logger.info(f"   Métricas a cada {self.metrics_interval}s")
        
        self.running = True
        last_save = time.time()
        last_metrics = time.time()
        
        try:
            while self.running:
                cycle_start = time.time()
                
                # Executar ciclo principal
                await self.run_autonomous_cycle()
                
                # Salvar estado periodicamente
                if time.time() - last_save >= self.save_interval:
                    await self._save_universe_state()
                    last_save = time.time()
                
                # Log de métricas periodicamente
                if time.time() - last_metrics >= self.metrics_interval:
                    self._log_universe_metrics()
                    last_metrics = time.time()
                
                # Aguardar próximo ciclo
                cycle_time = time.time() - cycle_start
                sleep_time = max(0, self.cycle_interval - cycle_time)
                
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                
        except Exception as e:
            logger.error(f"💥 Erro crítico no universo: {e}")
            raise
        
        finally:
            logger.info("🛑 Universo autônomo parado")
            await self._save_universe_state()
    
    def _signal_handler(self, signum, frame):
        """Handler para shutdown graceful"""
        logger.info(f"🛑 Sinal {signum} recebido. Parando universo...")
        self.running = False
    
    async def shutdown(self):
        """Shutdown graceful do universo"""
        logger.info("🔄 Iniciando shutdown...")
        self.running = False
        await self._save_universe_state()
        logger.info("✅ Shutdown concluído")


async def main():
    """Função principal"""
    
    print("🌟 LORE N.A. - UNIVERSO AUTÔNOMO")
    print("=" * 40)
    print("O universo funcionará sozinho 24/7!")
    print("Pressione Ctrl+C para parar gracefully")
    print()
    
    try:
        # Criar universo
        universe = AutonomousUniverse()
        
        # Inicializar com população
        await universe.initialize_universe(initial_population_size=8)
        
        # Executar para sempre
        await universe.run_forever()
        
    except KeyboardInterrupt:
        logger.info("⚡ Interrupção do usuário")
        if 'universe' in locals():
            await universe.shutdown()
    
    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🌟 Universo parado. Até a próxima! 👋")


if __name__ == "__main__":
    # Criar diretório de logs
    os.makedirs('/home/brendo/lore/logs', exist_ok=True)
    
    # Executar
    asyncio.run(main())
