#!/usr/bin/env python3
"""
Social Agent - Lore N.A.
========================

Agente social que combina DNA evolutivo com comportamento de rede neural.
Extende o EvolvedAgent para incluir:
- Participação ativa na Neural Web
- Formação e manutenção de conexões sociais
- Influência e susceptibilidade social
- Comportamento emergente baseado na rede

Autor: Lore N.A. Genesis Team
Data: 2024
"""

import traceback
import logging

# Configuração de logging robusto
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging

from evolved_agent import EvolvedAgent
from neural_web import NeuralWeb, ConnectionType, NeuralConnection
from agent_dna import AgentDNA

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialAgent(EvolvedAgent):
    """Agente social que participa ativamente da Neural Web"""
    
    def __init__(self, agent_id: str, dna: AgentDNA, neural_web: NeuralWeb):
        super().__init__(agent_id, "http://localhost:8000", dna)  # API base URL placeholder
        self.neural_web = neural_web
        self.social_memory: List[Dict] = []
        self.influence_received: List[Dict] = []
        self.influence_given: List[Dict] = []
        self.social_goals: List[str] = []
        self.relationship_preferences: Dict[str, float] = {}
        
        # Use o agent_id da identidade para consistência
        self.agent_id = self.identity.agent_id
        
        # Adiciona agente à rede neural
        self.neural_web.add_agent(self.agent_id)
        
        # Define objetivos sociais baseados no DNA
        self._define_social_goals()
        
        logger.info(f"SocialAgent {self.identity.full_name} '{self.identity.nickname}' inicializado na Neural Web")
        logger.info(f"  Personalidade: {self.identity.personality_archetype}")
        logger.info(f"  Origem: {self.identity.origin}")
        logger.info(f"  Objetivos sociais: {self.social_goals}")
    
    def _define_social_goals(self):
        """Define objetivos sociais baseados no DNA do agente"""
        ritual_genes = self.dna.genes['ritual']
        
        # Goals baseados em genes do universo Ritual
        if ritual_genes['leadership_tendency'] > 0.7:
            self.social_goals.append("become_leader")
        
        if ritual_genes['community_bonding'] > 0.7:
            self.social_goals.append("build_community")
        
        if ritual_genes['influence_susceptibility'] < 0.3:
            self.social_goals.append("maintain_independence")
        
        if ritual_genes['loyalty_factor'] > 0.8:
            self.social_goals.append("form_strong_bonds")
        
        # Goals baseados em outros universos
        odyssey_genes = self.dna.genes['odyssey']
        if odyssey_genes['creativity_drive'] > 0.7:
            self.social_goals.append("inspire_creativity")
        
        limbo_genes = self.dna.genes['limbo']
        if limbo_genes['risk_tolerance'] > 0.7:
            self.social_goals.append("influence_risk_taking")
    
    def discover_potential_connections(self, all_agents: List['SocialAgent']) -> List[Tuple[str, float]]:
        """Descobre potenciais conexões baseado em compatibilidade e objetivos"""
        potential_connections = []
        
        for other_agent in all_agents:
            if other_agent.agent_id == self.agent_id:
                continue
            
            # Verifica se já existe conexão
            existing_connection = self.neural_web.get_connection(self.agent_id, other_agent.agent_id)
            if existing_connection:
                continue
            
            # Calcula score de interesse em conexão
            interest_score = self._calculate_connection_interest(other_agent)
            
            if interest_score > 0.3:  # Threshold mínimo de interesse
                potential_connections.append((other_agent.agent_id, interest_score))
        
        # Ordena por interesse decrescente
        potential_connections.sort(key=lambda x: x[1], reverse=True)
        
        return potential_connections[:5]  # Top 5 candidatos
    
    def _calculate_connection_interest(self, other_agent: 'SocialAgent') -> float:
        """Calcula interesse em formar conexão com outro agente"""
        interest = 0.0
        
        # Compatibilidade genética básica
        compatibility = self.neural_web.calculate_compatibility(
            self.dna.genes, other_agent.dna.genes
        )
        interest += compatibility * 0.4
        
        # Interesse baseado em objetivos sociais
        my_goals = set(self.social_goals)
        other_goals = set(other_agent.social_goals)
        
        # Goals complementares aumentam interesse
        if "become_leader" in my_goals and "form_strong_bonds" in other_goals:
            interest += 0.3
        
        if "build_community" in my_goals and "build_community" in other_goals:
            interest += 0.2
        
        if "inspire_creativity" in my_goals and "maintain_independence" not in other_goals:
            interest += 0.2
        
        # Performance nos universos
        my_performance = self.performance_history[-5:] if hasattr(self, 'performance_history') and self.performance_history else []  # type: ignore
        other_performance = other_agent.performance_history[-5:] if hasattr(other_agent, 'performance_history') and other_agent.performance_history else []  # type: ignore
        
        if my_performance and other_performance:
            # Interesse em agentes com performance similar ou complementar
            my_avg = np.mean([p['total_fitness'] for p in my_performance])
            other_avg = np.mean([p['total_fitness'] for p in other_performance])
            
            fitness_similarity = 1.0 - abs(my_avg - other_avg)
            interest += fitness_similarity * 0.2
        
        # Personalidade
        my_personality = self._get_personality_summary() if hasattr(self, '_get_personality_summary') else {}  # type: ignore
        other_personality = other_agent._get_personality_summary() if hasattr(other_agent, '_get_personality_summary') else {}  # type: ignore
        
        # Algumas personalidades se atraem, outras se repelem
        if (my_personality == "Líder Comunitário" and 
            other_personality in ["Seguidor Leal", "Artista Inovador"]):
            interest += 0.2
        
        if (my_personality == "Artista Inovador" and 
            other_personality in ["Artista Inovador", "Especulador Corajoso"]):
            interest += 0.15
        
        # Adiciona ruído aleatório baseado na personalidade
        chaos_factor = self.dna.genes['odyssey']['experimentation']
        interest += random.uniform(-0.1, 0.1) * chaos_factor
        
        return max(0.0, min(1.0, float(interest)))  # type: ignore
    
    def initiate_connection(self, target_agent_id: str, all_agents: Dict[str, 'SocialAgent']) -> bool:
        """Inicia uma conexão com outro agente"""
        if target_agent_id not in all_agents:
            return False
        
        target_agent = all_agents[target_agent_id]
        
        # Cria conexão na neural web
        connection = self.neural_web.create_connection(
            self.agent_id, target_agent_id,
            self.dna.genes, target_agent.dna.genes
        )
        
        if connection:
            # Registra na memória social
            self.social_memory.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'connection_formed',
                'target': target_agent_id,
                'target_name': all_agents[target_agent_id].identity.full_name if target_agent_id in all_agents else target_agent_id,
                'connection_type': connection.connection_type.value,
                'strength': connection.strength
            })
            
            # Notifica agente alvo
            target_agent._receive_connection_request(self.agent_id, connection.connection_type)
            
            logger.info(f"{self.identity.full_name} iniciou conexão com {all_agents[target_agent_id].identity.full_name if target_agent_id in all_agents else target_agent_id}")
        return True
        
        return False
    
    def _receive_connection_request(self, requester_id: str, connection_type: ConnectionType):
        """Recebe notificação de nova conexão"""
        self.social_memory.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'connection_received',
            'requester': requester_id,
            'connection_type': connection_type.value
        })
    
    def maintain_relationships(self, all_agents: Dict[str, 'SocialAgent']):
        """Mantém relacionamentos existentes através de interações"""
        my_connections = self.neural_web.get_agent_connections(self.agent_id)
        
        for connection in my_connections:
            # Decide se vai interagir baseado na força da conexão e personalidade
            interaction_probability = connection.strength * 0.5
            interaction_probability += self.dna.genes['ritual']['community_bonding'] * 0.3
            
            if random.random() < interaction_probability:
                self._interact_with_connected_agent(connection, all_agents)
    
    def _interact_with_connected_agent(self, connection: NeuralConnection, 
                                     all_agents: Dict[str, 'SocialAgent']):
        """Interage com um agente conectado"""
        target_id = connection.target_id
        
        if target_id not in all_agents:
            return
        
        target_agent = all_agents[target_id]
        
        # Escolhe tipo de interação baseado no tipo de conexão
        interaction_type = self._choose_interaction_type(connection.connection_type)
        
        # Dados da interação
        interaction_data = {
            'initiator_personality': self._get_personality_summary() if hasattr(self, '_get_personality_summary') else {},  # type: ignore
            'target_personality': target_agent._get_personality_summary() if hasattr(target_agent, '_get_personality_summary') else {},  # type: ignore
            'success': random.random() < 0.7  # 70% de sucesso base
        }
        
        # Modifica chance de sucesso baseado na compatibilidade
        compatibility = self.neural_web.calculate_compatibility(
            self.dna.genes, target_agent.dna.genes
        )
        interaction_data['success'] = random.random() < (0.5 + compatibility * 0.4)
        
        # Executa interação
        success = self.neural_web.interact_agents(
            self.agent_id, target_id, interaction_type, interaction_data
        )
        
        if success:
            # Registra na memória
            self.social_memory.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'interaction',
                'target': target_id,
                'type': interaction_type,
                'success': interaction_data['success']
            })
            
            # Processa resultado da interação
            self._process_interaction_result(connection, interaction_type, interaction_data)
    
    def _choose_interaction_type(self, connection_type: ConnectionType) -> str:
        """Escolhe tipo de interação baseado no tipo de conexão"""
        interaction_map = {
            ConnectionType.MENTOR: ['mentoring', 'advice_giving', 'guidance'],
            ConnectionType.COLLABORATOR: ['collaboration', 'information_sharing', 'joint_planning'],
            ConnectionType.FRIEND: ['casual_chat', 'emotional_support', 'shared_activity'],
            ConnectionType.COMPETITOR: ['competitive_challenge', 'performance_comparison', 'rivalry'],
            ConnectionType.INFLUENCER: ['influence_attempt', 'trend_sharing', 'opinion_leadership'],
            ConnectionType.FOLLOWER: ['seeking_guidance', 'mimicking_behavior', 'approval_seeking'],
            ConnectionType.ENEMY: ['conflict', 'confrontation', 'undermining']
        }
        
        possible_interactions = interaction_map.get(connection_type, ['generic_interaction'])
        return random.choice(possible_interactions)
    
    def _process_interaction_result(self, connection: NeuralConnection, 
                                  interaction_type: str, interaction_data: Dict):
        """Processa resultado de uma interação"""
        success = interaction_data['success']
        
        # Influência baseada no tipo de conexão e sucesso da interação
        if connection.connection_type == ConnectionType.MENTOR and success:
            self._receive_mentoring_influence(connection, interaction_data)
        
        elif connection.connection_type == ConnectionType.INFLUENCER and success:
            self._receive_social_influence(connection, interaction_data)
        
        elif interaction_type == 'collaboration' and success:
            self._gain_collaboration_benefits(connection, interaction_data)
        
        # Atualiza preferências de relacionamento
        self._update_relationship_preferences(connection, success)
    
    def _receive_mentoring_influence(self, connection: NeuralConnection, interaction_data: Dict):
        """Recebe influência de mentoring"""
        # Mentoring pode melhorar performance em universos específicos
        influence_strength = connection.strength * 0.1
        
        # Registra influência recebida
        self.influence_received.append({
            'timestamp': datetime.now().isoformat(),
            'source': connection.target_id,
            'type': 'mentoring',
            'strength': influence_strength,
            'data': interaction_data
        })
        
        # Pequeno boost temporário na performance
        if hasattr(self, 'current_state') and self.current_state:  # type: ignore
            for universe in self.current_state:  # type: ignore
                if random.random() < influence_strength:
                    self.current_state[universe] = min(1.0, self.current_state[universe] + 0.05)  # type: ignore
    
    def _receive_social_influence(self, connection: NeuralConnection, interaction_data: Dict):
        """Recebe influência social"""
        # Influência social pode afetar decisões futuras
        influence_strength = connection.strength * self.dna.genes['ritual']['influence_susceptibility']
        
        self.influence_received.append({
            'timestamp': datetime.now().isoformat(),
            'source': connection.target_id,
            'type': 'social_influence',
            'strength': influence_strength,
            'data': interaction_data
        })
        
        # Modifica temporariamente alguns genes (epigenética social)
        if influence_strength > 0.3:
            ritual_genes = self.dna.genes['ritual']
            for gene in ['community_bonding', 'loyalty_factor']:
                current_value = ritual_genes[gene]
                influence_direction = random.choice([-1, 1])
                change = influence_strength * 0.1 * influence_direction
                ritual_genes[gene] = max(0.0, min(1.0, current_value + change))
    
    def _gain_collaboration_benefits(self, connection: NeuralConnection, interaction_data: Dict):
        """Ganha benefícios de colaboração"""
        # Colaboração pode melhorar fitness através de sinergia
        benefit_strength = connection.strength * 0.05
        
        # Melhora temporária na performance
        if hasattr(self, 'add_performance_bonus'):
            self.add_performance_bonus('collaboration', benefit_strength)  # type: ignore
        
        # Registra colaboração
        self.social_memory.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'collaboration_benefit',
            'partner': connection.target_id,
            'benefit': benefit_strength
        })
    
    def _update_relationship_preferences(self, connection: NeuralConnection, success: bool):
        """Atualiza preferências de relacionamento baseado em experiências"""
        connection_type = connection.connection_type.value
        
        if connection_type not in self.relationship_preferences:
            self.relationship_preferences[connection_type] = 0.5
        
        # Atualiza preferência baseado no sucesso
        change = 0.05 if success else -0.05
        self.relationship_preferences[connection_type] = max(0.0, min(1.0, 
            self.relationship_preferences[connection_type] + change))
    
    def seek_new_connections(self, all_agents: Dict[str, 'SocialAgent'], max_new_connections: int = 2):
        """Busca ativamente por novas conexões"""
        # Probabilidade de buscar conexões baseada na personalidade
        seek_probability = self.dna.genes['ritual']['community_bonding'] * 0.5
        seek_probability += self.dna.genes['odyssey']['experimentation'] * 0.3
        
        if random.random() > seek_probability:
            return
        
        # Descobre potenciais conexões
        potential_connections = self.discover_potential_connections(list(all_agents.values()))
        
        # Inicia conexões com os melhores candidatos
        new_connections_count = 0
        for target_id, interest_score in potential_connections:
            if new_connections_count >= max_new_connections:
                break
            
            # Decide se vai iniciar conexão baseado no interesse e personalidade
            if random.random() < interest_score:
                if self.initiate_connection(target_id, all_agents):
                    new_connections_count += 1
    
    def influence_network(self, all_agents: Dict[str, 'SocialAgent']):
        """Tenta influenciar sua rede de conexões"""
        # Só agentes com alto leadership_tendency tentam influenciar ativamente
        leadership = self.dna.genes['ritual']['leadership_tendency']
        
        if leadership < 0.5:
            return
        
        my_connections = self.neural_web.get_agent_connections(self.agent_id)
        influence_targets = [conn for conn in my_connections 
                           if conn.connection_type in [ConnectionType.FOLLOWER, ConnectionType.FRIEND]]
        
        for connection in influence_targets:
            if random.random() < leadership * 0.3:
                self._attempt_influence(connection, all_agents)
    
    def _attempt_influence(self, connection: NeuralConnection, all_agents: Dict[str, 'SocialAgent']):
        """Tenta influenciar um agente específico"""
        target_id = connection.target_id
        
        if target_id not in all_agents:
            return
        
        target_agent = all_agents[target_id]
        
        # Força da influência baseada na conexão e características do influenciador
        influence_power = connection.strength * self.dna.genes['ritual']['leadership_tendency']
        
        # Resistência do alvo
        target_resistance = target_agent.dna.genes['ritual']['influence_susceptibility']
        
        # Sucesso da influência
        influence_success = influence_power > target_resistance * random.uniform(0.8, 1.2)
        
        if influence_success:
            # Registra influência dada
            self.influence_given.append({
                'timestamp': datetime.now().isoformat(),
                'target': target_id,
                'type': 'leadership_influence',
                'success': True
            })
            
            # Alvo recebe a influência
            target_agent._receive_leadership_influence(self.agent_id, influence_power)
    
    def _receive_leadership_influence(self, leader_id: str, influence_power: float):
        """Recebe influência de liderança"""
        # Registra influência recebida
        self.influence_received.append({
            'timestamp': datetime.now().isoformat(),
            'source': leader_id,
            'type': 'leadership_influence',
            'power': influence_power
        })
        
        # Pode afetar decisões futuras ou comportamento
        if influence_power > 0.3:
            # Pequeno boost temporário em loyalty_factor
            ritual_genes = self.dna.genes['ritual']
            ritual_genes['loyalty_factor'] = min(1.0, ritual_genes['loyalty_factor'] + 0.05)
    
    def evaluate_social_performance(self) -> Dict[str, float]:
        """Avalia performance social do agente"""
        metrics = self.neural_web.agent_metrics.get(self.agent_id)
        if not metrics:
            return {}
        
        # Métricas básicas da rede
        social_metrics = {
            'network_centrality': metrics.centrality,
            'influence_score': metrics.influence_score,
            'popularity': metrics.popularity,
            'trust_rating': metrics.trust_rating,
            'community_standing': metrics.community_standing
        }
        
        # Métricas derivadas
        my_connections = self.neural_web.get_agent_connections(self.agent_id)
        
        social_metrics['total_connections'] = len(my_connections)
        social_metrics['average_connection_strength'] = (
            sum(conn.strength for conn in my_connections) / max(len(my_connections), 1)
        )
        
        # Score de diversidade de conexões
        connection_types = set(conn.connection_type for conn in my_connections)
        social_metrics['connection_diversity'] = len(connection_types) / len(ConnectionType)
        
        # Efetividade das influências
        successful_influences = len([inf for inf in self.influence_given 
                                   if inf.get('success', False)])
        total_influences = len(self.influence_given)
        social_metrics['influence_effectiveness'] = (
            successful_influences / max(total_influences, 1)
        )
        
        # Resistência social (low influence_received vs high independence)
        independence_gene = 1.0 - self.dna.genes['ritual']['influence_susceptibility']
        influences_received = len(self.influence_received)
        social_metrics['social_resistance'] = independence_gene / max(influences_received * 0.1, 1)
        
        return social_metrics
    
    def get_social_summary(self) -> Dict[str, Any]:
        """Retorna resumo da vida social do agente"""
        social_perf = self.evaluate_social_performance()
        my_connections = self.neural_web.get_agent_connections(self.agent_id)
        
        # Analisa tipos de conexão
        connection_breakdown = {}
        for conn in my_connections:
            conn_type = conn.connection_type.value
            connection_breakdown[conn_type] = connection_breakdown.get(conn_type, 0) + 1
        
        # Relacionamentos mais fortes
        strongest_connections = sorted(my_connections, key=lambda x: x.strength, reverse=True)[:3]
        
        # Memórias sociais recentes
        recent_memories = self.social_memory[-10:] if self.social_memory else []
        
        return {
            'agent_id': self.agent_id,
            'identity': self.get_identity_summary(),
            'personality': self.identity.personality_archetype,
            'social_goals': self.social_goals,
            'performance_metrics': social_perf,
            'total_connections': len(my_connections),
            'connection_breakdown': connection_breakdown,
            'strongest_connections': [
                {
                    'target': conn.target_id,
                    'type': conn.connection_type.value,
                    'strength': conn.strength
                }
                for conn in strongest_connections
            ],
            'recent_social_memories': recent_memories,
            'influences_given': len(self.influence_given),
            'influences_received': len(self.influence_received),
            'relationship_preferences': self.relationship_preferences
        }


def main():
    """Função principal para teste do SocialAgent"""
    print("👥 Social Agent System - Lore N.A.")
    print("==================================")
    
    # Cria neural web
    neural_web = NeuralWeb()
    
    # Cria agentes sociais de teste
    print("\n🧬 Criando agentes sociais...")
    
    from agent_dna import AgentDNA
    
    agents = {}
    for i in range(5):
        # Gera DNA aleatório
        dna = AgentDNA.generate_random()
        agent_id = f"social_agent_{i+1:03d}"
        
        # Cria agente social
        agent = SocialAgent(agent_id, dna, neural_web)
        agents[agent_id] = agent
        
        print(f"  ✓ {agent_id} criado:")
        print(f"     Nome: {agent.identity.full_name} '{agent.identity.nickname}'")
        print(f"     Título: {agent.identity.title}")
        print(f"     Origem: {agent.identity.origin}")
        print(f"     Personalidade: {agent.identity.personality_archetype}")
    
    print(f"\n🌐 {len(agents)} agentes sociais criados!")
    
    # Simula algumas rodadas de interação social
    print("\n🔄 Simulando interações sociais...")
    
    for round_num in range(3):
        print(f"\n--- Rodada {round_num + 1} ---")
        
        for agent in agents.values():
            # Busca novas conexões
            agent.seek_new_connections(agents, max_new_connections=1)
            
            # Mantém relacionamentos existentes
            agent.maintain_relationships(agents)
            
            # Tenta influenciar rede (se for líder)
            agent.influence_network(agents)
        
        # Atualiza métricas sociais
        neural_web.update_social_metrics()
    
    print("\n📊 Analisando resultados sociais...")
    
    # Mostra estatísticas da rede
    print("\n🌐 Estatísticas da Neural Web:")
    stats = neural_web.get_network_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Mostra resumo social de cada agente
    print("\n👤 Resumos Sociais dos Agentes:")
    for agent_id, agent in agents.items():
        summary = agent.get_social_summary()
        identity = summary['identity']
        print(f"\n  {identity['full_name']} '{identity['nickname']}' ({identity['personality']}):")
        print(f"    ID: {agent_id}")
        print(f"    Origem: {identity['origin']}")
        print(f"    Conexões: {summary['total_connections']}")
        print(f"    Influência: {summary['performance_metrics'].get('influence_score', 0):.3f}")
        print(f"    Centralidade: {summary['performance_metrics'].get('network_centrality', 0):.3f}")
        print(f"    Influências dadas: {summary['influences_given']}")
        print(f"    Influências recebidas: {summary['influences_received']}")
        
        if summary['strongest_connections']:
            print(f"    Conexão mais forte: {summary['strongest_connections'][0]['target']} "
                  f"({summary['strongest_connections'][0]['type']}, "
                  f"força: {summary['strongest_connections'][0]['strength']:.2f})")
    
    print("\n✅ Teste do Social Agent System concluído!")


if __name__ == "__main__":
    main()
