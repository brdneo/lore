#!/usr/bin/env python3
"""
Evolved Agent - Genesis Protocol Implementation
Agente neural evoluído que utiliza DNA digital para tomada de decisões nos 5 universos

Este agente representa a evolução do projeto Lore N.A., incorporando:
- Sistema de DNA digital com genes dos 5 universos
- Tomada de decisão influenciada pela genética
- Capacidade de evolução e reprodução
- Performance tracking para cálculo de fitness

Autor: Lore N.A. Genesis Protocol
Data: 26 de Junho de 2025
"""

import asyncio
import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from base_agent import BaseAgent
from agent_dna import AgentDNA, GeneticTraits
from sentiment_service import SentimentService, ConsumptionContext

logger = logging.getLogger(__name__)

class EvolvedAgent(BaseAgent):
    """
    Agente Neural Evoluído com DNA Digital
    
    Implementa comportamento complexo baseado em genes dos 5 universos:
    - Limbo: Comportamento de mercado e compras
    - Odyssey: Criatividade e personalização
    - Ritual: Comportamento social e comunitário
    - Engine: Capacidade analítica e estratégica
    - Logs: Expectativas operacionais
    """
    
    def __init__(self, name: str, api_base_url: str, dna: Optional[AgentDNA] = None):
        """
        Inicializa agente evoluído
        
        Args:
            name (str): Nome único do agente
            api_base_url (str): URL base da API
            dna (AgentDNA, optional): DNA herdado ou None para gerar novo
        """
        super().__init__(name, api_base_url, dna)
        
        # Log da identidade do agente evoluído
        self.logger.info(f"🧬 EvolvedAgent {self.identity.full_name} '{self.identity.nickname}' criado")
        self.logger.info(f"   Personalidade: {self.identity.personality_archetype}")
        self.logger.info(f"   DNA Geração: {self.dna.generation}")
        self.logger.info(f"   Origem: {self.identity.origin}")
        
        # Introdução pessoal
        introduction = self.introduce_self()
        self.logger.info(f"   Apresentação: {introduction}")
        
        # Inicializar sentiment service para análise emocional
        self.sentiment_service = SentimentService()
        
        # Histórico de decisões para aprendizado
        self.decision_history = []
        
        # Contadores de performance por universo
        self.universe_metrics = {
            "limbo": {"transactions": 0, "successful_purchases": 0, "profit": 0.0},
            "odyssey": {"customizations": 0, "innovations": 0, "popularity": 0.0},
            "ritual": {"social_interactions": 0, "influence_events": 0, "satisfaction": 0.0},
            "engine": {"predictions": 0, "correct_predictions": 0, "analyses": 0},
            "logs": {"deliveries": 0, "complaints": 0, "satisfaction_total": 0.0}
        }
        
        self.logger.info(f"🧬 EvolvedAgent inicializado: {self.get_genetic_personality()}")
    
    def get_genetic_personality(self) -> str:
        """
        Gera descrição da personalidade baseada no DNA
        
        Returns:
            str: Descrição da personalidade genética
        """
        # Identificar traits dominantes
        limbo_dominant = max(self.dna.limbo_genes.traits.items(), key=lambda x: x[1])
        odyssey_dominant = max(self.dna.odyssey_genes.traits.items(), key=lambda x: x[1])
        ritual_dominant = max(self.dna.ritual_genes.traits.items(), key=lambda x: x[1])
        
        personality_traits = []
        
        # Personalidade Limbo
        if limbo_dominant[0] == "risk_tolerance" and limbo_dominant[1] > 0.7:
            personality_traits.append("Especulador Corajoso")
        elif limbo_dominant[0] == "price_sensitivity" and limbo_dominant[1] > 0.7:
            personality_traits.append("Caçador de Barganha")
        elif limbo_dominant[0] == "quality_preference" and limbo_dominant[1] > 0.7:
            personality_traits.append("Perfeccionista Premium")
        
        # Personalidade Odyssey
        if odyssey_dominant[0] == "creativity_drive" and odyssey_dominant[1] > 0.7:
            personality_traits.append("Artista Inovador")
        elif odyssey_dominant[0] == "experimentation" and odyssey_dominant[1] > 0.7:
            personality_traits.append("Experimentador Nato")
        
        # Personalidade Ritual
        if ritual_dominant[0] == "community_bonding" and ritual_dominant[1] > 0.7:
            personality_traits.append("Líder Comunitário")
        elif ritual_dominant[0] == "influence_susceptibility" and ritual_dominant[1] > 0.7:
            personality_traits.append("Seguidor Leal")
        
        aesthetic = self.get_categorical_gene("odyssey", "aesthetic_bias")
        personality_traits.append(f"Estilo {aesthetic.title()}")
        
        return " | ".join(personality_traits) if personality_traits else "Personalidade Equilibrada"
    
    async def decide_and_act(self):
        """
        Implementa ciclo de decisão genético nos 5 universos
        """
        try:
            self.logger.info(f"🧬 Iniciando ciclo de decisão genético - Gen {self.dna.generation}")
            
            # Refresh JWT token if needed
            self._refresh_jwt_if_needed()
            
            # 1. Universo Limbo - Decisões de Mercado
            await self._act_in_limbo()
            
            # 2. Universo Odyssey - Criatividade e Personalização
            await self._act_in_odyssey()
            
            # 3. Universo Ritual - Comportamento Social
            await self._act_in_ritual()
            
            # 4. Universo Engine - Análise e Estratégia
            await self._act_in_engine()
            
            # 5. Universo Logs - Operações e Logística
            await self._act_in_logs()
            
            # Atualizar performance geral
            self._update_performance_metrics()
            
        except Exception as e:
            self.logger.error(f"🧬 Erro no ciclo de decisão: {e}")
    
    async def _act_in_limbo(self):
        """Ações no Universo Limbo - Mercado de commodities"""
        self.logger.info("🏪 Atuando no Universo Limbo...")
        
        try:
            # Buscar produtos disponíveis
            response = self.session.get(
                f"{self.api_base_url}/artifacts?select=*&order=price",
                headers=self.headers
            )
            response.raise_for_status()
            products = response.json()
            
            if not products:
                self.logger.info("🏪 Nenhum produto disponível no Limbo")
                return
            
            # Aplicar decisão genética
            agent_balance = self.agent_data.get("wallet_balance", 0) if self.agent_data else 0  # type: ignore
            decision_factors = {"products": products, "agent_balance": agent_balance}
            genetic_decision = self.make_decision_with_genes(decision_factors, "limbo")
            
            # Escolher produto baseado em genes
            risk_tolerance = self.get_gene_value("limbo", "risk_tolerance")
            price_sensitivity = self.get_gene_value("limbo", "price_sensitivity")
            
            best_product = None
            best_score = -1
            
            for product in genetic_decision["products"][:5]:  # Considerar top 5
                genetic_score = product.get("genetic_score", 0)
                
                # Adicionar fatores genéticos específicos
                if genetic_score > best_score and product["price"] <= decision_factors["agent_balance"]:
                    best_product = product
                    best_score = genetic_score
            
            if best_product:
                success = await self._attempt_purchase(best_product)
                self.universe_metrics["limbo"]["transactions"] += 1
                if success:
                    self.universe_metrics["limbo"]["successful_purchases"] += 1
                    
                    # Calcular profit estimado (simulado)
                    estimated_value = best_product.get("quality", 0.5) * best_product["price"] * 1.2
                    profit = estimated_value - best_product["price"]
                    self.universe_metrics["limbo"]["profit"] += profit
                    
                    self.logger.info(f"🏪 Compra realizada: {best_product['name']} por ${best_product['price']}")
                else:
                    self.logger.info(f"🏪 Falha na compra: {best_product['name']}")
            else:
                self.logger.info("🏪 Nenhum produto adequado encontrado no Limbo")
                
        except Exception as e:
            self.logger.error(f"🏪 Erro no Universo Limbo: {e}")
    
    async def _act_in_odyssey(self):
        """Ações no Universo Odyssey - Personalização e criatividade"""
        self.logger.info("🎨 Atuando no Universo Odyssey...")
        
        creativity_drive = self.get_gene_value("odyssey", "creativity_drive")
        experimentation = self.get_gene_value("odyssey", "experimentation")
        aesthetic_bias = self.get_categorical_gene("odyssey", "aesthetic_bias")
        
        # Simular atividade criativa baseada em genes
        if creativity_drive > 0.6:
            self.universe_metrics["odyssey"]["customizations"] += 1
            self.logger.info(f"🎨 Criando personalização no estilo {aesthetic_bias}")
            
            if experimentation > 0.7:
                self.universe_metrics["odyssey"]["innovations"] += 1
                self.logger.info("🎨 Inovação experimental criada!")
                
                # Simular popularidade baseada em criatividade
                popularity_boost = creativity_drive * experimentation
                self.universe_metrics["odyssey"]["popularity"] += popularity_boost
        
        # Atualizar performance da Odyssey
        odyssey_performance = {
            "creativity_score": creativity_drive,
            "popularity_score": min(self.universe_metrics["odyssey"]["popularity"] / 10, 1.0),
            "innovation_score": experimentation
        }
        self.update_performance("odyssey", odyssey_performance)
    
    async def _act_in_ritual(self):
        """Ações no Universo Ritual - Comportamento social"""
        self.logger.info("👥 Atuando no Universo Ritual...")
        
        community_bonding = self.get_gene_value("ritual", "community_bonding")
        influence_susceptibility = self.get_gene_value("ritual", "influence_susceptibility")
        leadership_tendency = self.get_gene_value("ritual", "leadership_tendency")
        
        # Simular interações sociais baseadas em genes
        if community_bonding > 0.5:
            self.universe_metrics["ritual"]["social_interactions"] += 1
            self.logger.info("👥 Participando da comunidade")
            
            if leadership_tendency > 0.7:
                self.universe_metrics["ritual"]["influence_events"] += 1
                self.logger.info("👥 Exercendo liderança na comunidade")
        
        # Simular satisfação com assinatura
        satisfaction = (community_bonding + (1 - influence_susceptibility) + leadership_tendency) / 3
        self.universe_metrics["ritual"]["satisfaction"] += satisfaction
        
        # Atualizar performance do Ritual
        ritual_performance = {
            "community_engagement": community_bonding,
            "social_influence": leadership_tendency,
            "subscription_satisfaction": min(self.universe_metrics["ritual"]["satisfaction"] / 10, 1.0)
        }
        self.update_performance("ritual", ritual_performance)
    
    async def _act_in_engine(self):
        """Ações no Universo Engine - Análise e inteligência"""
        self.logger.info("🧠 Atuando no Universo Engine...")
        
        analytical_thinking = self.get_gene_value("engine", "analytical_thinking")
        pattern_recognition = self.get_gene_value("engine", "pattern_recognition")
        strategic_planning = self.get_gene_value("engine", "strategic_planning")
        
        # Simular atividade analítica
        if analytical_thinking > 0.6:
            self.universe_metrics["engine"]["analyses"] += 1
            self.logger.info("🧠 Realizando análise de dados")
            
            # Simular previsão baseada em genes
            if pattern_recognition > 0.7:
                self.universe_metrics["engine"]["predictions"] += 1
                
                # Simular precisão da previsão
                prediction_accuracy = (analytical_thinking + pattern_recognition) / 2
                if random.random() < prediction_accuracy:
                    self.universe_metrics["engine"]["correct_predictions"] += 1
                    self.logger.info("🧠 Previsão precisa realizada!")
        
        # Atualizar performance do Engine
        engine_performance = {
            "prediction_accuracy": (
                self.universe_metrics["engine"]["correct_predictions"] / 
                max(self.universe_metrics["engine"]["predictions"], 1)
            ),
            "analysis_quality": analytical_thinking,
            "ai_contributions": strategic_planning
        }
        self.update_performance("engine", engine_performance)
    
    async def _act_in_logs(self):
        """Ações no Universo Logs - Operações e logística"""
        self.logger.info("📦 Atuando no Universo Logs...")
        
        patience_level = self.get_gene_value("logs", "patience_level")
        service_expectations = self.get_gene_value("logs", "service_expectations")
        complaint_tendency = self.get_gene_value("logs", "complaint_tendency")
        
        # Simular experiência de entrega
        self.universe_metrics["logs"]["deliveries"] += 1
        
        # Simular satisfação baseada em genes
        delivery_quality = random.random()  # Qualidade simulada da entrega
        
        satisfaction_threshold = service_expectations
        if delivery_quality < satisfaction_threshold:
            if random.random() < complaint_tendency:
                self.universe_metrics["logs"]["complaints"] += 1
                self.logger.info("📦 Reclamação registrada sobre entrega")
        
        # Calcular satisfação considerando paciência
        adjusted_satisfaction = delivery_quality
        if delivery_quality < 0.5:  # Entrega ruim
            adjusted_satisfaction *= patience_level  # Paciência diminui insatisfação
        
        self.universe_metrics["logs"]["satisfaction_total"] += adjusted_satisfaction
        
        # Atualizar performance dos Logs
        logs_performance = {
            "delivery_satisfaction": (
                self.universe_metrics["logs"]["satisfaction_total"] / 
                max(self.universe_metrics["logs"]["deliveries"], 1)
            ),
            "operational_efficiency": 1.0 - (
                self.universe_metrics["logs"]["complaints"] / 
                max(self.universe_metrics["logs"]["deliveries"], 1)
            ),
            "problem_resolution": patience_level
        }
        self.update_performance("logs", logs_performance)
    
    async def _attempt_purchase(self, product: Dict[str, Any]) -> bool:
        """
        Tenta realizar compra de um produto
        
        Args:
            product (dict): Dados do produto
            
        Returns:
            bool: True se compra bem-sucedida
        """
        try:
            # Simular compra (implementação simplificada)
            if product["price"] <= (self.agent_data.get("wallet_balance", 0) if self.agent_data else 0):  # type: ignore
                # Aqui seria feita a chamada real para a API de compra
                self.logger.info(f"💰 Compra simulada: {product['name']}")
                
                # Simular análise de sentimento pós-compra
                context = ConsumptionContext(
                    agent_id=self.name,
                    agent_name=self.name,
                    artifact_name=product["name"],
                    artifact_description=product.get("description", "Produto do Limbo"),
                    artifact_quality=product.get("quality", 0.5),
                    purchase_price=product["price"],
                    agent_current_sentiment=self.dna.fitness_scores.get("overall", 0.5),
                    agent_wallet_balance=self.agent_data.get("wallet_balance", 0) if self.agent_data else 0  # type: ignore
                )
                
                sentiment_result = await self.sentiment_service.analyze_consumption(context)
                self.logger.info(f"😊 Sentimento pós-compra: {sentiment_result.emotion_category}")
                
                return True
            else:
                self.logger.info(f"💸 Saldo insuficiente para {product['name']}")
                return False
                
        except Exception as e:
            self.logger.error(f"💥 Erro na compra: {e}")
            return False
    
    def _update_performance_metrics(self):
        """Atualiza métricas gerais de performance"""
        
        # Calcular métricas de performance por universo para fitness
        limbo_performance = {
            "profit_ratio": max(-1.0, min(1.0, self.universe_metrics["limbo"]["profit"] / 1000)),
            "decision_accuracy": (
                self.universe_metrics["limbo"]["successful_purchases"] / 
                max(self.universe_metrics["limbo"]["transactions"], 1)
            ),
            "market_timing": self.get_gene_value("limbo", "risk_tolerance")
        }
        self.update_performance("limbo", limbo_performance)
        
        self.logger.debug(f"🧬 Performance atualizada: Limbo={limbo_performance}")

# Função de teste
async def test_evolved_agent():
    """Testa o agente evoluído"""
    
    print("🧬 Testando EvolvedAgent com Genesis Protocol")
    print("=" * 60)
    
    # Criar agente evoluído
    agent = EvolvedAgent("evolved_agent_001", "http://localhost:8000")
    
    print(f"🧬 Agente criado: {agent.name}")
    print(f"🧬 Personalidade: {agent.get_genetic_personality()}")
    print(f"🧬 Geração: {agent.dna.generation}")
    
    # Simular alguns dados do agente
    agent.agent_data = {
        "id": "test_001",
        "name": agent.name,
        "wallet_balance": 1000.0,
        "sentiment": 0.5
    }
    
    # Executar alguns ciclos de decisão
    print("\n🧬 Executando ciclos de decisão...")
    for i in range(3):
        print(f"\n--- Ciclo {i+1} ---")
        await agent.decide_and_act()
        
        # Mostrar fitness atualizado
        fitness = agent.calculate_fitness()
        print(f"Fitness Overall: {fitness['overall']:.3f}")
    
    # Mostrar resumo do DNA
    dna_summary = agent.get_dna_summary()
    print(f"\n🧬 Resumo DNA:")
    print(f"  Geração: {dna_summary['generation']}")
    print(f"  Fitness: {dna_summary['fitness_scores']['overall']:.3f}")
    print(f"  Pode reproduzir: {agent.can_reproduce()}")
    
    print("\n✅ Teste do EvolvedAgent concluído!")

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Executar teste
    asyncio.run(test_evolved_agent())
