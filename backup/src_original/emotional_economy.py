#!/usr/bin/env python3
"""
Emotional Economy System - Lore N.A.
====================================

Sistema de economia emocional baseado no universo Limbo.
Agentes podem trocar "Emotion Tokens" baseado em sentimentos e interações.

Autor: Lore N.A. Genesis Team
Data: 27 de Junho de 2025
"""

import traceback
from typing import Optional, Any

# Configuração de logging robusto
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

import random
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EmotionType(Enum):
    """Tipos de emoções traduzidas em tokens"""
    JOY = "joy"           # Alegria - alta liquidez
    TRUST = "trust"       # Confiança - moeda estável
    FEAR = "fear"         # Medo - alta volatilidade
    SURPRISE = "surprise" # Surpresa - burst currency
    SADNESS = "sadness"   # Tristeza - valor baixo mas estável
    DISGUST = "disgust"   # Repulsa - moeda de resistência
    ANGER = "anger"       # Raiva - alta especulação
    ANTICIPATION = "anticipation"  # Antecipação - moeda futura

@dataclass
class EmotionToken:
    """Token emocional tradeable"""
    emotion_type: EmotionType
    amount: float
    quality: float  # 0.0 a 1.0 - pureza da emoção
    origin_agent: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    @property
    def market_value(self) -> float:
        """Calcula valor de mercado baseado em tipo, qualidade e tempo"""
        base_values = {
            EmotionType.JOY: 1.2,
            EmotionType.TRUST: 1.0,
            EmotionType.FEAR: 0.8,
            EmotionType.SURPRISE: 1.5,
            EmotionType.SADNESS: 0.6,
            EmotionType.DISGUST: 0.4,
            EmotionType.ANGER: 0.9,
            EmotionType.ANTICIPATION: 1.1
        }
        
        base_value = base_values[self.emotion_type]
        quality_modifier = 0.5 + (self.quality * 0.5)  # 0.5 to 1.0
        
        # Degradação temporal para algumas emoções
        if self.expires_at:
            time_left = (self.expires_at - datetime.now()).total_seconds()
            if time_left <= 0:
                return 0.0
            time_modifier = min(1.0, time_left / (24 * 3600))  # 24h degradation
        else:
            time_modifier = 1.0
        
        return base_value * quality_modifier * time_modifier

@dataclass
class EmotionalWallet:
    """Carteira emocional de um agente"""
    agent_id: str
    tokens: Dict[EmotionType, List[EmotionToken]] = field(default_factory=dict)
    transaction_history: List[Dict] = field(default_factory=list)
    
    def __post_init__(self):
        for emotion_type in EmotionType:
            if emotion_type not in self.tokens:
                self.tokens[emotion_type] = []
    
    def add_tokens(self, tokens: List[EmotionToken]):
        """Adiciona tokens à carteira"""
        for token in tokens:
            self.tokens[token.emotion_type].append(token)
            
            self.transaction_history.append({
                'type': 'earn',
                'emotion': token.emotion_type.value,
                'amount': token.amount,
                'quality': token.quality,
                'timestamp': datetime.now()
            })
    
    def spend_tokens(self, emotion_type: EmotionType, amount: float) -> bool:
        """Gasta tokens de um tipo específico"""
        available_tokens = self.tokens[emotion_type]
        available_tokens.sort(key=lambda x: x.market_value, reverse=True)  # Usa os melhores primeiro
        
        total_spent = 0.0
        tokens_to_remove = []
        
        for token in available_tokens:
            if total_spent >= amount:
                break
                
            needed = amount - total_spent
            if token.amount <= needed:
                total_spent += token.amount
                tokens_to_remove.append(token)
            else:
                # Quebra o token
                token.amount -= needed
                total_spent += needed
        
        if total_spent >= amount:
            # Remove tokens gastos
            for token in tokens_to_remove:
                available_tokens.remove(token)
            
            self.transaction_history.append({
                'type': 'spend',
                'emotion': emotion_type.value,
                'amount': total_spent,
                'timestamp': datetime.now()
            })
            return True
        
        return False
    
    def get_balance(self, emotion_type: EmotionType) -> Dict[str, float]:
        """Obtém balanço de um tipo de emoção"""
        tokens = self.tokens[emotion_type]
        
        total_amount = sum(token.amount for token in tokens)
        total_value = sum(token.amount * token.market_value for token in tokens)
        avg_quality = sum(token.quality for token in tokens) / len(tokens) if tokens else 0
        
        return {
            'amount': total_amount,
            'market_value': total_value,
            'average_quality': avg_quality,
            'token_count': len(tokens)
        }
    
    def get_total_wealth(self) -> float:
        """Calcula riqueza emocional total"""
        total = 0.0
        for emotion_type in EmotionType:
            balance = self.get_balance(emotion_type)
            total += balance['market_value']
        return total

class EmotionalMarket:
    """Mercado de emoções onde agentes podem trocar tokens"""
    
    def __init__(self):
        self.market_rates: Dict[EmotionType, float] = {}
        self.daily_volume: Dict[EmotionType, float] = {}
        self.price_history: Dict[EmotionType, List[Tuple[datetime, float]]] = {}
        self.active_orders: List[Dict] = []
        
        # Inicializa taxas base
        for emotion_type in EmotionType:
            self.market_rates[emotion_type] = 1.0
            self.daily_volume[emotion_type] = 0.0
            self.price_history[emotion_type] = []
    
    def update_market_rates(self):
        """Atualiza taxas de mercado baseado em oferta/demanda"""
        for emotion_type in EmotionType:
            # Simula volatilidade baseada no tipo de emoção
            volatility = {
                EmotionType.JOY: 0.05,
                EmotionType.TRUST: 0.02,
                EmotionType.FEAR: 0.15,
                EmotionType.SURPRISE: 0.20,
                EmotionType.SADNESS: 0.03,
                EmotionType.DISGUST: 0.08,
                EmotionType.ANGER: 0.12,
                EmotionType.ANTICIPATION: 0.10
            }
            
            change = random.gauss(0, volatility[emotion_type])
            new_rate = max(0.1, self.market_rates[emotion_type] * (1 + change))
            self.market_rates[emotion_type] = new_rate
            
            # Salva histórico
            self.price_history[emotion_type].append((datetime.now(), new_rate))
            
            # Mantém apenas últimos 100 pontos
            if len(self.price_history[emotion_type]) > 100:
                self.price_history[emotion_type] = self.price_history[emotion_type][-100:]
    
    def trade_tokens(self, seller_wallet: EmotionalWallet, buyer_wallet: EmotionalWallet,
                    sell_emotion: EmotionType, buy_emotion: EmotionType, amount: float) -> bool:
        """Realiza troca entre dois agentes"""
        
        # Calcula taxas de conversão
        sell_rate = self.market_rates[sell_emotion]
        buy_rate = self.market_rates[buy_emotion]
        conversion_rate = sell_rate / buy_rate
        
        # Verifica se vendedor tem tokens suficientes
        if not seller_wallet.spend_tokens(sell_emotion, amount):
            return False
        
        # Cria tokens para o comprador
        converted_amount = amount * conversion_rate
        quality = random.uniform(0.7, 1.0)  # Qualidade da conversão
        
        new_token = EmotionToken(
            emotion_type=buy_emotion,
            amount=converted_amount,
            quality=quality,
            origin_agent=f"market_conversion_{seller_wallet.agent_id}",
            created_at=datetime.now()
        )
        
        buyer_wallet.add_tokens([new_token])
        
        # Atualiza volume
        self.daily_volume[sell_emotion] += amount
        self.daily_volume[buy_emotion] += converted_amount
        
        logger.info(f"Trade: {seller_wallet.agent_id} → {buyer_wallet.agent_id}")
        logger.info(f"  {amount:.2f} {sell_emotion.value} → {converted_amount:.2f} {buy_emotion.value}")
        
        return True

class EmotionalEconomyEngine:
    """Engine principal da economia emocional"""
    
    def __init__(self):
        self.market = EmotionalMarket()
        self.wallets: Dict[str, EmotionalWallet] = {}
        self.daily_events: List[Dict] = []
    
    def register_agent(self, agent_id: str) -> EmotionalWallet:
        """Registra um novo agente na economia"""
        if agent_id not in self.wallets:
            wallet = EmotionalWallet(agent_id)
            
            # Tokens iniciais aleatórios
            initial_tokens = []
            for emotion_type in EmotionType:
                if random.random() < 0.6:  # 60% chance de ter cada tipo
                    amount = random.uniform(1.0, 5.0)
                    quality = random.uniform(0.5, 1.0)
                    
                    token = EmotionToken(
                        emotion_type=emotion_type,
                        amount=amount,
                        quality=quality,
                        origin_agent="genesis",
                        created_at=datetime.now()
                    )
                    initial_tokens.append(token)
            
            wallet.add_tokens(initial_tokens)
            self.wallets[agent_id] = wallet
            
            logger.info(f"Agente {agent_id} registrado na economia emocional")
        
        return self.wallets[agent_id]
    
    def generate_emotion_from_interaction(self, agent_id: str, interaction_data: Dict) -> List[EmotionToken]:
        """Gera tokens emocionais baseado em interação social"""
        sentiment = interaction_data.get('sentiment', 0.0)  # -1 a 1
        intensity = interaction_data.get('intensity', 0.5)   # 0 a 1
        success = interaction_data.get('success', True)
        
        tokens = []
        
        # Mapeia sentimento para emoções
        if sentiment > 0.5:
            # Sentimentos positivos
            emotions = [EmotionType.JOY, EmotionType.TRUST, EmotionType.ANTICIPATION]
            weights = [0.5, 0.3, 0.2]
        elif sentiment < -0.5:
            # Sentimentos negativos
            emotions = [EmotionType.SADNESS, EmotionType.ANGER, EmotionType.FEAR]
            weights = [0.4, 0.3, 0.3]
        else:
            # Sentimentos neutros/mistos
            emotions = [EmotionType.SURPRISE, EmotionType.TRUST]
            weights = [0.6, 0.4]
        
        # Gera tokens baseado na interação
        for emotion, weight in zip(emotions, weights):
            if random.random() < weight:
                amount = intensity * random.uniform(0.5, 2.0)
                quality = min(1.0, intensity + random.uniform(-0.2, 0.2))
                
                # Emoções negativas podem expirar mais rápido
                expires_at = None
                if emotion in [EmotionType.ANGER, EmotionType.FEAR]:
                    expires_at = datetime.now() + timedelta(hours=random.randint(6, 24))
                
                token = EmotionToken(
                    emotion_type=emotion,
                    amount=amount,
                    quality=max(0.1, quality),
                    origin_agent=agent_id,
                    created_at=datetime.now(),
                    expires_at=expires_at
                )
                tokens.append(token)
        
        return tokens
    
    def simulate_market_day(self):
        """Simula um dia de atividade no mercado"""
        logger.info("🏛️ Simulando dia de mercado emocional...")
        
        # Atualiza taxas de mercado
        self.market.update_market_rates()
        
        # Simula algumas trocas aleatórias
        agent_ids = list(self.wallets.keys())
        if len(agent_ids) >= 2:
            for _ in range(random.randint(1, 5)):
                seller_id = random.choice(agent_ids)
                buyer_id = random.choice([aid for aid in agent_ids if aid != seller_id])
                
                sell_emotion = random.choice(list(EmotionType))
                buy_emotion = random.choice(list(EmotionType))
                amount = random.uniform(0.5, 2.0)
                
                self.market.trade_tokens(
                    self.wallets[seller_id],
                    self.wallets[buyer_id],
                    sell_emotion,
                    buy_emotion,
                    amount
                )
        
        # Reset daily volume
        for emotion_type in EmotionType:
            self.market.daily_volume[emotion_type] = 0.0
    
    def get_economy_stats(self) -> Dict:
        """Estatísticas da economia"""
        total_agents = len(self.wallets)
        total_wealth = sum(wallet.get_total_wealth() for wallet in self.wallets.values())
        avg_wealth = total_wealth / total_agents if total_agents > 0 else 0
        
        # Agente mais rico
        richest_agent = None
        max_wealth = 0
        for agent_id, wallet in self.wallets.items():
            wealth = wallet.get_total_wealth()
            if wealth > max_wealth:
                max_wealth = wealth
                richest_agent = agent_id
        
        return {
            'total_agents': total_agents,
            'total_wealth': total_wealth,
            'average_wealth': avg_wealth,
            'richest_agent': richest_agent,
            'max_wealth': max_wealth,
            'market_rates': {et.value: rate for et, rate in self.market.market_rates.items()}
        }

# Exemplo de uso
def demo_emotional_economy():
    """Demonstração do sistema de economia emocional"""
    
    print("🏛️ Demo: Sistema de Economia Emocional")
    print("=" * 50)
    
    # Cria engine
    economy = EmotionalEconomyEngine()
    
    # Registra alguns agentes
    agents = ["alice", "bob", "charlie"]
    for agent_id in agents:
        wallet = economy.register_agent(agent_id)
        print(f"✓ {agent_id} registrado - Riqueza inicial: {wallet.get_total_wealth():.2f}")
    
    print("\n💰 Balanços Iniciais:")
    for agent_id in agents:
        wallet = economy.wallets[agent_id]
        print(f"  {agent_id}: {wallet.get_total_wealth():.2f} total")
        
        for emotion_type in EmotionType:
            balance = wallet.get_balance(emotion_type)
            if balance['amount'] > 0:
                print(f"    {emotion_type.value}: {balance['amount']:.2f} (valor: {balance['market_value']:.2f})")
    
    print("\n🔄 Simulando interações e geração de tokens...")
    
    # Simula algumas interações
    interactions = [
        {'agent': 'alice', 'sentiment': 0.8, 'intensity': 0.9, 'success': True},
        {'agent': 'bob', 'sentiment': -0.3, 'intensity': 0.6, 'success': False},
        {'agent': 'charlie', 'sentiment': 0.2, 'intensity': 0.7, 'success': True}
    ]
    
    for interaction in interactions:
        agent_id = interaction['agent']
        tokens = economy.generate_emotion_from_interaction(agent_id, interaction)
        
        if tokens:
            economy.wallets[agent_id].add_tokens(tokens)
            print(f"  {agent_id} ganhou {len(tokens)} novos tokens emocionais")
    
    print("\n📈 Simulando dia de mercado...")
    economy.simulate_market_day()
    
    print("\n📊 Estatísticas Finais da Economia:")
    stats = economy.get_economy_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v:.3f}")
        else:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    demo_emotional_economy()
