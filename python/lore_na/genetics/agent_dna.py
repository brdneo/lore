#!/usr/bin/env python3
"""
Agent DNA System - Genesis Protocol
Digital DNA System for Lore N.A. Neural Agents

Implements genetic inheritance based on the 5 Universes:
- Limbo: Market behavior genes
- Odyssey: Creativity and customization genes
- Ritual: Social behavior genes
- Engine: Intelligence and analysis genes
- Logs: Operational expectations genes

Author: Lore N.A. Genesis Protocol
Date: June 26, 2025
"""

import traceback
import logging
from datetime import datetime

# Robust logging configuration
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

import random
import json
import uuid
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class GeneticTraits(Enum):
    """Genetic traits that can be inherited and mutated"""
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
    """Aesthetic biases for Odyssey genes"""
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
    """Genes specific to each universe"""
    # Values between 0.0 and 1.0 for numerical traits
    traits: Dict[str, float]
    # Categorical values for special traits
    categorical_traits: Dict[str, str]
    
    def __post_init__(self):
        """Normalize values between 0 and 1"""
        for trait, value in self.traits.items():
            self.traits[trait] = max(0.0, min(1.0, value))

@dataclass
class AgentDNA:
    """Complete DNA of a neural agent"""
    agent_id: str
    generation: int
    parent_ids: List[str]
    birth_timestamp: str
    
    # Genes by universe
    limbo_genes: UniverseGenes
    odyssey_genes: UniverseGenes
    ritual_genes: UniverseGenes
    engine_genes: UniverseGenes
    logs_genes: UniverseGenes
    
    # Fitness metrics by universe
    fitness_scores: Dict[str, float]
    
    # Accumulated mutations
    mutation_history: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DNA to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentDNA':
        """Create DNA from dictionary"""
        return cls(**data)
    
    @classmethod
    def generate_random(cls, agent_id: Optional[str] = None) -> 'AgentDNA':
        """Generate completely random DNA - convenience method"""
        if agent_id is None:
            agent_id = str(uuid.uuid4())
        
        # Limbo Genes - Market Behavior
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
        
        # Odyssey Genes - Creativity and Customization
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
        
        # Ritual Genes - Social Behavior
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
        
        # Engine Genes - Intelligence and Analysis
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
        
        # Logs Genes - Operational Expectations
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
        """Compatible access to genes in the format expected by the system"""
        return {
            'limbo': self.limbo_genes.traits,
            'odyssey': self.odyssey_genes.traits,
            'ritual': self.ritual_genes.traits,
            'engine': self.engine_genes.traits,
            'logs': self.logs_genes.traits
        }

class DNAGenerator:
    """DNA generator for neural agents"""
    
    def __init__(self, mutation_rate: float = 0.1, crossover_rate: float = 0.7):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.logger = logging.getLogger(__name__ + ".DNAGenerator")
    
    def generate_random_dna(self, agent_id: str) -> AgentDNA:
        """Generate completely random DNA for Genesis agent"""
        
        self.logger.info(f"Generating Genesis DNA for agent {agent_id}")
        
        # Limbo Genes - Market Behavior
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
        
        # Odyssey Genes - Creativity and Customization
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
        
        # Ritual Genes - Social Behavior
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
        
        # Engine Genes - Intelligence and Analysis
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
        
        # Logs Genes - Operational Expectations
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
        """Sexual reproduction: combines DNA from two parents"""
        
        self.logger.info(f"Crossing DNA from {parent1.agent_id} and {parent2.agent_id} for {child_id}")
        
        def crossover_universe_genes(genes1: UniverseGenes, genes2: UniverseGenes) -> UniverseGenes:
            """Crossover between genes of a specific universe"""
            new_traits = {}
            new_categorical = {}
            
            # Numerical crossover - random weighted average
            for trait in genes1.traits:
                if random.random() < self.crossover_rate:
                    weight = random.random()
                    new_traits[trait] = weight * genes1.traits[trait] + (1 - weight) * genes2.traits[trait]
                else:
                    new_traits[trait] = random.choice([genes1.traits[trait], genes2.traits[trait]])
            
            # Categorical crossover - random choice
            for trait in genes1.categorical_traits:
                new_categorical[trait] = random.choice([
                    genes1.categorical_traits[trait], 
                    genes2.categorical_traits[trait]
                ])
                
            return UniverseGenes(traits=new_traits, categorical_traits=new_categorical)
        
        # Combine fitness scores (average of parents)
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
        """Apply random mutations to DNA"""
        
        mutations_applied = []
        
        def mutate_universe_genes(genes: UniverseGenes, universe_name: str) -> UniverseGenes:
            """Apply mutations to genes of a universe"""
            new_traits = genes.traits.copy()
            new_categorical = genes.categorical_traits.copy()
            
            for trait in new_traits:
                if random.random() < self.mutation_rate:
                    # Gaussian mutation
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
            
            # Categorical mutation
            for trait in new_categorical:
                if random.random() < self.mutation_rate / 2:  # Lower chance for categorical
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
            self.logger.info(f"Applying {len(mutations_applied)} mutations to agent {dna.agent_id}")
        
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
    """Evolution engine for neural agents"""
    
    def __init__(self, population_size: int = 100, elite_ratio: float = 0.2):
        self.population_size = population_size
        self.elite_ratio = elite_ratio
        self.dna_generator = DNAGenerator()
        self.logger = logging.getLogger(__name__ + ".EvolutionEngine")
        
    def calculate_fitness(self, dna: AgentDNA, performance_data: Dict[str, Any]) -> AgentDNA:
        """Calculate agent fitness based on performance in the 5 universes"""
        
        # Limbo Fitness - Market performance
        limbo_fitness = self._calculate_limbo_fitness(performance_data.get("limbo", {}))
        
        # Odyssey Fitness - Creativity and customization
        odyssey_fitness = self._calculate_odyssey_fitness(performance_data.get("odyssey", {}))
        
        # Ritual Fitness - Social engagement
        ritual_fitness = self._calculate_ritual_fitness(performance_data.get("ritual", {}))
        
        # Engine Fitness - Analysis capability
        engine_fitness = self._calculate_engine_fitness(performance_data.get("engine", {}))
        
        # Logs Fitness - Operational satisfaction
        logs_fitness = self._calculate_logs_fitness(performance_data.get("logs", {}))
        
        # Overall fitness - weighted average
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
        
        self.logger.info(f"Fitness calculated for {dna.agent_id}: {overall_fitness:.3f}")
        
        return updated_dna
    
    def _calculate_limbo_fitness(self, limbo_data: Dict[str, Any]) -> float:
        """Calculate fitness based on Limbo performance"""
        # Metrics: profit/loss, accurate buying decisions, market timing
        profit_ratio = limbo_data.get("profit_ratio", 0.0)
        decision_accuracy = limbo_data.get("decision_accuracy", 0.5)
        market_timing = limbo_data.get("market_timing", 0.5)
        
        return (profit_ratio * 0.4 + decision_accuracy * 0.3 + market_timing * 0.3)
    
    def _calculate_odyssey_fitness(self, odyssey_data: Dict[str, Any]) -> float:
        """Calculate fitness based on Odyssey performance"""
        # Metrics: unique creations, customization popularity, innovation
        creativity_score = odyssey_data.get("creativity_score", 0.5)
        popularity_score = odyssey_data.get("popularity_score", 0.5)
        innovation_score = odyssey_data.get("innovation_score", 0.5)
        
        return (creativity_score * 0.4 + popularity_score * 0.3 + innovation_score * 0.3)
    
    def _calculate_ritual_fitness(self, ritual_data: Dict[str, Any]) -> float:
        """Calculate fitness based on Ritual performance"""
        # Metrics: community engagement, social influence, subscription satisfaction
        community_engagement = ritual_data.get("community_engagement", 0.5)
        social_influence = ritual_data.get("social_influence", 0.5)
        subscription_satisfaction = ritual_data.get("subscription_satisfaction", 0.5)
        
        return (community_engagement * 0.4 + social_influence * 0.3 + subscription_satisfaction * 0.3)
    
    def _calculate_engine_fitness(self, engine_data: Dict[str, Any]) -> float:
        """Calculate fitness based on Engine performance"""
        # Metrics: prediction accuracy, analysis quality, AI contributions
        prediction_accuracy = engine_data.get("prediction_accuracy", 0.5)
        analysis_quality = engine_data.get("analysis_quality", 0.5)
        ai_contributions = engine_data.get("ai_contributions", 0.5)
        
        return (prediction_accuracy * 0.4 + analysis_quality * 0.3 + ai_contributions * 0.3)
    
    def _calculate_logs_fitness(self, logs_data: Dict[str, Any]) -> float:
        """Calculate fitness based on Logs performance"""
        # Metrics: delivery satisfaction, operational efficiency, problem resolution
        delivery_satisfaction = logs_data.get("delivery_satisfaction", 0.5)
        operational_efficiency = logs_data.get("operational_efficiency", 0.5)
        problem_resolution = logs_data.get("problem_resolution", 0.5)
        
        return (delivery_satisfaction * 0.4 + operational_efficiency * 0.3 + problem_resolution * 0.3)
    
    def select_parents(self, population: List[AgentDNA]) -> Tuple[AgentDNA, AgentDNA]:
        """Parent selection for reproduction - fitness-based tournament"""
        
        # Tournament selection
        def tournament_selection(participants: int = 3) -> AgentDNA:
            tournament = random.sample(population, min(participants, len(population)))
            return max(tournament, key=lambda dna: dna.fitness_scores["overall"])
        
        parent1 = tournament_selection()
        parent2 = tournament_selection()
        
        # Avoid self-reproduction
        while parent2.agent_id == parent1.agent_id and len(population) > 1:
            parent2 = tournament_selection()
        
        return parent1, parent2
    
    def evolve_generation(self, current_population: List[AgentDNA]) -> List[AgentDNA]:
        """Evolve a complete generation of agents"""
        
        self.logger.info(f"Evolving generation with {len(current_population)} agents")
        
        # Sort by fitness
        sorted_population = sorted(current_population, 
                                 key=lambda dna: dna.fitness_scores["overall"], 
                                 reverse=True)
        
        # Keep elite
        elite_size = int(len(sorted_population) * self.elite_ratio)
        elite = sorted_population[:elite_size]
        
        # Generate new generation
        new_generation = elite.copy()
        
        while len(new_generation) < self.population_size:
            parent1, parent2 = self.select_parents(sorted_population)
            
            # Create child
            child_id = f"gen_{sorted_population[0].generation + 1}_{len(new_generation)}"
            child = self.dna_generator.crossover_dna(parent1, parent2, child_id)
            
            # Apply mutation
            child = self.dna_generator.mutate_dna(child)
            
            new_generation.append(child)
        
        self.logger.info(f"New generation created with {len(new_generation)} agents")
        
        return new_generation

# Test/example function
def test_genesis_protocol():
    """Test the Genesis DNA system"""
    
    print("🧬 Testing Genesis Protocol - Digital DNA")
    print("=" * 60)
    
    # Create DNA generator
    dna_gen = DNAGenerator(mutation_rate=0.15)
    
    # Generate random DNA
    agent_dna = dna_gen.generate_random_dna("agent_genesis_001")
    
    print(f"DNA Generated for {agent_dna.agent_id}:")
    print(f"Generation: {agent_dna.generation}")
    print(f"Parents: {agent_dna.parent_ids}")
    
    print("\n🏪 Limbo Genes (Market):")
    for trait, value in agent_dna.limbo_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    print("\n🎨 Odyssey Genes (Creativity):")
    for trait, value in agent_dna.odyssey_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    for trait, value in agent_dna.odyssey_genes.categorical_traits.items():
        print(f"  {trait}: {value}")
    
    print("\n👥 Ritual Genes (Social):")
    for trait, value in agent_dna.ritual_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    print("\n🧠 Engine Genes (Intelligence):")
    for trait, value in agent_dna.engine_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    print("\n📦 Logs Genes (Operational):")
    for trait, value in agent_dna.logs_genes.traits.items():
        print(f"  {trait}: {value:.3f}")
    
    # Test mutation
    print("\n🔬 Testing Mutation...")
    mutated_dna = dna_gen.mutate_dna(agent_dna)
    print(f"Mutations applied: {len(mutated_dna.mutation_history)}")
    
    # Test reproduction
    print("\n👶 Testing Reproduction...")
    parent2_dna = dna_gen.generate_random_dna("agent_genesis_002")
    child_dna = dna_gen.crossover_dna(agent_dna, parent2_dna, "agent_child_001")
    print(f"Child created: {child_dna.agent_id}, Generation: {child_dna.generation}")
    
    print("\n✅ Genesis Protocol working!")
    
    return agent_dna

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run test
    test_genesis_protocol()
