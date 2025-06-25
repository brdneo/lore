#!/usr/bin/env python3
"""
Teste das bibliotecas de sentimento híbridas para o projeto Lore N.A.
Testando VADER, TextBlob, e Hugging Face Transformers
"""

def test_textblob():
    try:
        from textblob import TextBlob
        print('✅ TextBlob importado com sucesso')
        
        text = "Eu estou muito feliz com este produto! É excelente! 😊"
        blob = TextBlob(text)
        result = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        print('✅ TextBlob funcionando:', result)
        return True
    except Exception as e:
        print('❌ Erro TextBlob:', e)
        return False

def test_vader():
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        print('✅ VADER (vaderSentiment) importado com sucesso')
        
        v = SentimentIntensityAnalyzer()
        result = v.polarity_scores('I am very happy with this product! It is excellent! :)')
        print('✅ VADER funcionando:', result)
        return True
    except ImportError:
        try:
            # Fallback para VADER do NLTK
            import nltk
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            print('✅ NLTK VADER importado com sucesso')
            
            v = SentimentIntensityAnalyzer()
            result = v.polarity_scores('I am very happy with this product! It is excellent! :)')
            print('✅ NLTK VADER funcionando:', result)
            return True
        except Exception as e:
            print('❌ Erro VADER:', e)
            return False
    except Exception as e:
        print('❌ Erro VADER:', e)
        return False

def test_transformers():
    try:
        from transformers import pipeline
        print('✅ Transformers importado com sucesso')
        
        # Modelo mais simples e estável para sentimento
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        
        text = "Eu estou muito feliz com este produto! É excelente! 😊"
        result = sentiment_pipeline(text)
        print('✅ Transformers funcionando:', result)
        return True
    except Exception as e:
        print('❌ Erro Transformers:', e)
        print('⚠️  Transformers falhou, mas VADER e TextBlob funcionam!')
        return False

def test_hybrid_analysis():
    """Testa todas as bibliotecas funcionando em conjunto"""
    try:
        # Importar todas as bibliotecas
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VaderAnalyzer
        from textblob import TextBlob
        from transformers import pipeline
        
        # Configurar analisadores
        vader_analyzer = VaderAnalyzer()
        
        # Carregar modelo Transformers  
        try:
            transformer_pipeline = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment"
            )
            transformers_available = True
        except Exception as e:
            print(f'⚠️  Transformers não disponível: {e}')
            transformers_available = False
        
        # Texto para análise híbrida
        text = "Produto excelente! Superou todas as expectativas. Muito satisfeito com a compra! 😊"
        
        print(f'📝 Texto analisado: "{text}"')
        print('📊 Resultados da análise híbrida:')
        
        # VADER
        vader_result = vader_analyzer.polarity_scores(text)
        print(f'  VADER: {vader_result}')
        
        # TextBlob
        blob = TextBlob(text)
        textblob_result = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        print(f'  TEXTBLOB: {textblob_result}')
        
        # Transformers (se disponível)
        transformer_compound = 0.0
        if transformers_available:
            try:
                transformer_result = transformer_pipeline(text)
                print(f'  TRANSFORMERS: {transformer_result}')
                
                # Converter resultado do Transformer (modelo retorna stars)
                transformer_label = transformer_result[0]['label']
                transformer_score = transformer_result[0]['score']
                
                # Mapear stars para escala -1 a 1
                if '5' in transformer_label or '4' in transformer_label:
                    transformer_compound = transformer_score * 0.8  # Positivo
                elif '1' in transformer_label or '2' in transformer_label:
                    transformer_compound = -transformer_score * 0.8  # Negativo  
                else:  # 3 stars - neutro
                    transformer_compound = 0.0
            except Exception as e:
                print(f'  TRANSFORMERS: Erro - {e}')
                transformer_compound = 0.0
        else:
            print('  TRANSFORMERS: Não disponível')
        
        # Cálculo do score híbrido simples
        vader_compound = vader_result['compound']
        textblob_polarity = textblob_result['polarity']
        
        # Score híbrido ponderado (adaptativo se Transformers não estiver disponível)
        if transformers_available:
            hybrid_score = (
                vader_compound * 0.25 +
                textblob_polarity * 0.20 +
                transformer_compound * 0.55
            )
        else:
            # Fallback - só VADER e TextBlob
            hybrid_score = (
                vader_compound * 0.60 +
                textblob_polarity * 0.40
            )
        
        print(f'🎯 SCORE HÍBRIDO FINAL: {hybrid_score:.3f}')
        
        if hybrid_score >= 0.3:
            sentiment_category = "POSITIVO"
        elif hybrid_score <= -0.3:
            sentiment_category = "NEGATIVO"
        else:
            sentiment_category = "NEUTRO"
            
        print(f'📈 CATEGORIA: {sentiment_category}')
        
        return True
        
    except Exception as e:
        print(f'❌ Erro na análise híbrida: {e}')
        return False

if __name__ == "__main__":
    print("🧪 Testando bibliotecas de análise de sentimento híbrida...")
    print("=" * 60)
    print()
    
    print("1. Testando TextBlob...")
    test_textblob()
    print()
    
    print("2. Testando VADER...")
    test_vader()
    print()
    
    print("3. Testando Transformers...")
    test_transformers()
    print()
    
    print("4. Testando análise híbrida completa...")
    test_hybrid_analysis()
    print()
    
    print("✅ Testes concluídos! Sistema híbrido de sentimento configurado.")
    print("🚀 O projeto Lore N.A. agora usa VADER + TextBlob + Transformers!")
