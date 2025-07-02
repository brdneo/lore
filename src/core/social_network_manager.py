#!/usr/bin/env python3
"""
Social Network Manager - Lore N.A.
==================================

Gerenciador da rede social neural que coordena:
- Evolução dinâmica da rede social
- Formação e dissolução de comunidades
- Eventos sociais e tendências emergentes
- Métricas e análises da rede neural
- Integração com o sistema evolutivo

Autor: Lore N.A. Genesis Team
Data: 2024
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging
import matplotlib.pyplot as plt
import seaborn as sns

from neural_web import NeuralWeb, ConnectionType
from social_agent import SocialAgent
from population_manager import PopulationManager
from agent_dna import AgentDNA

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SocialEvent:
    """Representa um evento social na rede"""
    event_id: str
    event_type: str
    timestamp: datetime
    participants: List[str]
    impact_radius: int
    intensity: float
    effects: Dict[str, Any]
    description: str
    
    def to_dict(self) -> Dict:
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'timestamp': self.timestamp.isoformat(),
            'participants': self.participants,
            'impact_radius': self.impact_radius,
            'intensity': self.intensity,
            'effects': self.effects,
            'description': self.description
        }


@dataclass
class CommunityState:
    """Estado de uma comunidade na rede"""
    community_id: str
    members: Set[str]
    leader: Optional[str]
    cohesion: float
    activity_level: float
    formation_date: datetime
    shared_values: Dict[str, float]
    collective_goals: List[str]
    
    def to_dict(self) -> Dict:
        return {
            'community_id': self.community_id,
            'members': list(self.members),
            'leader': self.leader,
            'cohesion': self.cohesion,
            'activity_level': self.activity_level,
            'formation_date': self.formation_date.isoformat(),
            'shared_values': self.shared_values,
            'collective_goals': self.collective_goals
        }


class SocialNetworkManager:
    """Gerenciador da rede social neural"""
    
    def __init__(self, neural_web: NeuralWeb, population_manager: PopulationManager):
        self.neural_web = neural_web
        self.population_manager = population_manager
        self.social_agents: Dict[str, SocialAgent] = {}
        self.communities: Dict[str, CommunityState] = {}
        self.social_events: List[SocialEvent] = []
        self.trends: Dict[str, float] = {}
        self.social_metrics_history: List[Dict] = []
        
        # Configurações
        self.max_community_size = 10
        self.min_community_cohesion = 0.3
        self.event_probability = 0.1
        
        logger.info("SocialNetworkManager inicializado")
    
    def add_social_agent(self, agent: SocialAgent):
        """Adiciona um agente social ao gerenciador"""
        self.social_agents[agent.agent_id] = agent
        logger.info(f"Agente social {agent.agent_id} adicionado ao gerenciador")
    
    def create_social_agents_from_population(self):
        """Converte agentes da população em agentes sociais"""
        for agent_id, agent_data in self.population_manager.agents.items():
            if agent_id not in self.social_agents:
                # Reconstrói DNA do agente
                dna = AgentDNA()
                dna.genes = agent_data['dna']
                
                # Cria agente social
                social_agent = SocialAgent(agent_id, dna, self.neural_web)
                self.add_social_agent(social_agent)
    
    def simulate_social_round(self):
        """Simula uma rodada de atividade social"""
        logger.info("Iniciando rodada social...")
        
        # Atualiza agentes sociais da população
        self.create_social_agents_from_population()
        
        # Fase 1: Busca por novas conexões
        self._connection_discovery_phase()
        
        # Fase 2: Manutenção de relacionamentos
        self._relationship_maintenance_phase()
        
        # Fase 3: Influência e liderança
        self._influence_phase()
        
        # Fase 4: Eventos sociais
        self._social_events_phase()
        
        # Fase 5: Evolução de comunidades
        self._community_evolution_phase()
        
        # Fase 6: Análise de tendências
        self._trend_analysis_phase()
        
        # Atualiza métricas
        self.neural_web.update_social_metrics()
        self._record_social_metrics()
        
        logger.info("Rodada social concluída")
    
    def _connection_discovery_phase(self):
        """Fase de descoberta de novas conexões"""
        logger.info("Fase: Descoberta de conexões")
        
        new_connections = 0
        for agent in self.social_agents.values():
            # Probabilidade baseada na personalidade do agente
            discovery_prob = agent.dna.genes['ritual']['community_bonding'] * 0.3
            discovery_prob += agent.dna.genes['odyssey']['experimentation'] * 0.2
            
            if random.random() < discovery_prob:
                agent.seek_new_connections(self.social_agents, max_new_connections=2)
                new_connections += 1
        
        logger.info(f"  {new_connections} agentes buscaram novas conexões")
    
    def _relationship_maintenance_phase(self):
        """Fase de manutenção de relacionamentos"""
        logger.info("Fase: Manutenção de relacionamentos")
        
        total_interactions = 0
        for agent in self.social_agents.values():
            connections_before = len(agent.neural_web.get_agent_connections(agent.agent_id))
            agent.maintain_relationships(self.social_agents)
            
            # Conta interações (aproximação)
            connections_after = len(agent.neural_web.get_agent_connections(agent.agent_id))
            total_interactions += max(0, connections_after - connections_before)
        
        logger.info(f"  ~{total_interactions} interações registradas")
    
    def _influence_phase(self):
        """Fase de influência e liderança"""
        logger.info("Fase: Influência e liderança")
        
        leaders_active = 0
        for agent in self.social_agents.values():
            leadership = agent.dna.genes['ritual']['leadership_tendency']
            if leadership > 0.6:
                agent.influence_network(self.social_agents)
                leaders_active += 1
        
        logger.info(f"  {leaders_active} líderes ativos influenciando a rede")
    
    def _social_events_phase(self):
        """Fase de eventos sociais emergentes"""
        if random.random() < self.event_probability:
            event = self._generate_social_event()
            if event:
                self._execute_social_event(event)
                logger.info(f"Evento social: {event.event_type} ({len(event.participants)} participantes)")
    
    def _generate_social_event(self) -> Optional[SocialEvent]:
        """Gera um evento social baseado no estado da rede"""
        if not self.social_agents:
            return None
        
        event_types = [
            "trend_emergence",
            "community_gathering", 
            "influence_campaign",
            "competitive_challenge",
            "collaborative_project",
            "social_crisis",
            "innovation_wave"
        ]
        
        event_type = random.choice(event_types)
        event_id = f"event_{len(self.social_events):04d}"
        
        # Seleciona participantes baseado no tipo de evento
        participants = self._select_event_participants(event_type)
        
        if not participants:
            return None
        
        # Determina intensidade baseada nos participantes
        total_influence = sum(
            self.neural_web.agent_metrics.get(p, type('obj', (object,), {'influence_score': 0})).influence_score
            for p in participants
        )
        intensity = min(1.0, total_influence / len(participants))
        
        # Efeitos do evento
        effects = self._determine_event_effects(event_type, participants, intensity)
        
        # Descrição
        description = self._generate_event_description(event_type, participants, intensity)
        
        return SocialEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=datetime.now(),
            participants=participants,
            impact_radius=len(participants) + random.randint(1, 3),
            intensity=intensity,
            effects=effects,
            description=description
        )
    
    def _select_event_participants(self, event_type: str) -> List[str]:
        """Seleciona participantes para um evento social"""
        if event_type == "trend_emergence":
            # Influenciadores e agentes criativos
            candidates = [
                agent_id for agent_id, agent in self.social_agents.items()
                if (agent.dna.genes['ritual']['leadership_tendency'] > 0.6 or
                    agent.dna.genes['odyssey']['creativity_drive'] > 0.7)
            ]
            return random.sample(candidates, min(3, len(candidates)))
        
        elif event_type == "community_gathering":
            # Membros de uma comunidade específica
            if self.communities:
                community = random.choice(list(self.communities.values()))
                return random.sample(list(community.members), min(5, len(community.members)))
            else:
                # Agentes com alto community_bonding
                candidates = [
                    agent_id for agent_id, agent in self.social_agents.items()
                    if agent.dna.genes['ritual']['community_bonding'] > 0.6
                ]
                return random.sample(candidates, min(4, len(candidates)))
        
        elif event_type == "competitive_challenge":
            # Agentes competitivos
            candidates = [
                agent_id for agent_id, agent in self.social_agents.items()
                if agent.dna.genes['limbo']['risk_tolerance'] > 0.6
            ]
            return random.sample(candidates, min(4, len(candidates)))
        
        elif event_type == "collaborative_project":
            # Agentes colaborativos
            candidates = [
                agent_id for agent_id, agent in self.social_agents.items()
                if agent.dna.genes['ritual']['community_bonding'] > 0.5
            ]
            return random.sample(candidates, min(6, len(candidates)))
        
        else:
            # Seleção aleatória
            return random.sample(list(self.social_agents.keys()), min(3, len(self.social_agents)))
    
    def _determine_event_effects(self, event_type: str, participants: List[str], intensity: float) -> Dict[str, Any]:
        """Determina os efeitos de um evento social"""
        effects = {}
        
        if event_type == "trend_emergence":
            effects = {
                'type': 'trend_boost',
                'affected_universe': random.choice(['limbo', 'odyssey', 'ritual']),
                'boost_amount': intensity * 0.1,
                'duration_rounds': random.randint(2, 5)
            }
        
        elif event_type == "community_gathering":
            effects = {
                'type': 'community_bonding',
                'cohesion_boost': intensity * 0.15,
                'new_connections_probability': intensity * 0.3
            }
        
        elif event_type == "competitive_challenge":
            effects = {
                'type': 'performance_boost',
                'fitness_multiplier': 1.0 + (intensity * 0.2),
                'affected_universe': 'limbo'
            }
        
        elif event_type == "collaborative_project":
            effects = {
                'type': 'collaboration_bonus',
                'skill_sharing': True,
                'collective_benefit': intensity * 0.1
            }
        
        elif event_type == "social_crisis":
            effects = {
                'type': 'stress_test',
                'connection_strain': intensity * 0.2,
                'leadership_opportunity': True
            }
        
        elif event_type == "innovation_wave":
            effects = {
                'type': 'creativity_boost',
                'affected_universe': 'odyssey',
                'innovation_bonus': intensity * 0.15
            }
        
        return effects
    
    def _generate_event_description(self, event_type: str, participants: List[str], intensity: float) -> str:
        """Gera descrição textual do evento"""
        descriptions = {
            "trend_emergence": f"Uma nova tendência emergiu na rede, liderada por {len(participants)} agentes influentes",
            "community_gathering": f"Reunião comunitária com {len(participants)} membros fortalecendo laços sociais",
            "competitive_challenge": f"Desafio competitivo entre {len(participants)} agentes ambiciosos",
            "collaborative_project": f"Projeto colaborativo reunindo {len(participants)} agentes inovadores",
            "social_crisis": f"Crise social testando a resiliência de {len(participants)} agentes",
            "innovation_wave": f"Onda de inovação inspirando {len(participants)} agentes criativos"
        }
        
        base_desc = descriptions.get(event_type, f"Evento social com {len(participants)} participantes")
        intensity_desc = ""
        
        if intensity > 0.8:
            intensity_desc = " (impacto muito alto)"
        elif intensity > 0.6:
            intensity_desc = " (impacto alto)"
        elif intensity > 0.4:
            intensity_desc = " (impacto moderado)"
        else:
            intensity_desc = " (impacto baixo)"
        
        return base_desc + intensity_desc
    
    def _execute_social_event(self, event: SocialEvent):
        """Executa os efeitos de um evento social"""
        self.social_events.append(event)
        
        effects = event.effects
        participants = event.participants
        
        if effects.get('type') == 'trend_boost':
            universe = effects['affected_universe']
            boost = effects['boost_amount']
            
            for agent_id in participants:
                if agent_id in self.social_agents:
                    agent = self.social_agents[agent_id]
                    agent.add_performance_bonus(f"trend_{universe}", boost)
        
        elif effects.get('type') == 'community_bonding':
            # Fortalece conexões entre participantes
            for i, agent1_id in enumerate(participants):
                for agent2_id in participants[i+1:]:
                    connection = self.neural_web.get_connection(agent1_id, agent2_id)
                    if connection:
                        connection.strength = min(1.0, connection.strength + effects['cohesion_boost'])
        
        elif effects.get('type') == 'performance_boost':
            # Boost de performance temporário
            for agent_id in participants:
                if agent_id in self.social_agents:
                    agent = self.social_agents[agent_id]
                    universe = effects['affected_universe']
                    multiplier = effects['fitness_multiplier']
                    agent.add_performance_bonus(f"challenge_{universe}", multiplier - 1.0)
        
        elif effects.get('type') == 'collaboration_bonus':
            # Benefícios de colaboração
            if len(participants) > 1:
                collective_benefit = effects['collective_benefit']
                for agent_id in participants:
                    if agent_id in self.social_agents:
                        agent = self.social_agents[agent_id]
                        agent.add_performance_bonus("collaboration", collective_benefit)
        
        logger.info(f"Evento {event.event_id} executado: {event.description}")
    
    def _community_evolution_phase(self):
        """Fase de evolução das comunidades"""
        # Detecta comunidades atuais
        current_communities = self.neural_web.detect_communities()
        
        # Atualiza ou cria estados de comunidade
        for comm_id, members in current_communities.items():
            if comm_id not in self.communities:
                # Nova comunidade
                leader = self._elect_community_leader(members)
                shared_values = self._calculate_shared_values(members)
                
                self.communities[comm_id] = CommunityState(
                    community_id=comm_id,
                    members=members,
                    leader=leader,
                    cohesion=0.5,
                    activity_level=0.5,
                    formation_date=datetime.now(),
                    shared_values=shared_values,
                    collective_goals=self._determine_collective_goals(members)
                )
                
                logger.info(f"Nova comunidade formada: {comm_id} ({len(members)} membros)")
            
            else:
                # Atualiza comunidade existente
                community = self.communities[comm_id]
                community.members = members
                community.cohesion = self._calculate_community_cohesion(members)
                community.activity_level = self._calculate_community_activity(members)
                
                # Reeleição de líder se necessário
                if (community.leader not in members or 
                    random.random() < 0.1):  # 10% chance de reeleição
                    community.leader = self._elect_community_leader(members)
        
        # Remove comunidades que não existem mais
        active_community_ids = set(current_communities.keys())
        inactive_communities = set(self.communities.keys()) - active_community_ids
        
        for inactive_id in inactive_communities:
            logger.info(f"Comunidade dissolvida: {inactive_id}")
            del self.communities[inactive_id]
    
    def _elect_community_leader(self, members: Set[str]) -> Optional[str]:
        """Elege líder de uma comunidade"""
        candidates = []
        
        for member_id in members:
            if member_id in self.social_agents:
                agent = self.social_agents[member_id]
                leadership = agent.dna.genes['ritual']['leadership_tendency']
                influence = self.neural_web.agent_metrics.get(member_id, type('obj', (object,), {'influence_score': 0})).influence_score
                
                score = leadership * 0.6 + influence * 0.4
                candidates.append((member_id, score))
        
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
        
        return None
    
    def _calculate_shared_values(self, members: Set[str]) -> Dict[str, float]:
        """Calcula valores compartilhados de uma comunidade"""
        if not members:
            return {}
        
        shared_values = {}
        gene_sums = {}
        gene_counts = {}
        
        # Agrega genes de todos os membros
        for member_id in members:
            if member_id in self.social_agents:
                agent = self.social_agents[member_id]
                for universe, genes in agent.dna.genes.items():
                    for gene_name, gene_value in genes.items():
                        key = f"{universe}_{gene_name}"
                        gene_sums[key] = gene_sums.get(key, 0) + gene_value
                        gene_counts[key] = gene_counts.get(key, 0) + 1
        
        # Calcula médias
        for key in gene_sums:
            shared_values[key] = gene_sums[key] / gene_counts[key]
        
        return shared_values
    
    def _determine_collective_goals(self, members: Set[str]) -> List[str]:
        """Determina objetivos coletivos de uma comunidade"""
        goals = []
        
        # Conta objetivos individuais
        goal_counts = {}
        for member_id in members:
            if member_id in self.social_agents:
                agent = self.social_agents[member_id]
                for goal in agent.social_goals:
                    goal_counts[goal] = goal_counts.get(goal, 0) + 1
        
        # Objetivos compartilhados por maioria viram objetivos coletivos
        threshold = len(members) * 0.5
        for goal, count in goal_counts.items():
            if count >= threshold:
                goals.append(f"collective_{goal}")
        
        # Adiciona objetivos baseados nos valores da comunidade
        shared_values = self._calculate_shared_values(members)
        
        if shared_values.get('ritual_community_bonding', 0) > 0.7:
            goals.append("strengthen_community_bonds")
        
        if shared_values.get('odyssey_creativity_drive', 0) > 0.7:
            goals.append("foster_collective_creativity")
        
        if shared_values.get('limbo_risk_tolerance', 0) > 0.7:
            goals.append("pursue_bold_ventures")
        
        return goals
    
    def _calculate_community_cohesion(self, members: Set[str]) -> float:
        """Calcula coesão de uma comunidade"""
        if len(members) < 2:
            return 1.0
        
        total_connections = 0
        total_strength = 0.0
        possible_connections = len(members) * (len(members) - 1)
        
        for member1 in members:
            for member2 in members:
                if member1 != member2:
                    connection = self.neural_web.get_connection(member1, member2)
                    if connection:
                        total_connections += 1
                        total_strength += connection.strength
        
        if total_connections == 0:
            return 0.0
        
        # Coesão = densidade das conexões * força média
        density = total_connections / possible_connections
        avg_strength = total_strength / total_connections
        
        return (density * 0.6 + avg_strength * 0.4)
    
    def _calculate_community_activity(self, members: Set[str]) -> float:
        """Calcula nível de atividade de uma comunidade"""
        if not members:
            return 0.0
        
        total_interactions = 0
        recent_cutoff = datetime.now() - timedelta(days=7)
        
        for member in members:
            connections = self.neural_web.get_agent_connections(member)
            for conn in connections:
                if (conn.target_id in members and 
                    conn.last_interaction > recent_cutoff):
                    total_interactions += conn.interaction_count
        
        # Normaliza pela quantidade de membros
        return min(1.0, total_interactions / (len(members) * 10))
    
    def _trend_analysis_phase(self):
        """Fase de análise de tendências emergentes"""
        # Analisa padrões de comportamento da rede
        current_trends = {}
        
        # Tendência de tipos de conexão
        connection_types = {}
        for agent_id in self.social_agents:
            connections = self.neural_web.get_agent_connections(agent_id)
            for conn in connections:
                conn_type = conn.connection_type.value
                connection_types[conn_type] = connection_types.get(conn_type, 0) + 1
        
        total_connections = sum(connection_types.values())
        if total_connections > 0:
            for conn_type, count in connection_types.items():
                current_trends[f"connection_trend_{conn_type}"] = count / total_connections
        
        # Tendência de personalidades
        personality_counts = {}
        for agent in self.social_agents.values():
            personality = agent._get_personality_summary()
            personality_counts[personality] = personality_counts.get(personality, 0) + 1
        
        total_agents = len(self.social_agents)
        if total_agents > 0:
            for personality, count in personality_counts.items():
                current_trends[f"personality_trend_{personality}"] = count / total_agents
        
        # Tendência de atividade social
        total_recent_interactions = 0
        recent_cutoff = datetime.now() - timedelta(hours=1)
        
        for event in self.social_events:
            if event.timestamp > recent_cutoff:
                total_recent_interactions += len(event.participants)
        
        current_trends['social_activity_level'] = min(1.0, total_recent_interactions / max(total_agents, 1))
        
        # Atualiza tendências históricas
        for trend_name, value in current_trends.items():
            if trend_name not in self.trends:
                self.trends[trend_name] = value
            else:
                # Média móvel simples
                self.trends[trend_name] = (self.trends[trend_name] * 0.8 + value * 0.2)
    
    def _record_social_metrics(self):
        """Registra métricas sociais históricas"""
        stats = self.neural_web.get_network_statistics()
        
        social_metrics = {
            'timestamp': datetime.now().isoformat(),
            'network_stats': stats,
            'total_communities': len(self.communities),
            'total_events': len(self.social_events),
            'trends': self.trends.copy(),
            'agent_count': len(self.social_agents)
        }
        
        # Adiciona métricas de comunidades
        if self.communities:
            community_metrics = {
                'avg_community_size': np.mean([len(c.members) for c in self.communities.values()]),
                'avg_cohesion': np.mean([c.cohesion for c in self.communities.values()]),
                'avg_activity': np.mean([c.activity_level for c in self.communities.values()])
            }
            social_metrics['community_metrics'] = community_metrics
        
        self.social_metrics_history.append(social_metrics)
        
        # Limita histórico a últimas 100 entradas
        if len(self.social_metrics_history) > 100:
            self.social_metrics_history = self.social_metrics_history[-100:]
    
    def get_social_network_report(self) -> Dict[str, Any]:
        """Gera relatório completo da rede social"""
        stats = self.neural_web.get_network_statistics()
        
        # Análise de agentes
        agent_analysis = {}
        for agent_id, agent in self.social_agents.items():
            social_summary = agent.get_social_summary()
            agent_analysis[agent_id] = {
                'personality': social_summary['personality'],
                'social_performance': social_summary['performance_metrics'],
                'connections': social_summary['total_connections'],
                'influence_given': social_summary['influences_given'],
                'influence_received': social_summary['influences_received']
            }
        
        # Análise de comunidades
        community_analysis = {}
        for comm_id, community in self.communities.items():
            community_analysis[comm_id] = {
                'size': len(community.members),
                'leader': community.leader,
                'cohesion': community.cohesion,
                'activity_level': community.activity_level,
                'age_days': (datetime.now() - community.formation_date).days,
                'collective_goals': community.collective_goals
            }
        
        # Eventos recentes
        recent_events = []
        recent_cutoff = datetime.now() - timedelta(hours=24)
        for event in self.social_events:
            if event.timestamp > recent_cutoff:
                recent_events.append(event.to_dict())
        
        # Top influenciadores
        top_influencers = []
        for agent_id, agent in self.social_agents.items():
            metrics = self.neural_web.agent_metrics.get(agent_id)
            if metrics:
                top_influencers.append({
                    'agent_id': agent_id,
                    'personality': agent._get_personality_summary(),
                    'influence_score': metrics.influence_score,
                    'centrality': metrics.centrality,
                    'popularity': metrics.popularity
                })
        
        top_influencers.sort(key=lambda x: x['influence_score'], reverse=True)
        top_influencers = top_influencers[:10]
        
        return {
            'timestamp': datetime.now().isoformat(),
            'network_statistics': stats,
            'agent_count': len(self.social_agents),
            'community_count': len(self.communities),
            'recent_events_count': len(recent_events),
            'agent_analysis': agent_analysis,
            'community_analysis': community_analysis,
            'recent_events': recent_events,
            'top_influencers': top_influencers,
            'current_trends': self.trends,
            'metrics_history_length': len(self.social_metrics_history)
        }
    
    def visualize_network(self, save_path: Optional[str] = None):
        """Cria visualização da rede social"""
        try:
            import networkx as nx
            
            # Cria grafo
            G = nx.Graph()
            
            # Adiciona nós
            for agent_id in self.social_agents:
                agent = self.social_agents[agent_id]
                G.add_node(agent_id, 
                          personality=agent._get_personality_summary(),
                          influence=self.neural_web.agent_metrics.get(agent_id, type('obj', (object,), {'influence_score': 0})).influence_score)
            
            # Adiciona arestas
            for agent_id in self.social_agents:
                connections = self.neural_web.get_agent_connections(agent_id)
                for conn in connections:
                    if not G.has_edge(agent_id, conn.target_id):
                        G.add_edge(agent_id, conn.target_id, 
                                 weight=conn.strength,
                                 connection_type=conn.connection_type.value)
            
            # Visualização
            plt.figure(figsize=(15, 10))
            
            # Layout
            pos = nx.spring_layout(G, k=1, iterations=50)
            
            # Desenha nós com cores baseadas na personalidade
            personality_colors = {
                'Especulador Corajoso': 'red',
                'Caçador de Barganha': 'orange', 
                'Artista Inovador': 'purple',
                'Líder Comunitário': 'gold',
                'Seguidor Leal': 'lightblue',
                'Analista Metódico': 'green',
                'Aventureiro Social': 'pink'
            }
            
            node_colors = []
            node_sizes = []
            for node in G.nodes():
                agent = self.social_agents[node]
                personality = agent._get_personality_summary()
                node_colors.append(personality_colors.get(personality, 'gray'))
                
                # Tamanho baseado na influência
                influence = self.neural_web.agent_metrics.get(node, type('obj', (object,), {'influence_score': 0})).influence_score
                node_sizes.append(200 + influence * 800)
            
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
            
            # Desenha arestas com espessura baseada na força
            edges = G.edges()
            edge_weights = [G[u][v]['weight'] for u, v in edges]
            nx.draw_networkx_edges(G, pos, width=[w*3 for w in edge_weights], alpha=0.6, edge_color='gray')
            
            # Labels
            nx.draw_networkx_labels(G, pos, font_size=8)
            
            plt.title("Rede Social Neural - Lore N.A.")
            plt.axis('off')
            
            # Legenda
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                        markerfacecolor=color, markersize=10, label=personality)
                             for personality, color in personality_colors.items()]
            plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Visualização salva em: {save_path}")
            else:
                plt.show()
                
        except ImportError:
            logger.warning("networkx não disponível para visualização")
        except Exception as e:
            logger.error(f"Erro na visualização: {e}")
    
    def save_social_state(self, filepath: str):
        """Salva estado completo da rede social"""
        state_data = {
            'neural_web_state': {
                'connections': {
                    agent_id: [conn.to_dict() for conn in connections]
                    for agent_id, connections in self.neural_web.connections.items()
                },
                'agent_metrics': {
                    agent_id: metrics.to_dict()
                    for agent_id, metrics in self.neural_web.agent_metrics.items()
                }
            },
            'communities': {
                comm_id: community.to_dict()
                for comm_id, community in self.communities.items()
            },
            'social_events': [event.to_dict() for event in self.social_events[-100:]],  # Últimos 100
            'trends': self.trends,
            'social_metrics_history': self.social_metrics_history[-50:],  # Últimos 50
            'saved_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Estado social salvo em: {filepath}")


def main():
    """Função principal para teste do sistema"""
    print("🌐 Social Network Manager - Lore N.A.")
    print("=====================================")
    
    # Configuração inicial
    from neural_web import NeuralWeb
    from population_manager import PopulationManager
    
    # Cria componentes
    neural_web = NeuralWeb()
    population_manager = PopulationManager(max_population=10)
    social_manager = SocialNetworkManager(neural_web, population_manager)
    
    print("\n🧬 Criando população inicial...")
    
    # Cria população de agentes evoluídos
    population_manager.initialize_population()
    
    # Converte para agentes sociais
    social_manager.create_social_agents_from_population()
    
    print(f"✓ {len(social_manager.social_agents)} agentes sociais criados")
    
    print("\n🔄 Simulando evolução social...")
    
    # Simula várias rodadas sociais
    for round_num in range(5):
        print(f"\n--- Rodada Social {round_num + 1} ---")
        social_manager.simulate_social_round()
        
        # Mostra estatísticas básicas
        stats = neural_web.get_network_statistics()
        print(f"  Conexões totais: {stats.get('total_connections', 0)}")
        print(f"  Comunidades: {len(social_manager.communities)}")
        print(f"  Eventos recentes: {len([e for e in social_manager.social_events if (datetime.now() - e.timestamp).seconds < 3600])}")
    
    print("\n📊 Gerando relatório final...")
    
    # Gera relatório completo
    report = social_manager.get_social_network_report()
    
    print(f"\n🌐 Estatísticas Finais da Rede:")
    print(f"  Agentes: {report['agent_count']}")
    print(f"  Conexões: {report['network_statistics'].get('total_connections', 0)}")
    print(f"  Comunidades: {report['community_count']}")
    print(f"  Densidade da rede: {report['network_statistics'].get('network_density', 0):.3f}")
    
    print(f"\n👑 Top 3 Influenciadores:")
    for i, influencer in enumerate(report['top_influencers'][:3]):
        print(f"  {i+1}. {influencer['agent_id']} ({influencer['personality']})")
        print(f"     Influência: {influencer['influence_score']:.3f}")
    
    print(f"\n🏘️ Comunidades Ativas:")
    for comm_id, community in report['community_analysis'].items():
        print(f"  {comm_id}: {community['size']} membros")
        print(f"    Líder: {community['leader']}")
        print(f"    Coesão: {community['cohesion']:.3f}")
        print(f"    Atividade: {community['activity_level']:.3f}")
    
    print(f"\n📈 Tendências Atuais:")
    for trend_name, value in report['current_trends'].items():
        if value > 0.1:  # Só mostra tendências significativas
            print(f"  {trend_name}: {value:.3f}")
    
    print(f"\n💾 Salvando estado...")
    social_manager.save_social_state('/tmp/social_network_state.json')
    
    print(f"\n🎨 Gerando visualização...")
    social_manager.visualize_network('/tmp/social_network_visualization.png')
    
    print("\n✅ Teste do Social Network Manager concluído!")


if __name__ == "__main__":
    main()
