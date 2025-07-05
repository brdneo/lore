# python/lore_na/agents/base_agent.py
# Base class for all Lore N.A. agents with Genesis Protocol support

import logging
import os
import time
import requests
import jwt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any, Optional

# Genesis Protocol imports
from ..genetics.agent_dna import AgentDNA, DNAGenerator, EvolutionEngine
from ..genetics.agent_name_generator import AgentNameGenerator, AgentIdentity

# Configure logger for this module
logger = logging.getLogger(__name__)

class BaseAgent:
    """
    Base class for all Lore N.A. Neural Agents.
    
    GENESIS PROTOCOL EVOLUTION:
    - Each agent now has unique digital DNA
    - Behavior influenced by genes from the 5 universes
    - Evolution and reproduction capabilities
    
    Responsibilities:
    - Manage secure and resilient API communication
    - Maintain internal agent state (ID, balance, etc.)
    - Provide methods to perceive environment and act upon it
    - Define a lifecycle that can be executed
    - Evolve based on performance across the 5 universes
    """
    
    def __init__(self, name: str, api_base_url: str, dna: Optional[AgentDNA] = None):
        """
        Initialize the agent.
        
        Args:
            name (str): Unique agent name, used to fetch its state
            api_base_url (str): Base URL of the Lore API (ex: http://kong:8000)
            dna (AgentDNA, optional): Agent DNA. If None, generates random DNA
        """
        self.name = name
        self.api_base_url = api_base_url
        self.agent_data = None  # Stores agent data from API
        
        # 🧬 GENESIS PROTOCOL: Initialize DNA
        if dna is None:
            dna_generator = DNAGenerator()
            self.dna = dna_generator.generate_random_dna(name)
        else:
            self.dna = dna
        
        # 🎭 IDENTITY SYSTEM: Generate unique identity
        name_generator = AgentNameGenerator()
        personality = self._determine_personality_from_dna()
        self.identity = name_generator.generate_identity(name, personality, self.dna.genes)
        
        # Performance tracking for fitness calculation
        self.performance_data = {
            "limbo": {"profit_ratio": 0.0, "decision_accuracy": 0.5, "market_timing": 0.5},
            "odyssey": {"creativity_score": 0.5, "popularity_score": 0.5, "innovation_score": 0.5},
            "ritual": {"community_engagement": 0.5, "social_influence": 0.5, "subscription_satisfaction": 0.5},
            "engine": {"prediction_accuracy": 0.5, "analysis_quality": 0.5, "ai_contributions": 0.5},
            "logs": {"delivery_satisfaction": 0.5, "operational_efficiency": 0.5, "problem_resolution": 0.5}
        }
        
        # Kong JWT configuration
        self.kong_jwt_iss = os.getenv("KONG_JWT_ISS", "agent_genesis")
        self.kong_jwt_secret = os.getenv("KONG_JWT_SECRET")
        
        if not self.kong_jwt_secret:
            raise ValueError("KONG_JWT_SECRET must be defined in environment variables")
        
        # Add agent name to logs for easy tracking
        self.logger = logging.LoggerAdapter(logger, {'agent_name': self.identity.full_name})

        # Initialization logging with identity
        self.logger.info(f"🎭 Agent {self.identity.full_name} '{self.identity.nickname}' initialized")
        self.logger.info(f"🧬 DNA Generation {self.dna.generation} - {self.identity.personality_archetype}")
        self.logger.info(f"🌍 Origin: {self.identity.origin}")

        # Configure resilient request session
        self.session = self._create_resilient_session()
        self.headers = {
            "Authorization": f"Bearer {self._generate_jwt_token()}",
            "Prefer": "return=representation,resolution=merge-duplicates"
        }
        
        self.initialize()

    def _generate_jwt_token(self) -> str:
        """
        Generate JWT token for Kong authentication.
        Token expires in 1 hour.
        """
        payload = {
            "iss": self.kong_jwt_iss,
            "exp": int(time.time()) + 60 * 60  # expires in 1h
        }
        token = jwt.encode(payload, self.kong_jwt_secret, algorithm="HS256")
        self.logger.info(f"New JWT token generated for issuer: {self.kong_jwt_iss}")
        return token

    def _refresh_jwt_if_needed(self):
        """
        Check if JWT token is close to expiry and renew if needed.
        """
        try:
            current_token = self.headers["Authorization"].split("Bearer ")[1]
            decoded = jwt.decode(current_token, self.kong_jwt_secret, algorithms=["HS256"])
            
            # If less than 5 minutes remain, renew token
            if decoded['exp'] - time.time() < 300:
                self.logger.info("JWT token close to expiry, renewing...")
                new_token = self._generate_jwt_token()
                self.headers["Authorization"] = f"Bearer {new_token}"
                
        except jwt.ExpiredSignatureError:
            self.logger.warning("JWT token expired, generating new one...")
            new_token = self._generate_jwt_token()
            self.headers["Authorization"] = f"Bearer {new_token}"
        except Exception as e:
            self.logger.error(f"Error checking JWT token: {e}")

    def _create_resilient_session(self) -> requests.Session:
        """
        Create a request session with retry strategy.
        Makes the agent robust to transient network failures.
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=5,  # Total number of retries
            backoff_factor=1,  # Wait factor (ex: 1s, 2s, 4s, 8s)
            status_forcelist=[500, 502, 503, 504],  # Error codes that trigger retry
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def initialize(self):
        """Fetch initial agent state from API by name."""
        self.logger.info("Initializing and fetching state from API...")
        try:
            self._refresh_jwt_if_needed()
            response = self.session.get(f"{self.api_base_url}/agents?name=eq.{self.name}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if data:
                self.agent_data = data[0]
                self.logger.info(f"Initial state loaded: ID={self.agent_data['id']}, Balance={self.agent_data['wallet_balance']}")
            else:
                self.logger.error(f"Could not find agent with name '{self.name}'.")
                self.agent_data = None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Communication error during initialization: {e}")
            self.agent_data = None

    def _update_local_state(self):
        """Update local agent state by fetching latest data from API."""
        if not self.agent_data:
            return
        try:
            self._refresh_jwt_if_needed()
            response = self.session.get(f"{self.api_base_url}/agents?id=eq.{self.agent_data['id']}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data:
                self.agent_data = data[0]
                self.logger.info(f"Local state updated. New balance: {self.agent_data['wallet_balance']}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Could not update local state: {e}")

    def decide_and_act(self):
        """
        Abstract method for decision logic.
        Child classes MUST implement this method.
        """
        raise NotImplementedError("Agent subclass must implement the 'decide_and_act' method.")
    
    # 🧬 GENESIS PROTOCOL: Evolution and genetic behavior methods
    
    def get_gene_value(self, universe: str, trait: str) -> float:
        """
        Get specific gene value
        
        Args:
            universe (str): Universe name (limbo, odyssey, ritual, engine, logs)
            trait (str): Genetic trait name
            
        Returns:
            float: Gene value (0.0 to 1.0)
        """
        universe_genes = getattr(self.dna, f"{universe}_genes")
        return universe_genes.traits.get(trait, 0.5)
    
    def get_categorical_gene(self, universe: str, trait: str) -> str:
        """
        Get categorical gene value
        
        Args:
            universe (str): Universe name
            trait (str): Categorical trait name
            
        Returns:
            str: Categorical gene value
        """
        universe_genes = getattr(self.dna, f"{universe}_genes")
        return universe_genes.categorical_traits.get(trait, "default")
    
    def update_performance(self, universe: str, metrics: Dict[str, float]):
        """
        Update performance data for fitness calculation
        
        Args:
            universe (str): Universe name
            metrics (dict): Performance metrics
        """
        if universe in self.performance_data:
            self.performance_data[universe].update(metrics)
            self.logger.debug(f"Performance updated in {universe}: {metrics}")
    
    def calculate_fitness(self) -> Dict[str, float]:
        """
        Calculate agent fitness based on performance
        
        Returns:
            dict: Fitness scores by universe
        """
        evolution_engine = EvolutionEngine()
        updated_dna = evolution_engine.calculate_fitness(self.dna, self.performance_data)
        self.dna = updated_dna
        
        self.logger.info(f"🧬 Fitness calculated: {self.dna.fitness_scores['overall']:.3f}")
        return self.dna.fitness_scores
    
    def make_decision_with_genes(self, decision_factors: Dict[str, Any], universe: str) -> Dict[str, Any]:
        """
        Make decision influenced by genes from specific universe
        
        Args:
            decision_factors (dict): Decision factors
            universe (str): Universe where decision is being made
            
        Returns:
            dict: Decision influenced by genes
        """
        if universe == "limbo":
            return self._limbo_genetic_decision(decision_factors)
        elif universe == "odyssey":
            return self._odyssey_genetic_decision(decision_factors)
        elif universe == "ritual":
            return self._ritual_genetic_decision(decision_factors)
        elif universe == "engine":
            return self._engine_genetic_decision(decision_factors)
        elif universe == "logs":
            return self._logs_genetic_decision(decision_factors)
        else:
            return decision_factors
    
    def _limbo_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decision influenced by Limbo genes"""
        risk_tolerance = self.get_gene_value("limbo", "risk_tolerance")
        price_sensitivity = self.get_gene_value("limbo", "price_sensitivity")
        quality_preference = self.get_gene_value("limbo", "quality_preference")
        
        # Influence purchase decision based on genes
        if "products" in factors:
            weighted_products = []
            for product in factors["products"]:
                score = 0.0
                
                # Risk tolerance gene affects new/experimental products
                if product.get("is_new", False):
                    score += risk_tolerance * 0.3
                
                # Price sensitivity gene
                price_factor = 1.0 - (product.get("price", 50) / 100.0)  # Normalize price
                score += price_factor * price_sensitivity * 0.4
                
                # Quality preference gene
                quality_factor = product.get("quality", 0.5)
                score += quality_factor * quality_preference * 0.3
                
                weighted_products.append({**product, "genetic_score": score})
            
            factors["products"] = sorted(weighted_products, key=lambda x: x["genetic_score"], reverse=True)
        
        return factors
    
    def _odyssey_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decision influenced by Odyssey genes"""
        creativity_drive = self.get_gene_value("odyssey", "creativity_drive")
        experimentation = self.get_gene_value("odyssey", "experimentation")
        aesthetic_bias = self.get_categorical_gene("odyssey", "aesthetic_bias")
        
        # Influence customization decisions
        if "customization_options" in factors:
            factors["customization_probability"] = creativity_drive
            factors["experimentation_level"] = experimentation
            factors["preferred_aesthetic"] = aesthetic_bias
        
        return factors
    
    def _ritual_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decision influenced by Ritual genes"""
        community_bonding = self.get_gene_value("ritual", "community_bonding")
        influence_susceptibility = self.get_gene_value("ritual", "influence_susceptibility")
        leadership_tendency = self.get_gene_value("ritual", "leadership_tendency")
        
        # Influence social and subscription decisions
        factors["community_weight"] = community_bonding
        factors["follow_influencers"] = influence_susceptibility
        factors["leadership_probability"] = leadership_tendency
        
        return factors
    
    def _engine_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decision influenced by Engine genes"""
        analytical_thinking = self.get_gene_value("engine", "analytical_thinking")
        pattern_recognition = self.get_gene_value("engine", "pattern_recognition")
        strategic_planning = self.get_gene_value("engine", "strategic_planning")
        
        # Influence analytical and strategic decisions
        factors["analysis_depth"] = analytical_thinking
        factors["pattern_sensitivity"] = pattern_recognition
        factors["planning_horizon"] = strategic_planning
        
        return factors
    
    def _logs_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decision influenced by Logs genes"""
        patience_level = self.get_gene_value("logs", "patience_level")
        service_expectations = self.get_gene_value("logs", "service_expectations")
        complaint_tendency = self.get_gene_value("logs", "complaint_tendency")
        
        # Influence operational expectations
        factors["delivery_patience"] = patience_level
        factors["service_standards"] = service_expectations
        factors["complaint_threshold"] = 1.0 - complaint_tendency
        
        return factors
    
    def can_reproduce(self) -> bool:
        """
        Determine if agent can reproduce based on fitness
        
        Returns:
            bool: True if can reproduce
        """
        overall_fitness = self.dna.fitness_scores.get("overall", 0.0)
        reproduction_threshold = 0.7  # Only successful agents reproduce
        
        return overall_fitness >= reproduction_threshold
    
    def get_dna_summary(self) -> Dict[str, Any]:
        """
        Return summary of agent DNA
        
        Returns:
            dict: Genetic summary
        """
        return {
            "agent_id": self.dna.agent_id,
            "generation": self.dna.generation,
            "parents": self.dna.parent_ids,
            "fitness_scores": self.dna.fitness_scores,
            "mutation_count": len(self.dna.mutation_history),
            "dominant_traits": {
                "limbo": max(self.dna.limbo_genes.traits.items(), key=lambda x: x[1]),
                "odyssey": max(self.dna.odyssey_genes.traits.items(), key=lambda x: x[1]),
                "ritual": max(self.dna.ritual_genes.traits.items(), key=lambda x: x[1]),
                "engine": max(self.dna.engine_genes.traits.items(), key=lambda x: x[1]),
                "logs": max(self.dna.logs_genes.traits.items(), key=lambda x: x[1])
            }
        }

    def run_life_cycle(self, tick_interval: int):
        """
        Main lifecycle that orchestrates the agent.
        Now includes genetic evolution.
        
        Args:
            tick_interval (int): Number of seconds to wait between each cycle
        """
        self.logger.info(f"🧬 Starting genetic lifecycle with {tick_interval} second intervals.")
        self.logger.info(f"🧬 DNA Summary: Generation {self.dna.generation}, Fitness: {self.dna.fitness_scores.get('overall', 0.0):.3f}")
        
        cycle_count = 0
        while True:
            self.logger.info("--- New Cycle (Tick) ---")
            if self.agent_data:
                self.decide_and_act()
                
                # Every 10 cycles, calculate fitness
                if cycle_count % 10 == 0:
                    fitness_scores = self.calculate_fitness()
                    self.logger.info(f"🧬 Fitness updated: {fitness_scores['overall']:.3f}")
                    
                    # Log reproduction if qualified
                    if self.can_reproduce():
                        self.logger.info("🧬 Agent qualified for reproduction!")
                
                cycle_count += 1
            else:
                self.logger.error("Agent data not loaded. Trying to re-initialize...")
                self.initialize()
            
            time.sleep(tick_interval)
    
    # 🎭 IDENTITY SYSTEM METHODS
    
    def _determine_personality_from_dna(self) -> str:
        """Determine personality based on agent DNA"""
        if not hasattr(self, 'dna') or not self.dna.genes:
            return "Social Adventurer"  # Default
        
        genes = self.dna.genes
        
        # Analyze dominant genes to determine personality
        scores = {}
        
        # Brave Speculator: High risk_tolerance + quality_preference
        if 'limbo' in genes:
            limbo_genes = genes['limbo']
            scores['Brave Speculator'] = (
                limbo_genes.get('risk_tolerance', 0.5) * 0.6 +
                limbo_genes.get('quality_preference', 0.5) * 0.4
            )
        
        # Bargain Hunter: High price_sensitivity + analytical_thinking
        if 'limbo' in genes and 'engine' in genes:
            scores['Bargain Hunter'] = (
                genes['limbo'].get('price_sensitivity', 0.5) * 0.5 +
                genes['engine'].get('analytical_thinking', 0.5) * 0.5
            )
        
        # Innovative Artist: High creativity_drive + experimentation
        if 'odyssey' in genes:
            odyssey_genes = genes['odyssey']
            scores['Innovative Artist'] = (
                odyssey_genes.get('creativity_drive', 0.5) * 0.6 +
                odyssey_genes.get('experimentation', 0.5) * 0.4
            )
        
        # Community Leader: High leadership_tendency + community_bonding
        if 'ritual' in genes:
            ritual_genes = genes['ritual']
            scores['Community Leader'] = (
                ritual_genes.get('leadership_tendency', 0.5) * 0.6 +
                ritual_genes.get('community_bonding', 0.5) * 0.4
            )
        
        # Loyal Follower: High influence_susceptibility + loyalty_factor
        if 'ritual' in genes:
            ritual_genes = genes['ritual']
            scores['Loyal Follower'] = (
                ritual_genes.get('influence_susceptibility', 0.5) * 0.5 +
                ritual_genes.get('loyalty_factor', 0.5) * 0.5
            )
        
        # Methodical Analyst: High analytical_thinking + low risk_tolerance
        if 'engine' in genes and 'limbo' in genes:
            scores['Methodical Analyst'] = (
                genes['engine'].get('analytical_thinking', 0.5) * 0.6 +
                (1.0 - genes['limbo'].get('risk_tolerance', 0.5)) * 0.4
            )
        
        # Social Adventurer: High community_bonding + experimentation
        if 'ritual' in genes and 'odyssey' in genes:
            scores['Social Adventurer'] = (
                genes['ritual'].get('community_bonding', 0.5) * 0.5 +
                genes['odyssey'].get('experimentation', 0.5) * 0.5
            )
        
        # Return personality with highest score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        else:
            return "Social Adventurer"
    
    def get_display_name(self, format_type: str = 'full') -> str:
        """Return formatted name for display"""
        if not hasattr(self, 'identity'):
            return self.name
        
        from ..genetics.agent_name_generator import AgentNameGenerator
        name_generator = AgentNameGenerator()
        return name_generator.get_display_name(self.identity, format_type)
    
    def introduce_self(self) -> str:
        """Generate personal introduction of the agent"""
        if not hasattr(self, 'identity'):
            return f"Hello, I am {self.name}."
        
        from ..genetics.agent_name_generator import AgentNameGenerator
        name_generator = AgentNameGenerator()
        return name_generator.generate_introduction(self.identity)
    
    def get_identity_summary(self) -> Dict[str, Any]:
        """Return complete summary of agent identity"""
        if not hasattr(self, 'identity'):
            return {'agent_id': self.name, 'error': 'Identity not initialized'}
        
        return {
            'agent_id': self.identity.agent_id,
            'full_name': self.identity.full_name,
            'nickname': self.identity.nickname,
            'title': self.identity.title,
            'origin': self.identity.origin,
            'personality': self.identity.personality_archetype,
            'name_meaning': self.identity.name_meaning,
            'display_formats': {
                'full': self.get_display_name('full'),
                'formal': self.get_display_name('formal'),
                'casual': self.get_display_name('casual'),
                'nickname': self.get_display_name('nickname')
            },
            'dna_generation': self.dna.generation if hasattr(self, 'dna') else None,
            'creation_timestamp': self.identity.generation_timestamp.isoformat()
        }
