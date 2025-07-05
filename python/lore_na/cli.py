#!/usr/bin/env python3
"""
Lore N.A. Command Line Interface
===============================

Provides command-line tools for managing the Lore N.A. ecosystem.
"""

import argparse
import sys
import logging
from typing import List, Optional
import asyncio

from .core.simulation import SimulationManager
from .genetics import DNAGenerator, AgentNameGenerator
from .agents import BaseAgent, FrugalBuyerAgent
from .utils.config import LoreConfig


def setup_logging(level: str = "INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_agent_command(args):
    """Create a new agent"""
    print(f"🧬 Creating agent: {args.name}")
    
    # Generate DNA
    dna_gen = DNAGenerator()
    agent_dna = dna_gen.generate_random_dna(args.name)
    
    # Generate identity
    name_gen = AgentNameGenerator()
    identity = name_gen.generate_identity(
        args.name,
        args.personality or "Social Adventurer",
        agent_dna.genes
    )
    
    print(f"✅ Agent created:")
    print(f"   Name: {identity.full_name}")
    print(f"   Nickname: {identity.nickname}")
    print(f"   Origin: {identity.origin}")
    print(f"   DNA Generation: {agent_dna.generation}")
    print(f"   Fitness: {agent_dna.fitness_scores['overall']:.3f}")
    
    if args.save:
        # Save agent configuration
        import json
        agent_config = {
            "identity": identity.to_dict(),
            "dna": agent_dna.to_dict()
        }
        
        with open(f"{args.name}.json", "w") as f:
            json.dump(agent_config, f, indent=2)
        
        print(f"💾 Agent configuration saved to {args.name}.json")


def run_agent_command(args):
    """Run an agent"""
    print(f"🚀 Starting agent: {args.name}")
    
    # Load configuration
    config = LoreConfig.from_env()
    
    # Create agent based on type
    if args.agent_type == "frugal":
        agent = FrugalBuyerAgent(
            name=args.name,
            api_base_url=config.api_base_url
        )
    else:
        agent = BaseAgent(
            name=args.name,
            api_base_url=config.api_base_url
        )
    
    # Run agent lifecycle
    try:
        agent.run_life_cycle(tick_interval=args.interval)
    except KeyboardInterrupt:
        print("\n⏹️  Agent stopped by user")
    except Exception as e:
        print(f"❌ Agent error: {e}")
        sys.exit(1)


def simulate_command(args):
    """Run a simulation"""
    print(f"🌍 Starting simulation with {args.agents} agents")
    
    config = LoreConfig.from_env()
    sim_manager = SimulationManager(config)
    
    # Run simulation
    try:
        asyncio.run(sim_manager.run_simulation(
            num_agents=args.agents,
            duration=args.duration,
            tick_interval=args.interval
        ))
    except KeyboardInterrupt:
        print("\n⏹️  Simulation stopped by user")
    except Exception as e:
        print(f"❌ Simulation error: {e}")
        sys.exit(1)


def status_command(args):
    """Check system status"""
    print("📊 Lore N.A. System Status")
    print("=" * 30)
    
    config = LoreConfig.from_env()
    
    # Check API connectivity
    import requests
    try:
        response = requests.get(f"{config.api_base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API: Connected")
        else:
            print(f"⚠️  API: Error {response.status_code}")
    except Exception as e:
        print(f"❌ API: Not reachable - {e}")
    
    # Check database
    try:
        from .core.database import DatabaseManager
        db = DatabaseManager(config.database_url)
        if db.is_connected():
            print("✅ Database: Connected")
        else:
            print("❌ Database: Not connected")
    except Exception as e:
        print(f"❌ Database: Error - {e}")
    
    # Check Rust engine
    try:
        import lore_engine
        info = lore_engine.get_system_info()
        print("✅ Rust Engine: Available")
        print(f"   Version: {info}")
    except ImportError:
        print("⚠️  Rust Engine: Not available (optional)")
    except Exception as e:
        print(f"❌ Rust Engine: Error - {e}")


def evolve_command(args):
    """Run genetic evolution"""
    print(f"🧬 Running genetic evolution for {args.generations} generations")
    
    from .genetics import EvolutionEngine
    
    # Create evolution engine
    engine = EvolutionEngine(
        population_size=args.population,
        elite_ratio=args.elite_ratio
    )
    
    # Generate initial population
    dna_gen = DNAGenerator()
    population = []
    
    for i in range(args.population):
        agent_dna = dna_gen.generate_random_dna(f"agent_{i:03d}")
        population.append(agent_dna)
    
    print(f"🌱 Initial population: {len(population)} agents")
    
    # Run evolution
    for generation in range(args.generations):
        print(f"\n🔄 Generation {generation + 1}")
        
        # Calculate fitness for population
        for agent_dna in population:
            # Simulate performance data
            performance_data = {
                "limbo": {"profit_ratio": 0.5, "decision_accuracy": 0.6},
                "odyssey": {"creativity_score": 0.7},
                "ritual": {"community_engagement": 0.6},
                "engine": {"prediction_accuracy": 0.8},
                "logs": {"delivery_satisfaction": 0.7}
            }
            engine.calculate_fitness(agent_dna, performance_data)
        
        # Evolve population
        population = engine.evolve_generation(population)
        
        # Show stats
        avg_fitness = sum(dna.fitness_scores["overall"] for dna in population) / len(population)
        best_fitness = max(dna.fitness_scores["overall"] for dna in population)
        
        print(f"   Average fitness: {avg_fitness:.3f}")
        print(f"   Best fitness: {best_fitness:.3f}")
    
    print(f"\n✅ Evolution completed!")
    
    # Show best agent
    best_agent = max(population, key=lambda dna: dna.fitness_scores["overall"])
    print(f"\n🏆 Best agent: {best_agent.agent_id}")
    print(f"   Fitness: {best_agent.fitness_scores['overall']:.3f}")
    print(f"   Generation: {best_agent.generation}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Lore N.A. - Neural Agent Simulation Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lore-na create-agent --name "explorer_001" --personality "Social Adventurer"
  lore-na run-agent --name "explorer_001" --agent-type frugal --interval 10
  lore-na simulate --agents 50 --duration 3600 --interval 5
  lore-na status
  lore-na evolve --population 100 --generations 20
        """
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create agent command
    create_parser = subparsers.add_parser("create-agent", help="Create a new agent")
    create_parser.add_argument("--name", required=True, help="Agent name")
    create_parser.add_argument("--personality", help="Agent personality archetype")
    create_parser.add_argument("--save", action="store_true", help="Save agent to file")
    create_parser.set_defaults(func=create_agent_command)
    
    # Run agent command
    run_parser = subparsers.add_parser("run-agent", help="Run an agent")
    run_parser.add_argument("--name", required=True, help="Agent name")
    run_parser.add_argument("--agent-type", choices=["base", "frugal"], default="base", help="Agent type")
    run_parser.add_argument("--interval", type=int, default=10, help="Tick interval in seconds")
    run_parser.set_defaults(func=run_agent_command)
    
    # Simulate command
    sim_parser = subparsers.add_parser("simulate", help="Run a simulation")
    sim_parser.add_argument("--agents", type=int, default=10, help="Number of agents")
    sim_parser.add_argument("--duration", type=int, default=3600, help="Duration in seconds")
    sim_parser.add_argument("--interval", type=int, default=5, help="Tick interval in seconds")
    sim_parser.set_defaults(func=simulate_command)
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check system status")
    status_parser.set_defaults(func=status_command)
    
    # Evolution command
    evolve_parser = subparsers.add_parser("evolve", help="Run genetic evolution")
    evolve_parser.add_argument("--population", type=int, default=50, help="Population size")
    evolve_parser.add_argument("--generations", type=int, default=10, help="Number of generations")
    evolve_parser.add_argument("--elite-ratio", type=float, default=0.2, help="Elite ratio")
    evolve_parser.set_defaults(func=evolve_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Execute command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
