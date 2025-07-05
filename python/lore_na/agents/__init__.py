"""
Lore N.A. Agents Module
======================

This module contains the neural agent implementations for the Lore N.A. ecosystem.
It provides base classes and specialized agent types for different behaviors.

Components:
- BaseAgent: Foundation class for all neural agents
- FrugalAgent: Cost-conscious marketplace agents
- SocialAgent: Community-focused agents
- EvolvedAgent: Advanced agents with genetic capabilities
- EmotionalAgent: Agents with emotional intelligence

All agents implement the Genesis Protocol for genetic evolution and unique identities.
"""

from .base_agent import BaseAgent

__all__ = [
    'BaseAgent'
]

__version__ = '1.0.0'
__author__ = 'Lore N.A. Genesis Team'
