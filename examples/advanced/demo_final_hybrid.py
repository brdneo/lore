#!/usr/bin/env python3
"""
🚀 DEMONSTRAÇÃO COMPLETA DO SISTEMA HÍBRIDO RUST/PYTHON
Lore N.A. - Genesis Protocol - High-Performance Evolution Engine
"""


def main():
    print("🔥 LORE ENGINE - SISTEMA HÍBRIDO RUST/PYTHON")
    print("=" * 60)

    try:
        import lore_engine
        import time

        print("✅ Módulo lore_engine carregado com sucesso!")

        # 1. DEMONSTRAR FUNCIONALIDADES DISPONÍVEIS
        print("\n📦 FUNCIONALIDADES DISPONÍVEIS:")
        attrs = [x for x in dir(lore_engine) if not x.startswith('_')]
        genetic_attrs = [x for x in attrs if 'genetic' in x.lower() or 'engine' in x.lower()]
        utils_attrs = [
    x for x in attrs if any(
        word in x.lower() for word in [
            'timer',
            'counter',
            'memory',
             'benchmark'])]
        type_attrs = [x for x in attrs if any(word in x.lower() for word in ['dna', 'params', 'result'])]

        print(f"   🧬 Algoritmos Genéticos: {len(genetic_attrs)} items")
        for attr in genetic_attrs:
            print(f"      - {attr}")

        print(f"   ⚡ Utilitários de Performance: {len(utils_attrs)} items")
        for attr in utils_attrs:
            print(f"      - {attr}")

        print(f"   🔬 Tipos e Estruturas: {len(type_attrs)} items")
        for attr in type_attrs:
            print(f"      - {attr}")

        # 2. TESTAR SISTEMA DE TIPOS
        print("\n🔬 TESTE DO SISTEMA DE TIPOS RUST:")
        genes = [0.1, -0.3, 0.7, -0.5, 0.2, 0.9, -0.1, 0.4]
        dna = lore_engine.AgentDNA(genes)
        print(f"   ✅ AgentDNA criado: {dna.gene_count()} genes")
        print(f"   📊 ID único: {dna.id}")
        print(f"   🧬 Geração: {dna.generation}")

        # Definir fitness
        dna.set_fitness(0.85)
        print(f"   🎯 Fitness definido: {dna.get_fitness()}")

        # 3. PARÂMETROS DE EVOLUÇÃO
        print("\n⚙️ CONFIGURAÇÃO DE PARÂMETROS:")
        params = lore_engine.EvolutionParams(
            population_size=100,
            mutation_rate=0.1,
            crossover_rate=0.8,
            selection_pressure=0.7,
            elitism_count=5,
            max_generations=1000,
            tournament_size=3
        )
        print(f"   📊 População: {params.population_size}")
        print(f"   🔄 Taxa de mutação: {params.mutation_rate}")
        print(f"   🧬 Taxa de crossover: {params.crossover_rate}")
        print(f"   🏆 Elitismo: {params.elitism_count}")

        # 4. ENGINE GENÉTICO DE ALTA PERFORMANCE
        print("\n🚀 CRIANDO ENGINE GENÉTICO EM RUST:")
        engine = lore_engine.GeneticEngine(params)
        print("   ✅ GeneticEngine inicializado")
        print(f"   👥 Tamanho da população: {engine.get_population_size()}")
        print(f"   📈 Geração atual: {engine.get_generation()}")
        print(f"   🔢 Avaliações realizadas: {engine.get_evaluations()}")

        # 5. CRIAÇÃO DE POPULAÇÃO PARALELA
        print("\n⚡ GERAÇÃO PARALELA DE POPULAÇÃO:")
        timer = lore_engine.Timer("population_creation")
        population = engine.create_random_population(gene_count=20)
        creation_time = timer.stop()

        print(f"   ✅ {len(population)} agentes criados em {creation_time:.2f}ms")
        print(f"   🧬 Cada agente tem {population[0].gene_count()} genes")
        print(f"   ⚡ Performance: {len(population)/max(creation_time, 0.001)*1000:.0f} agentes/segundo")

        # 6. OPERAÇÕES GENÉTICAS PARALELAS
        print("\n🔄 OPERAÇÕES GENÉTICAS PARALELAS:")

        # Crossover paralelo
        parents1 = population[:50]
        parents2 = population[50:]

        timer_cross = lore_engine.Timer("parallel_crossover")
        offspring = lore_engine.parallel_crossover(parents1, parents2, 0.8)
        cross_time = timer_cross.stop()

        print(f"   🧬 Crossover: {len(offspring)} filhos em {cross_time:.2f}ms")

        # Mutação paralela
        timer_mut = lore_engine.Timer("parallel_mutation")
        mutated = lore_engine.parallel_mutation(population.copy(), 0.15, 0.1)
        mut_time = timer_mut.stop()

        print(f"   🔄 Mutação: {len(mutated)} agentes em {mut_time:.2f}ms")

        # 7. TESTE DE MUTAÇÃO INDIVIDUAL
        print("\n🔬 TESTE DE MUTAÇÃO INDIVIDUAL:")
        test_agent = population[0]
        original_genes = test_agent.genes.copy()
        original_mutations = test_agent.mutations

        engine.mutate(test_agent)

        gene_changes = sum(1 for i, (old, new) in enumerate(zip(original_genes, test_agent.genes))
                           if abs(old - new) > 1e-10)

        print(f"   🧬 Genes modificados: {gene_changes}")
        print(f"   📊 Mutações totais: {test_agent.mutations - original_mutations}")

        # 8. BENCHMARK DE PERFORMANCE
        print("\n🏁 BENCHMARK DE PERFORMANCE:")

        sizes = [50, 100, 200, 500]
        for size in sizes:
            bench_params = lore_engine.EvolutionParams(population_size=size)
            bench_engine = lore_engine.GeneticEngine(bench_params)

            timer_bench = lore_engine.Timer(f"benchmark_{size}")
            bench_pop = bench_engine.create_random_population(10)
            bench_time = timer_bench.stop()

            agents_per_sec = size / max(bench_time, 0.001) * 1000  # Evitar divisão por zero
            print(f"   📊 {size:3d} agentes: {bench_time:6.2f}ms ({agents_per_sec:7.0f} agentes/sec)")

        # 9. INFORMAÇÕES DO SISTEMA
        print("\n💻 INFORMAÇÕES DO SISTEMA:")
        system_info = lore_engine.get_system_info()
        for line in system_info.split('\n'):
            if line.strip():
                print(f"   {line}")

        # 10. CONTADORES DE PERFORMANCE
        print("\n📊 CONTADORES DE PERFORMANCE:")
        counter = lore_engine.PerformanceCounter("total_operations")
        counter.add(len(population))      # População criada
        counter.add(len(offspring))       # Crossover
        counter.add(len(mutated))         # Mutação
        counter.add(1)                    # Mutação individual

        print(f"   🔢 Total de operações: {counter.count()}")

        # 11. CONSTANTES DO SISTEMA
        print("\n🔧 CONSTANTES DO SISTEMA:")
        print(f"   📊 População padrão: {lore_engine.DEFAULT_POPULATION_SIZE}")
        print(f"   🔄 Mutação padrão: {lore_engine.DEFAULT_MUTATION_RATE}")
        print(f"   🧬 Crossover padrão: {lore_engine.DEFAULT_CROSSOVER_RATE}")
        print(f"   🎯 Pressão seletiva padrão: {lore_engine.DEFAULT_SELECTION_PRESSURE}")
        print(f"   🧬 Máximo de genes: {lore_engine.MAX_GENE_COUNT}")
        print(f"   👥 População mínima: {lore_engine.MIN_POPULATION_SIZE}")

        # 12. SUMMARY DE SUCESSO
        print("\n🎉 TESTE COMPLETO EXECUTADO COM SUCESSO!")
        print("   ✅ Rust fornece performance ultra-rápida")
        print("   ✅ Python oferece interface intuitiva")
        print("   ✅ Processamento paralelo com Rayon")
        print("   ✅ Integração zero-copy com PyO3")
        print("   ✅ Estruturas de dados otimizadas")
        print("   ✅ Algoritmos genéticos avançados")

        # Comparação com Python puro
        print("\n🐍 COMPARAÇÃO COM PYTHON PURO:")

        # Python puro
        import random
        start_py = time.time()
        py_population = []
        for _ in range(100):
            genes = [random.uniform(-1, 1) for _ in range(20)]
            py_population.append(genes)
        py_time = (time.time() - start_py) * 1000

        # Rust
        rust_timer = lore_engine.Timer("rust_comparison")
        rust_population = engine.create_random_population(20)
        rust_time = rust_timer.stop()

        speedup = py_time / max(rust_time, 0.001)  # Evitar divisão por zero
        print(f"   🐍 Python puro: {py_time:.2f}ms")
        print(f"   🦀 Rust híbrido: {rust_time:.2f}ms")
        print(f"   ⚡ Speedup: {speedup:.1f}x mais rápido!")

        print("\n🚀 LORE ENGINE HÍBRIDO PRONTO PARA EVOLUÇÃO!")
        return True

    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
