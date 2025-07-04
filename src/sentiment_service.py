"""
SentimentService - Análise de Sentimento Robusta para o MVM
Implementa o loop de feedback emocional: Ação -> Resultado -> Sentimento -> Novo Estado

Abordagem Híbrida Multi-Biblioteca:
- VADER: Análise rápida e otimizada para textos informais/redes sociais
- TextBlob: Análise de polaridade e subjetividade com simplicidade
- Transformers: Modelos estado-da-arte para máxima precisão contextual
- Análise Contextual: Lógica baseada em qualidade, preço e expectativas

Fluxo:
1. Agente compra artefato (registrado no inventário)
2. Agente decide consumir o artefato
3. SentimentService simula experiência e gera review em português
4. Análise híbrida com múltiplas bibliotecas
5. Combina resultados com fatores contextuais
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

# VADER - Otimizado para textos informais e redes sociais
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VaderAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    try:
        # Fallback para VADER do NLTK
        import nltk
        from nltk.sentiment.vader import SentimentIntensityAnalyzer as VaderAnalyzer
        VADER_AVAILABLE = True
    except ImportError:
        VADER_AVAILABLE = False
        logging.warning("VADER não disponível")

# TextBlob - Análise simples de polaridade e subjetividade
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logging.warning("TextBlob não disponível")

# Hugging Face Transformers - Estado da arte para análise contextual
try:
    from transformers import pipeline  # type: ignore
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers não disponível")
    pipeline = None  # type: ignore
    
    # Fallback para NLTK
    try:
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
    """Contexto da experiência de consumo do agente"""
    agent_id: str
    agent_name: str
    artifact_name: str
    artifact_description: str
    artifact_quality: float  # 0.0 a 1.0
    purchase_price: float
    agent_current_sentiment: float  # -1.0 a 1.0 (estado emocional atual)
    agent_wallet_balance: float


@dataclass
class SentimentResult:
    """Resultado completo da análise de sentimento híbrida"""
    sentiment_score: float  # -1.0 a 1.0
    emotion_category: str   # happy, neutral, disappointed, etc.
    reasoning: str          # Explicação detalhada
    vader_score: float      # Score do VADER
    textblob_score: float   # Score do TextBlob
    transformers_score: float  # Score do modelo Transformer
    quality_impact: float   # Impacto da qualidade
    price_impact: float     # Impacto do preço
    expectation_impact: float  # Impacto das expectativas
    review_text: str        # Review gerada em português


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
    hybrid_analysis: Optional[Dict] = None  # Análise combinada dos três métodos
    analysis_method: str = "hybrid"  # Método usado: leia, nltk, hybrid, context_only


class SentimentService:
    """
    Serviço principal de análise de sentimento.
    
    Algoritmo de Sentimento v3.0 (Híbrido Multi-Biblioteca):
    - VADER: Análise rápida para textos informais
    - TextBlob: Polaridade e subjetividade
    - Transformers: Análise contextual estado-da-arte
    - Quality Impact: Qualidade do item vs expectativa
    - Price Impact: Preço pago vs valor percebido
    - Expectation Impact: Sentimento atual influencia expectativa
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Inicializar analisadores disponíveis
        self.analyzers = {}
        
        # VADER - Análise otimizada para redes sociais
        if VADER_AVAILABLE:
            try:
                self.analyzers['vader'] = VaderAnalyzer()
                self.logger.info("VADER inicializado com sucesso")
            except Exception as e:
                self.logger.warning(f"Erro ao inicializar VADER: {e}")
        
        # TextBlob - Análise de polaridade simples
        if TEXTBLOB_AVAILABLE:
            try:
                # TextBlob não precisa inicialização específica
                self.analyzers['textblob'] = True
                self.logger.info("TextBlob disponível")
            except Exception as e:
                self.logger.warning(f"Erro com TextBlob: {e}")
        
        # Transformers - Modelo estado-da-arte (carregamento lazy)
        self.transformer_pipeline = None
        if TRANSFORMERS_AVAILABLE:
            self.logger.info("Transformers disponível (carregamento sob demanda)")
        
        # Configuração de pesos para análise híbrida
        self.weights = {
            'vader': 0.25,        # Análise rápida
            'textblob': 0.20,     # Polaridade/subjetividade  
            'transformers': 0.35, # Estado-da-arte
            'quality': 0.15,      # Experiência real
            'price': 0.03,        # Contexto econômico
            'expectation': 0.02   # Estado emocional
        }

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
        
        self.logger.info(f"SentimentService inicializado com {len(self.analyzers)} analisadores")
    
    def _get_transformer_pipeline(self):
        """Carrega o modelo Transformer sob demanda para economizar recursos"""
        if self.transformer_pipeline is None and TRANSFORMERS_AVAILABLE and pipeline:
            try:
                # Modelo multilingual estável para sentimento 
                self.transformer_pipeline = pipeline(  # type: ignore
                    "sentiment-analysis",
                    model="nlptown/bert-base-multilingual-uncased-sentiment"
                )
                self.logger.info("Modelo Transformer carregado com sucesso")
            except Exception as e:
                self.logger.warning(f"Erro ao carregar modelo Transformer: {e}")
                # Tentar modelo alternativo mais simples
                try:
                    self.transformer_pipeline = pipeline("sentiment-analysis")  # type: ignore
                    self.logger.info("Modelo Transformer padrão carregado")
                except Exception as e2:
                    self.logger.warning(f"Erro ao carregar modelo padrão: {e2}")
        return self.transformer_pipeline
    
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

    async def analyze_consumption(self, context: ConsumptionContext) -> SentimentResult:
        """
        Método principal que implementa o loop de feedback de sentimento.
        
        Fluxo híbrido v3.0:
        1. Gera review naturalística da experiência
        2. Análise com VADER, TextBlob e Transformers
        3. Calcula impactos contextuais (qualidade, preço, expectativa)
        4. Combina análises para sentimento final
        5. Retorna resultado completo
        """
        try:
            # 1. Gerar review naturalística baseada na experiência
            review_text = self._generate_review_text(context)
            self.logger.info(f"Review gerada: {review_text}")
            
            # 2. Análise híbrida de sentimento com múltiplas bibliotecas
            analysis_results = {}
            
            # VADER - Análise rápida e eficiente
            if 'vader' in self.analyzers:
                try:
                    vader_result = self.analyzers['vader'].polarity_scores(review_text)
                    analysis_results['vader'] = vader_result['compound']
                    self.logger.info(f"VADER análise: {vader_result}")
                except Exception as e:
                    self.logger.warning(f"Erro na análise VADER: {e}")
                    analysis_results['vader'] = 0.0
            
            # TextBlob - Polaridade e subjetividade
            if 'textblob' in self.analyzers:
                try:
                    blob = TextBlob(review_text)
                    # TextBlob retorna polaridade entre -1 e 1
                    analysis_results['textblob'] = blob.sentiment.polarity
                    analysis_results['textblob_subjectivity'] = blob.sentiment.subjectivity
                    self.logger.info(f"TextBlob análise: polaridade={blob.sentiment.polarity:.3f}, subjetividade={blob.sentiment.subjectivity:.3f}")
                except Exception as e:
                    self.logger.warning(f"Erro na análise TextBlob: {e}")
                    analysis_results['textblob'] = 0.0
            
            # Transformers - Estado da arte (carregamento sob demanda)
            analysis_results['transformers'] = 0.0
            if TRANSFORMERS_AVAILABLE:
                try:
                    transformer_pipeline = self._get_transformer_pipeline()
                    if transformer_pipeline:
                        transformer_result = transformer_pipeline(review_text)
                        # Converter resultado para escala -1 a 1
                        analysis_results['transformers'] = self._parse_transformer_result(transformer_result)
                        self.logger.info(f"Transformers análise: {analysis_results['transformers']:.3f}")
                except Exception as e:
                    self.logger.warning(f"Erro na análise Transformers: {e}")
                    analysis_results['transformers'] = 0.0
            
            # 3. Calcular impactos contextuais
            artifact_category = self.categorize_artifact(context.artifact_name, context.artifact_description)
            quality_impact = self.calculate_quality_impact(context.artifact_quality, artifact_category)
            price_impact = self.calculate_price_impact(context.purchase_price, context.artifact_quality, context.agent_wallet_balance)
            expectation_impact = self.calculate_expectation_impact(context.agent_current_sentiment)
            
            # 4. Combinar análises com pesos configuráveis
            final_sentiment = self._combine_sentiment_scores_v3(
                analysis_results=analysis_results,
                quality_impact=quality_impact,
                price_impact=price_impact,
                expectation_impact=expectation_impact
            )
            
            # 5. Gerar categorias e reasoning
            emotion_category = self.generate_emotion_category(final_sentiment)
            reasoning = self.generate_reasoning(
                context, artifact_category, quality_impact, price_impact, 
                expectation_impact, final_sentiment
            )
            
            # 6. Retornar resultado completo
            return SentimentResult(
                sentiment_score=final_sentiment,
                emotion_category=emotion_category,
                reasoning=reasoning,
                vader_score=analysis_results.get('vader', 0.0),
                textblob_score=analysis_results.get('textblob', 0.0),
                transformers_score=analysis_results.get('transformers', 0.0),
                quality_impact=quality_impact,
                price_impact=price_impact,
                expectation_impact=expectation_impact,
                review_text=review_text
            )
            
        except Exception as e:
            self.logger.error(f"Erro na análise de sentimento: {e}")
            # Fallback básico em caso de erro
            return SentimentResult(
                sentiment_score=0.0,
                emotion_category="neutral",
                reasoning=f"Erro na análise de sentimento para {context.artifact_name}",
                vader_score=0.0,
                textblob_score=0.0,
                transformers_score=0.0,
                quality_impact=0.0,
                price_impact=0.0,
                expectation_impact=0.0,
                review_text=""
            )

    def _generate_review_text(self, context: ConsumptionContext) -> str:
        """
        Gera uma review naturalística em português baseada na experiência do agente.
        Simula como um usuário real descreveria sua experiência com o artefato.
        """
        artifact_name = context.artifact_name
        artifact_description = context.artifact_description
        agent_name = context.agent_name
        quality = context.artifact_quality
        price = context.purchase_price
        
        # Templates de review baseados na qualidade
        if quality >= 0.8:
            templates = [
                f"Comprei o {artifact_name} e estou muito satisfeito! {artifact_description} Realmente funciona como prometido.",
                f"O {artifact_name} superou minhas expectativas. Vale cada centavo que paguei. {artifact_description}",
                f"Excelente compra! O {artifact_name} é incrível. {artifact_description} Recomendo muito!"
            ]
        elif quality >= 0.6:
            templates = [
                f"O {artifact_name} é bom, mas nada excepcional. {artifact_description} Atende ao prometido.",
                f"Comprei o {artifact_name} e estou satisfeito. {artifact_description} É ok pelo preço.",
                f"O {artifact_name} funciona como esperado. {artifact_description} Produto decente."
            ]
        elif quality >= 0.4:
            templates = [
                f"O {artifact_name} não é lá essas coisas. {artifact_description} Meio decepcionante.",
                f"Comprei o {artifact_name} mas não fiquei muito impressionado. {artifact_description}",
                f"O {artifact_name} é mediano. {artifact_description} Esperava mais pela descrição."
            ]
        else:
            templates = [
                f"O {artifact_name} foi uma decepção total. {artifact_description} Não funciona direito.",
                f"Que arrependimento comprar o {artifact_name}. {artifact_description} Perda de dinheiro.",
                f"O {artifact_name} é terrível. {artifact_description} Não recomendo de jeito nenhum."
            ]
        
        # Adicionar contexto de preço
        if price < 20:
            price_context = " É barato, então até que vale."
        elif price < 50:
            price_context = " O preço é justo para o que oferece."
        elif price < 100:
            price_context = " Um pouco caro, mas ok."
        else:
            price_context = " Muito caro para o que entrega."
        
        base_review = random.choice(templates)
        
        # Adicionar emoções e expressões brasileiras
        if quality >= 0.7:
            emotion_expressions = [" Adorei! 😊", " Top demais! 👏", " Amei! ❤️"]
        elif quality >= 0.5:
            emotion_expressions = [" Tá bom.", " Ok.", " Razoável."]
        else:
            emotion_expressions = [" Que decepção... 😞", " Péssimo! 😠", " Não recomendo. 👎"]
        
        emotion = random.choice(emotion_expressions)
        
        return base_review + price_context + emotion

    def _combine_sentiment_scores(
        self, 
        leia_score: float,
        vader_score: float,
        quality_impact: float,
        price_impact: float,
        expectation_impact: float
    ) -> float:
        """
        Combina todos os scores de sentimento com pesos configuráveis.
        
        Pesos padrão:
        - LeIA: 40% (análise em português)
        - VADER: 30% (fallback universal)
        - Qualidade: 20% (experiência real)
        - Preço: 7% (contexto econômico)
        - Expectativa: 3% (estado emocional)
        """
        # Pesos para combinar análises
        weights = {
            'leia': 0.40,      # LeIA tem peso maior para português
            'vader': 0.30,     # VADER como fallback
            'quality': 0.20,   # Qualidade é importante
            'price': 0.07,     # Preço tem impacto menor
            'expectation': 0.03 # Expectativa ajusta levemente
        }
        
        # Calcular score combinado
        combined_score = (
            leia_score * weights['leia'] +
            vader_score * weights['vader'] +
            quality_impact * weights['quality'] +
            price_impact * weights['price'] +
            expectation_impact * weights['expectation']
        )
        
        # Normalizar entre -1 e 1
        combined_score = max(-1.0, min(1.0, combined_score))
        
        logger.info(f"Scores combinados: LeIA={leia_score:.3f}, VADER={vader_score:.3f}, "
                   f"Quality={quality_impact:.3f}, Price={price_impact:.3f}, "
                   f"Expectation={expectation_impact:.3f} → Final={combined_score:.3f}")
        
        return combined_score

    def _parse_transformer_result(self, transformer_result) -> float:
        """
        Converte o resultado do modelo Transformer para escala -1 a 1.
        
        Suporta diferentes tipos de modelos:
        - nlptown/bert-base-multilingual-uncased-sentiment (1-5 stars)
        - modelos padrão (POSITIVE/NEGATIVE/NEUTRAL)
        """
        try:
            if not transformer_result or len(transformer_result) == 0:
                return 0.0
                
            result = transformer_result[0]  # Primeira entrada (nossa única frase)
            
            # Extrair label e score
            label = result['label'].upper()
            score = result['score']
            
            # Mapear para escala -1 a 1 baseado no tipo de modelo
            if 'STAR' in label or any(star in label for star in ['1', '2', '3', '4', '5']):
                # Modelo de estrelas (1-5)
                if '5' in label or '4' in label:
                    compound_score = score * 0.8  # Positivo forte
                elif '1' in label or '2' in label:
                    compound_score = -score * 0.8  # Negativo forte
                else:  # 3 stars
                    compound_score = 0.0  # Neutro
            else:
                # Modelo padrão (POSITIVE/NEGATIVE/NEUTRAL)
                if label == 'POSITIVE':
                    compound_score = score
                elif label == 'NEGATIVE':
                    compound_score = -score
                else:  # NEUTRAL ou outros
                    compound_score = 0.0
            
            # Normalizar para garantir que esteja entre -1 e 1
            compound_score = max(-1.0, min(1.0, compound_score))
            
            self.logger.debug(f"Transformer parsing: label={label}, score={score:.3f} -> compound={compound_score:.3f}")
            
            return compound_score
            
        except Exception as e:
            self.logger.warning(f"Erro ao processar resultado Transformer: {e}")
            return 0.0

    def _combine_sentiment_scores_v3(
        self, 
        analysis_results: Dict[str, float],
        quality_impact: float,
        price_impact: float,
        expectation_impact: float
    ) -> float:
        """
        Combina todos os scores de sentimento com pesos configuráveis v3.0.
        
        Pesos padrão:
        - VADER: 25% (análise rápida)
        - TextBlob: 20% (polaridade/subjetividade)
        - Transformers: 35% (estado-da-arte)
        - Qualidade: 15% (experiência real)
        - Preço: 3% (contexto econômico)
        - Expectativa: 2% (estado emocional)
        """
        # Calcular score combinado das bibliotecas
        library_score = (
            analysis_results.get('vader', 0.0) * self.weights['vader'] +
            analysis_results.get('textblob', 0.0) * self.weights['textblob'] +
            analysis_results.get('transformers', 0.0) * self.weights['transformers']
        )
        
        # Normalizar pelos pesos das bibliotecas usadas
        total_library_weight = (
            self.weights['vader'] + 
            self.weights['textblob'] + 
            self.weights['transformers']
        )
        
        if total_library_weight > 0:
            library_score = library_score / total_library_weight
        
        # Combinar com fatores contextuais
        combined_score = (
            library_score * (1.0 - self.weights['quality'] - self.weights['price'] - self.weights['expectation']) +
            quality_impact * self.weights['quality'] +
            price_impact * self.weights['price'] +
            expectation_impact * self.weights['expectation']
        )
        
        # Normalizar entre -1 e 1
        combined_score = max(-1.0, min(1.0, combined_score))
        
        self.logger.info(f"Scores combinados v3.0: VADER={analysis_results.get('vader', 0.0):.3f}, "
                        f"TextBlob={analysis_results.get('textblob', 0.0):.3f}, "
                        f"Transformers={analysis_results.get('transformers', 0.0):.3f}, "
                        f"Quality={quality_impact:.3f}, Price={price_impact:.3f}, "
                        f"Expectation={expectation_impact:.3f} → Final={combined_score:.3f}")
        
        return combined_score
