"""
SentimentService - Serviço de Análise de Sentimento para o MVM
Implementa o loop de feedback emocional: Ação -> Resultado -> Sentimento -> Novo Estado

Integração com LeIA (Léxico para Inferência Adaptada):
- Gera "reviews" naturalísticas baseadas na experiência
- Usa LeIA para extrair sentimento real em português
- Combina análise LeIA com nossa lógica de contexto

Fluxo:
1. Agente compra artefato (registrado no inventário)
2. Agente decide consumir o artefato
3. SentimentService simula experiência e gera review em português
4. LeIA analisa o sentimento da review
5. Combina resultado LeIA com fatores contextuais
6. Atualiza o estado emocional do agente
7. Agente usa novo estado para próxima decisão
"""

import logging
import json
import random
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import asyncio
import math

# Importar LeIA para análise de sentimento em português
try:
    from leia import SentimentIntensityAnalyzer as LeIASentimentAnalyzer
    LEIA_AVAILABLE = True
except ImportError:
    LEIA_AVAILABLE = False
    logging.warning("LeIA não disponível. Usando análise básica.")

# Importar NLTK VADER para análise de sentimento (otimizado para redes sociais)
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer as NLTKSentimentAnalyzer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    logging.warning("NLTK VADER não disponível.")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentCategory(Enum):
    """Categorias de sentimento do artefato"""
    CALMING = "calming"          # Fruta da Calma
    ENERGIZING = "energizing"    # Cristal de Energia  
    INTELLECTUAL = "intellectual" # Orbe do Conhecimento


@dataclass
class ConsumptionContext:
    """Contexto do consumo do artefato"""
    agent_id: str
    agent_name: str
    artifact_name: str
    artifact_description: str
    artifact_quality: float
    purchase_price: float
    agent_current_sentiment: float
    agent_wallet_balance: float


@dataclass
class SentimentAnalysis:
    """Resultado da análise de sentimento"""
    sentiment_score: float  # -1.0 a 1.0
    emotion_category: str   # happy, neutral, disappointed, etc.
    reasoning: str          # Explicação do sentimento
    impact_magnitude: float # 0.0 a 1.0 - quão forte foi o impacto
    leia_analysis: Optional[Dict] = None  # Dados raw do LeIA
    nltk_analysis: Optional[Dict] = None  # Dados raw do NLTK VADER
    generated_review: Optional[str] = None  # Review gerada
    analysis_method: str = "hybrid"  # Método usado: leia, nltk, hybrid, context_only


class SentimentService:
    """
    Serviço principal de análise de sentimento.
    
    Algoritmo de Sentimento v2.0 (com LeIA):
    - Quality Impact: Qualidade do item vs expectativa
    - Price Impact: Preço pago vs valor percebido
    - Personality Impact: Como o tipo de agente reage
    - Expectation Impact: Sentimento atual influencia expectativa
    - LeIA Analysis: Análise de sentimento em português de review gerada
    """
    
    def __init__(self):
        # Inicializar analisador LeIA se disponível
        if LEIA_AVAILABLE:
            try:
                self.leia_analyzer = LeIASentimentAnalyzer()
                logger.info("LeIA inicializado com sucesso para análise em português")
            except Exception as e:
                logger.warning(f"Erro ao inicializar LeIA: {e}")
                self.leia_analyzer = None
        else:
            self.leia_analyzer = None
        
        # Inicializar analisador NLTK VADER se disponível
        if NLTK_AVAILABLE:
            try:
                self.nltk_analyzer = NLTKSentimentAnalyzer()
                logger.info("NLTK VADER inicializado com sucesso para análise em inglês")
            except Exception as e:
                logger.warning(f"Erro ao inicializar NLTK VADER: {e}")
                self.nltk_analyzer = None
        else:
            self.nltk_analyzer = None
        
        # Mapeamento de categorias para efeitos emocionais base
        self.sentiment_effects = {
            SentimentCategory.CALMING: {
                "base_effect": 0.3,
                "keywords": ["calma", "foco", "tranquil", "sereno"],
                "optimal_quality_range": (0.7, 1.0),
                "positive_reviews": [
                    "Nossa, que sensação incrível! Me sinto muito mais calmo e focado.",
                    "Exatamente o que eu precisava. Uma paz interior maravilhosa.",
                    "Finalmente consegui relaxar. Produto excelente!",
                    "Que tranquilidade! Recomendo para quem precisa de paz mental.",
                    "Impressionante como me acalmou. Valeu cada centavo."
                ],
                "negative_reviews": [
                    "Esperava mais. Não senti nada de especial.",
                    "Caro demais para o que oferece. Decepcionante.",
                    "Não funcionou comigo. Talvez seja placebo mesmo.",
                    "Marketing enganoso. Continuo estressado como sempre.",
                    "Perda de dinheiro. Não vale a pena."
                ]
            },
            SentimentCategory.ENERGIZING: {
                "base_effect": 0.4,
                "keywords": ["energia", "vigor", "força", "poder"],
                "optimal_quality_range": (0.6, 1.0),
                "positive_reviews": [
                    "Que energia incrível! Me sinto renovado e poderoso.",
                    "Uau! É como se tivesse bebido 10 cafés, mas melhor!",
                    "Energia limpa e duradoura. Simplesmente fantástico!",
                    "Me deu a força que eu precisava. Produto top!",
                    "Incrível como me revigorou. Super recomendo!"
                ],
                "negative_reviews": [
                    "Muito hype e pouco resultado. Não senti diferença.",
                    "Caro e sem efeito. Prefiro um energético comum.",
                    "Propaganda enganosa. Continuo sem energia.",
                    "Não valeu o investimento. Decepção total.",
                    "Esperava muito mais pelo preço cobrado."
                ]
            },
            SentimentCategory.INTELLECTUAL: {
                "base_effect": 0.2,
                "keywords": ["conhecimento", "sabedoria", "fatos", "aprender"],
                "optimal_quality_range": (0.4, 0.8),
                "positive_reviews": [
                    "Que conhecimento fascinante! Aprendi coisas incríveis.",
                    "Informações valiosas que nunca tinha visto antes.",
                    "Expandiu minha mente de forma surpreendente.",
                    "Conhecimento que realmente faz diferença. Excelente!",
                    "Insights únicos e profundos. Vale cada centavo."
                ],
                "negative_reviews": [
                    "Informações básicas que já sabia. Nada novo.",
                    "Muito superficial para o preço cobrado.",
                    "Conhecimento inútil e sem aplicação prática.",
                    "Esperava sabedoria, recebi obviedades.",
                    "Perda de tempo e dinheiro. Muito decepcionante."
                ]
            }
        }
    
    def categorize_artifact(self, name: str, description: str) -> SentimentCategory:
        """Categoriza o artefato baseado no nome e descrição"""
        name_lower = name.lower()
        desc_lower = description.lower() if description else ""
        
        # Mapeamento direto por nome conhecido
        if "calma" in name_lower or "fruta" in name_lower:
            return SentimentCategory.CALMING
        elif "energia" in name_lower or "cristal" in name_lower:
            return SentimentCategory.ENERGIZING
        elif "conhecimento" in name_lower or "orbe" in name_lower:
            return SentimentCategory.INTELLECTUAL
        
        # Análise por palavras-chave na descrição
        for category, effects in self.sentiment_effects.items():
            keywords = effects["keywords"]
            if any(keyword in desc_lower for keyword in keywords):
                return category
        
        # Padrão
        return SentimentCategory.CALMING
    
    def calculate_quality_impact(
        self, 
        artifact_quality: float, 
        category: SentimentCategory
    ) -> float:
        """
        Calcula impacto da qualidade no sentimento.
        
        Lógica:
        - Cada categoria tem uma faixa de qualidade "ótima"
        - Qualidade dentro da faixa = impacto positivo
        - Qualidade fora da faixa = impacto negativo
        """
        optimal_range = self.sentiment_effects[category]["optimal_quality_range"]
        min_quality, max_quality = optimal_range
        
        if min_quality <= artifact_quality <= max_quality:
            # Dentro da faixa ótima - impacto positivo
            center = (min_quality + max_quality) / 2
            distance_from_center = abs(artifact_quality - center)
            normalized_distance = distance_from_center / ((max_quality - min_quality) / 2)
            return 0.5 + (0.5 * (1 - normalized_distance))  # 0.5 a 1.0
        else:
            # Fora da faixa ótima - impacto negativo
            if artifact_quality < min_quality:
                distance = min_quality - artifact_quality
            else:
                distance = artifact_quality - max_quality
            
            # Limita penalidade máxima
            max_penalty = 0.6
            penalty = min(distance * 2, max_penalty)
            return 0.5 - penalty  # Mínimo ~-0.1
    
    def calculate_price_impact(
        self, 
        purchase_price: float, 
        artifact_quality: float,
        agent_wallet_balance: float
    ) -> float:
        """
        Calcula impacto do preço no sentimento.
        
        Lógica:
        - Preço justo vs qualidade = impacto neutro/positivo
        - Preço alto vs qualidade baixa = impacto negativo
        - % do wallet gasto influencia a percepção
        """
        # Preço "justo" baseado na qualidade (range 10-100)
        fair_price = 10 + (artifact_quality * 90)
        price_ratio = purchase_price / fair_price
        
        # Impacto do % do wallet gasto
        if agent_wallet_balance > 0:
            wallet_impact = min(purchase_price / agent_wallet_balance, 1.0)
        else:
            wallet_impact = 1.0
        
        # Combina os fatores
        if price_ratio <= 1.0:
            # Preço justo ou barato
            price_impact = 0.3 + (0.4 * (1 - price_ratio))  # 0.3 a 0.7
        else:
            # Preço caro
            price_impact = 0.3 - (0.5 * min(price_ratio - 1, 1))  # 0.3 a -0.2
        
        # Ajusta pelo impacto no wallet
        wallet_penalty = wallet_impact * 0.3
        return price_impact - wallet_penalty
    
    def calculate_expectation_impact(
        self, 
        current_sentiment: float
    ) -> float:
        """
        Calcula como o sentimento atual influencia a expectativa.
        
        Lógica:
        - Sentimento positivo = expectativas altas = maior chance de decepção
        - Sentimento negativo = expectativas baixas = maior chance de surpresa positiva
        """
        # Normaliza sentimento (-1 a 1) para fator de expectativa
        if current_sentiment > 0:
            # Sentimento positivo = expectativas altas
            expectation_factor = -0.2 * current_sentiment  # Ligeiramente negativo
        else:
            # Sentimento negativo = expectativas baixas
            expectation_factor = -0.3 * current_sentiment  # Positivo
        
        return expectation_factor
    
    def generate_emotion_category(self, sentiment_score: float) -> str:
        """Gera categoria emocional baseada no score"""
        if sentiment_score >= 0.7:
            return "euphoric"
        elif sentiment_score >= 0.4:
            return "happy"
        elif sentiment_score >= 0.1:
            return "pleased"
        elif sentiment_score >= -0.1:
            return "neutral"
        elif sentiment_score >= -0.4:
            return "disappointed"
        elif sentiment_score >= -0.7:
            return "frustrated"
        else:
            return "miserable"
    
    def generate_reasoning(
        self, 
        context: ConsumptionContext,
        category: SentimentCategory,
        quality_impact: float,
        price_impact: float,
        expectation_impact: float,
        final_sentiment: float
    ) -> str:
        """Gera explicação do sentimento em linguagem natural"""
        artifact_name = context.artifact_name
        agent_name = context.agent_name
        
        reasoning_parts = []
        
        # Análise de qualidade
        if quality_impact > 0.7:
            reasoning_parts.append(f"O {artifact_name} superou as expectativas de qualidade")
        elif quality_impact > 0.3:
            reasoning_parts.append(f"O {artifact_name} atendeu às expectativas")
        else:
            reasoning_parts.append(f"O {artifact_name} decepcionou em qualidade")
        
        # Análise de preço
        if price_impact > 0.2:
            reasoning_parts.append("e teve um preço justo")
        elif price_impact > -0.1:
            reasoning_parts.append("com preço razoável")
        else:
            reasoning_parts.append("mas custou caro demais")
        
        # Análise de expectativa
        if expectation_impact > 0.1:
            reasoning_parts.append(f"{agent_name} teve uma surpresa positiva")
        elif expectation_impact < -0.1:
            reasoning_parts.append(f"{agent_name} esperava mais")
        
        # Resultado final
        emotion = self.generate_emotion_category(final_sentiment)
        reasoning_parts.append(f"resultando em um sentimento {emotion}")
        
        return ". ".join(reasoning_parts) + "."
    
    def generate_naturalistic_review(
        self,
        context: ConsumptionContext,
        category: SentimentCategory,
        quality_impact: float,
        price_impact: float,
        overall_satisfaction: float
    ) -> str:
        """
        Gera uma review naturalística em português baseada na experiência.
        
        Esta review será analisada pelo LeIA para extrair sentimento real.
        """
        category_data = self.sentiment_effects[category]
        
        # Determinar se a experiência foi positiva ou negativa
        is_positive = overall_satisfaction > 0.1
        
        if is_positive:
            # Escolher review positiva da categoria
            base_review = random.choice(category_data["positive_reviews"])
            
            # Adicionar modificadores baseados na qualidade e preço
            if quality_impact > 0.8:
                modifiers = [
                    " A qualidade superou todas as expectativas!",
                    " Produto premium de verdade.",
                    " Qualidade excepcional!"
                ]
                base_review += random.choice(modifiers)
            
            if price_impact > 0.3:
                price_modifiers = [
                    " E o preço foi justo.",
                    " Excelente custo-benefício.",
                    " Vale cada centavo gasto."
                ]
                base_review += random.choice(price_modifiers)
                
        else:
            # Escolher review negativa da categoria
            base_review = random.choice(category_data["negative_reviews"])
            
            # Adicionar modificadores baseados nos problemas
            if quality_impact < 0.3:
                quality_issues = [
                    " A qualidade deixou muito a desejar.",
                    " Produto de baixa qualidade.",
                    " Qualidade inferior ao esperado."
                ]
                base_review += random.choice(quality_issues)
            
            if price_impact < -0.2:
                price_issues = [
                    " E ainda por cima é caro demais!",
                    " Preço abusivo para o que oferece.",
                    " Não vale o que cobra."
                ]
                base_review += random.choice(price_issues)
        
        # Adicionar contexto pessoal ocasionalmente
        personal_touches = [
            f" Como {context.agent_name.lower()}, posso dizer que",
            f" Na minha experiência como {context.agent_name.lower()},",
            f" Falando por mim ({context.agent_name.lower()}),",
            ""  # Sem contexto pessoal na maioria das vezes
        ]
        
        if random.random() < 0.3:  # 30% de chance de adicionar toque pessoal
            personal = random.choice(personal_touches)
            if personal:
                base_review = personal + " " + base_review.lower()
        
        return base_review
    
    def analyze_with_leia(self, review_text: str) -> Optional[Dict]:
        """
        Analisa o sentimento de uma review usando LeIA.
        
        Returns:
            Dict com scores LeIA ou None se LeIA não estiver disponível
        """
        if not self.leia_analyzer:
            return None
        
        try:
            # LeIA retorna um dict com scores
            leia_scores = self.leia_analyzer.polarity_scores(review_text)
            
            logger.info(f"LeIA analysis: {leia_scores}")
            
            return {
                'compound': leia_scores.get('compound', 0.0),
                'pos': leia_scores.get('pos', 0.0),
                'neu': leia_scores.get('neu', 0.0),
                'neg': leia_scores.get('neg', 0.0),
                'analyzed_text': review_text
            }
            
        except Exception as e:
            logger.error(f"Erro na análise LeIA: {e}")
            return None
    
    def combine_leia_with_context(
        self,
        leia_result: Optional[Dict],
        context_sentiment: float,
        weight_leia: float = 0.6,
        weight_context: float = 0.4
    ) -> float:
        """
        Combina o resultado do LeIA com nossa análise contextual.
        
        Args:
            leia_result: Resultado da análise LeIA
            context_sentiment: Sentimento calculado por nossa lógica
            weight_leia: Peso do LeIA na decisão final
            weight_context: Peso do contexto na decisão final
        
        Returns:
            Sentimento final combinado
        """
        if not leia_result:
            # Se LeIA não disponível, usar apenas contexto
            return context_sentiment
        
        # Extrair sentimento composto do LeIA (-1 a 1)
        leia_compound = leia_result.get('compound', 0.0)
        
        # Combinar os sentimentos com pesos
        combined_sentiment = (
            leia_compound * weight_leia +
            context_sentiment * weight_context
        )
        
        # Garantir que está no range [-1, 1]
        return max(-1.0, min(1.0, combined_sentiment))

    async def analyze_consumption(
        self, 
        context: ConsumptionContext
    ) -> SentimentAnalysis:
        """
        Analisa o consumo de um artefato e gera sentimento.
        
        Este é o método principal chamado quando um agente consome um artefato.
        """
        logger.info(f"Analisando consumo: {context.agent_name} -> {context.artifact_name}")
        
        # 1. Categorizar o artefato
        category = self.categorize_artifact(
            context.artifact_name, 
            context.artifact_description
        )
        
        # 2. Calcular impactos individuais
        quality_impact = self.calculate_quality_impact(
            context.artifact_quality, 
            category
        )
        
        price_impact = self.calculate_price_impact(
            context.purchase_price,
            context.artifact_quality,
            context.agent_wallet_balance
        )
        
        expectation_impact = self.calculate_expectation_impact(
            context.agent_current_sentiment
        )
        
        # 3. Aplicar efeito base da categoria
        base_effect = self.sentiment_effects[category]["base_effect"]
        
        # 4. Combinar todos os fatores
        raw_sentiment = (
            base_effect +
            quality_impact * 0.4 +
            price_impact * 0.3 +
            expectation_impact * 0.2 +
            random.uniform(-0.1, 0.1)  # Fator aleatório pequeno
        )
        
        # 5. Normalizar para range [-1, 1]
        final_sentiment = max(-1.0, min(1.0, raw_sentiment))
        
        # 6. Calcular magnitude do impacto
        impact_magnitude = abs(final_sentiment - context.agent_current_sentiment)
        impact_magnitude = min(1.0, impact_magnitude)
        
        # 7. Gerar categoria emocional e reasoning
        emotion_category = self.generate_emotion_category(final_sentiment)
        reasoning = self.generate_reasoning(
            context, category, quality_impact, 
            price_impact, expectation_impact, final_sentiment
        )
        
        # 8. Gerar review naturalística
        generated_review = self.generate_naturalistic_review(
            context, category, quality_impact, price_impact, final_sentiment
        )
        
        # 9. Analisar review com LeIA
        leia_analysis = self.analyze_with_leia(generated_review)
        
        # 10. Combinar resultado LeIA com análise contextual
        final_sentiment = self.combine_leia_with_context(
            leia_analysis,
            final_sentiment,
            weight_leia=0.6,
            weight_context=0.4
        )
        
        # 11. Log da análise
        logger.info(f"Sentimento gerado: {final_sentiment:.2f} ({emotion_category})")
        logger.info(f"Impactos - Qualidade: {quality_impact:.2f}, Preço: {price_impact:.2f}, Expectativa: {expectation_impact:.2f}")
        
        return SentimentAnalysis(
            sentiment_score=final_sentiment,
            emotion_category=emotion_category,
            reasoning=reasoning,
            impact_magnitude=impact_magnitude,
            leia_analysis=leia_analysis,
            generated_review=generated_review
        )


# Função utilitária para consumo direto do artefato
async def consume_artifact_with_sentiment(
    inventory_id: str,
    agent_data: Dict,
    artifact_data: Dict,
    sentiment_service: Optional[SentimentService] = None
) -> Dict:
    """
    Função de conveniência que combina consumo + análise de sentimento.
    
    Args:
        inventory_id: ID do item no inventário
        agent_data: Dados do agente
        artifact_data: Dados do artefato
        sentiment_service: Instância do serviço (opcional, criará uma nova se None)
    
    Returns:
        Dict com resultado do consumo e análise de sentimento
    """
    if sentiment_service is None:
        sentiment_service = SentimentService()
    
    # Preparar contexto
    context = ConsumptionContext(
        agent_id=agent_data.get('id'),
        agent_name=agent_data.get('name'),
        artifact_name=artifact_data.get('name'),
        artifact_description=artifact_data.get('description'),
        artifact_quality=artifact_data.get('quality_score', 0.5),
        purchase_price=artifact_data.get('purchase_price', 0.0),
        agent_current_sentiment=agent_data.get('sentiment_score', 0.0),
        agent_wallet_balance=agent_data.get('wallet_balance', 0.0)
    )
    
    # Analisar sentimento
    sentiment_analysis = await sentiment_service.analyze_consumption(context)
    
    return {
        'inventory_id': inventory_id,
        'sentiment_analysis': sentiment_analysis,
        'consumption_context': context
    }


if __name__ == "__main__":
    """Teste básico do SentimentService"""
    
    async def test_sentiment_service():
        service = SentimentService()
        
        # Teste 1: Agente comprando Fruta da Calma
        context1 = ConsumptionContext(
            agent_id="test-agent-1",
            agent_name="Agente Teste",
            artifact_name="Fruta da Calma",
            artifact_description="Uma fruta que acalma a mente e traz foco.",
            artifact_quality=0.75,
            purchase_price=15.50,
            agent_current_sentiment=0.0,
            agent_wallet_balance=1000.0
        )
        
        result1 = await service.analyze_consumption(context1)
        print(f"Teste 1 - Sentimento: {result1.sentiment_score:.2f}")
        print(f"Emoção: {result1.emotion_category}")
        print(f"Reasoning: {result1.reasoning}\n")
        
        # Teste 2: Mesmo agente comprando algo caro
        context2 = ConsumptionContext(
            agent_id="test-agent-1",
            agent_name="Agente Teste",
            artifact_name="Orbe do Conhecimento Efêmero",
            artifact_description="Sussurra fatos esquecidos por um curto período.",
            artifact_quality=0.45,
            purchase_price=75.25,
            agent_current_sentiment=result1.sentiment_score,  # Usa resultado anterior
            agent_wallet_balance=984.50
        )
        
        result2 = await service.analyze_consumption(context2)
        print(f"Teste 2 - Sentimento: {result2.sentiment_score:.2f}")
        print(f"Emoção: {result2.emotion_category}")
        print(f"Reasoning: {result2.reasoning}")
    
    # Executar teste
    asyncio.run(test_sentiment_service())
