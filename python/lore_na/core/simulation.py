"""
Core simulation module for Lore N.A.
===================================

This module provides the main Universe and Simulation classes
for orchestrating intelligent agent simulations.
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from ..utils.config import Config
from ..models.agent import Agent
from .population import PopulationManager
from .database import DatabaseManager

logger = logging.getLogger(__name__)

@dataclass
class SimulationStats:
    """Statistics for a simulation run."""
    generation: int
    population_size: int
    average_fitness: float
    best_fitness: float
    evolution_time: float
    total_time: float

class Universe:
    """
    Main universe container for agent simulation.
    
    The Universe manages the entire simulation environment,
    including agents, evolution, and persistence.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize universe with configuration."""
        self.config = config or Config.default()
        self.population_manager = PopulationManager(self.config)
        self.database = DatabaseManager(self.config.database_path)
        self.stats_history: List[SimulationStats] = []
        self.generation = 0
        self.running = False
        
        logger.info(f"Universe initialized with config: {self.config}")
    
    def create_population(self, size: int) -> int:
        """
        Create initial population of agents.
        
        Args:
            size: Number of agents to create
            
        Returns:
            Number of agents actually created
        """
        logger.info(f"Creating population of {size} agents")
        
        created = self.population_manager.create_initial_population(size)
        
        # Save to database
        agents = self.population_manager.get_all_agents()
        for agent in agents:
            self.database.save_agent(agent.to_dict())
        
        logger.info(f"Created {created} agents successfully")
        return created
    
    def run_simulation(self, generations: int = 10) -> List[SimulationStats]:
        """
        Run evolution simulation for specified generations.
        
        Args:
            generations: Number of generations to evolve
            
        Returns:
            List of statistics for each generation
        """
        logger.info(f"Starting simulation for {generations} generations")
        self.running = True
        
        try:
            for gen in range(generations):
                if not self.running:
                    break
                
                start_time = time.time()
                
                # Evolve population
                evolution_start = time.time()
                self.population_manager.evolve_generation()
                evolution_time = time.time() - evolution_start
                
                # Calculate statistics
                agents = self.population_manager.get_all_agents()
                fitness_scores = [agent.fitness for agent in agents]
                
                stats = SimulationStats(
                    generation=self.generation,
                    population_size=len(agents),
                    average_fitness=sum(fitness_scores) / len(fitness_scores),
                    best_fitness=max(fitness_scores),
                    evolution_time=evolution_time,
                    total_time=time.time() - start_time
                )
                
                self.stats_history.append(stats)
                self.generation += 1
                
                logger.info(f"Generation {self.generation}: "
                          f"avg_fitness={stats.average_fitness:.3f}, "
                          f"best_fitness={stats.best_fitness:.3f}")
        
        finally:
            self.running = False
        
        logger.info(f"Simulation completed after {len(self.stats_history)} generations")
        return self.stats_history
    
    def get_best_agents(self, count: int = 10) -> List[Agent]:
        """Get the best performing agents."""
        agents = self.population_manager.get_all_agents()
        return sorted(agents, key=lambda a: a.fitness, reverse=True)[:count]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current universe statistics."""
        agents = self.population_manager.get_all_agents()
        
        return {
            "generation": self.generation,
            "population_size": len(agents),
            "total_simulations": len(self.stats_history),
            "database_agents": self.database.count_agents(),
            "rust_engine_active": hasattr(self.population_manager, 'engine'),
        }
    
    def stop_simulation(self):
        """Stop running simulation."""
        self.running = False
        logger.info("Simulation stop requested")

class Simulation:
    """
    Individual simulation runner.
    
    Used for running specific simulation scenarios
    or experiments within a Universe.
    """
    
    def __init__(self, universe: Universe, name: str = "Default"):
        """Initialize simulation with universe context."""
        self.universe = universe
        self.name = name
        self.results: Dict[str, Any] = {}
        
    def run_experiment(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a specific experiment with given parameters.
        
        Args:
            parameters: Experiment configuration
            
        Returns:
            Experiment results
        """
        logger.info(f"Running experiment '{self.name}' with parameters: {parameters}")
        
        # Apply parameters to universe
        if "population_size" in parameters:
            self.universe.create_population(parameters["population_size"])
        
        if "generations" in parameters:
            stats = self.universe.run_simulation(parameters["generations"])
            self.results["evolution_stats"] = stats
        
        # Collect results
        self.results.update({
            "experiment_name": self.name,
            "parameters": parameters,
            "final_stats": self.universe.get_stats(),
            "best_agents": [agent.to_dict() for agent in self.universe.get_best_agents(5)]
        })
        
        logger.info(f"Experiment '{self.name}' completed")
        return self.results
