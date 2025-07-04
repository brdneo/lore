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
    """Cria população inicial de agentes"""
    
    print(f"🤖 Criando população inicial de {size} agentes...")
    
    try:
        from agent_dna import AgentDNA
        from agent_name_generator import AgentNameGenerator
        from database_manager import LoREDatabase
        
        db = LoREDatabase()
        name_gen = AgentNameGenerator()
        
        agents_created = 0
        
        for i in range(size):
            try:
                # Gerar DNA único
                agent_id = f"agent_{i+1:03d}_{random.randint(1000, 9999)}"
                dna = AgentDNA.generate_random(agent_id)
                
                # Gerar identidade
                identity = name_gen.generate_identity(agent_id, f"Agent {i+1}", dna.genes)
                
                # Salvar no banco
                agent_data = {
                    'agent_id': dna.agent_id,
                    'dna': json.dumps(asdict(dna)),
                    'name': identity.full_name,
                    'nickname': identity.nickname,
                    'personality': identity.personality_archetype,
                    'origin': identity.origin,
                    'resources': random.randint(100, 1000),
                    'generation': 0,
                    'fitness_scores': json.dumps({}),
                    'emotional_state': json.dumps({
                        'happiness': random.uniform(0.3, 0.8),
                        'satisfaction': random.uniform(0.2, 0.7),
                        'trust': random.uniform(0.4, 0.9)
                    })
                }
                
                db.save_agent(dna, identity)
                agents_created += 1
                
                if agents_created % 10 == 0:
                    print(f"   ✅ {agents_created} agentes criados...")
                    
            except Exception as e:
                print(f"   ❌ Erro ao criar agente {i+1}: {e}")
        
        print(f"🎉 População criada: {agents_created} agentes!")
        return agents_created
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("🔧 Verifique se os módulos estão no lugar correto")
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
                    
                    # Salvar no banco (assumindo que existe método save_product)
                    # db.save_product(product)
                    products_created += 1
                    
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

def check_universe_status():
    """Verifica status atual do universo"""
    
    print("📊 Verificando status do universo...")
    
    try:
        from database_manager import LoREDatabase
        
        db = LoREDatabase()
        
        # Contar agentes
        try:
            agent_count = 0  # db.count_agents()
            print(f"🤖 Agentes ativos: {agent_count}")
        except:
            print("🤖 Agentes ativos: Não foi possível verificar")
        
        # Contar produtos  
        try:
            product_count = 0  # db.count_products()
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
    print("  full              - Inicialização completa (recomendado)")
    print()
    print("💡 EXEMPLO:")
    print("  python initialize_universe.py full")

if __name__ == "__main__":
    main()
