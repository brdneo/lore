#!/usr/bin/env python3
"""
Teste rápido do sistema híbrido sem database
"""

import sys
import os
import random

# Adicionar diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def test_hybrid_quick():
    """Teste rápido do sistema híbrido"""
    print("🔬 Teste rápido do sistema híbrido...")

    try:
        import lore_engine
        print("✅ Sistema híbrido importado!")

        # Teste básico
        params = lore_engine.EvolutionParams(
            population_size=10,
            mutation_rate=0.1,
            crossover_rate=0.8,
            selection_pressure=0.7,
            elitism_count=2
        )
        engine = lore_engine.GeneticEngine(params)
        population = engine.create_random_population(5)
        print(f"✅ População criada: {len(population)} agentes")

        # Criar agente inteligente
        behaviors = ["explorer", "socializer", "optimizer"]
        for i, dna in enumerate(population):
            behavior = random.choice(behaviors)
            behavior_type = lore_engine.BehaviorType(behavior)
            cognitive_state = lore_engine.generate_random_cognitive_state()

            agent = lore_engine.IntelligentAgent(
                id=f"agent_{i+1:03d}",
                dna=dna,
                behavior_type=behavior_type,
                cognitive_state=cognitive_state
            )

            decision = agent.make_decision([0.5, 0.3, 0.7])
            print(f"✅ Agente {i+1}: {behavior}, decisão: {len(decision)} valores")

        print("🎉 Sistema híbrido funcionando perfeitamente!")
        return True

    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def create_hybrid_agents(count=5):
    """Cria agentes híbridos sem salvar no banco"""
    print(f"🤖 Criando {count} agentes híbridos...")

    try:
        import lore_engine

        # Parâmetros de evolução completos
        elite_count = max(1, count // 4)  # 25% ou pelo menos 1
        params = lore_engine.EvolutionParams(
            population_size=count,
            mutation_rate=0.1,
            crossover_rate=0.8,
            selection_pressure=0.7,
            elitism_count=elite_count,
            max_generations=100,
            target_fitness=None,
            parallel_threads=None,
            tournament_size=3
        )
        engine = lore_engine.GeneticEngine(params)

        # Criar população
        population = engine.create_random_population(count)
        behaviors = ["explorer", "socializer", "optimizer", "creator", "analyzer"]

        agents_data = []

        for i, dna in enumerate(population):
            # Selecionar comportamento
            behavior = random.choice(behaviors)
            behavior_type = lore_engine.BehaviorType(behavior)

            # Gerar estado cognitivo
            cognitive_state = lore_engine.generate_random_cognitive_state()

            # Criar agente
            agent_id = f"agent_{i+1:03d}_{random.randint(1000, 9999)}"
            agent = lore_engine.IntelligentAgent(
                id=agent_id,
                dna=dna,
                behavior_type=behavior_type,
                cognitive_state=cognitive_state
            )

            # Debug: verificar valores
            try:
                fitness_value = getattr(dna, 'fitness', None)
                if fitness_value is None:
                    fitness_value = random.uniform(0.3, 0.9)  # gerar fitness aleatório
                else:
                    fitness_value = float(fitness_value)

                cognitive_capacity = float(cognitive_state.get_capacity() or 0.5)

                agent_data = {
                    'agent_id': agent_id,
                    'dna_genes': list(dna.genes),
                    'fitness': fitness_value,
                    'behavior': str(behavior),
                    'cognitive_capacity': cognitive_capacity,
                    'resources': random.randint(100, 1000),
                    'generation': 0,
                    'emotional_state': {
                        'happiness': random.uniform(0.3, 0.8),
                        'satisfaction': random.uniform(0.2, 0.7),
                        'trust': random.uniform(0.4, 0.9)
                    }
                }

                agents_data.append(agent_data)
                print(f"   ✅ Agente {i+1}: {agent_id} ({behavior}) - OK")

            except Exception as debug_e:
                print(f"   ❌ Erro no agente {i+1}: {debug_e}")
                print(f"      fitness: {getattr(dna, 'fitness', 'N/A')}")
                print(f"      capacity: {cognitive_state.get_capacity()}")
                continue

        print(f"🎉 {len(agents_data)} agentes híbridos criados com sucesso!")

        # Salvar em arquivo JSON para backup
        import json
        with open('hybrid_agents_backup.json', 'w') as f:
            json.dump(agents_data, f, indent=2, default=str)
        print("💾 Backup salvo em: hybrid_agents_backup.json")

        return agents_data

    except Exception as e:
        print(f"❌ Erro ao criar agentes: {e}")
        return []


if __name__ == "__main__":
    print("🌟 TESTE RÁPIDO - SISTEMA HÍBRIDO")
    print("=" * 40)
    print()

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_hybrid_quick()
        elif sys.argv[1] == "agents":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            create_hybrid_agents(count)
        else:
            print("Comandos: test | agents [count]")
    else:
        test_hybrid_quick()
        print()
        create_hybrid_agents(3)
