# services/agent_runner/base_agent.py
# Contém a classe mãe para todos os agentes, encapsulando a comunicação com a API.

import logging
import os
import time
import requests
import jwt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
# Genesis Protocol imports
from agent_dna import AgentDNA, DNAGenerator, EvolutionEngine
from agent_name_generator import AgentNameGenerator, AgentIdentity
from typing import Dict, Any, Optional

# Configura o logger para este módulo.
logger = logging.getLogger(__name__)

class BaseAgent:
    """
    A classe base para todos os Agentes Neurais do Lore N.A.
    
    EVOLUÇÃO GENESIS PROTOCOL:
    - Agora cada agente possui DNA digital único
    - Comportamento influenciado por genes dos 5 universos
    - Capacidade de evolução e reprodução
    
    Responsabilidades:
    - Gerenciar a comunicação segura e resiliente com a API.
    - Manter o estado interno do agente (ID, saldo, etc.).
    - Fornecer métodos para perceber o ambiente e atuar sobre ele.
    - Definir um ciclo de vida que pode ser executado.
    - Evoluir baseado em performance nos 5 universos.
    """
    
    def __init__(self, name: str, api_base_url: str, dna: Optional[AgentDNA] = None):
        """
        Inicializa o agente.
        
        Args:
            name (str): O nome único do agente, usado para buscar seu estado.
            api_base_url (str): A URL base da API do Lore (ex: http://kong:8000).
            dna (AgentDNA, optional): DNA do agente. Se None, gera DNA aleatório.
        """
        self.name = name
        self.api_base_url = api_base_url
        self.agent_data = None  # Armazena os dados do agente vindos da API.
        
        # 🧬 GENESIS PROTOCOL: Inicializar DNA
        if dna is None:
            dna_generator = DNAGenerator()
            self.dna = dna_generator.generate_random_dna(name)
        else:
            self.dna = dna
        
        # 🎭 IDENTITY SYSTEM: Gerar identidade única
        name_generator = AgentNameGenerator()
        personality = self._determine_personality_from_dna()
        self.identity = name_generator.generate_identity(name, personality, self.dna.genes)
        
        # Performance tracking para cálculo de fitness
        self.performance_data = {
            "limbo": {"profit_ratio": 0.0, "decision_accuracy": 0.5, "market_timing": 0.5},
            "odyssey": {"creativity_score": 0.5, "popularity_score": 0.5, "innovation_score": 0.5},
            "ritual": {"community_engagement": 0.5, "social_influence": 0.5, "subscription_satisfaction": 0.5},
            "engine": {"prediction_accuracy": 0.5, "analysis_quality": 0.5, "ai_contributions": 0.5},
            "logs": {"delivery_satisfaction": 0.5, "operational_efficiency": 0.5, "problem_resolution": 0.5}
        }
        
        # Configuração JWT do Kong
        self.kong_jwt_iss = os.getenv("KONG_JWT_ISS", "agent_genesis")
        self.kong_jwt_secret = os.getenv("KONG_JWT_SECRET")
        
        if not self.kong_jwt_secret:
            raise ValueError("KONG_JWT_SECRET deve ser definido nas variáveis de ambiente")
        
        # Adiciona o nome do agente aos logs para fácil rastreamento.
        self.logger = logging.LoggerAdapter(logger, {'agent_name': self.identity.full_name})

        # Log de inicialização com identidade
        self.logger.info(f"🎭 Agente {self.identity.full_name} '{self.identity.nickname}' inicializado")
        self.logger.info(f"🧬 DNA Geração {self.dna.generation} - {self.identity.personality_archetype}")
        self.logger.info(f"🌍 Origem: {self.identity.origin}")

        # Configura a sessão de requisições com resiliência.
        self.session = self._create_resilient_session()
        self.headers = {
            "Authorization": f"Bearer {self._generate_jwt_token()}",
            "Prefer": "return=representation,resolution=merge-duplicates"
        }
        
        self.initialize()

    def _generate_jwt_token(self) -> str:
        """
        Gera um token JWT para autenticação no Kong.
        O token expira em 1 hora.
        """
        payload = {
            "iss": self.kong_jwt_iss,
            "exp": int(time.time()) + 60 * 60  # expira em 1h
        }
        token = jwt.encode(payload, self.kong_jwt_secret, algorithm="HS256")
        self.logger.info(f"Novo token JWT gerado para issuer: {self.kong_jwt_iss}")
        return token

    def _refresh_jwt_if_needed(self):
        """
        Verifica se o token JWT está próximo de expirar e o renova se necessário.
        """
        try:
            current_token = self.headers["Authorization"].split("Bearer ")[1]
            decoded = jwt.decode(current_token, self.kong_jwt_secret, algorithms=["HS256"])
            
            # Se restam menos de 5 minutos, renova o token
            if decoded['exp'] - time.time() < 300:
                self.logger.info("Token JWT próximo de expirar, renovando...")
                new_token = self._generate_jwt_token()
                self.headers["Authorization"] = f"Bearer {new_token}"
                
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token JWT expirado, gerando novo...")
            new_token = self._generate_jwt_token()
            self.headers["Authorization"] = f"Bearer {new_token}"
        except Exception as e:
            self.logger.error(f"Erro ao verificar token JWT: {e}")

    def _create_resilient_session(self) -> requests.Session:
        """
        Cria uma sessão de requisições com uma estratégia de reintentos.
        Isso torna o agente robusto a falhas de rede transitórias.
        (Implementa a Recomendação nº 4 da Revisão Arquitetônica)
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=5,  # Número total de reintentos.
            backoff_factor=1,  # Fator de espera (ex: 1s, 2s, 4s, 8s).
            status_forcelist=[500, 502, 503, 504],  # Códigos de erro que disparam o reintento.
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def initialize(self):
        """Busca o estado inicial do agente na API pelo seu nome."""
        self.logger.info("Inicializando e buscando estado na API...")
        try:
            self._refresh_jwt_if_needed()
            response = self.session.get(f"{self.api_base_url}/agents?name=eq.{self.name}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if data:
                self.agent_data = data[0]
                self.logger.info(f"Estado inicial carregado: ID={self.agent_data['id']}, Saldo={self.agent_data['wallet_balance']}")
            else:
                self.logger.error(f"Não foi possível encontrar o agente com o nome '{self.name}'.")
                self.agent_data = None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro de comunicação ao inicializar: {e}")
            self.agent_data = None

    def _update_local_state(self):
        """Atualiza o estado local do agente buscando os dados mais recentes da API."""
        if not self.agent_data:
            return
        try:
            self._refresh_jwt_if_needed()
            response = self.session.get(f"{self.api_base_url}/agents?id=eq.{self.agent_data['id']}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data:
                self.agent_data = data[0]
                self.logger.info(f"Estado local atualizado. Novo saldo: {self.agent_data['wallet_balance']}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Não foi possível atualizar o estado local: {e}")

    def decide_and_act(self):
        """
        Método abstrato para a lógica de decisão.
        As classes filhas DEVEM implementar este método.
        """
        raise NotImplementedError("A subclasse do agente deve implementar o método 'decide_and_act'.")
    
    # 🧬 GENESIS PROTOCOL: Métodos de evolução e comportamento genético
    
    def get_gene_value(self, universe: str, trait: str) -> float:
        """
        Obtém valor de um gene específico
        
        Args:
            universe (str): Nome do universo (limbo, odyssey, ritual, engine, logs)
            trait (str): Nome do trait genético
            
        Returns:
            float: Valor do gene (0.0 a 1.0)
        """
        universe_genes = getattr(self.dna, f"{universe}_genes")
        return universe_genes.traits.get(trait, 0.5)
    
    def get_categorical_gene(self, universe: str, trait: str) -> str:
        """
        Obtém valor de um gene categórico
        
        Args:
            universe (str): Nome do universo
            trait (str): Nome do trait categórico
            
        Returns:
            str: Valor categórico do gene
        """
        universe_genes = getattr(self.dna, f"{universe}_genes")
        return universe_genes.categorical_traits.get(trait, "default")
    
    def update_performance(self, universe: str, metrics: Dict[str, float]):
        """
        Atualiza dados de performance para cálculo de fitness
        
        Args:
            universe (str): Nome do universo
            metrics (dict): Métricas de performance
        """
        if universe in self.performance_data:
            self.performance_data[universe].update(metrics)
            self.logger.debug(f"Performance atualizada em {universe}: {metrics}")
    
    def calculate_fitness(self) -> Dict[str, float]:
        """
        Calcula fitness do agente baseado em performance
        
        Returns:
            dict: Scores de fitness por universo
        """
        evolution_engine = EvolutionEngine()
        updated_dna = evolution_engine.calculate_fitness(self.dna, self.performance_data)
        self.dna = updated_dna
        
        self.logger.info(f"🧬 Fitness calculado: {self.dna.fitness_scores['overall']:.3f}")
        return self.dna.fitness_scores
    
    def make_decision_with_genes(self, decision_factors: Dict[str, Any], universe: str) -> Dict[str, Any]:
        """
        Toma decisão influenciada por genes do universo específico
        
        Args:
            decision_factors (dict): Fatores para decisão
            universe (str): Universo onde a decisão está sendo tomada
            
        Returns:
            dict: Decisão influenciada pelos genes
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
        """Decisão influenciada por genes do Limbo"""
        risk_tolerance = self.get_gene_value("limbo", "risk_tolerance")
        price_sensitivity = self.get_gene_value("limbo", "price_sensitivity")
        quality_preference = self.get_gene_value("limbo", "quality_preference")
        
        # Influenciar decisão de compra baseado em genes
        if "products" in factors:
            weighted_products = []
            for product in factors["products"]:
                score = 0.0
                
                # Gene de tolerância a risco afeta produtos novos/experimentais
                if product.get("is_new", False):
                    score += risk_tolerance * 0.3
                
                # Gene de sensibilidade a preço
                price_factor = 1.0 - (product.get("price", 50) / 100.0)  # Normalizar preço
                score += price_factor * price_sensitivity * 0.4
                
                # Gene de preferência por qualidade
                quality_factor = product.get("quality", 0.5)
                score += quality_factor * quality_preference * 0.3
                
                weighted_products.append({**product, "genetic_score": score})
            
            factors["products"] = sorted(weighted_products, key=lambda x: x["genetic_score"], reverse=True)
        
        return factors
    
    def _odyssey_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decisão influenciada por genes da Odyssey"""
        creativity_drive = self.get_gene_value("odyssey", "creativity_drive")
        experimentation = self.get_gene_value("odyssey", "experimentation")
        aesthetic_bias = self.get_categorical_gene("odyssey", "aesthetic_bias")
        
        # Influenciar decisões de personalização
        if "customization_options" in factors:
            factors["customization_probability"] = creativity_drive
            factors["experimentation_level"] = experimentation
            factors["preferred_aesthetic"] = aesthetic_bias
        
        return factors
    
    def _ritual_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decisão influenciada por genes do Ritual"""
        community_bonding = self.get_gene_value("ritual", "community_bonding")
        influence_susceptibility = self.get_gene_value("ritual", "influence_susceptibility")
        leadership_tendency = self.get_gene_value("ritual", "leadership_tendency")
        
        # Influenciar decisões sociais e de assinatura
        factors["community_weight"] = community_bonding
        factors["follow_influencers"] = influence_susceptibility
        factors["leadership_probability"] = leadership_tendency
        
        return factors
    
    def _engine_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decisão influenciada por genes do Engine"""
        analytical_thinking = self.get_gene_value("engine", "analytical_thinking")
        pattern_recognition = self.get_gene_value("engine", "pattern_recognition")
        strategic_planning = self.get_gene_value("engine", "strategic_planning")
        
        # Influenciar decisões analíticas e estratégicas
        factors["analysis_depth"] = analytical_thinking
        factors["pattern_sensitivity"] = pattern_recognition
        factors["planning_horizon"] = strategic_planning
        
        return factors
    
    def _logs_genetic_decision(self, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Decisão influenciada por genes dos Logs"""
        patience_level = self.get_gene_value("logs", "patience_level")
        service_expectations = self.get_gene_value("logs", "service_expectations")
        complaint_tendency = self.get_gene_value("logs", "complaint_tendency")
        
        # Influenciar expectativas operacionais
        factors["delivery_patience"] = patience_level
        factors["service_standards"] = service_expectations
        factors["complaint_threshold"] = 1.0 - complaint_tendency
        
        return factors
    
    def can_reproduce(self) -> bool:
        """
        Determina se agente pode se reproduzir baseado em fitness
        
        Returns:
            bool: True se pode reproduzir
        """
        overall_fitness = self.dna.fitness_scores.get("overall", 0.0)
        reproduction_threshold = 0.7  # Apenas agentes bem-sucedidos reproduzem
        
        return overall_fitness >= reproduction_threshold
    
    def get_dna_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo do DNA do agente
        
        Returns:
            dict: Resumo genético
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
        O ciclo de vida principal que orquestra o agente.
        Agora inclui evolução genética.
        
        Args:
            tick_interval (int): O número de segundos a esperar entre cada ciclo.
        """
        self.logger.info(f"🧬 Iniciando ciclo de vida genético com intervalo de {tick_interval} segundos.")
        self.logger.info(f"🧬 DNA Summary: Geração {self.dna.generation}, Fitness: {self.dna.fitness_scores.get('overall', 0.0):.3f}")
        
        cycle_count = 0
        while True:
            self.logger.info("--- Novo Ciclo (Tick) ---")
            if self.agent_data:
                self.decide_and_act()
                
                # A cada 10 ciclos, calcular fitness
                if cycle_count % 10 == 0:
                    fitness_scores = self.calculate_fitness()
                    self.logger.info(f"🧬 Fitness atualizado: {fitness_scores['overall']:.3f}")
                    
                    # Log de reprodução se qualificado
                    if self.can_reproduce():
                        self.logger.info("🧬 Agente qualificado para reprodução!")
                
                cycle_count += 1
            else:
                self.logger.error("Dados do agente não carregados. Tentando re-inicializar...")
                self.initialize()
            
            time.sleep(tick_interval)
    
    # 🎭 IDENTITY SYSTEM METHODS
    
    def _determine_personality_from_dna(self) -> str:
        """Determina personalidade baseada no DNA do agente"""
        if not hasattr(self, 'dna') or not self.dna.genes:
            return "Aventureiro Social"  # Default
        
        genes = self.dna.genes
        
        # Analisa genes dominantes para determinar personalidade
        scores = {}
        
        # Especulador Corajoso: Alto risk_tolerance + quality_preference
        if 'limbo' in genes:
            limbo_genes = genes['limbo']
            scores['Especulador Corajoso'] = (
                limbo_genes.get('risk_tolerance', 0.5) * 0.6 +
                limbo_genes.get('quality_preference', 0.5) * 0.4
            )
        
        # Caçador de Barganha: Alto price_sensitivity + analytical_thinking
        if 'limbo' in genes and 'engine' in genes:
            scores['Caçador de Barganha'] = (
                genes['limbo'].get('price_sensitivity', 0.5) * 0.5 +
                genes['engine'].get('analytical_thinking', 0.5) * 0.5
            )
        
        # Artista Inovador: Alto creativity_drive + experimentation
        if 'odyssey' in genes:
            odyssey_genes = genes['odyssey']
            scores['Artista Inovador'] = (
                odyssey_genes.get('creativity_drive', 0.5) * 0.6 +
                odyssey_genes.get('experimentation', 0.5) * 0.4
            )
        
        # Líder Comunitário: Alto leadership_tendency + community_bonding
        if 'ritual' in genes:
            ritual_genes = genes['ritual']
            scores['Líder Comunitário'] = (
                ritual_genes.get('leadership_tendency', 0.5) * 0.6 +
                ritual_genes.get('community_bonding', 0.5) * 0.4
            )
        
        # Seguidor Leal: Alto influence_susceptibility + loyalty_factor
        if 'ritual' in genes:
            ritual_genes = genes['ritual']
            scores['Seguidor Leal'] = (
                ritual_genes.get('influence_susceptibility', 0.5) * 0.5 +
                ritual_genes.get('loyalty_factor', 0.5) * 0.5
            )
        
        # Analista Metódico: Alto analytical_thinking + low risk_tolerance
        if 'engine' in genes and 'limbo' in genes:
            scores['Analista Metódico'] = (
                genes['engine'].get('analytical_thinking', 0.5) * 0.6 +
                (1.0 - genes['limbo'].get('risk_tolerance', 0.5)) * 0.4
            )
        
        # Aventureiro Social: Alto community_bonding + experimentation
        if 'ritual' in genes and 'odyssey' in genes:
            scores['Aventureiro Social'] = (
                genes['ritual'].get('community_bonding', 0.5) * 0.5 +
                genes['odyssey'].get('experimentation', 0.5) * 0.5
            )
        
        # Retorna personalidade com maior score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        else:
            return "Aventureiro Social"
    
    def get_display_name(self, format_type: str = 'full') -> str:
        """Retorna nome formatado para exibição"""
        if not hasattr(self, 'identity'):
            return self.name
        
        from agent_name_generator import AgentNameGenerator
        name_generator = AgentNameGenerator()
        return name_generator.get_display_name(self.identity, format_type)
    
    def introduce_self(self) -> str:
        """Gera introdução pessoal do agente"""
        if not hasattr(self, 'identity'):
            return f"Olá, eu sou {self.name}."
        
        from agent_name_generator import AgentNameGenerator
        name_generator = AgentNameGenerator()
        return name_generator.generate_introduction(self.identity)
    
    def get_identity_summary(self) -> Dict[str, Any]:
        """Retorna resumo completo da identidade do agente"""
        if not hasattr(self, 'identity'):
            return {'agent_id': self.name, 'error': 'Identidade não inicializada'}
        
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

