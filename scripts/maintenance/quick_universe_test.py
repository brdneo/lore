#!/usr/bin/env python3
"""
Quick Universe Test - Criar primeiros agentes
"""

import os
import sys

# Adicionar src ao path
sys.path.append('/home/brendo/lore/src')

# Configurar variáveis de ambiente necessárias
os.environ['KONG_JWT_SECRET'] = 'test-secret-for-universe'
os.environ['DATABASE_URL'] = 'sqlite:///test_universe.db'

def test_agent_creation():
    """Teste rápido de criação de agentes"""
    print("🌟 TESTE RÁPIDO - CRIAÇÃO DE UNIVERSO")
    print("=" * 40)
    
    try:
        # Importar componentes necessários
        print("📦 Importando componentes...")
        from agent_dna import AgentDNA
        from neural_web import NeuralWeb
        from social_agent import SocialAgent
        
        print("✅ Componentes importados com sucesso!")
        
        # Criar neural web
        print("\n🧠 Criando Neural Web...")
        neural_web = NeuralWeb()
        print("✅ Neural Web criada!")
        
        # Criar 3 agentes de teste
        print("\n🧬 Criando agentes...")
        agents = []
        
        for i in range(3):
            print(f"  Criando agente {i+1}...")
            
            # Gerar DNA
            dna = AgentDNA.generate_random()
            agent_id = f"test_agent_{i+1:03d}"
            
            # Criar agente social
            agent = SocialAgent(agent_id, dna, neural_web)
            agents.append(agent)
            
            print(f"  ✅ {agent.identity.full_name} '{agent.identity.nickname}' criado!")
            print(f"     Personalidade: {agent.identity.personality_archetype}")
        
        print(f"\n🎉 {len(agents)} agentes criados com sucesso!")
        
        # Mostrar informações dos agentes
        print("\n👥 POPULAÇÃO INICIAL:")
        for i, agent in enumerate(agents, 1):
            print(f"\n  {i}. {agent.identity.full_name} '{agent.identity.nickname}'")
            print(f"     🏷️  ID: {agent.agent_id}")
            print(f"     🎭 Personalidade: {agent.identity.personality_archetype}")
            print(f"     🌍 Origem: {agent.identity.origin}")
            print(f"     🎯 Objetivos: {', '.join(agent.social_goals)}")
        
        # Testar uma interação simples
        print("\n🔄 TESTE DE INTERAÇÃO:")
        if len(agents) >= 2:
            agent1 = agents[0]
            agent2 = agents[1]
            
            print(f"  {agent1.identity.nickname} tentando conectar com {agent2.identity.nickname}...")
            
            # Criar dict de agentes para a função
            agents_dict = {agent.agent_id: agent for agent in agents}
            
            # Tentar conexão
            success = agent1.initiate_connection(agent2.agent_id, agents_dict)
            
            if success:
                print(f"  ✅ Conexão estabelecida!")
                
                # Verificar conexões
                connections = neural_web.get_agent_connections(agent1.agent_id)
                print(f"  📡 {agent1.identity.nickname} agora tem {len(connections)} conexão(ões)")
            else:
                print(f"  ❌ Falha na conexão")
        
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. ✅ População inicial criada")
        print("2. 🔄 Agentes podem se conectar")
        print("3. 🛒 Próximo: Criar marketplace com produtos")
        print("4. 🔄 Próximo: Iniciar ciclos automáticos")
        print("5. 🌐 Próximo: Ativar API web")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agent_creation()
    if success:
        print("\n🎉 UNIVERSO DANDO SEUS PRIMEIROS PASSOS!")
    else:
        print("\n💥 Erro na inicialização do universo")
