"""
Lore N.A. Genetics Module
========================

This module contains the Genesis Protocol implementation for neural agent genetics.
It provides the foundation for agent DNA, evolution, and identity generation.

Components:
- AgentDNA: Digital DNA structure for neural agents
- DNAGenerator: Creates and manipulates agent DNA
- EvolutionEngine: Handles genetic evolution and fitness calculation
- AgentIdentity: Complete identity information for agents
- AgentNameGenerator: Generates unique names and identities

The genetics system is based on the 5 Lore N.A. universes:
- Limbo: Market behavior genes
- Odyssey: Creativity and customization genes
- Ritual: Social behavior genes
- Engine: Intelligence and analysis genes
- Logs: Operational expectations genes
"""

from .agent_dna import (
    AgentDNA,
    DNAGenerator,
    EvolutionEngine,
    UniverseGenes,
    GeneticTraits,
    AestheticBias
)

from .agent_name_generator import (
    AgentIdentity,
    AgentNameGenerator
)

__all__ = [
    'AgentDNA',
    'DNAGenerator',
    'EvolutionEngine',
    'UniverseGenes',
    'GeneticTraits',
    'AestheticBias',
    'AgentIdentity',
    'AgentNameGenerator'
]

__version__ = '1.0.0'
__author__ = 'Lore N.A. Genesis Team'
