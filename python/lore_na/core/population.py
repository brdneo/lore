"""
Population management for Lore N.A.
==================================

Handles creation, evolution, and management of agent populations
using the hybrid Rust+Python architecture.
"""

import random
import logging
from typing import List, Dict, Any, Optional
from ..models.agent import Agent, AgentDNA
from ..utils.config import Config

logger = logging.getLogger(__name__)

class PopulationManager:
    """Manages populations of intelligent agents."""
    
    def __init__(self, config: Config):
        """Initialize population manager."""
        self.config = config
        self.agents: List[Agent] = []
        self.generation = 0
        
        # Try to initialize Rust engine
        self.engine = None
        self.use_rust = False
        
        try:
            import lore_engine
            
            params = lore_engine.EvolutionParams(
                population_size=config.population_size,
                mutation_rate=config.mutation_rate,
                crossover_rate=config.crossover_rate,
                selection_pressure=config.selection_pressure,
                elitism_count=max(1, config.population_size // 10),
                max_generations=config.max_generations
            )
            
            self.engine = lore_engine.GeneticEngine(params)
            self.use_rust = True
            logger.info("Rust engine initialized successfully")
            
        except ImportError:
            logger.warning("Rust engine not available, using Python implementation")
    
    def create_initial_population(self, size: int) -> int:
        """
        Create initial population of agents.
        
        Args:
            size: Desired population size
            
        Returns:
            Number of agents created
        """
        logger.info(f"Creating initial population of {size} agents")
        
        if self.use_rust and self.engine:
            return self._create_population_rust(size)
        else:
            return self._create_population_python(size)
    
    def _create_population_rust(self, size: int) -> int:
        """Create population using Rust engine."""
        import lore_engine
        
        # Create population with Rust
        rust_population = self.engine.create_random_population(size)
        
        # Convert to Python agents
        behaviors = ["explorer", "socializer", "optimizer", "creator", "analyzer"]
        
        for i, rust_dna in enumerate(rust_population):
            # Generate cognitive state and behavior
            cognitive_state = lore_engine.generate_random_cognitive_state()
            behavior = random.choice(behaviors)
            behavior_type = lore_engine.BehaviorType(behavior)
            
            # Create intelligent agent
            agent_id = f"agent_{i+1:03d}_{random.randint(1000, 9999)}"
            rust_agent = lore_engine.IntelligentAgent(
                id=agent_id,
                dna=rust_dna,
                behavior_type=behavior_type,
                cognitive_state=cognitive_state
            )
            
            # Convert to Python agent
            fitness = getattr(rust_dna, 'fitness', None) or random.uniform(0.3, 0.9)
            
            agent = Agent(
                id=agent_id,
                dna=AgentDNA(genes=list(rust_dna.genes)),
                fitness=fitness,
                behavior=behavior,
                cognitive_capacity=cognitive_state.get_capacity() or 0.5,
                generation=self.generation
            )
            
            self.agents.append(agent)
        
        logger.info(f"Created {len(self.agents)} agents using Rust engine")
        return len(self.agents)
    
    def _create_population_python(self, size: int) -> int:
        """Create population using pure Python."""
        behaviors = ["explorer", "socializer", "optimizer", "creator", "analyzer"]
        
        for i in range(size):
            agent_id = f"agent_{i+1:03d}_{random.randint(1000, 9999)}"
            
            # Generate random DNA
            genes = [random.uniform(-1.0, 1.0) for _ in range(10)]
            dna = AgentDNA(genes=genes)
            
            # Create agent
            agent = Agent(
                id=agent_id,
                dna=dna,
                fitness=random.uniform(0.3, 0.9),
                behavior=random.choice(behaviors),
                cognitive_capacity=random.uniform(0.3, 0.8),
                generation=self.generation
            )
            
            self.agents.append(agent)
        
        logger.info(f"Created {len(self.agents)} agents using Python implementation")
        return len(self.agents)
    
    def evolve_generation(self) -> List[Agent]:
        """
        Evolve the current population to the next generation.
        
        Returns:
            New generation of agents
        """
        if not self.agents:
            raise ValueError("No population to evolve")
        
        if self.use_rust and self.engine:
            return self._evolve_rust()
        else:
            return self._evolve_python()
    
    def _evolve_rust(self) -> List[Agent]:
        """Evolve population using Rust engine."""
        # TODO: Implement Rust evolution
        # For now, use Python implementation
        return self._evolve_python()
    
    def _evolve_python(self) -> List[Agent]:
        """Evolve population using Python implementation."""
        # Sort by fitness
        self.agents.sort(key=lambda a: a.fitness, reverse=True)
        
        # Keep elite (top 20%)
        elite_count = max(1, len(self.agents) // 5)
        elite_agents = self.agents[:elite_count]
        
        # Generate new population
        new_agents = elite_agents.copy()
        
        while len(new_agents) < len(self.agents):
            # Select parents (tournament selection)
            parent1 = self._tournament_selection()
            parent2 = self._tournament_selection()
            
            # Crossover and mutation
            child = self._crossover(parent1, parent2)
            child = self._mutate(child)
            child.generation = self.generation + 1
            
            new_agents.append(child)
        
        self.agents = new_agents
        self.generation += 1
        
        logger.info(f"Evolved to generation {self.generation} with {len(self.agents)} agents")
        return self.agents
    
    def _tournament_selection(self, tournament_size: int = 3) -> Agent:
        """Select agent using tournament selection."""
        tournament = random.sample(self.agents, min(tournament_size, len(self.agents)))
        return max(tournament, key=lambda a: a.fitness)
    
    def _crossover(self, parent1: Agent, parent2: Agent) -> Agent:
        """Create child agent through crossover."""
        # Simple uniform crossover
        child_genes = []
        for g1, g2 in zip(parent1.dna.genes, parent2.dna.genes):
            child_genes.append(g1 if random.random() < 0.5 else g2)
        
        child_id = f"child_{random.randint(1000, 9999)}"
        child_dna = AgentDNA(genes=child_genes)
        
        return Agent(
            id=child_id,
            dna=child_dna,
            fitness=0.5,  # Will be evaluated later
            behavior=random.choice([parent1.behavior, parent2.behavior]),
            cognitive_capacity=(parent1.cognitive_capacity + parent2.cognitive_capacity) / 2,
            generation=self.generation + 1
        )
    
    def _mutate(self, agent: Agent) -> Agent:
        """Apply mutation to agent."""
        mutation_rate = self.config.mutation_rate
        
        # Mutate genes
        for i in range(len(agent.dna.genes)):
            if random.random() < mutation_rate:
                agent.dna.genes[i] += random.gauss(0, 0.1)
                agent.dna.genes[i] = max(-1.0, min(1.0, agent.dna.genes[i]))
        
        # Occasionally mutate behavior
        if random.random() < mutation_rate * 0.1:
            behaviors = ["explorer", "socializer", "optimizer", "creator", "analyzer"]
            agent.behavior = random.choice(behaviors)
        
        return agent
    
    def get_all_agents(self) -> List[Agent]:
        """Get all agents in current population."""
        return self.agents.copy()
    
    def get_best_agents(self, count: int) -> List[Agent]:
        """Get top performing agents."""
        sorted_agents = sorted(self.agents, key=lambda a: a.fitness, reverse=True)
        return sorted_agents[:count]
    
    def get_population_stats(self) -> Dict[str, Any]:
        """Get statistics about current population."""
        if not self.agents:
            return {"population_size": 0}
        
        fitness_scores = [agent.fitness for agent in self.agents]
        behaviors = [agent.behavior for agent in self.agents]
        
        return {
            "population_size": len(self.agents),
            "generation": self.generation,
            "average_fitness": sum(fitness_scores) / len(fitness_scores),
            "best_fitness": max(fitness_scores),
            "worst_fitness": min(fitness_scores),
            "behavior_distribution": {behavior: behaviors.count(behavior) for behavior in set(behaviors)},
            "engine_type": "rust" if self.use_rust else "python"
        }
