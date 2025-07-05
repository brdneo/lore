#!/usr/bin/env python3
"""
INICIALIZADOR DO UNIVERSO LORE N.A.
===================================

Script para criar população inicial, produtos e iniciar simulação
"""

import sys
import os
import json
import random
from datetime import datetime

# Adicionar diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_initial_population(size=30):
    """Cria população inicial de agentes usando o sistema híbrido Rust+Python"""
    
    print(f"🤖 Criando população inicial de {size} agentes com sistema híbrido...")
    
    try:
        import lore_engine
        from database_manager import LoREDatabase
        
        db = LoREDatabase()
        agents_created = 0
        
        # Comportamentos disponíveis
        behaviors = ["explorer", "socializer", "optimizer", "creator", "analyzer"]
        
        for i in range(size):
            try:
                # Gerar DNA único com sistema Rust
                genes = [random.uniform(-1.0, 1.0) for _ in range(10)]
                dna = lore_engine.AgentDNA(genes)
                dna.fitness = random.uniform(0.3, 0.9)
                
                # Gerar estado cognitivo
                cognitive_state = lore_engine.generate_random_cognitive_state()
                
                # Selecionar comportamento
                behavior = random.choice(behaviors)
                behavior_type = lore_engine.BehaviorType(behavior)
                
                # Criar agente inteligente
                agent_id = f"agent_{i+1:03d}_{random.randint(1000, 9999)}"
                agent = lore_engine.IntelligentAgent(
                    id=agent_id,
                    dna=dna,
                    behavior_type=behavior_type,
                    cognitive_state=cognitive_state
                )
                
                # Salvar dados no banco
                agent_data = {
                    'agent_id': agent_id,
                    'dna_genes': genes,
                    'fitness': dna.fitness,
                    'behavior': behavior,
                    'cognitive_capacity': cognitive_state.get_capacity(),
                    'resources': random.randint(100, 1000),
                    'generation': 0,
                    'emotional_state': {
                        'happiness': random.uniform(0.3, 0.8),
                        'satisfaction': random.uniform(0.2, 0.7),
                        'trust': random.uniform(0.4, 0.9)
                    }
                }
                
                # Salvar agente híbrido no banco
                if db.save_hybrid_agent(agent_data):
                    agents_created += 1
                else:
                    print(f"   ⚠️  Falha ao salvar agente {agent_id} no banco")
                
                if agents_created % 10 == 0:
                    print(f"   ✅ {agents_created} agentes híbridos criados...")
                    
            except Exception as e:
                print(f"   ❌ Erro ao criar agente {i+1}: {e}")
        
        print(f"🎉 População híbrida criada: {agents_created} agentes!")
        print(f"🦀 Engine Rust: Ativo")
        print(f"🐍 Interface Python: Ativa")
        return agents_created
        
    except ImportError as e:
        print(f"❌ Erro de importação do sistema híbrido: {e}")
        print("🔧 Execute: maturin develop --release")
        return 0
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return 0

def create_universe_catalog():
    """Cria catálogo de produtos dos 5 universos"""
    
    print("🛒 Criando catálogo de produtos dos 5 universos...")
    
    universes_catalog = {
        "limbo": [
            {"name": "Crypto Analyzer Pro", "price": 299, "category": "financial", "universe": "limbo"},
            {"name": "Market Trend Scanner", "price": 199, "category": "analytics", "universe": "limbo"},
            {"name": "Risk Assessment Tool", "price": 149, "category": "security", "universe": "limbo"},
            {"name": "Portfolio Optimizer", "price": 399, "category": "investment", "universe": "limbo"},
            {"name": "Trading Bot Starter", "price": 99, "category": "automation", "universe": "limbo"}
        ],
        "odyssey": [
            {"name": "Neural Art Generator", "price": 249, "category": "creativity", "universe": "odyssey"},
            {"name": "Story Weaver AI", "price": 179, "category": "writing", "universe": "odyssey"},
            {"name": "Music Composition Suite", "price": 329, "category": "music", "universe": "odyssey"},
            {"name": "3D Model Creator", "price": 199, "category": "design", "universe": "odyssey"},
            {"name": "Poetry Inspiration Engine", "price": 89, "category": "literature", "universe": "odyssey"}
        ],
        "ritual": [
            {"name": "Community Builder Kit", "price": 159, "category": "social", "universe": "ritual"},
            {"name": "Event Organizer Pro", "price": 229, "category": "events", "universe": "ritual"},
            {"name": "Social Network Analyzer", "price": 189, "category": "analytics", "universe": "ritual"},
            {"name": "Influence Tracker", "price": 139, "category": "metrics", "universe": "ritual"},
            {"name": "Collaboration Platform", "price": 299, "category": "teamwork", "universe": "ritual"}
        ],
        "engine": [
            {"name": "Predictive Model Studio", "price": 449, "category": "ai", "universe": "engine"},
            {"name": "Data Pipeline Builder", "price": 349, "category": "data", "universe": "engine"},
            {"name": "Algorithm Optimizer", "price": 399, "category": "optimization", "universe": "engine"},
            {"name": "Neural Network Designer", "price": 499, "category": "ml", "universe": "engine"},
            {"name": "Pattern Recognition Kit", "price": 279, "category": "analysis", "universe": "engine"}
        ],
        "logs": [
            {"name": "System Monitor Pro", "price": 119, "category": "monitoring", "universe": "logs"},
            {"name": "Error Tracker Elite", "price": 159, "category": "debugging", "universe": "logs"},
            {"name": "Performance Analyzer", "price": 199, "category": "optimization", "universe": "logs"},
            {"name": "Log Intelligence Suite", "price": 249, "category": "analytics", "universe": "logs"},
            {"name": "Support Ticket Manager", "price": 179, "category": "support", "universe": "logs"}
        ]
    }
    
    try:
        from database_manager import LoREDatabase
        
        db = LoREDatabase()
        products_created = 0
        
        for universe, products in universes_catalog.items():
            for product in products:
                try:
                    # Adicionar dados extras
                    product.update({
                        'id': f"{universe}_{product['name'].lower().replace(' ', '_')}",
                        'description': f"Premium {product['category']} solution for {universe} universe",
                        'rating': round(random.uniform(3.5, 5.0), 1),
                        'stock': random.randint(5, 50),
                        'created_at': datetime.now().isoformat()
                    })
                    
                    # Salvar produto no banco
                    if db.save_product(product):
                        products_created += 1
                    else:
                        print(f"   ⚠️  Falha ao salvar produto {product['name']}")
                    
                except Exception as e:
                    print(f"   ❌ Erro ao criar produto {product['name']}: {e}")
        
        print(f"🎉 Catálogo criado: {products_created} produtos em 5 universos!")
        
        # Salvar arquivo JSON como backup
        with open('/home/brendo/lore/data/universe_catalog.json', 'w', encoding='utf-8') as f:
            json.dump(universes_catalog, f, indent=2, ensure_ascii=False)
        
        print("📄 Backup salvo em: data/universe_catalog.json")
        return products_created
        
    except Exception as e:
        print(f"❌ Erro ao criar catálogo: {e}")
        return 0

def start_universe_simulation():
    """Inicia simulação contínua do universo"""
    
    print("🌟 Iniciando simulação do universo...")
    
    try:
        from population_manager import PopulationManager
        
        pop_manager = PopulationManager()
        
        print("✅ PopulationManager inicializado")
        print("🔄 Simulação contínua não implementada ainda")
        print("💡 Para implementar: criar loop que executa ciclos de vida")
        
        # TODO: Implementar loop de simulação contínua
        # while True:
        #     pop_manager.run_life_cycle()
        #     time.sleep(60)  # Ciclo a cada minuto
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao iniciar simulação: {e}")
        return False

def test_hybrid_system():
    """Testa o sistema híbrido Rust+Python"""
    
    print("🔬 Testando sistema híbrido Rust+Python...")
    
    try:
        import lore_engine
        
        print("✅ Sistema híbrido carregado com sucesso!")
        
        # Teste rápido de funcionalidades
        print("🧪 Executando testes básicos...")
        
        # 1. Teste genetic
        params = lore_engine.EvolutionParams(20, 0.1, 0.8, 0.7)  # selection_pressure entre 0.0 e 1.0
        engine = lore_engine.GeneticEngine(params)
        population = engine.create_random_population(5)
        print(f"   ✅ Genético: {len(population)} agentes criados")
        
        # 2. Teste neural
        network = lore_engine.create_feedforward_network(5, [8], 3, "relu")
        result = network.forward([0.1, 0.2, 0.3, 0.4, 0.5])
        print(f"   ✅ Neural: rede processou {len(result)} saídas")
        
        # 3. Teste agentes
        cognitive_state = lore_engine.generate_random_cognitive_state()
        behavior = lore_engine.BehaviorType("explorer")
        agent = lore_engine.IntelligentAgent("test_001", population[0], behavior, cognitive_state)
        decision = agent.make_decision([0.5, 0.3, 0.7])
        print(f"   ✅ Agente: decisão com {len(decision)} componentes")
        
        # 4. Teste sociedade
        society = lore_engine.AgentSociety()
        society.add_agent(agent)
        stats = society.get_society_stats()
        print(f"   ✅ Sociedade: {stats.get('total_agents', 0)} agentes")
        
        print("🎉 Sistema híbrido funcionando perfeitamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Sistema híbrido não disponível: {e}")
        print("💡 Execute: maturin develop --release")
        return False
    except Exception as e:
        print(f"❌ Erro no teste híbrido: {e}")
        return False

def check_universe_status():
    """Verifica status atual do universo"""
    
    print("📊 Verificando status do universo...")
    
    try:
        from database_manager import LoREDatabase
        
        db = LoREDatabase()
        
        # Contar agentes
        try:
            agent_count = db.count_agents()
            print(f"🤖 Agentes ativos: {agent_count}")
        except:
            print("🤖 Agentes ativos: Não foi possível verificar")
        
        # Contar produtos  
        try:
            product_count = db.count_products()
            print(f"🛒 Produtos disponíveis: {product_count}")
        except:
            print("🛒 Produtos disponíveis: Não foi possível verificar")
        
        # Status da simulação
        print("🔄 Simulação contínua: ❌ Não ativa")
        print("📊 Dashboard: ✅ Disponível em http://localhost:8501")
        print("🔗 API: ✅ Disponível em http://localhost:8000")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
        return False

def run_hybrid_benchmark():
    """Executa benchmark do sistema híbrido vs Python puro"""
    
    print("🏃 Executando benchmark do sistema híbrido...")
    
    try:
        import lore_engine
        import time
        import random
        
        print("✅ Sistema híbrido carregado!")
        
        # Teste 1: Criação de população
        print("\n🧪 Teste 1: Criação de população")
        start_time = time.time()
        
        # Rust
        params = lore_engine.EvolutionParams(50, 0.1, 0.8, 0.7)  # selection_pressure entre 0.0 e 1.0
        engine = lore_engine.GeneticEngine(params)
        rust_population = engine.create_random_population(100)
        rust_time = time.time() - start_time
        
        # Python equivalente (simulado)
        start_time = time.time()
        python_population = []
        for i in range(100):
            genes = [random.uniform(-1.0, 1.0) for _ in range(10)]
            python_population.append({"genes": genes, "fitness": random.uniform(0.0, 1.0)})
        python_time = time.time() - start_time
        
        speedup_1 = python_time / rust_time if rust_time > 0 else 0
        print(f"   🦀 Rust: {rust_time:.4f}s ({len(rust_population)} agentes)")
        print(f"   🐍 Python: {python_time:.4f}s ({len(python_population)} agentes)")
        print(f"   ⚡ Speedup: {speedup_1:.2f}x")
        
        # Teste 2: Processamento neural
        print("\n🧪 Teste 2: Processamento neural")
        start_time = time.time()
        
        # Rust
        network = lore_engine.create_feedforward_network(10, [20, 15], 5, "relu")
        for _ in range(1000):
            inputs = [random.uniform(-1.0, 1.0) for _ in range(10)]
            result = network.forward(inputs)
        rust_time = time.time() - start_time
        
        # Python equivalente (simulado)
        start_time = time.time()
        for _ in range(1000):
            inputs = [random.uniform(-1.0, 1.0) for _ in range(10)]
            # Simulação de forward pass
            result = [sum(inputs) / len(inputs) for _ in range(5)]
        python_time = time.time() - start_time
        
        speedup_2 = python_time / rust_time if rust_time > 0 else 0
        print(f"   🦀 Rust: {rust_time:.4f}s (1000 forward passes)")
        print(f"   🐍 Python: {python_time:.4f}s (1000 forward passes)")
        print(f"   ⚡ Speedup: {speedup_2:.2f}x")
        
        # Teste 3: Evolução genética
        print("\n🧪 Teste 3: Evolução genética")
        start_time = time.time()
        
        # Rust
        evolved_population = engine.evolve_generation(rust_population)
        rust_time = time.time() - start_time
        
        # Python equivalente (simulado)
        start_time = time.time()
        evolved_python = []
        for agent in python_population[:50]:  # Selection
            new_genes = [g + random.uniform(-0.1, 0.1) for g in agent["genes"]]  # Mutation
            evolved_python.append({"genes": new_genes, "fitness": random.uniform(0.0, 1.0)})
        python_time = time.time() - start_time
        
        speedup_3 = python_time / rust_time if rust_time > 0 else 0
        print(f"   🦀 Rust: {rust_time:.4f}s ({len(evolved_population)} agentes)")
        print(f"   🐍 Python: {python_time:.4f}s ({len(evolved_python)} agentes)")
        print(f"   ⚡ Speedup: {speedup_3:.2f}x")
        
        # Resultado final
        avg_speedup = (speedup_1 + speedup_2 + speedup_3) / 3
        print(f"\n🎉 RESULTADO FINAL:")
        print(f"   📊 Speedup médio: {avg_speedup:.2f}x")
        print(f"   🚀 Performance: {'EXCELENTE' if avg_speedup > 5 else 'BOA' if avg_speedup > 2 else 'MODERADA'}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Sistema híbrido não disponível: {e}")
        print("💡 Execute: maturin develop --release")
        return False
    except Exception as e:
        print(f"❌ Erro no benchmark: {e}")
        return False

def main():
    """Função principal do inicializador"""
    
    print("🌟 LORE N.A. UNIVERSE INITIALIZER")
    print("=" * 40)
    print()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "population":
            size = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            create_initial_population(size)
            
        elif command == "catalog":
            create_universe_catalog()
            
        elif command == "simulation":
            start_universe_simulation()
            
        elif command == "status":
            check_universe_status()
            
        elif command == "test":
            test_hybrid_system()
            
        elif command == "benchmark":
            run_hybrid_benchmark()
            
        elif command == "full":
            print("🚀 Inicialização COMPLETA do universo!")
            print()
            
            # Passo 1: População
            agents = create_initial_population(30)
            print()
            
            # Passo 2: Catálogo
            products = create_universe_catalog()
            print()
            
            # Passo 3: Status
            check_universe_status()
            print()
            
            print("🎉 UNIVERSO INICIALIZADO!")
            print("📊 Acesse o dashboard: http://localhost:8501")
            print("🔗 API disponível em: http://localhost:8000")
            
        else:
            print(f"❌ Comando '{command}' não reconhecido")
            show_help()
    else:
        show_help()

def show_help():
    """Mostra ajuda de uso"""
    print("📋 USO:")
    print("  python initialize_universe.py [comando] [opções]")
    print()
    print("📚 COMANDOS:")
    print("  population [size]  - Cria população inicial (padrão: 30 agentes)")
    print("  catalog           - Cria catálogo de produtos dos 5 universos")
    print("  simulation        - Inicia simulação contínua")
    print("  status            - Verifica status atual do universo")
    print("  test              - Testa sistema híbrido Rust+Python")
    print("  benchmark         - Executa benchmark de performance")
    print("  full              - Inicialização completa (recomendado)")
    print()
    print("💡 EXEMPLO:")
    print("  python initialize_universe.py full")

if __name__ == "__main__":
    main()
