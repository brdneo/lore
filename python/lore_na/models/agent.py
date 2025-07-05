"""
Agent models for Lore N.A.
=========================

Data models representing agents, DNA, and related structures
in the intelligent agent simulation system.
"""

import uuid
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AgentDNA:
    """
    Genetic representation of an agent.
    
    Contains the core genetic information that defines
    an agent's capabilities and characteristics.
    """
    genes: List[float] = field(default_factory=list)
    fitness: Optional[float] = None
    generation: int = 0
    parent_ids: List[str] = field(default_factory=list)
    mutations: int = 0
    creation_time: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Initialize DNA with random genes if empty."""
        if not self.genes:
            self.genes = [random.uniform(-1.0, 1.0) for _ in range(10)]
    
    @classmethod
    def random(cls, gene_count: int = 10) -> "AgentDNA":
        """Create random DNA."""
        return cls(genes=[random.uniform(-1.0, 1.0) for _ in range(gene_count)])
    
    @classmethod
    def from_parents(cls, parent1: "AgentDNA", parent2: "AgentDNA") -> "AgentDNA":
        """Create DNA from two parents via crossover."""
        # Uniform crossover
        child_genes = []
        for g1, g2 in zip(parent1.genes, parent2.genes):
            child_genes.append(g1 if random.random() < 0.5 else g2)
        
        return cls(
            genes=child_genes,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=[str(id(parent1)), str(id(parent2))]
        )
    
    def mutate(self, mutation_rate: float = 0.1, mutation_strength: float = 0.1):
        """Apply mutation to the DNA."""
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] += random.gauss(0, mutation_strength)
                self.genes[i] = max(-1.0, min(1.0, self.genes[i]))  # Clamp to [-1, 1]
        
        self.mutations += 1
    
    def distance_to(self, other: "AgentDNA") -> float:
        """Calculate genetic distance to another DNA."""
        if len(self.genes) != len(other.genes):
            raise ValueError("Cannot compare DNA with different gene counts")
        
        return sum((g1 - g2) ** 2 for g1, g2 in zip(self.genes, other.genes)) ** 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "genes": self.genes,
            "fitness": self.fitness,
            "generation": self.generation,
            "parent_ids": self.parent_ids,
            "mutations": self.mutations,
            "creation_time": self.creation_time.isoformat()
        }

@dataclass
class Agent:
    """
    Intelligent agent with genetic and behavioral characteristics.
    
    Represents a single agent in the simulation with its DNA,
    behavior patterns, cognitive abilities, and state.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    dna: AgentDNA = field(default_factory=AgentDNA)
    fitness: float = 0.0
    behavior: str = "explorer"
    cognitive_capacity: float = 0.5
    generation: int = 0
    
    # State variables
    energy: float = 100.0
    resources: int = 0
    experience: int = 0
    age: int = 0
    
    # Social variables
    reputation: float = 0.5
    connections: List[str] = field(default_factory=list)
    
    # Emotional state
    emotional_state: Dict[str, float] = field(default_factory=lambda: {
        "happiness": 0.5,
        "curiosity": 0.5,
        "aggression": 0.3,
        "cooperation": 0.7
    })
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Initialize agent after creation."""
        if self.dna.fitness is None:
            self.dna.fitness = self.fitness
    
    @classmethod
    def random(cls, agent_id: Optional[str] = None) -> "Agent":
        """Create a random agent."""
        behaviors = ["explorer", "socializer", "optimizer", "creator", "analyzer"]
        
        return cls(
            id=agent_id or str(uuid.uuid4()),
            dna=AgentDNA.random(),
            fitness=random.uniform(0.1, 0.9),
            behavior=random.choice(behaviors),
            cognitive_capacity=random.uniform(0.3, 0.9),
            energy=random.uniform(80, 100),
            resources=random.randint(0, 100)
        )
    
    def update_fitness(self, new_fitness: float):
        """Update agent's fitness score."""
        self.fitness = new_fitness
        self.dna.fitness = new_fitness
        self.updated_at = datetime.now()
    
    def age_agent(self):
        """Age the agent by one time step."""
        self.age += 1
        self.experience += 1
        
        # Gradually decrease energy
        self.energy = max(0, self.energy - random.uniform(0.1, 0.5))
        
        self.updated_at = datetime.now()
    
    def interact_with(self, other: "Agent") -> float:
        """
        Interact with another agent.
        
        Returns interaction strength (0-1).
        """
        # Base interaction on behavioral compatibility
        behavior_compatibility = {
            ("explorer", "explorer"): 0.8,
            ("socializer", "socializer"): 0.9,
            ("optimizer", "optimizer"): 0.7,
            ("creator", "analyzer"): 0.8,
            ("creator", "creator"): 0.6,
        }
        
        key = (self.behavior, other.behavior)
        base_strength = behavior_compatibility.get(key, 0.5)
        
        # Modify by emotional compatibility
        emotional_factor = (
            abs(self.emotional_state["cooperation"] - other.emotional_state["cooperation"])
        )
        
        interaction_strength = base_strength * (1 - emotional_factor * 0.3)
        
        # Update connection if strong interaction
        if interaction_strength > 0.6 and other.id not in self.connections:
            self.connections.append(other.id)
        
        return max(0, min(1, interaction_strength))
    
    def make_decision(self, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a decision based on current state and environment.
        
        Returns decision dictionary with action and parameters.
        """
        decision = {
            "action": "explore",
            "confidence": 0.5,
            "reasoning": []
        }
        
        # Behavior-specific decision making
        if self.behavior == "explorer":
            decision["action"] = "explore"
            decision["confidence"] = self.emotional_state["curiosity"]
            
        elif self.behavior == "socializer":
            decision["action"] = "interact"
            decision["confidence"] = self.emotional_state["cooperation"]
            
        elif self.behavior == "optimizer":
            decision["action"] = "optimize"
            decision["confidence"] = self.cognitive_capacity
            
        elif self.behavior == "creator":
            decision["action"] = "create"
            decision["confidence"] = (self.emotional_state["curiosity"] + self.cognitive_capacity) / 2
            
        elif self.behavior == "analyzer":
            decision["action"] = "analyze"
            decision["confidence"] = self.cognitive_capacity
        
        # Modify based on energy
        if self.energy < 30:
            decision["action"] = "rest"
            decision["confidence"] = 0.9
            decision["reasoning"].append("low_energy")
        
        return decision
    
    def get_genome_summary(self) -> Dict[str, Any]:
        """Get summary of genetic characteristics."""
        return {
            "gene_count": len(self.dna.genes),
            "gene_average": sum(self.dna.genes) / len(self.dna.genes),
            "gene_variance": sum((g - sum(self.dna.genes) / len(self.dna.genes)) ** 2 for g in self.dna.genes) / len(self.dna.genes),
            "generation": self.generation,
            "mutations": self.dna.mutations,
            "fitness": self.fitness
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary."""
        return {
            "id": self.id,
            "dna": self.dna.to_dict(),
            "fitness": self.fitness,
            "behavior": self.behavior,
            "cognitive_capacity": self.cognitive_capacity,
            "generation": self.generation,
            "energy": self.energy,
            "resources": self.resources,
            "experience": self.experience,
            "age": self.age,
            "reputation": self.reputation,
            "connections": self.connections,
            "emotional_state": self.emotional_state,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Agent":
        """Create agent from dictionary."""
        # Parse datetime fields
        created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        updated_at = datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        
        # Create DNA
        dna_data = data.get("dna", {})
        dna = AgentDNA(
            genes=dna_data.get("genes", []),
            fitness=dna_data.get("fitness"),
            generation=dna_data.get("generation", 0),
            parent_ids=dna_data.get("parent_ids", []),
            mutations=dna_data.get("mutations", 0)
        )
        
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            dna=dna,
            fitness=data.get("fitness", 0.0),
            behavior=data.get("behavior", "explorer"),
            cognitive_capacity=data.get("cognitive_capacity", 0.5),
            generation=data.get("generation", 0),
            energy=data.get("energy", 100.0),
            resources=data.get("resources", 0),
            experience=data.get("experience", 0),
            age=data.get("age", 0),
            reputation=data.get("reputation", 0.5),
            connections=data.get("connections", []),
            emotional_state=data.get("emotional_state", {}),
            created_at=created_at,
            updated_at=updated_at
        )
