#!/usr/bin/env python3
"""
Teste de Universo Autônomo - Versão Simples
"""

import asyncio
import os
import sys
import time
from datetime import datetime

# Configurar environment
os.environ['KONG_JWT_SECRET'] = 'test-autonomous-key'
os.environ['DATABASE_URL'] = 'sqlite:///test_autonomous.db'

# Adicionar src ao path
sys.path.append('/home/brendo/lore/src')

async def test_autonomous_universe():
    """Teste básico do universo autônomo"""
    
    print("🌟 TESTE UNIVERSO AUTÔNOMO")
    print("=" * 30)
    
    try:
        # Importar após configurar environment
        from agent_dna import AgentDNA
        from neural_web import NeuralWeb  
        from social_agent import SocialAgent
        
        print("✅ Imports realizados com sucesso")
        
        # Criar componentes
        neural_web = NeuralWeb()
        agents = {}
        
        print("🧬 Criando 5 agentes...")
        
        # Criar agentes
        for i in range(5):
            dna = AgentDNA.generate_random()
            agent_id = f"auto_agent_{i+1:03d}"
            
            agent = SocialAgent(agent_id, dna, neural_web)
            agents[agent_id] = agent
            
            print(f"  ✓ {agent.identity.nickname} criado")
        
        print(f"\n🎉 {len(agents)} agentes criados!")
        
        # Simular 10 ciclos autônomos
        print("\n🔄 Simulando ciclos autônomos...")
        
        for cycle in range(1, 11):
            print(f"\n--- Ciclo {cycle} ---")
            
            # Cada agente busca conexões
            for agent in agents.values():
                if cycle % 3 == 0:  # A cada 3 ciclos
                    agent.seek_new_connections(agents, max_new_connections=1)
                
                if cycle % 2 == 0:  # A cada 2 ciclos
                    agent.maintain_relationships(agents)
                
                if cycle % 5 == 0:  # A cada 5 ciclos
                    agent.influence_network(agents)
            
            # Atualizar métricas
            neural_web.update_social_metrics()
            
            # Mostrar estatísticas
            total_connections = len(neural_web.connections) if neural_web.connections else 0
            print(f"  📊 Conexões totais: {total_connections}")
            
            # Aguardar entre ciclos (simulação)
            await asyncio.sleep(1)
        
        print("\n📈 RESULTADO FINAL:")
        
        # Estatísticas finais
        stats = neural_web.get_network_statistics()
        print(f"  🌐 Estatísticas da rede: {stats}")
        
        # Resumo dos agentes
        print("\n👥 POPULAÇÃO FINAL:")
        for agent_id, agent in agents.items():
            try:
                summary = agent.get_social_summary()
                connections = summary['total_connections']
                influences = summary['influences_given']
                
                print(f"  {agent.identity.nickname}: {connections} conexões, {influences} influências")
            except Exception as e:
                print(f"  {agent.identity.nickname}: erro no resumo - {e}")
        
        print("\n✅ TESTE AUTÔNOMO CONCLUÍDO!")
        print("🚀 O universo pode funcionar sozinho!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_autonomous_universe())
    if success:
        print("\n🎯 PRÓXIMO PASSO: Executar versão completa 24/7")
    else:
        print("\n💥 Falha no teste - verificar erros")
