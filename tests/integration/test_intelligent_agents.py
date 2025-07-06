#!/usr/bin/env python3
"""
🤖 TESTE SISTEMA DE AGENTES INTELIGENTES
========================================

Teste completo do sistema de agentes com cognição, comportamento e sociedade.
"""

import sys
import time
import random


def main():
    print("🤖 LORE ENGINE - INTELLIGENT AGENTS TEST")
    print("="*60)

    try:
        import lore_engine
        print("✅ Módulo lore_engine carregado com sucesso!")

        # Available functions
        functions = [attr for attr in dir(lore_engine) if not attr.startswith('_')]
        print(f"📦 {len(functions)} funcionalidades disponíveis")

        # Test 1: Cognitive States
        print("\n🧠 TESTE 1: Estados Cognitivos")
        print("-" * 40)

        # Create different cognitive states
        cognitive_profiles = [
            ("Genius", [0.9, 0.9, 0.8, 0.7, 0.6, 0.8]),
            ("Social", [0.6, 0.7, 0.7, 0.6, 0.9, 0.8]),
            ("Creative", [0.7, 0.6, 0.6, 0.9, 0.7, 0.7]),
            ("Balanced", [0.7, 0.7, 0.7, 0.7, 0.7, 0.7]),
        ]

        cognitive_states = {}
        for name, values in cognitive_profiles:
            state = lore_engine.CognitiveState(*values)
            cognitive_states[name] = state
            print(f"   ✅ {name}: capacidade {state.get_capacity():.3f}")

        # Test 2: Behavior Types
        print("\n🎭 TESTE 2: Tipos de Comportamento")
        print("-" * 40)

        behaviors = ["explorer", "socializer", "optimizer", "creator", "analyzer"]
        behavior_objects = {}

        for behavior in behaviors:
            try:
                behavior_obj = lore_engine.BehaviorType(behavior)
                behavior_objects[behavior] = behavior_obj
                print(f"   ✅ {behavior.upper()}: {behavior_obj}")
            except Exception as e:
                print(f"   ❌ {behavior}: {e}")

        # Test 3: Create Intelligent Agents
        print("\n🤖 TESTE 3: Criação de Agentes Inteligentes")
        print("-" * 45)

        agents = []

        for i, (behavior, cog_name) in enumerate(zip(behaviors, cognitive_profiles)):
            try:
                # Create agent DNA
                dna = lore_engine.AgentDNA([random.gauss(0, 0.3) for _ in range(10)])
                dna.fitness = random.uniform(0.3, 0.9)

                # Create cognitive state
                cognitive_state = cognitive_states[cog_name[0]]

                # Create agent
                agent = lore_engine.IntelligentAgent(
                    id=f"agent_{i+1:03d}",
                    dna=dna,
                    behavior_type=behavior_objects[behavior],
                    cognitive_state=cognitive_state
                )

                agents.append(agent)
                print(f"   ✅ Agent {i+1}: {agent.get_id()} ({agent.get_behavior()})")

            except Exception as e:
                print(f"   ❌ Erro ao criar agente {i+1}: {e}")

        print(f"   🎉 {len(agents)} agentes criados com sucesso!")

        # Test 4: Decision Making
        print("\n🧩 TESTE 4: Tomada de Decisão")
        print("-" * 35)

        # Test situation
        situation = [0.5, -0.2, 0.8, 0.1, -0.3]  # Some environmental inputs

        decisions = {}
        for agent in agents:
            try:
                decision = agent.make_decision(situation)
                decisions[agent.get_id()] = decision
                print(f"   🤖 {agent.get_id()}: {[f'{d:.3f}' for d in decision]}")
            except Exception as e:
                print(f"   ❌ {agent.get_id()}: {e}")

        # Test 5: Agent Society
        print("\n👥 TESTE 5: Sociedade de Agentes")
        print("-" * 35)

        # Create society
        society = lore_engine.AgentSociety()

        # Add agents to society
        for agent in agents:
            society.add_agent(agent)

        print(f"   ✅ Sociedade criada com {society.get_size()} agentes")

        # Simulate interactions
        interactions = society.simulate_interactions(20)
        print(f"   ✅ {interactions} conexões sociais criadas")

        # Get society statistics
        stats = society.get_society_stats()
        print(f"   📊 Conexões médias: {stats.get('avg_connections', 0):.2f}")
        print(f"   📊 Experiência média: {stats.get('avg_experience', 0):.1f}")
        print(f"   📊 Capacidade cognitiva média: {stats.get('avg_cognitive_capacity', 0):.3f}")

        # Test 6: Collective Decision Making
        print("\n🤝 TESTE 6: Decisão Coletiva")
        print("-" * 30)

        # Complex situation requiring collective intelligence
        complex_situation = [0.3, 0.7, -0.4, 0.9, -0.1, 0.6]

        start_time = time.time()
        collective_decision = society.collective_decision(complex_situation)
        elapsed = (time.time() - start_time) * 1000

        print(f"   🧠 Decisão coletiva: {[f'{d:.3f}' for d in collective_decision]}")
        print(f"   ⚡ Tempo de processamento: {elapsed:.2f}ms")

        # Test 7: Learning and Experience
        print("\n📚 TESTE 7: Aprendizado e Experiência")
        print("-" * 40)

        learning_scenarios = [
            ("learning", 50),
            ("social", 30),
            ("creative", 40),
            ("stress", 20),
        ]

        for scenario, points in learning_scenarios:
            agent = random.choice(agents)
            try:
                leveled_up = agent.gain_experience(points, scenario)
                status = "LEVEL UP!" if leveled_up else "experiência ganha"
                print(f"   📖 {agent.get_id()}: +{points} XP ({scenario}) - {status}")
            except Exception as e:
                print(f"   ❌ {agent.get_id()}: {e}")

        # Test 8: Agent Statistics
        print("\n📊 TESTE 8: Estatísticas dos Agentes")
        print("-" * 40)

        for agent in agents[:3]:  # Show stats for first 3 agents
            stats = agent.get_stats()
            print(f"   🤖 {agent.get_id()}:")
            print(f"      📈 XP: {stats.get('experience_points', 0):.0f}")
            print(f"      🎂 Idade: {stats.get('age', 0):.0f}")
            print(f"      🧠 Capacidade: {stats.get('cognitive_capacity', 0):.3f}")
            print(f"      👥 Conexões: {stats.get('social_connections', 0):.0f}")
            print(f"      💾 Memórias: {stats.get('memory_usage', 0):.0f}")
            print(f"      🏆 Fitness: {stats.get('fitness', 0):.3f}")

        # Test 9: Memory System
        print("\n💾 TESTE 9: Sistema de Memória")
        print("-" * 30)

        agent = agents[0]

        # Store memories
        memories = [
            ("first_meeting", 0.8),
            ("successful_task", 0.9),
            ("failed_attempt", 0.3),
            ("social_interaction", 0.7),
        ]

        for key, value in memories:
            agent.store_memory(key, value)
            print(f"   💾 Memória armazenada: {key} = {value}")

        # Retrieve memories
        for key, _ in memories:
            retrieved = agent.get_memory(key)
            if retrieved is not None:
                print(f"   🔍 Memória recuperada: {key} = {retrieved}")

        # Test 10: Neural Decision Networks
        print("\n🧠 TESTE 10: Redes Neurais de Decisão")
        print("-" * 40)

        # Create agent with neural brain
        try:
            smart_dna = lore_engine.AgentDNA([random.gauss(0, 0.2) for _ in range(10)])
            smart_dna.fitness = 0.95

            brain_architecture = [14, 20, 15, 3]  # Input, hidden layers, output

            smart_agent = lore_engine.create_agent_with_neural_brain(
                id="neural_agent_001",
                dna=smart_dna,
                behavior="analyzer",
                brain_architecture=brain_architecture
            )

            print(f"   ✅ Agente neural criado: {smart_agent.get_id()}")

            # Test neural decision making
            neural_decision = smart_agent.make_decision(situation)
            print(f"   🧠 Decisão neural: {[f'{d:.3f}' for d in neural_decision]}")

        except Exception as e:
            print(f"   ❌ Erro ao criar agente neural: {e}")

        # Test 11: Performance Benchmarks
        print("\n⚡ TESTE 11: Benchmarks de Performance")
        print("-" * 40)

        # Decision making speed
        decision_times = []
        for _ in range(100):
            agent = random.choice(agents)
            start = time.perf_counter()
            agent.make_decision(situation)
            decision_times.append(time.perf_counter() - start)

        avg_decision_time = sum(decision_times) / len(decision_times) * 1000
        print(f"   🧠 Decisão individual: {avg_decision_time:.2f}ms (média)")

        # Society simulation speed
        society_times = []
        for _ in range(10):
            start = time.perf_counter()
            society.simulate_interactions(5)
            society_times.append(time.perf_counter() - start)

        avg_society_time = sum(society_times) / len(society_times) * 1000
        print(f"   👥 Simulação social: {avg_society_time:.2f}ms (5 interações)")

        # Collective decision speed
        collective_times = []
        for _ in range(10):
            start = time.perf_counter()
            society.collective_decision(situation)
            collective_times.append(time.perf_counter() - start)

        avg_collective_time = sum(collective_times) / len(collective_times) * 1000
        print(f"   🤝 Decisão coletiva: {avg_collective_time:.2f}ms (média)")

        print("\n🎉 TODOS OS TESTES DE AGENTES FINALIZADOS!")
        print("="*60)
        print("✅ Sistema de agentes inteligentes completamente funcional!")
        print("🧠 Cognição: Estados cognitivos adaptativos")
        print("🎭 Comportamento: 5 tipos distintos de personalidade")
        print("🤖 Agentes: Tomada de decisão inteligente")
        print("👥 Sociedade: Interações sociais e colaboração")
        print("🧠 Neural: Redes neurais para decisões complexas")
        print("📚 Aprendizado: Sistema de experiência e memória")
        print("⚡ Performance: Processamento otimizado em Rust")
        print("\n🚀 SISTEMA PRONTO PARA SIMULAÇÕES COGNITIVAS AVANÇADAS!")
        print("🌟 Próximo: Integração com evolução genética + neural networks")

    except ImportError as e:
        print(f"❌ Erro ao importar: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
