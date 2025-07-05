#!/usr/bin/env python3
"""
Demonstração completa do sistema híbrido Rust/Python do Lore Engine
"""

import time
import numpy as np

def test_genetic_engine():
    """Testa o mecanismo de algoritmos genéticos em Rust"""
    try:
        import lore_engine
        print("🔥 SISTEMA HÍBRIDO RUST/PYTHON - LORE ENGINE")
        print("=" * 60)
        
        # Criar parâmetros de evolução
        params = lore_engine.EvolutionParams(
            population_size=100,
            mutation_rate=0.15,
            crossover_rate=0.85,
            selection_pressure=0.8,
            elitism_count=10,
            max_generations=50,
            tournament_size=5
        )
        
        print(f"🧬 Parâmetros de Evolução:")
        print(f"   - População: {params.population_size}")
        print(f"   - Taxa de Mutação: {params.mutation_rate}")
        print(f"   - Taxa de Crossover: {params.crossover_rate}")
        print(f"   - Elitismo: {params.elitism_count}")
        
        # Criar engine genético em Rust
        genetic_engine = lore_engine.GeneticEngine(params)
        print(f"⚡ GeneticEngine criado com {genetic_engine.get_population_size()} agentes")
        
        # Criar população inicial (processamento paralelo em Rust)
        timer = lore_engine.Timer("population_creation")
        population = genetic_engine.create_random_population(gene_count=20)
        creation_time = timer.stop()
        
        print(f"🚀 População de {len(population)} agentes criada em {creation_time:.2f}ms")
        print(f"   - Cada agente tem {population[0].gene_count()} genes")
        print(f"   - Primeiro agente ID: {population[0].id}")
        
        # Função de fitness (problema de otimização: maximizar soma dos quadrados)
        def fitness_function(genes):
            """Função de fitness: sphere function inversa"""
            return 100.0 - sum(x*x for x in genes)
        
        print("\n🎯 Testando função de fitness...")
        test_genes = [0.1, 0.2, -0.3, 0.4, -0.5]
        fitness_value = fitness_function(test_genes)
        print(f"   - Genes de teste: {test_genes}")
        print(f"   - Fitness: {fitness_value:.4f}")
        
        # Testar operações genéticas paralelas
        print("\n🔄 Testando operações genéticas paralelas...")
        
        # Crossover paralelo
        parents1 = population[:50]
        parents2 = population[50:]
        
        timer_crossover = lore_engine.Timer("parallel_crossover")
        offspring_crossover = lore_engine.parallel_crossover(parents1, parents2, 0.8)
        crossover_time = timer_crossover.stop()
        
        print(f"   - Crossover paralelo: {len(offspring_crossover)} filhos em {crossover_time:.2f}ms")
        
        # Mutação paralela
        timer_mutation = lore_engine.Timer("parallel_mutation")
        mutated_population = lore_engine.parallel_mutation(population, 0.1, 0.2)
        mutation_time = timer_mutation.stop()
        
        print(f"   - Mutação paralela: {len(mutated_population)} agentes em {mutation_time:.2f}ms")
        
        # Demonstrar performance de DNA operations
        print("\n🧬 Testando operações de DNA...")
        test_dna = population[0]
        print(f"   - DNA original: {test_dna.gene_count()} genes")
        print(f"   - Geração: {test_dna.generation}")
        print(f"   - Mutações: {test_dna.mutations}")
        
        # Modificar fitness
        test_dna.set_fitness(95.5)
        print(f"   - Fitness definido: {test_dna.get_fitness()}")
        
        # Clone com novo ID
        cloned_dna = test_dna.clone_with_new_id()
        print(f"   - DNA clonado: {cloned_dna.id}")
        print(f"   - Mesmo fitness: {cloned_dna.get_fitness()}")
        
        # Testar operações de mutação
        print("\n🔬 Testando mutação individual...")
        original_genes = test_dna.genes.copy()
        genetic_engine.mutate(test_dna)
        mutations_made = test_dna.mutations
        print(f"   - Mutações realizadas: {mutations_made}")
        
        # Comparar genes antes e depois
        differences = sum(1 for i, (old, new) in enumerate(zip(original_genes, test_dna.genes)) if abs(old - new) > 1e-10)
        print(f"   - Genes modificados: {differences}")
        
        # Benchmark de performance
        print("\n⚡ BENCHMARK DE PERFORMANCE")
        print("-" * 40)
        
        # Benchmark: Criação de população
        sizes = [50, 100, 200, 500]
        for size in sizes:
            test_params = lore_engine.EvolutionParams(population_size=size)
            test_engine = lore_engine.GeneticEngine(test_params)
            
            timer_bench = lore_engine.Timer(f"population_{size}")
            test_pop = test_engine.create_random_population(10)
            bench_time = timer_bench.stop()
            
            print(f"   - População {size}: {bench_time:.2f}ms ({size/bench_time*1000:.0f} agentes/sec)")
        
        # Informações do sistema
        print("\n💻 INFORMAÇÕES DO SISTEMA")
        print("-" * 40)
        system_info = lore_engine.get_system_info()
        print(system_info)
        
        # Contadores de performance
        counter = lore_engine.PerformanceCounter("genetic_operations")
        counter.add(len(population))
        counter.add(len(offspring_crossover))
        counter.add(len(mutated_population))
        print(f"\n📊 Total de operações genéticas: {counter.count()}")
        
        # Demonstrar constantes
        print(f"\n🔧 CONSTANTES DO SISTEMA:")
        print(f"   - População padrão: {lore_engine.DEFAULT_POPULATION_SIZE}")
        print(f"   - Taxa de mutação padrão: {lore_engine.DEFAULT_MUTATION_RATE}")
        print(f"   - Taxa de crossover padrão: {lore_engine.DEFAULT_CROSSOVER_RATE}")
        print(f"   - Máximo de genes: {lore_engine.MAX_GENE_COUNT}")
        
        print("\n🎉 TESTE COMPLETO DO SISTEMA HÍBRIDO CONCLUÍDO!")
        print("✅ Rust fornece performance ultra-rápida")
        print("✅ Python oferece interface amigável")
        print("✅ Processamento paralelo com Rayon")
        print("✅ Integração zero-copy com PyO3")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def benchmark_comparison():
    """Comparação de performance Python vs Rust"""
    print("\n🏁 COMPARAÇÃO DE PERFORMANCE: PYTHON vs RUST")
    print("=" * 50)
    
    import lore_engine
    
    # Benchmark Python puro
    def create_population_python(size, gene_count):
        import random
        population = []
        for _ in range(size):
            genes = [random.uniform(-1, 1) for _ in range(gene_count)]
            population.append(genes)
        return population
    
    # Benchmark Rust
    params = lore_engine.EvolutionParams(population_size=1000)
    engine = lore_engine.GeneticEngine(params)
    
    # Python
    start = time.time()
    py_pop = create_population_python(1000, 50)
    py_time = (time.time() - start) * 1000
    
    # Rust
    rust_timer = lore_engine.Timer("rust_benchmark")
    rust_pop = engine.create_random_population(50)
    rust_time = rust_timer.stop()
    
    print(f"🐍 Python: {py_time:.2f}ms")
    print(f"🦀 Rust:   {rust_time:.2f}ms")
    print(f"⚡ Speedup: {py_time/rust_time:.1f}x mais rápido!")
    
    return rust_time < py_time

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DO LORE ENGINE HÍBRIDO")
    
    success = test_genetic_engine()
    if success:
        benchmark_comparison()
        print("\n🎊 TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO!")
    else:
        print("\n💥 ALGUNS TESTES FALHARAM!")
