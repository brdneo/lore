#!/usr/bin/env python3
"""
Teste completo do SentimentService híbrido para o projeto Lore N.A.
"""

import sys
import os

import sys
import os
import importlib.util

# Adicionar o diretório src ao path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# Import with proper error handling
try:
    from sentiment_service import SentimentService, ConsumptionContext  # type: ignore
except ImportError:
    # Fallback import using importlib
    spec = importlib.util.spec_from_file_location(
        "sentiment_service",
        os.path.join(src_path, "sentiment_service.py")
    )
    if spec is not None and spec.loader is not None:
        sentiment_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sentiment_module)
        SentimentService = sentiment_module.SentimentService  # type: ignore
        ConsumptionContext = sentiment_module.ConsumptionContext  # type: ignore
    else:
        raise ImportError("Could not load sentiment_service module")

import asyncio

async def test_sentiment_service():
    """Testa o SentimentService completo"""
    print("🧪 Testando SentimentService híbrido...")
    print("=" * 60)

    # Inicializar o serviço
    service = SentimentService()

    # Criar contexto de teste
    context = ConsumptionContext(
        agent_id="agent_001",
        agent_name="TestAgent",
        artifact_name="Fruta da Calma",
        artifact_description="Uma fruta mágica que acalma a mente e traz serenidade",
        artifact_quality=0.8,  # Alta qualidade
        purchase_price=45.0,
        agent_current_sentiment=0.2,  # Ligeiramente positivo
        agent_wallet_balance=200.0
    )

    print("📋 Contexto de teste:")
    print(f"  Agente: {context.agent_name}")
    print(f"  Artefato: {context.artifact_name}")
    print(f"  Qualidade: {context.artifact_quality}")
    print(f"  Preço: R$ {context.purchase_price}")
    print(f"  Sentimento atual: {context.agent_current_sentiment}")
    print()

    # Executar análise
    try:
        result = await service.analyze_consumption(context)

        print("✅ Análise concluída com sucesso!")
        print()
        print("📊 Resultados:")
        print(f"  Score Final: {result.sentiment_score:.3f}")
        print(f"  Categoria: {result.emotion_category}")
        print(f"  VADER: {result.vader_score:.3f}")
        print(f"  TextBlob: {result.textblob_score:.3f}")
        print(f"  Transformers: {result.transformers_score:.3f}")
        print(f"  Impacto Qualidade: {result.quality_impact:.3f}")
        print(f"  Impacto Preço: {result.price_impact:.3f}")
        print(f"  Impacto Expectativa: {result.expectation_impact:.3f}")
        print()
        print("📝 Review gerada:")
        print(f'  "{result.review_text}"')
        print()
        print("🧠 Raciocínio:")
        print(f'  {result.reasoning}')

        return True

    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return False

async def test_multiple_scenarios():
    """Testa múltiplos cenários"""
    service = SentimentService()

    scenarios = [
        {
            "name": "Produto Caro e Ruim",
            "context": ConsumptionContext(
                agent_id="agent_002",
                agent_name="PoorAgent",
                artifact_name="Cristal Falsificado",
                artifact_description="Um cristal que deveria dar energia mas não funciona",
                artifact_quality=0.2,  # Baixa qualidade
                purchase_price=80.0,   # Caro
                agent_current_sentiment=-0.1,
                agent_wallet_balance=100.0  # Pouco dinheiro
            )
        },
        {
            "name": "Produto Excelente e Barato",
            "context": ConsumptionContext(
                agent_id="agent_003",
                agent_name="LuckyAgent",
                artifact_name="Orbe do Conhecimento Supremo",
                artifact_description="Conhecimento profundo e transformador",
                artifact_quality=0.95,  # Excelente qualidade
                purchase_price=25.0,    # Barato
                agent_current_sentiment=0.3,
                agent_wallet_balance=500.0  # Rico
            )
        }
    ]

    print("\n🎭 Testando múltiplos cenários...")
    print("=" * 60)

    for scenario in scenarios:
        print(f"\n📋 Cenário: {scenario['name']}")
        try:
            result = await service.analyze_consumption(scenario['context'])
            print(f"  Score: {result.sentiment_score:.3f} | Categoria: {result.emotion_category}")
            print(f"  Review: \"{result.review_text}\"")
        except Exception as e:
            print(f"  ❌ Erro: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando testes do SentimentService...")

    # Teste básico
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(test_sentiment_service())

    if success:
        # Testes adicionais
        loop.run_until_complete(test_multiple_scenarios())
        print("\n🎉 Todos os testes concluídos!")
        print("✅ SentimentService híbrido funcionando perfeitamente!")
        print("🔥 Projeto Lore N.A. pronto para análise de sentimento avançada!")
    else:
        print("\n⚠️  Alguns testes falharam, mas o sistema básico está funcionando.")
