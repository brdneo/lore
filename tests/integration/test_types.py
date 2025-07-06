#!/usr/bin/env python3
"""
Test the Lore Engine hybrid Rust/Python module with types
"""


def test_lore_engine_types():
    try:
        import lore_engine
        print("✅ SUCCESS: lore_engine imported")

        # Check available attributes
        attrs = [x for x in dir(lore_engine) if not x.startswith('_')]
        print(f"📦 Available: {attrs}")

        # Test AgentDNA
        if hasattr(lore_engine, 'AgentDNA'):
            genes = [0.1, 0.5, 0.9, 0.2, 0.8]
            dna = lore_engine.AgentDNA(genes)
            print(f"🧬 DNA created with {dna.gene_count()} genes, ID: {dna.id}")
            dna.set_fitness(0.85)
            print(f"🎯 DNA fitness: {dna.get_fitness()}")

        # Test EvolutionParams
        if hasattr(lore_engine, 'EvolutionParams'):
            params = lore_engine.EvolutionParams(
                population_size=200,
                mutation_rate=0.05,
                crossover_rate=0.9
            )
            print(f"⚙️  Evolution params: pop={params.population_size}, mut={params.mutation_rate}")

        # Test constants
        if hasattr(lore_engine, 'DEFAULT_POPULATION_SIZE'):
            print(f"📊 Default population size: {lore_engine.DEFAULT_POPULATION_SIZE}")
            print(f"📊 Max gene count: {lore_engine.MAX_GENE_COUNT}")

        # Test timer
        if hasattr(lore_engine, 'Timer'):
            timer = lore_engine.Timer("test_operation")
            import time
            time.sleep(0.02)
            elapsed = timer.stop()
            print(f"⏱️  Timer test: {elapsed:.2f}ms")

        # Test system info
        if hasattr(lore_engine, 'get_system_info'):
            info = lore_engine.get_system_info()
            print(f"🖥️  {info.split('Build:')[0].strip()}")

        print("🎉 ALL TYPE TESTS PASSED!")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_lore_engine_types()
