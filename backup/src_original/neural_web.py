#!/usr/bin/env python3
"""
Neural Web System - Lore N.A.
============================

Sistema de rede social neural entre agentes evoluídos.
Permite conexões dinâmicas, influência mútua e formação de comunidades baseadas em:
- Compatibilidade genética
- Interesses compartilhados
- Performance nos 5 universos
- Personalidades emergentes

Autor: Lore N.A. Genesis Team
Data: 2024
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionType(Enum):
    """Tipos de conexão neural entre agentes"""
    MENTOR = "mentor"           # Relação mentor-aprendiz
    COMPETITOR = "competitor"   # Rivalidade saudável
    COLLABORATOR = "collaborator"  # Parceria produtiva
    INFLUENCER = "influencer"   # Relação de influência
    FOLLOWER = "follower"       # Seguidor de tendências
    FRIEND = "friend"           # Amizade casual
    ENEMY = "enemy"             # Conflito/antagonismo


@dataclass
class NeuralConnection:
    """Representa uma conexão neural entre dois agentes"""
    agent_id: str
    target_id: str
    connection_type: ConnectionType
    strength: float  # 0.0 a 1.0
    created_at: datetime
    last_interaction: datetime
    interaction_count: int = 0
    shared_experiences: List[str] = field(default_factory=list)
    influence_history: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Converte conexão para dicionário"""
        return {
            'agent_id': self.agent_id,
            'target_id': self.target_id,
            'connection_type': self.connection_type.value,
            'strength': self.strength,
            'created_at': self.created_at.isoformat(),
            'last_interaction': self.last_interaction.isoformat(),
            'interaction_count': self.interaction_count,
            'shared_experiences': self.shared_experiences,
            'influence_history': self.influence_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'NeuralConnection':
        """Cria conexão a partir de dicionário"""
        return cls(
            agent_id=data['agent_id'],
            target_id=data['target_id'],
            connection_type=ConnectionType(data['connection_type']),
            strength=data['strength'],
            created_at=datetime.fromisoformat(data['created_at']),
            last_interaction=datetime.fromisoformat(data['last_interaction']),
            interaction_count=data.get('interaction_count', 0),
            shared_experiences=data.get('shared_experiences', []),
            influence_history=data.get('influence_history', [])
        )


@dataclass
class SocialMetrics:
    """Métricas sociais de um agente na rede neural"""
    centrality: float = 0.0        # Centralidade na rede
    influence_score: float = 0.0   # Poder de influência
    popularity: float = 0.0        # Popularidade geral
    trust_rating: float = 0.0      # Confiabilidade
    community_standing: float = 0.0  # Posição na comunidade
    
    def to_dict(self) -> Dict:
        return {
            'centrality': self.centrality,
            'influence_score': self.influence_score,
            'popularity': self.popularity,
            'trust_rating': self.trust_rating,
            'community_standing': self.community_standing
        }


class NeuralWeb:
    """Sistema de rede social neural para agentes evoluídos"""
    
    def __init__(self):
        self.connections: Dict[str, List[NeuralConnection]] = {}
        self.agent_metrics: Dict[str, SocialMetrics] = {}
        self.communities: Dict[str, Set[str]] = {}
        self.influence_events: List[Dict] = []
        self.social_graph = {}
        
    def add_agent(self, agent_id: str, initial_metrics: Optional[SocialMetrics] = None):
        """Adiciona um agente à rede neural"""
        if agent_id not in self.connections:
            self.connections[agent_id] = []
            self.agent_metrics[agent_id] = initial_metrics or SocialMetrics()
            logger.info(f"Agente {agent_id} adicionado à Neural Web")
    
    def calculate_compatibility(self, agent1_dna: Dict, agent2_dna: Dict) -> float:
        """Calcula compatibilidade genética entre dois agentes"""
        compatibility = 0.0
        gene_count = 0
        
        for universe in ['limbo', 'odyssey', 'ritual', 'engine', 'logs']:
            if universe in agent1_dna and universe in agent2_dna:
                genes1 = agent1_dna[universe]
                genes2 = agent2_dna[universe]
                
                for gene_name in genes1:
                    if gene_name in genes2:
                        # Compatibilidade baseada na similaridade dos genes
                        diff = abs(genes1[gene_name] - genes2[gene_name])
                        compatibility += (1.0 - diff)
                        gene_count += 1
        
        return compatibility / max(gene_count, 1)
    
    def create_connection(self, agent_id: str, target_id: str, 
                         agent_dna: Dict, target_dna: Dict,
                         connection_type: Optional[ConnectionType] = None) -> Optional[NeuralConnection]:
        """Cria uma conexão neural entre dois agentes"""
        if agent_id == target_id:
            return None
            
        # Adiciona agentes se não existirem
        self.add_agent(agent_id)
        self.add_agent(target_id)
        
        # Calcula compatibilidade
        compatibility = self.calculate_compatibility(agent_dna, target_dna)
        
        # Determina tipo de conexão se não especificado
        if connection_type is None:
            connection_type = self._determine_connection_type(agent_dna, target_dna, compatibility)
        
        # Calcula força da conexão
        strength = self._calculate_connection_strength(agent_dna, target_dna, compatibility, connection_type)
        
        # Cria conexão
        connection = NeuralConnection(
            agent_id=agent_id,
            target_id=target_id,
            connection_type=connection_type,
            strength=strength,
            created_at=datetime.now(),
            last_interaction=datetime.now()
        )
        
        self.connections[agent_id].append(connection)
        
        # Cria conexão recíproca com tipo apropriado
        reciprocal_type = self._get_reciprocal_type(connection_type)
        reciprocal_connection = NeuralConnection(
            agent_id=target_id,
            target_id=agent_id,
            connection_type=reciprocal_type,
            strength=strength,
            created_at=datetime.now(),
            last_interaction=datetime.now()
        )
        
        self.connections[target_id].append(reciprocal_connection)
        
        logger.info(f"Conexão criada: {agent_id} -> {target_id} ({connection_type.value}, força: {strength:.2f})")
        return connection
    
    def _determine_connection_type(self, agent_dna: Dict, target_dna: Dict, compatibility: float) -> ConnectionType:
        """Determina o tipo de conexão baseado nos DNAs dos agentes"""
        # Extrai personalidades dos DNAs
        agent_personality = self._extract_personality_traits(agent_dna)
        target_personality = self._extract_personality_traits(target_dna)
        
        # Lógica de determinação baseada em personalidades e compatibilidade
        if compatibility > 0.8:
            if agent_personality.get('leadership_tendency', 0) > target_personality.get('leadership_tendency', 0):
                return ConnectionType.MENTOR
            else:
                return ConnectionType.COLLABORATOR
        
        elif compatibility > 0.6:
            return ConnectionType.FRIEND
        
        elif compatibility > 0.4:
            if agent_personality.get('competitiveness', 0) > 0.7:
                return ConnectionType.COMPETITOR
            else:
                return ConnectionType.FOLLOWER
        
        else:
            if random.random() < 0.3:  # 30% chance de criar inimigo
                return ConnectionType.ENEMY
            else:
                return ConnectionType.COMPETITOR
    
    def _extract_personality_traits(self, dna: Dict) -> Dict[str, float]:
        """Extrai traços de personalidade do DNA"""
        traits = {}
        
        # Extrai genes relevantes de cada universo
        for universe, genes in dna.items():
            if universe == 'ritual':
                traits['leadership_tendency'] = genes.get('leadership_tendency', 0.5)
                traits['community_bonding'] = genes.get('community_bonding', 0.5)
                traits['influence_susceptibility'] = genes.get('influence_susceptibility', 0.5)
            
            elif universe == 'limbo':
                traits['competitiveness'] = genes.get('risk_tolerance', 0.5)
                traits['ambition'] = genes.get('quality_preference', 0.5)
            
            elif universe == 'odyssey':
                traits['creativity'] = genes.get('creativity_drive', 0.5)
                traits['innovation'] = genes.get('experimentation', 0.5)
        
        return traits
    
    def _calculate_connection_strength(self, agent_dna: Dict, target_dna: Dict, 
                                     compatibility: float, connection_type: ConnectionType) -> float:
        """Calcula a força da conexão baseada em múltiplos fatores"""
        base_strength = compatibility
        
        # Modifica força baseada no tipo de conexão
        type_modifiers = {
            ConnectionType.MENTOR: 0.8,
            ConnectionType.COLLABORATOR: 0.9,
            ConnectionType.FRIEND: 0.7,
            ConnectionType.INFLUENCER: 0.6,
            ConnectionType.FOLLOWER: 0.5,
            ConnectionType.COMPETITOR: 0.4,
            ConnectionType.ENEMY: 0.2
        }
        
        strength = base_strength * type_modifiers.get(connection_type, 0.5)
        
        # Adiciona ruído aleatório
        strength += random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, strength))
    
    def _get_reciprocal_type(self, connection_type: ConnectionType) -> ConnectionType:
        """Retorna o tipo de conexão recíproca"""
        reciprocal_map = {
            ConnectionType.MENTOR: ConnectionType.FOLLOWER,
            ConnectionType.COLLABORATOR: ConnectionType.COLLABORATOR,
            ConnectionType.FRIEND: ConnectionType.FRIEND,
            ConnectionType.INFLUENCER: ConnectionType.FOLLOWER,
            ConnectionType.FOLLOWER: ConnectionType.INFLUENCER,
            ConnectionType.COMPETITOR: ConnectionType.COMPETITOR,
            ConnectionType.ENEMY: ConnectionType.ENEMY
        }
        
        return reciprocal_map.get(connection_type, ConnectionType.FRIEND)
    
    def interact_agents(self, agent_id: str, target_id: str, interaction_type: str, 
                       interaction_data: Dict) -> bool:
        """Simula uma interação entre dois agentes conectados"""
        # Encontra conexão
        connection = self.get_connection(agent_id, target_id)
        if not connection:
            return False
        
        # Atualiza conexão
        connection.last_interaction = datetime.now()
        connection.interaction_count += 1
        connection.shared_experiences.append(f"{interaction_type}:{datetime.now().isoformat()}")
        
        # Registra evento de influência
        influence_event = {
            'timestamp': datetime.now().isoformat(),
            'agent_id': agent_id,
            'target_id': target_id,
            'interaction_type': interaction_type,
            'connection_strength': connection.strength,
            'data': interaction_data
        }
        
        self.influence_events.append(influence_event)
        connection.influence_history.append(influence_event)
        
        # Modifica força da conexão baseada na interação
        self._update_connection_strength(connection, interaction_type, interaction_data)
        
        logger.info(f"Interação: {agent_id} -> {target_id} ({interaction_type})")
        return True
    
    def _update_connection_strength(self, connection: NeuralConnection, 
                                  interaction_type: str, interaction_data: Dict):
        """Atualiza a força da conexão baseada na interação"""
        strength_change = 0.0
        
        # Diferentes tipos de interação afetam a força de forma diferente
        if interaction_type == 'positive_feedback':
            strength_change = 0.05
        elif interaction_type == 'negative_feedback':
            strength_change = -0.05
        elif interaction_type == 'collaboration':
            strength_change = 0.03
        elif interaction_type == 'conflict':
            strength_change = -0.08
        elif interaction_type == 'trade':
            success = interaction_data.get('success', True)
            strength_change = 0.02 if success else -0.02
        
        # Aplica mudança
        connection.strength = max(0.0, min(1.0, connection.strength + strength_change))
    
    def get_connection(self, agent_id: str, target_id: str) -> Optional[NeuralConnection]:
        """Busca conexão entre dois agentes"""
        if agent_id not in self.connections:
            return None
        
        for connection in self.connections[agent_id]:
            if connection.target_id == target_id:
                return connection
        
        return None
    
    def get_agent_connections(self, agent_id: str) -> List[NeuralConnection]:
        """Retorna todas as conexões de um agente"""
        return self.connections.get(agent_id, [])
    
    def calculate_influence_network(self, agent_id: str, max_depth: int = 3) -> Dict[str, float]:
        """Calcula rede de influência de um agente até determinada profundidade"""
        influence_map = {}
        visited = set()
        
        def explore_influence(current_agent: str, depth: int, current_influence: float):
            if depth <= 0 or current_agent in visited:
                return
            
            visited.add(current_agent)
            influence_map[current_agent] = current_influence
            
            # Explora conexões do agente atual
            for connection in self.get_agent_connections(current_agent):
                if connection.connection_type in [ConnectionType.INFLUENCER, ConnectionType.MENTOR]:
                    new_influence = current_influence * connection.strength * 0.8
                    if new_influence > 0.1:  # Threshold mínimo de influência
                        explore_influence(connection.target_id, depth - 1, new_influence)
        
        explore_influence(agent_id, max_depth, 1.0)
        return influence_map
    
    def detect_communities(self) -> Dict[str, Set[str]]:
        """Detecta comunidades na rede neural usando algoritmo simples"""
        communities = {}
        visited = set()
        community_id = 0
        
        for agent_id in self.connections:
            if agent_id not in visited:
                community = self._explore_community(agent_id, visited)
                if len(community) > 1:  # Comunidade deve ter pelo menos 2 membros
                    communities[f"community_{community_id}"] = community
                    community_id += 1
        
        self.communities = communities
        return communities
    
    def _explore_community(self, start_agent: str, visited: Set[str]) -> Set[str]:
        """Explora uma comunidade a partir de um agente"""
        community = set()
        stack = [start_agent]
        
        while stack:
            current_agent = stack.pop()
            if current_agent in visited:
                continue
            
            visited.add(current_agent)
            community.add(current_agent)
            
            # Adiciona agentes conectados com força suficiente
            for connection in self.get_agent_connections(current_agent):
                if (connection.strength > 0.5 and 
                    connection.target_id not in visited and
                    connection.connection_type not in [ConnectionType.ENEMY]):
                    stack.append(connection.target_id)
        
        return community
    
    def update_social_metrics(self):
        """Atualiza métricas sociais de todos os agentes"""
        for agent_id in self.connections:
            metrics = self.agent_metrics[agent_id]
            
            # Calcula centralidade (baseado no número e força das conexões)
            connections = self.get_agent_connections(agent_id)
            metrics.centrality = sum(conn.strength for conn in connections) / max(len(connections), 1)
            
            # Calcula score de influência
            influence_connections = [conn for conn in connections 
                                   if conn.connection_type in [ConnectionType.INFLUENCER, ConnectionType.MENTOR]]
            metrics.influence_score = sum(conn.strength for conn in influence_connections)
            
            # Calcula popularidade (baseado em conexões de entrada)
            incoming_connections = []
            for other_agent in self.connections:
                for conn in self.connections[other_agent]:
                    if conn.target_id == agent_id:
                        incoming_connections.append(conn)
            
            metrics.popularity = len(incoming_connections) / max(len(self.connections), 1)
            
            # Calcula confiabilidade (baseado no histórico de interações)
            positive_interactions = 0
            total_interactions = 0
            
            for conn in connections:
                total_interactions += conn.interaction_count
                # Simula interações positivas baseado na força da conexão
                positive_interactions += conn.interaction_count * conn.strength
            
            metrics.trust_rating = positive_interactions / max(total_interactions, 1)
            
            # Calcula posição na comunidade
            agent_communities = [comm_id for comm_id, members in self.communities.items() 
                               if agent_id in members]
            
            if agent_communities:
                # Score baseado no tamanho da maior comunidade
                largest_community = max(agent_communities, 
                                      key=lambda x: len(self.communities[x]))
                metrics.community_standing = len(self.communities[largest_community]) / len(self.connections)
            else:
                metrics.community_standing = 0.0
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais da rede neural"""
        total_agents = len(self.connections)
        total_connections = sum(len(conns) for conns in self.connections.values())
        
        if total_agents == 0:
            return {'error': 'Nenhum agente na rede'}
        
        # Distribição de tipos de conexão
        connection_types = {}
        for connections in self.connections.values():
            for conn in connections:
                conn_type = conn.connection_type.value
                connection_types[conn_type] = connection_types.get(conn_type, 0) + 1
        
        # Força média das conexões
        all_strengths = []
        for connections in self.connections.values():
            all_strengths.extend([conn.strength for conn in connections])
        
        avg_strength = sum(all_strengths) / len(all_strengths) if all_strengths else 0
        
        # Detecta comunidades
        communities = self.detect_communities()
        
        return {
            'total_agents': total_agents,
            'total_connections': total_connections,
            'average_connections_per_agent': total_connections / total_agents,
            'average_connection_strength': avg_strength,
            'connection_types_distribution': connection_types,
            'total_communities': len(communities),
            'largest_community_size': max([len(members) for members in communities.values()]) if communities else 0,
            'network_density': total_connections / (total_agents * (total_agents - 1)) if total_agents > 1 else 0
        }
    
    def save_to_file(self, filepath: str):
        """Salva estado da rede neural em arquivo JSON"""
        data = {
            'connections': {
                agent_id: [conn.to_dict() for conn in connections]
                for agent_id, connections in self.connections.items()
            },
            'agent_metrics': {
                agent_id: metrics.to_dict()
                for agent_id, metrics in self.agent_metrics.items()
            },
            'communities': {
                comm_id: list(members)
                for comm_id, members in self.communities.items()
            },
            'influence_events': self.influence_events[-1000:],  # Últimos 1000 eventos
            'saved_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Neural Web salva em: {filepath}")
    
    def load_from_file(self, filepath: str):
        """Carrega estado da rede neural de arquivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Reconstrói conexões
            self.connections = {}
            for agent_id, conn_list in data['connections'].items():
                self.connections[agent_id] = [
                    NeuralConnection.from_dict(conn_data) 
                    for conn_data in conn_list
                ]
            
            # Reconstrói métricas
            self.agent_metrics = {}
            for agent_id, metrics_data in data['agent_metrics'].items():
                metrics = SocialMetrics()
                for key, value in metrics_data.items():
                    setattr(metrics, key, value)
                self.agent_metrics[agent_id] = metrics
            
            # Reconstrói comunidades
            self.communities = {
                comm_id: set(members)
                for comm_id, members in data['communities'].items()
            }
            
            # Reconstrói eventos de influência
            self.influence_events = data.get('influence_events', [])
            
            logger.info(f"Neural Web carregada de: {filepath}")
            
        except Exception as e:
            logger.error(f"Erro ao carregar Neural Web: {e}")
            raise


def main():
    """Função principal para teste do sistema"""
    print("🧠 Neural Web System - Lore N.A.")
    print("================================")
    
    # Cria instância da rede neural
    neural_web = NeuralWeb()
    
    # Dados de teste - DNAs simplificados
    test_agents = {
        'agent_001': {
            'limbo': {'risk_tolerance': 0.8, 'quality_preference': 0.6},
            'ritual': {'leadership_tendency': 0.9, 'community_bonding': 0.7},
            'odyssey': {'creativity_drive': 0.5, 'experimentation': 0.4}
        },
        'agent_002': {
            'limbo': {'risk_tolerance': 0.3, 'quality_preference': 0.9},
            'ritual': {'leadership_tendency': 0.2, 'community_bonding': 0.8},
            'odyssey': {'creativity_drive': 0.8, 'experimentation': 0.9}
        },
        'agent_003': {
            'limbo': {'risk_tolerance': 0.6, 'quality_preference': 0.7},
            'ritual': {'leadership_tendency': 0.7, 'community_bonding': 0.6},
            'odyssey': {'creativity_drive': 0.6, 'experimentation': 0.5}
        }
    }
    
    print("\n📊 Criando conexões neurais...")
    
    # Cria conexões entre agentes
    agents = list(test_agents.keys())
    for i, agent1 in enumerate(agents):
        for agent2 in agents[i+1:]:
            neural_web.create_connection(
                agent1, agent2,
                test_agents[agent1], test_agents[agent2]
            )
    
    print("\n🔄 Simulando interações...")
    
    # Simula algumas interações
    interactions = [
        ('agent_001', 'agent_002', 'collaboration', {'success': True}),
        ('agent_002', 'agent_003', 'trade', {'success': True}),
        ('agent_001', 'agent_003', 'positive_feedback', {}),
        ('agent_003', 'agent_001', 'negative_feedback', {}),
    ]
    
    for agent_id, target_id, interaction_type, data in interactions:
        neural_web.interact_agents(agent_id, target_id, interaction_type, data)
    
    print("\n📈 Atualizando métricas sociais...")
    neural_web.update_social_metrics()
    
    print("\n🌐 Estatísticas da Rede Neural:")
    stats = neural_web.get_network_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n👥 Métricas Sociais dos Agentes:")
    for agent_id, metrics in neural_web.agent_metrics.items():
        print(f"\n  {agent_id}:")
        for metric, value in metrics.to_dict().items():
            print(f"    {metric}: {value:.3f}")
    
    print("\n🔗 Conexões Ativas:")
    for agent_id in neural_web.connections:
        connections = neural_web.get_agent_connections(agent_id)
        print(f"\n  {agent_id}:")
        for conn in connections:
            print(f"    -> {conn.target_id} ({conn.connection_type.value}, força: {conn.strength:.2f})")
    
    print("\n💾 Salvando estado da rede...")
    neural_web.save_to_file('/tmp/neural_web_test.json')
    
    print("\n✅ Teste do Neural Web System concluído!")


if __name__ == "__main__":
    main()
