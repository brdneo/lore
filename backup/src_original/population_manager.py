#!/usr/bin/env python3
"""
Population Manager - Genesis Protocol
Sistema de gerenciamento de população para evolução de agentes neurais

Implementa:
- Gerenciamento de população de agentes
- Seleção natural baseada em fitness
- Reprodução e criação de novas gerações
- Migração entre populações
- Análise de diversidade genética
- Estatísticas evolutivas

Autor: Lore N.A. Genesis Protocol
Data: 26 de Junho de 2025
"""

import asyncio
import json
import random
import statistics
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import logging
from pathlib import Path

from agent_dna import AgentDNA, DNAGenerator, EvolutionEngine, GeneticTraits
from evolved_agent import EvolvedAgent
from database_manager import LoREDatabase

logger = logging.getLogger(__name__)

class PopulationManager:
    """
    Gerenciador de população de agentes neurais
    
    Responsabilidades:
    - Manter população ativa de agentes
    - Executar ciclos evolutivos
    - Gerenciar reprodução e seleção natural
    - Coletar estatísticas de evolução
    - Persistir dados populacionais
    """
    
    def __init__(self, 
                 api_base_url: str,
                 population_size: int = 50,
                 elite_ratio: float = 0.2,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7,
                 generation_cycles: int = 100,
                 enable_persistence: bool = True,
                 database_path: str = "lore_universe.db"):
        """
        Inicializa gerenciador de população
        
        Args:
            api_base_url (str): URL base da API
            population_size (int): Tamanho da população
            elite_ratio (float): Proporção de elite mantida
            mutation_rate (float): Taxa de mutação
            crossover_rate (float): Taxa de crossover
            generation_cycles (int): Ciclos entre gerações
            enable_persistence (bool): Habilitar persistência automática
            database_path (str): Caminho para o banco de dados
        """
        self.api_base_url = api_base_url
        self.population_size = population_size
        self.elite_ratio = elite_ratio
        self.generation_cycles = generation_cycles
        
        # Configurar logger
        self.logger = logging.getLogger(__name__)
        
        # Persistência
        self.enable_persistence = enable_persistence
        self.database = None
        if self.enable_persistence:
            try:
                self.database = LoREDatabase(database_path)
                self.logger.info(f"💾 Persistência ativada: {database_path}")
            except Exception as e:
                self.logger.warning(f"⚠️ Persistência falhou: {e}")
                self.enable_persistence = False
        """
        Inicializa gerenciador de população
        
        Args:
            api_base_url (str): URL base da API
            population_size (int): Tamanho da população
            elite_ratio (float): Proporção de elite mantida
            mutation_rate (float): Taxa de mutação
            crossover_rate (float): Taxa de crossover
            generation_cycles (int): Ciclos entre gerações
        """
        self.api_base_url = api_base_url
        self.population_size = population_size
        self.elite_ratio = elite_ratio
        self.generation_cycles = generation_cycles
        
        # Componentes de evolução
        self.dna_generator = DNAGenerator(mutation_rate, crossover_rate)
        self.evolution_engine = EvolutionEngine(population_size, elite_ratio)
        
        # População ativa
        self.active_population: List[EvolvedAgent] = []
        self.population_dna: List[AgentDNA] = []
        self.current_generation = 0
        
        # Estatísticas evolutivas
        self.evolution_stats = {
            "generations": [],
            "fitness_history": [],
            "diversity_metrics": [],
            "trait_distributions": [],
            "reproduction_events": []
        }
        
        # Contadores de ciclo
        self.cycle_count = 0
        self.last_evolution = datetime.now()
        
        self.logger = logging.getLogger(__name__ + ".PopulationManager")
        self.logger.info(f"🧬 PopulationManager inicializado: {population_size} agentes")
    
    async def initialize_genesis_population(self):
        """Cria população inicial (Geração 0)"""
        
        self.logger.info("🧬 Criando população Genesis (Geração 0)...")
        
        self.active_population.clear()
        self.population_dna.clear()
        
        for i in range(self.population_size):
            agent_name = f"genesis_gen0_{i:03d}"
            
            # Criar agente com DNA aleatório
            agent = EvolvedAgent(agent_name, self.api_base_url)
            
            # Simular dados iniciais do agente
            agent.agent_data = {
                "id": f"agent_{i:03d}",
                "name": agent_name,
                "wallet_balance": random.uniform(500, 1500),
                "sentiment": random.uniform(0.3, 0.7)
            }
            
            self.active_population.append(agent)
            self.population_dna.append(agent.dna)
            
            # Log com identidade completa
            self.logger.debug(f"🧬 Agente Genesis criado: {agent.identity.full_name} ({agent.identity.nickname})")
            self.logger.debug(f"   Personalidade: {agent.identity.personality_archetype}")
        
        self.current_generation = 0
        self.logger.info(f"🧬 População Genesis criada: {len(self.active_population)} agentes com identidades únicas")
        
        # Coletar estatísticas iniciais
        await self._collect_generation_stats()
        
        # Persistir população inicial
        await self.persist_full_population()
        
        # Registrar evento de criação do universo
        if self.database:
            self.database.log_universe_event(
                "universe_genesis",
                {
                    "generation": 0,
                    "population_size": len(self.active_population),
                    "timestamp": datetime.now().isoformat()
                },
                [agent.agent_id for agent in self.active_population]
            )
    
    async def run_population_cycle(self):
        """Executa um ciclo completo da população"""
        
        self.logger.info(f"🧬 Executando ciclo populacional {self.cycle_count}")
        
        # Executar ciclo de vida de todos os agentes
        tasks = []
        for agent in self.active_population:
            if agent.agent_data:  # Apenas agentes inicializados
                tasks.append(agent.decide_and_act())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self.cycle_count += 1
        
        # Verificar se é hora de evoluir
        if self.cycle_count % self.generation_cycles == 0:
            await self.evolve_generation()
    
    async def evolve_generation(self):
        """Executa evolução para próxima geração"""
        
        self.logger.info(f"🧬 Iniciando evolução: Geração {self.current_generation} → {self.current_generation + 1}")
        
        # 1. Calcular fitness de todos os agentes
        await self._calculate_population_fitness()
        
        # 2. Coletar estatísticas da geração atual
        await self._collect_generation_stats()
        
        # 3. Persistir geração atual (antes da evolução)
        await self.persist_full_population()
        
        # 4. Evolução do DNA
        current_dna_population = [agent.dna for agent in self.active_population]
        new_dna_population = self.evolution_engine.evolve_generation(current_dna_population)
        
        # 5. Criar nova população de agentes
        await self._create_new_generation(new_dna_population)
        
        # 6. Atualizar estatísticas
        self.current_generation += 1
        self.last_evolution = datetime.now()
        
        self.logger.info(f"🧬 Evolução concluída: Geração {self.current_generation}")
        
        # 7. Salvar dados evolutivos
        await self._save_evolution_data()
        
        # 8. Persistir nova geração
        await self.persist_full_population()
    
    async def _calculate_population_fitness(self):
        """Calcula fitness de toda a população"""
        
        self.logger.info("🧬 Calculando fitness populacional...")
        
        for agent in self.active_population:
            if agent.agent_data:
                fitness_scores = agent.calculate_fitness()
                self.logger.debug(f"🧬 Fitness {agent.name}: {fitness_scores['overall']:.3f}")
    
    async def _create_new_generation(self, new_dna_population: List[AgentDNA]):
        """Cria nova geração de agentes baseada no DNA evoluído"""
        
        self.logger.info(f"🧬 Criando nova geração com {len(new_dna_population)} agentes...")
        
        # Limpar população atual
        old_population = self.active_population.copy()
        self.active_population.clear()
        
        # Criar novos agentes com DNA evoluído
        for i, dna in enumerate(new_dna_population):
            agent_name = f"evolved_gen{self.current_generation + 1}_{i:03d}"
            
            # Criar agente com DNA específico
            agent = EvolvedAgent(agent_name, self.api_base_url, dna)
            
            # Herdar alguns dados do agente predecessor (se houver)
            if i < len(old_population):
                old_agent = old_population[i]
                if old_agent.agent_data:
                    # Herdar carteira com variação
                    base_balance = old_agent.agent_data.get("wallet_balance", 1000)
                    variation = random.uniform(0.8, 1.2)  # ±20% variação
                    
                    agent.agent_data = {
                        "id": f"agent_gen{self.current_generation + 1}_{i:03d}",
                        "name": agent_name,
                        "wallet_balance": base_balance * variation,
                        "sentiment": random.uniform(0.3, 0.7)
                    }
            else:
                # Novo agente sem predecessor
                agent.agent_data = {
                    "id": f"agent_new_{i:03d}",
                    "name": agent_name,
                    "wallet_balance": random.uniform(500, 1500),
                    "sentiment": random.uniform(0.3, 0.7)
                }
            
            self.active_population.append(agent)
            
            self.logger.debug(f"🧬 Agente evoluído criado: {agent_name} (Gen {dna.generation})")
        
        # Atualizar DNA da população
        self.population_dna = new_dna_population
        
        self.logger.info(f"🧬 Nova geração criada: {len(self.active_population)} agentes")
    
    async def _collect_generation_stats(self):
        """Coleta estatísticas da geração atual"""
        
        if not self.active_population:
            return
        
        self.logger.info("🧬 Coletando estatísticas geracionais...")
        
        # Fitness scores
        fitness_scores = [agent.dna.fitness_scores["overall"] for agent in self.active_population]
        
        generation_stats = {
            "generation": self.current_generation,
            "timestamp": datetime.now().isoformat(),
            "population_size": len(self.active_population),
            "fitness": {
                "mean": statistics.mean(fitness_scores),
                "median": statistics.median(fitness_scores),
                "std": statistics.stdev(fitness_scores) if len(fitness_scores) > 1 else 0,
                "min": min(fitness_scores),
                "max": max(fitness_scores)
            }
        }
        
        # Diversidade genética por universo
        diversity_metrics = self._calculate_genetic_diversity()
        generation_stats["diversity"] = diversity_metrics
        
        # Distribuição de traits
        trait_distributions = self._calculate_trait_distributions()
        generation_stats["trait_distributions"] = trait_distributions
        
        # Informações de reprodução
        reproduction_info = self._analyze_reproduction_potential()
        generation_stats["reproduction"] = reproduction_info
        
        # Adicionar às estatísticas evolutivas
        self.evolution_stats["generations"].append(generation_stats)
        self.evolution_stats["fitness_history"].append(fitness_scores)
        
        self.logger.info(f"🧬 Stats: Fitness médio={generation_stats['fitness']['mean']:.3f}, "
                        f"Max={generation_stats['fitness']['max']:.3f}")
    
    def _calculate_genetic_diversity(self) -> Dict[str, float]:
        """Calcula diversidade genética da população"""
        
        diversity = {}
        
        for universe in ["limbo", "odyssey", "ritual", "engine", "logs"]:
            universe_traits = []
            
            for agent in self.active_population:
                universe_genes = getattr(agent.dna, f"{universe}_genes")
                trait_values = list(universe_genes.traits.values())
                universe_traits.append(trait_values)
            
            if universe_traits:
                # Calcular diversidade como desvio padrão médio dos traits
                trait_stds = []
                for trait_idx in range(len(universe_traits[0])):
                    trait_values = [traits[trait_idx] for traits in universe_traits]
                    if len(trait_values) > 1:
                        trait_stds.append(statistics.stdev(trait_values))
                
                diversity[universe] = statistics.mean(trait_stds) if trait_stds else 0.0
        
        return diversity
    
    def _calculate_trait_distributions(self) -> Dict[str, Dict[str, float]]:
        """Calcula distribuições de traits por universo"""
        
        distributions = {}
        
        for universe in ["limbo", "odyssey", "ritual", "engine", "logs"]:
            universe_distributions = {}
            
            # Coletar todos os valores de traits
            trait_collections = {}
            for agent in self.active_population:
                universe_genes = getattr(agent.dna, f"{universe}_genes")
                for trait, value in universe_genes.traits.items():
                    if trait not in trait_collections:
                        trait_collections[trait] = []
                    trait_collections[trait].append(value)
            
            # Calcular estatísticas por trait
            for trait, values in trait_collections.items():
                if values:
                    universe_distributions[trait] = {
                        "mean": statistics.mean(values),
                        "std": statistics.stdev(values) if len(values) > 1 else 0,
                        "min": min(values),
                        "max": max(values)
                    }
            
            distributions[universe] = universe_distributions
        
        return distributions
    
    def _analyze_reproduction_potential(self) -> Dict[str, Any]:
        """Analisa potencial reprodutivo da população"""
        
        reproductive_agents = [agent for agent in self.active_population if agent.can_reproduce()]
        
        return {
            "total_population": len(self.active_population),
            "reproductive_agents": len(reproductive_agents),
            "reproduction_rate": len(reproductive_agents) / len(self.active_population),
            "average_generation": statistics.mean([agent.dna.generation for agent in self.active_population]),
            "max_generation": max([agent.dna.generation for agent in self.active_population]),
        }
    
    async def _save_evolution_data(self):
        """Salva dados evolutivos em arquivo"""
        
        try:
            # Criar diretório de dados evolutivos
            data_dir = Path("evolution_data")
            data_dir.mkdir(exist_ok=True)
            
            # Salvar estatísticas gerais
            stats_file = data_dir / f"evolution_stats_gen{self.current_generation}.json"
            with open(stats_file, 'w') as f:
                json.dump(self.evolution_stats, f, indent=2, default=str)
            
            # Salvar DNA da população atual
            dna_file = data_dir / f"population_dna_gen{self.current_generation}.json"
            population_dna_data = [dna.to_dict() for dna in self.population_dna]
            with open(dna_file, 'w') as f:
                json.dump(population_dna_data, f, indent=2, default=str)
            
            self.logger.info(f"🧬 Dados evolutivos salvos: Gen {self.current_generation}")
            
        except Exception as e:
            self.logger.error(f"🧬 Erro ao salvar dados evolutivos: {e}")
    
    def _save_agent_to_database(self, agent: EvolvedAgent):
        """Salva um agente no database"""
        if not self.enable_persistence or not self.database:
            return
            
        try:
            # Preparar dados do agente
            agent_data = {
                'id': agent.dna.agent_id,
                'name': agent.identity.name if hasattr(agent, 'identity') else agent.dna.agent_id,
                'created_at': datetime.now()
            }
            
            # Preparar dados do DNA
            dna_data = {
                'agent_id': agent.dna.agent_id,
                'genes': agent.dna.genes,
                'fitness': agent.dna.fitness_scores,
                'generation': agent.dna.generation,
                'parents': getattr(agent.dna, 'parents', []),
                'mutations': getattr(agent.dna, 'mutations', [])
            }
            
            # Preparar dados da identidade
            identity_data = {}
            if hasattr(agent, 'identity'):
                identity_data = {
                    'name': agent.identity.name,
                    'full_name': agent.identity.full_name,
                    'nickname': agent.identity.nickname,
                    'personality_archetype': agent.identity.personality_archetype,
                    'origin': agent.identity.origin
                }
            
            # Salvar no database
            self.database.save_agent(agent_data)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar agente {agent.dna.agent_id}: {e}")
    
    def _save_generation_stats(self):
        """Salva estatísticas da geração atual"""
        if not self.enable_persistence or not self.database:
            return
            
        try:
            # Calcular estatísticas
            fitness_scores = [agent.dna.fitness_scores['overall'] for agent in self.active_population]
            
            stats = {
                'population_size': len(self.active_population),
                'avg_fitness': sum(fitness_scores) / len(fitness_scores) if fitness_scores else 0,
                'max_fitness': max(fitness_scores) if fitness_scores else 0,
                'min_fitness': min(fitness_scores) if fitness_scores else 0,
                'diversity_index': len(set(fitness_scores)) / len(fitness_scores) if fitness_scores else 0
            }
            
            # Salvar no database
            self.database.save_generation_stats(self.current_generation, stats)
            
            self.logger.info(f"📊 Estatísticas da geração {self.current_generation} salvas")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar estatísticas: {e}")
    
    def _save_evolution_event(self, event_type: str, event_data: dict):
        """Salva um evento de evolução no database"""
        if not self.enable_persistence or not self.database:
            return
            
        try:
            # Preparar dados do evento
            event_record = {
                'event_type': event_type,
                'event_data': event_data,
                'agents_involved': event_data.get('agents_involved', []),
                'timestamp': datetime.now()
            }
            
            # Salvar evento
            # Note: Assumindo que database_manager tem método para eventos
            if hasattr(self.database, 'save_universe_event'):
                self.database.save_universe_event(event_type, event_data, event_data.get('agents_involved', []))
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar evento {event_type}: {e}")
    
    def get_population_summary(self) -> Dict[str, Any]:
        """Retorna resumo da população atual"""
        
        if not self.active_population:
            return {"status": "empty_population"}
        
        fitness_scores = [agent.dna.fitness_scores["overall"] for agent in self.active_population]
        
        return {
            "generation": self.current_generation,
            "population_size": len(self.active_population),
            "cycle_count": self.cycle_count,
            "last_evolution": self.last_evolution.isoformat(),
            "fitness_stats": {
                "mean": statistics.mean(fitness_scores),
                "max": max(fitness_scores),
                "min": min(fitness_scores)
            },
            "top_performers": [
                {
                    "name": agent.name,
                    "fitness": agent.dna.fitness_scores["overall"],
                    "generation": agent.dna.generation,
                    "personality": agent.get_genetic_personality()
                }
                for agent in sorted(self.active_population, 
                                  key=lambda x: x.dna.fitness_scores["overall"], 
                                  reverse=True)[:5]
            ],
            "reproductive_potential": len([agent for agent in self.active_population if agent.can_reproduce()]),
            "genetic_diversity": self._calculate_genetic_diversity()
        }
    
    async def run_simulation(self, total_generations: int = 10, cycles_per_check: int = 10):
        """
        Executa simulação evolutiva completa
        
        Args:
            total_generations (int): Número total de gerações
            cycles_per_check (int): Ciclos entre verificações
        """
        
        self.logger.info(f"🧬 Iniciando simulação evolutiva: {total_generations} gerações")
        
        # Inicializar população Genesis
        await self.initialize_genesis_population()
        
        try:
            while self.current_generation < total_generations:
                # Executar ciclos de vida
                for _ in range(cycles_per_check):
                    await self.run_population_cycle()
                
                # Log de progresso
                summary = self.get_population_summary()
                self.logger.info(f"🧬 Progresso: Gen {self.current_generation}, "
                               f"Fitness médio: {summary['fitness_stats']['mean']:.3f}, "
                               f"Reprodutivos: {summary['reproductive_potential']}")
                
                # Pequena pausa para não sobrecarregar
                await asyncio.sleep(1)
        
        except KeyboardInterrupt:
            self.logger.info("🧬 Simulação interrompida pelo usuário")
        except Exception as e:
            self.logger.error(f"🧬 Erro na simulação: {e}")
        
        # Estatísticas finais
        final_summary = self.get_population_summary()
        self.logger.info("🧬 Simulação concluída!")
        self.logger.info(f"🧬 Geração final: {final_summary['generation']}")
        self.logger.info(f"🧬 Fitness médio final: {final_summary['fitness_stats']['mean']:.3f}")
        self.logger.info(f"🧬 Melhor fitness: {final_summary['fitness_stats']['max']:.3f}")
        
        return final_summary

# Função de teste
async def test_population_manager():
    """Testa o gerenciador de população"""
    
    print("🧬 Testando PopulationManager - Genesis Protocol")
    print("=" * 60)
    
    # Criar gerenciador com população pequena para teste
    manager = PopulationManager(
        api_base_url="http://localhost:8000",
        population_size=10,
        generation_cycles=5
    )
    
    # Executar simulação curta
    await manager.run_simulation(total_generations=3, cycles_per_check=2)
    
    # Mostrar resumo final
    summary = manager.get_population_summary()
    print("\n🧬 Resumo Final:")
    print(f"  Geração: {summary['generation']}")
    print(f"  População: {summary['population_size']}")
    print(f"  Fitness médio: {summary['fitness_stats']['mean']:.3f}")
    print(f"  Melhor fitness: {summary['fitness_stats']['max']:.3f}")
    print(f"  Agentes reprodutivos: {summary['reproductive_potential']}")
    
    print("\n🧬 Top Performers:")
    for performer in summary['top_performers']:
        print(f"  {performer['name']}: {performer['fitness']:.3f} ({performer['personality']})")
    
    print("\n✅ Teste do PopulationManager concluído!")

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Executar teste
    asyncio.run(test_population_manager())
