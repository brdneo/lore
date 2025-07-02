#!/usr/bin/env python3
"""
Agent DNA System - Genesis Protocol
Sistema de DNA Digital para Agentes Neurais do Lore N.A.

Implementa herança genética baseada nos 5 Universos:
- Limbo: Genes de comportamento de mercado
- Odyssey: Genes de criatividade e personalização  
- Ritual: Genes de comportamento social
- Engine: Genes de inteligência e análise
- Logs: Genes de expectativas operacionais

Autor: Lore N.A. Genesis Protocol
Data: 26 de Junho de 2025
"""

import random
import json
import uuid
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class GeneticTraits(Enum):
    """Traits genéticos que podem ser herdados e mutados"""
    # Limbo Universe Traits
    RISK_TOLERANCE = "risk_tolerance"
    PRICE_SENSITIVITY = "price_sensitivity" 
    QUALITY_PREFERENCE = "quality_preference"
    NOVELTY_SEEKING = "novelty_seeking"
    BRAND_LOYALTY = "brand_loyalty"
    
    # Odyssey Universe Traits
    CREATIVITY_DRIVE = "creativity_drive"
    EXPERIMENTATION = "experimentation"
    AESTHETIC_BIAS = "aesthetic_bias"
    CUSTOMIZATION_DESIRE = "customization_desire"
    INNOVATION_APPETITE = "innovation_appetite"
    
    # Ritual Universe Traits
    COMMUNITY_BONDING = "community_bonding"
    INFLUENCE_SUSCEPTIBILITY = "influence_susceptibility"
    LOYALTY_FACTOR = "loyalty_factor"
    SOCIAL_CONFORMITY = "social_conformity"
    LEADERSHIP_TENDENCY = "leadership_tendency"
    
    # Engine Universe Traits
    ANALYTICAL_THINKING = "analytical_thinking"
    PATTERN_RECOGNITION = "pattern_recognition"
    STRATEGIC_PLANNING = "strategic_planning"
    DATA_INTERPRETATION = "data_interpretation"
    DECISION_CONFIDENCE = "decision_confidence"
    
    # Logs Universe Traits
    PATIENCE_LEVEL = "patience_level"
    SERVICE_EXPECTATIONS = "service_expectations"
    COMPLAINT_TENDENCY = "complaint_tendency"
    EFFICIENCY_PRIORITY = "efficiency_priority"
    RELIABILITY_VALUE = "reliability_value"

class AestheticBias(Enum):
    """Bias estéticos para genes da Odyssey"""
    MINIMALIST = "minimalist"
    MAXIMALIST = "maximalist"
    VINTAGE = "vintage"
    FUTURISTIC = "futuristic"
    NATURAL = "natural"
    GEOMETRIC = "geometric"
    ORGANIC = "organic"
    INDUSTRIAL = "industrial"

@dataclass
class UniverseGenes:
    """Genes específicos de cada universo"""
    # Valores entre 0.0 e 1.0 para traits numéricos
    traits: Dict[str, float]
    # Valores categóricos para traits especiais
    categorical_traits: Dict[str, str]
    
    def __post_init__(self):
        """Normaliza valores entre 0 e 1"""
        for trait, value in self.traits.items():
            self.traits[trait] = max(0.0, min(1.0, value))

@dataclass
class AgentDNA:
    """DNA completo de um agente neural"""
    agent_id: str
    generation: int
    parent_ids: List[str]
    birth_timestamp: str
    
    # Genes por universo
    limbo_genes: UniverseGenes
    odyssey_genes: UniverseGenes
    ritual_genes: UniverseGenes
    engine_genes: UniverseGenes
    logs_genes: UniverseGenes
    
    # Métricas de fitness por universo
    fitness_scores: Dict[str, float]
    
    # Mutações acumuladas
    mutation_history: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte DNA para dicionário"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentDNA':
        """Cria DNA a partir de dicionário"""
        return cls(**data)
    
    @classmethod
    def generate_random(cls, agent_id: Optional[str] = None) -> 'AgentDNA':
        """Gera DNA completamente aleatório - método de conveniência"""
        if agent_id is None:
            agent_id = str(uuid.uuid4())
        
        # Genes Limbo - Comportamento de Mercado
        limbo_genes = UniverseGenes(
            traits={
                GeneticTraits.RISK_TOLERANCE.value: random.random(),
                GeneticTraits.PRICE_SENSITIVITY.value: random.random(),
                GeneticTraits.QUALITY_PREFERENCE.value: random.random(),
                GeneticTraits.NOVELTY_SEEKING.value: random.random(),
                GeneticTraits.BRAND_LOYALTY.value: random.random(),
            },
            categorical_traits={}
        )
        
        # Genes Odyssey - Criatividade e Personalização
        odyssey_genes = UniverseGenes(
            traits={
                GeneticTraits.CREATIVITY_DRIVE.value: random.random(),
                GeneticTraits.EXPERIMENTATION.value: random.random(),
                GeneticTraits.CUSTOMIZATION_DESIRE.value: random.random(),
                GeneticTraits.INNOVATION_APPETITE.value: random.random(),
            },
            categorical_traits={
                GeneticTraits.AESTHETIC_BIAS.value: random.choice(list(AestheticBias)).value
            }
        )
        
        # Genes Ritual - Comportamento Social
        ritual_genes = UniverseGenes(
            traits={
                GeneticTraits.COMMUNITY_BONDING.value: random.random(),
                GeneticTraits.INFLUENCE_SUSCEPTIBILITY.value: random.random(),
                GeneticTraits.LOYALTY_FACTOR.value: random.random(),
                GeneticTraits.SOCIAL_CONFORMITY.value: random.random(),
                GeneticTraits.LEADERSHIP_TENDENCY.value: random.random(),
            },
            categorical_traits={}
        )
        
        # Genes Engine - Inteligência e Análise
        engine_genes = UniverseGenes(
            traits={
                GeneticTraits.ANALYTICAL_THINKING.value: random.random(),
                GeneticTraits.PATTERN_RECOGNITION.value: random.random(),
                GeneticTraits.STRATEGIC_PLANNING.value: random.random(),
                GeneticTraits.DATA_INTERPRETATION.value: random.random(),
                GeneticTraits.DECISION_CONFIDENCE.value: random.random(),
            },
            categorical_traits={}
        )
        
        # Genes Logs - Expectativas Operacionais
        logs_genes = UniverseGenes(
            traits={
                GeneticTraits.PATIENCE_LEVEL.value: random.random(),
                GeneticTraits.SERVICE_EXPECTATIONS.value: random.random(),
                GeneticTraits.COMPLAINT_TENDENCY.value: random.random(),
                GeneticTraits.EFFICIENCY_PRIORITY.value: random.random(),
                GeneticTraits.RELIABILITY_VALUE.value: random.random(),
            },
            categorical_traits={}
        )
        
        return cls(
            agent_id=agent_id,
            generation=0,
            parent_ids=[],
            birth_timestamp=str(uuid.uuid4()),
            limbo_genes=limbo_genes,
            odyssey_genes=odyssey_genes,
            ritual_genes=ritual_genes,
            engine_genes=engine_genes,
            logs_genes=logs_genes,
            fitness_scores={
                "limbo": 0.5,
                "odyssey": 0.5,
                "ritual": 0.5,
                "engine": 0.5,
                "logs": 0.5,
                "overall": 0.5
            },
            mutation_history=[]
        )

    @property
    def genes(self) -> Dict[str, Dict[str, float]]:
        """Acesso compatível aos genes no formato esperado pelo sistema"""
        return {
            'limbo': self.limbo_genes.traits,
            'odyssey': self.odyssey_genes.traits,
            'ritual': self.ritual_genes.traits,
            'engine': self.engine_genes.traits,
            'logs': self.logs_genes.traits
        }

class DNAGenerator:
    """Gerador de DNA para agentes neurais"""
    
    def __init__(self, mutation_rate: float = 0.1, crossover_rate: float = 0.7):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.logger = logging.getLogger(__name__ + ".DNAGenerator")
    
    def generate_random_dna(self, agent_id: str) -> AgentDNA:
        """Gera DNA completamente aleatório para agente Genesis"""
        
        self.logger.info(f"Gerando DNA Genesis para agente {agent_id}")
        
        # Genes Limbo - Comportamento de Mercado
        limbo_genes = UniverseGenes(
            traits={
                GeneticTraits.RISK_TOLERANCE.value: random.random(),
                GeneticTraits.PRICE_SENSITIVITY.value: random.random(),
                GeneticTraits.QUALITY_PREFERENCE.value: random.random(),
                GeneticTraits.NOVELTY_SEEKING.value: random.random(),
                GeneticTraits.BRAND_LOYALTY.value: random.random(),
            },
            categorical_traits={}
        )
        
        # Genes Odyssey - Criatividade e Personalização
        odyssey_genes = UniverseGenes(
            traits={
                GeneticTraits.CREATIVITY_DRIVE.value: random.random(),
                GeneticTraits.EXPERIMENTATION.value: random.random(),
                GeneticTraits.CUSTOMIZATION_DESIRE.value: random.random(),
                GeneticTraits.INNOVATION_APPETITE.value: random.random(),
            },
            categorical_traits={
                GeneticTraits.AESTHETIC_BIAS.value: random.choice(list(AestheticBias)).value
            }
        )
        
        # Genes Ritual - Comportamento Social
        ritual_genes = UniverseGenes(
            traits={
                GeneticTraits.COMMUNITY_BONDING.value: random.random(),
                GeneticTraits.INFLUENCE_SUSCEPTIBILITY.value: random.random(),
                GeneticTraits.LOYALTY_FACTOR.value: random.random(),
                GeneticTraits.SOCIAL_CONFORMITY.value: random.random(),
                GeneticTraits.LEADERSHIP_TENDENCY.value: random.random(),
            },
            categorical_traits={}
        )
        
        # Genes Engine - Inteligência e Análise
        engine_genes = UniverseGenes(
            traits={
                GeneticTraits.ANALYTICAL_THINKING.value: random.random(),
                GeneticTraits.PATTERN_RECOGNITION.value: random.random(),
                GeneticTraits.STRATEGIC_PLANNING.value: random.random(),
                GeneticTraits.DATA_INTERPRETATION.value: random.random(),
                GeneticTraits.DECISION_CONFIDENCE.value: random.random(),
            },
            categorical_traits={}
        )
        
        # Genes Logs - Expectativas Operacionais
        logs_genes = UniverseGenes(
            traits={
                GeneticTraits.PATIENCE_LEVEL.value: random.random(),
                GeneticTraits.SERVICE_EXPECTATIONS.value: random.random(),
                GeneticTraits.COMPLAINT_TENDENCY.value: random.random(),
                GeneticTraits.EFFICIENCY_PRIORITY.value: random.random(),
                GeneticTraits.RELIABILITY_VALUE.value: random.random(),
            },
            categorical_traits={}
        )
        
        return AgentDNA(
            agent_id=agent_id,
            generation=0,
            parent_ids=[],
            birth_timestamp=str(uuid.uuid4()),
            limbo_genes=limbo_genes,
            odyssey_genes=odyssey_genes,
            ritual_genes=ritual_genes,
            engine_genes=engine_genes,
            logs_genes=logs_genes,
            fitness_scores={
                "limbo": 0.5,
                "odyssey": 0.5,
                "ritual": 0.5,
                "engine": 0.5,
                "logs": 0.5,
                "overall": 0.5
            },
            mutation_history=[]
        )
    
    def crossover_dna(self, parent1: AgentDNA, parent2: AgentDNA, child_id: str) -> AgentDNA:
        """Reprodução sexual: combina DNA de dois pais"""
        
        self.logger.info(f"Cruzando DNA de {parent1.agent_id} e {parent2.agent_id} para {child_id}")
        
        def crossover_universe_genes(genes1: UniverseGenes, genes2: UniverseGenes) -> UniverseGenes:
            """Crossover entre genes de um universo específico"""
            new_traits = {}
            new_categorical = {}
            
            # Crossover numérico - média ponderada aleatória
            for trait in genes1.traits:
                if random.random() < self.crossover_rate:
                    weight = random.random()
                    new_traits[trait] = weight * genes1.traits[trait] + (1 - weight) * genes2.traits[trait]
                else:
                    new_traits[trait] = random.choice([genes1.traits[trait], genes2.traits[trait]])
            
            # Crossover categórico - escolha aleatória
            for trait in genes1.categorical_traits:
                new_categorical[trait] = random.choice([
                    genes1.categorical_traits[trait], 
                    genes2.categorical_traits[trait]
                ])
                
            return UniverseGenes(traits=new_traits, categorical_traits=new_categorical)
        
        # Combinar fitness scores (média dos pais)
        new_fitness = {}
        for metric in parent1.fitness_scores:
            new_fitness[metric] = (parent1.fitness_scores[metric] + parent2.fitness_scores[metric]) / 2
        
        return AgentDNA(
            agent_id=child_id,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=[parent1.agent_id, parent2.agent_id],
            birth_timestamp=str(uuid.uuid4()),
            limbo_genes=crossover_universe_genes(parent1.limbo_genes, parent2.limbo_genes),
            odyssey_genes=crossover_universe_genes(parent1.odyssey_genes, parent2.odyssey_genes),
            ritual_genes=crossover_universe_genes(parent1.ritual_genes, parent2.ritual_genes),
            engine_genes=crossover_universe_genes(parent1.engine_genes, parent2.engine_genes),
            logs_genes=crossover_universe_genes(parent1.logs_genes, parent2.logs_genes),
            fitness_scores=new_fitness,
            mutation_history=[]
        )
    
    def mutate_dna(self, dna: AgentDNA) -> AgentDNA:
        """Aplica mutações aleatórias ao DNA"""
        
        mutations_applied = []
        
        def mutate_universe_genes(genes: UniverseGenes, universe_name: str) -> UniverseGenes:
            """Aplica mutações em genes de um universo"""
            new_traits = genes.traits.copy()
            new_categorical = genes.categorical_traits.copy()
            
            for trait in new_traits:
                if random.random() < self.mutation_rate:
                    # Mutação gaussiana
                    mutation_strength = random.gauss(0, 0.1)
                    old_value = new_traits[trait]
                    new_traits[trait] = max(0.0, min(1.0, old_value + mutation_strength))
                    
                    mutations_applied.append({
                        "universe": universe_name,
                        "trait": trait,
                        "old_value": old_value,
                        "new_value": new_traits[trait],
                        "mutation_strength": mutation_strength
                    })
            
            # Mutação categórica
            for trait in new_categorical:
                if random.random() < self.mutation_rate / 2:  # Menor chance para categóricas
                    if trait == GeneticTraits.AESTHETIC_BIAS.value:
                        old_value = new_categorical[trait]
                        new_categorical[trait] = random.choice(list(AestheticBias)).value
                        
                        mutations_applied.append({
                            "universe": universe_name,
                            "trait": trait,
                            "old_value": old_value,
                            "new_value": new_categorical[trait],
                            "mutation_type": "categorical"
                        })
            
            return UniverseGenes(traits=new_traits, categorical_traits=new_categorical)
        
        if mutations_applied:
            self.logger.info(f"Aplicando {len(mutations_applied)} mutações ao agente {dna.agent_id}")
        
        mutated_dna = AgentDNA(
            agent_id=dna.agent_id,
            generation=dna.generation,
            parent_ids=dna.parent_ids,
            birth_timestamp=dna.birth_timestamp,
            limbo_genes=mutate_universe_genes(dna.limbo_genes, "limbo"),
            odyssey_genes=mutate_universe_genes(dna.odyssey_genes, "odyssey"),
            ritual_genes=mutate_universe_genes(dna.ritual_genes, "ritual"),
            engine_genes=mutate_universe_genes(dna.engine_genes, "engine"),
            logs_genes=mutate_universe_genes(dna.logs_genes, "logs"),
            fitness_scores=dna.fitness_scores.copy(),
            mutation_history=dna.mutation_history + mutations_applied
        )
        
        return mutated_dna

class EvolutionEngine:
    """Motor de evolução dos agentes neurais"""
    
    def __init__(self, population_size: int = 100, elite_ratio: float = 0.2):
        self.population_size = population_size
        self.elite_ratio = elite_ratio
        self.dna_generator = DNAGenerator()
        self.logger = logging.getLogger(__name__ + ".EvolutionEngine")
        
    def calculate_fitness(self, dna: AgentDNA, performance_data: Dict[str, Any]) -> AgentDNA:
        """Calcula fitness do agente baseado em performance nos 5 universos"""
        
        # Fitness Limbo - Performance no mercado
        limbo_fitness = self._calculate_limbo_fitness(performance_data.get("limbo", {}))
        
        # Fitness Odyssey - Criatividade e personalização
        odyssey_fitness = self._calculate_odyssey_fitness(performance_data.get("odyssey", {}))
        
        # Fitness Ritual - Engajamento social
        ritual_fitness = self._calculate_ritual_fitness(performance_data.get("ritual", {}))
        
        # Fitness Engine - Capacidade de análise
        engine_fitness = self._calculate_engine_fitness(performance_data.get("engine", {}))
        
        # Fitness Logs - Satisfação operacional
        logs_fitness = self._calculate_logs_fitness(performance_data.get("logs", {}))
        
        # Fitness overall - média ponderada
        overall_fitness = (
            limbo_fitness * 0.25 +
            odyssey_fitness * 0.20 +
            ritual_fitness * 0.25 +
            engine_fitness * 0.15 +
            logs_fitness * 0.15
        )
        
        updated_dna = dna
        updated_dna.fitness_scores = {
            "limbo": limbo_fitness,
            "odyssey": odyssey_fitness,
            "ritual": ritual_fitness,
            "engine": engine_fitness,
            "logs": logs_fitness,
            "overall": overall_fitness
        }
        
        self.logger.info(f"Fitness calculado para {dna.agent_id}: {overall_fitness:.3f}")
        
        return updated_dna
    
    def _calculate_limbo_fitness(self, limbo_data: Dict[str, Any]) -> float:
        """Calcula fitness baseado em performance no Limbo"""
        # Métricas: profit/loss, decisões de compra acertadas, timing de mercado
        profit_ratio = limbo_data.get("profit_ratio", 0.0)
        decision_accuracy = limbo_data.get("decision_accuracy", 0.5)
        market_timing = limbo_data.get("market_timing", 0.5)
        
        return (profit_ratio * 0.4 + decision_accuracy * 0.3 + market_timing * 0.3)
    
    def _calculate_odyssey_fitness(self, odyssey_data: Dict[str, Any]) -> float:
        """Calcula fitness baseado em performance na Odyssey"""
        # Métricas: criações únicas, popularidade das customizações, inovação
        creativity_score = odyssey_data.get("creativity_score", 0.5)
        popularity_score = odyssey_data.get("popularity_score", 0.5)
        innovation_score = odyssey_data.get("innovation_score", 0.5)
        
        return (creativity_score * 0.4 + popularity_score * 0.3 + innovation_score * 0.3)
    
    def _calculate_ritual_fitness(self, ritual_data: Dict[str, Any]) -> float:
        """Calcula fitness baseado em performance no Ritual"""
        # Métricas: engajamento comunitário, influência social, satisfação com assinaturas
        community_engagement = ritual_data.get("community_engagement", 0.5)
        social_influence = ritual_data.get("social_influence", 0.5)
        subscription_satisfaction = ritual_data.get("subscription_satisfaction", 0.5)
        
        return (community_engagement * 0.4 + social_influence * 0.3 + subscription_satisfaction * 0.3)
    
    def _calculate_engine_fitness(self, engine_data: Dict[str, Any]) -> float:
        """Calcula fitness baseado em performance no Engine"""
        # Métricas: precisão de previsões, qualidade de análises, contribuições para IA
        prediction_accuracy = engine_data.get("prediction_accuracy", 0.5)
        analysis_quality = engine_data.get("analysis_quality", 0.5)
        ai_contributions = engine_data.get("ai_contributions", 0.5)
        
        return (prediction_accuracy * 0.4 + analysis_quality * 0.3 + ai_contributions * 0.3)
    
    def _calculate_logs_fitness(self, logs_data: Dict[str, Any]) -> float:
        """Calcula fitness baseado em performance nos Logs"""
        # Métricas: satisfação com entregas, eficiência operacional, resolução de problemas
        delivery_satisfaction = logs_data.get("delivery_satisfaction", 0.5)
        operational_efficiency = logs_data.get("operational_efficiency", 0.5)
        problem_resolution = logs_data.get("problem_resolution", 0.5)
        
        return (delivery_satisfaction * 0.4 + operational_efficiency * 0.3 + problem_resolution * 0.3)
    
    def select_parents(self, population: List[AgentDNA]) -> Tuple[AgentDNA, AgentDNA]:
        """Seleção de pais para reprodução - torneio baseado em fitness"""
        
        # Seleção por torneio
        def tournament_selection(participants: int = 3) -> AgentDNA:
            tournament = random.sample(population, min(participants, len(population)))
            return max(tournament, key=lambda dna: dna.fitness_scores["overall"])
        
        parent1 = tournament_selection()
        parent2 = tournament_selection()
        
        # Evitar auto-reprodução
        while parent2.agent_id == parent1.agent_id and len(population) > 1:
            parent2 = tournament_selection()
        
        return parent1, parent2
    
    def evolve_generation(self, current_population: List[AgentDNA]) -> List[AgentDNA]:
        """Evolui uma geração completa de agentes"""
        
        self.logger.info(f"Evoluindo geração com {len(current_population)} agentes")
        
        # Ordenar por fitness
        sorted_population = sorted(current_population, 
                                 key=lambda dna: dna.fitness_scores["overall"], 
                                 reverse=True)
        
        # Manter elite
        elite_size = int(len(sorted_population) * self.elite_ratio)
        elite = sorted_population[:elite_size]
        
        # Gerar nova geração
        new_generation = elite.copy()
        
        while len(new_generation) < self.population_size:
            parent1, parent2 = self.select_parents(sorted_population)
            
            # Criar filho
            child_id = f"gen_{sorted_population[0].generation + 1}_{len(new_generation)}"
            child = self.dna_generator.crossover_dna(parent1, parent2, child_id)
            
            # Aplicar mutação
            child = self.dna_generator.mutate_dna(child)
            
            new_generation.append(child)
        
        self.logger.info(f"Nova geração criada com {len(new_generation)} agentes")
        
        return new_generation

# Função de teste/exemplo
def test_genesis_protocol():
    """Testa o sistema de DNA Genesis"""
    
    print("🧬 Testando Genesis Protocol - DNA Digital")
    print("=" * 60)
    
    # Criar gerador de DNA
    dna_gen = DNAGenerator(mutation_rate=0.15)
    
    # Gerar DNA aleatório
    agent_dna = dna_gen.generate_random_dna("agent_genesis_001")
    
    print(f"DNA Gerado para {agent_dna.agent_id}:")
    print(f"Geração: {agent_dna.generation}")
    print(f"Pais: {agent_dna.parent_ids}")
    
    print("\n🏪 Genes Limbo (Mercado):")
    for trait, value in agent_dna.limbo_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    print("\n🎨 Genes Odyssey (Criatividade):")
    for trait, value in agent_dna.odyssey_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    for trait, value in agent_dna.odyssey_genes.categorical_traits.items():
        print(f"  {trait}: {value}")
    
    print("\n👥 Genes Ritual (Social):")
    for trait, value in agent_dna.ritual_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    print("\n🧠 Genes Engine (Inteligência):")
    for trait, value in agent_dna.engine_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    print("\n📦 Genes Logs (Operacional):")
    for trait, value in agent_dna.logs_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    # Testar mutação
    print("\n🔬 Testando Mutação...")
    mutated_dna = dna_gen.mutate_dna(agent_dna)
    print(f"Mutações aplicadas: {len(mutated_dna.mutation_history)}")
    
    # Testar reprodução
    print("\n👶 Testando Reprodução...")
    parent2_dna = dna_gen.generate_random_dna("agent_genesis_002")
    child_dna = dna_gen.crossover_dna(agent_dna, parent2_dna, "agent_child_001")
    print(f"Filho criado: {child_dna.agent_id}, Geração: {child_dna.generation}")
    
    print("\n✅ Genesis Protocol funcionando!")
    
    return agent_dna

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Executar teste
    test_genesis_protocol()
