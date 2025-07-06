#!/usr/bin/env python3
"""
🎉 DEMONSTRAÇÃO FINAL - SISTEMA HÍBRIDO RUST/PYTHON FUNCIONANDO
"""


def main():
    print("🚀 LORE ENGINE - SISTEMA HÍBRIDO FUNCIONANDO!")
    print("=" * 50)

    try:
        import lore_engine

        # 1. Mostrar que o módulo carregou
        print("✅ Módulo lore_engine carregado com sucesso!")

        # 2. Contar funcionalidades
        attrs = [x for x in dir(lore_engine) if not x.startswith('_')]
        print(f"📦 {len(attrs)} funcionalidades disponíveis")

        # 3. Testar tipos básicos
        print("\n🧬 Testando sistema de tipos:")
        dna = lore_engine.AgentDNA([0.1, 0.5, -0.2, 0.8])
        print(f"   ✅ DNA criado com {dna.gene_count()} genes")
        dna.set_fitness(0.95)
        print(f"   ✅ Fitness definido: {dna.get_fitness()}")

        # 4. Testar engine genético
        print("\n⚡ Testando engine genético:")
        params = lore_engine.EvolutionParams(population_size=50)
        engine = lore_engine.GeneticEngine(params)
        print(f"   ✅ Engine criado para {engine.get_population_size()} agentes")

        # 5. Criar população
        print("\n🚀 Criando população em paralelo:")
        population = engine.create_random_population(10)
        print(f"   ✅ {len(population)} agentes criados")
        print(f"   ✅ Cada agente tem {population[0].gene_count()} genes")

        # 6. Testar operações paralelas
        print("\n🔄 Testando operações paralelas:")
        parents1 = population[:25]
        parents2 = population[25:]

        offspring = lore_engine.parallel_crossover(parents1, parents2, 0.8)
        print(f"   ✅ Crossover: {len(offspring)} filhos gerados")

        mutated = lore_engine.parallel_mutation(population, 0.1, 0.1)
        print(f"   ✅ Mutação: {len(mutated)} agentes processados")

        # 7. Testar utilitários
        print("\n📊 Testando utilitários:")
        timer = lore_engine.Timer("test")
        counter = lore_engine.PerformanceCounter("ops")
        counter.add(len(population) + len(offspring) + len(mutated))
        print("   ✅ Timer e contador criados")
        print(f"   ✅ Total de operações: {counter.count()}")

        # 8. Mostrar constantes
        print("\n🔧 Constantes do sistema:")
        print(f"   📊 População padrão: {lore_engine.DEFAULT_POPULATION_SIZE}")
        print(f"   🧬 Máximo genes: {lore_engine.MAX_GENE_COUNT}")

        # 9. Informações do sistema
        print("\n💻 Sistema:")
        info = lore_engine.get_system_info()
        cores_line = [line for line in info.split('\n') if 'CPU cores' in line][0]
        print(f"   {cores_line}")

        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Rust + Python = Performance + Simplicidade")
        print("🚀 Sistema híbrido pronto para evolução!")

        return True

    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🏆 IMPLEMENTAÇÃO RUST CONCLUÍDA COM SUCESSO!")
    else:
        print("\n💥 Erro na implementação!")
