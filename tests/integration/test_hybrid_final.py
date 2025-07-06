#!/usr/bin/env python3
"""
🚀 FINAL HYBRID SYSTEM TEST - Neural + Genetic Integration
===========================================================

Test the complete hybrid Rust system with neural networks and genetic algorithms.
"""

import sys
import time
import random
import numpy as np


def main():
    print("🚀 LORE ENGINE - FINAL HYBRID SYSTEM TEST")
    print("="*60)

    try:
        import lore_engine
        print("✅ Módulo lore_engine carregado com sucesso!")

        # Count available functions
        functions = [attr for attr in dir(lore_engine) if not attr.startswith('_')]
        print(f"📦 {len(functions)} funcionalidades disponíveis")
        print("🧬 Módulos: Genetic, Neural, Types, Utils")

        # Test 1: Create neural network for evolution fitness evaluation
        print("\n🧠 FASE 1: Neural Network para Avaliação de Fitness")
        print("-" * 50)

        # Create a neural network that will evaluate agent fitness
        fitness_network = lore_engine.create_feedforward_network(
            input_size=10,    # Agent genes
            hidden_sizes=[15, 10],
            output_size=1,    # Fitness score
            activation="relu"
        )

        print(f"   ✅ Rede de fitness criada: {fitness_network.get_architecture()}")
        print(f"   📊 Parâmetros: {fitness_network.get_parameter_count():,}")

        # Test 2: Create genetic engine and population
        print("\n🧬 FASE 2: Sistema Genético para Evolução")
        print("-" * 50)

        evolution_params = lore_engine.EvolutionParams(
            population_size=50,
            mutation_rate=0.1,
            crossover_rate=0.8,
            max_generations=100
        )

        genetic_engine = lore_engine.GeneticEngine(evolution_params)
        print(f"   ✅ Engine genético criado para {genetic_engine.get_population_size()} agentes")

        # Create initial population
        population = genetic_engine.create_random_population(10)  # 10 genes per agent
        print(f"   ✅ População inicial: {len(population)} agentes com 10 genes cada")

        # Test 3: Evaluate population using neural network
        print("\n⚡ FASE 3: Avaliação Neural da População")
        print("-" * 50)

        start_time = time.time()

        # Extract genes from population for batch processing
        agent_genes = [agent.genes for agent in population]

        # Batch evaluation using neural network
        fitness_scores = fitness_network.batch_forward(agent_genes)

        # Apply fitness scores back to agents
        for agent, score in zip(population, fitness_scores):
            agent.fitness = score[0]  # Neural net outputs a single value

        evaluation_time = (time.time() - start_time) * 1000
        print(f"   ✅ {len(population)} agentes avaliados em {evaluation_time:.2f}ms")

        # Show fitness distribution
        fitness_values = [agent.fitness for agent in population]
        print(
    f"   📊 Fitness: min={
        min(fitness_values):.3f}, max={
            max(fitness_values):.3f}, avg={
                np.mean(fitness_values):.3f}")

        # Test 4: Evolution cycles with neural evaluation
        print("\n🔄 FASE 4: Ciclos de Evolução Híbrida")
        print("-" * 50)

        best_fitness_history = []

        for generation in range(5):  # Run 5 generations
            start_gen = time.time()

            # Selection: Sort by fitness and take top half
            population.sort(key=lambda agent: agent.fitness, reverse=True)
            elite = population[:25]  # Top 50%

            # Crossover: Create offspring
            parents1 = random.choices(elite, k=25)
            parents2 = random.choices(elite, k=25)

            offspring = lore_engine.parallel_crossover(
                parents1, parents2, evolution_params.crossover_rate
            )

            # Mutation: Apply random mutations
            offspring = lore_engine.parallel_mutation(
                offspring, evolution_params.mutation_rate, 0.1
            )

            # Neural evaluation of offspring
            offspring_genes = [agent.genes for agent in offspring]
            offspring_fitness = fitness_network.batch_forward(offspring_genes)

            for agent, score in zip(offspring, offspring_fitness):
                agent.fitness = score[0]

            # New population: Elite + offspring
            population = elite + offspring

            # Statistics
            current_fitness = [agent.fitness for agent in population]
            best_fitness = max(current_fitness)
            avg_fitness = np.mean(current_fitness)
            best_fitness_history.append(best_fitness)

            gen_time = (time.time() - start_gen) * 1000

            print(f"   Gen {generation+1}: best={best_fitness:.3f}, avg={avg_fitness:.3f}, time={gen_time:.1f}ms")

        # Test 5: Performance analysis
        print("\n📊 FASE 5: Análise de Performance Híbrida")
        print("-" * 50)

        # Evolution progress
        improvement = best_fitness_history[-1] - best_fitness_history[0]
        print(f"   📈 Melhoria total: {improvement:.3f} ({improvement/best_fitness_history[0]*100:.1f}%)")

        # Compare hybrid vs pure approaches
        print("\n   🔬 Benchmark: Rust vs Python na Avaliação")

        # Rust neural network (already tested above)
        rust_times = []
        for _ in range(100):
            start = time.perf_counter()
            fitness_network.forward(agent_genes[0])
            rust_times.append(time.perf_counter() - start)

        rust_avg = np.mean(rust_times) * 1_000_000  # microseconds

        # Simple Python fitness function for comparison
        def python_fitness(genes):
            # Simple polynomial fitness function
            return sum(g**2 - 0.1*g**3 for g in genes)

        python_times = []
        for _ in range(100):
            start = time.perf_counter()
            python_fitness(agent_genes[0])
            python_times.append(time.perf_counter() - start)

        python_avg = np.mean(python_times) * 1_000_000

        print(f"   🦀 Neural Rust:  {rust_avg:.1f}μs (complexo)")
        print(f"   🐍 Python simples: {python_avg:.1f}μs (básico)")
        print("   💡 Trade-off: Complexidade vs Performance")

        # Test 6: Memory and system stats
        print("\n💾 FASE 6: Estatísticas do Sistema")
        print("-" * 50)

        # Create performance counter
        counter = lore_engine.PerformanceCounter("hybrid_test")

        # Multiple operations
        for _ in range(1000):
            counter.increment()

        print(f"   📊 Operações contadas: {counter.get_count():,}")

        # Memory info
        system_info = lore_engine.get_system_info()
        print(f"   � Sistema: {system_info}")

        # Test 7: Advanced neural architectures
        print("\n🏗️ FASE 7: Arquiteturas Neurais Avançadas")
        print("-" * 50)

        # Create different network architectures for comparison
        architectures = [
            ("Shallow", [10, 20, 1]),
            ("Deep", [10, 15, 10, 5, 1]),
            ("Wide", [10, 50, 1]),
            ("Complex", [10, 25, 15, 8, 3, 1])
        ]

        networks = []
        for name, arch in architectures:
            net = lore_engine.create_feedforward_network(
                arch[0], arch[1:-1], arch[-1], "relu"
            )
            networks.append((name, net))
            print(f"   ✅ {name}: {arch} ({net.get_parameter_count():,} params)")

        # Compare inference times
        test_input = [random.gauss(0, 1) for _ in range(10)]

        for name, net in networks:
            times = []
            for _ in range(1000):
                start = time.perf_counter()
                net.forward(test_input)
                times.append(time.perf_counter() - start)

            avg_time = np.mean(times) * 1_000_000
            print(f"   ⚡ {name}: {avg_time:.1f}μs")

        print("\n🎉 TESTE HÍBRIDO COMPLETO FINALIZADO!")
        print("="*60)
        print("✅ Todos os sistemas funcionando em perfeita harmonia!")
        print("🧠 Neural Networks: ✓ (Avaliação de fitness complexa)")
        print("🧬 Genetic Algorithms: ✓ (Evolução populacional)")
        print("⚡ Parallel Processing: ✓ (Operações otimizadas)")
        print("🔗 Hybrid Integration: ✓ (Python ↔ Rust)")
        print("📊 Performance Monitoring: ✓ (Métricas em tempo real)")
        print("\n🚀 SISTEMA PRONTO PARA SIMULAÇÕES AVANÇADAS!")

    except ImportError as e:
        print(f"❌ Erro ao importar lore_engine: {e}")
        print("💡 Execute: maturin develop --release")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
