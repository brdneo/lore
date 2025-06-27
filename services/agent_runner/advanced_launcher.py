#!/usr/bin/env python3
"""
Advanced Launcher - Lore N.A.
=============================

Launcher para módulos avançados do sistema Lore N.A.
- API Server (FastAPI)
- Dashboard (Streamlit)
- Sistema de Economia Emocional

Autor: Lore N.A. Genesis Team
Data: 27 de Junho de 2025
"""

import subprocess
import sys
import os
import signal
import webbrowser
from time import sleep
import threading

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def run_api_server():
    """Executa o servidor API FastAPI"""
    print("🚀 Iniciando API Server...")
    print("🌐 API estará disponível em: http://localhost:8000")
    print("📖 Documentação automática em: http://localhost:8000/docs")
    print("💡 Pressione Ctrl+C para parar")
    
    try:
        subprocess.run([
            "uvicorn", "api_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 API Server parado pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar API Server: {e}")

def run_dashboard():
    """Executa o dashboard Streamlit"""
    print("📊 Iniciando Dashboard...")
    print("🌐 Dashboard estará disponível em: http://localhost:8501")
    print("💡 Pressione Ctrl+C para parar")
    
    # Aguarda um pouco e abre automaticamente o browser
    def open_browser():
        sleep(3)
        webbrowser.open("http://localhost:8501")
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        subprocess.run([
            "streamlit", "run", "dashboard.py",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard parado pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Dashboard: {e}")

def test_emotional_economy():
    """Testa o sistema de economia emocional"""
    print("💰 Testando Sistema de Economia Emocional...")
    
    try:
        subprocess.run([sys.executable, "-c", """
import sys
sys.path.append('.')
from emotional_economy import *
from agent_dna import AgentDNA
from agent_name_generator import AgentNameGenerator

print('\\n🏦 SISTEMA DE ECONOMIA EMOCIONAL - TESTE')
print('=' * 50)

# Criar wallet emocional
wallet = EmotionalWallet("demo_agent_01")
print(f'💳 Wallet criada: {wallet.agent_id}')

# Gerar tokens emocionais
joy_token = EmotionToken(
    emotion_type=EmotionType.JOY,
    amount=100.0,
    quality=0.8,
    origin_agent="demo_agent_01"
)
print(f'😊 Token de alegria criado: {joy_token.amount} unidades')

trust_token = EmotionToken(
    emotion_type=EmotionType.TRUST,
    amount=75.0,
    quality=0.9,
    origin_agent="demo_agent_01"
)
print(f'🤝 Token de confiança criado: {trust_token.amount} unidades')

# Adicionar tokens à wallet
wallet.add_token(joy_token)
wallet.add_token(trust_token)

print(f'\\n💰 Balance total: {wallet.total_balance:.2f} tokens')
print(f'📊 Portfolios: {len(wallet.portfolios)} tipos de emoção')

# Criar marketplace
marketplace = EmotionalMarketplace()
print(f'\\n🏬 Marketplace criado')

# Listar tokens
print(f'\\n📋 Tokens na wallet:')
for emotion_type, tokens in wallet.portfolios.items():
    total = sum(token.amount for token in tokens)
    print(f'  {emotion_type.value}: {total:.1f} tokens')

# Valor de mercado
market_value = wallet.calculate_market_value()
print(f'\\n💵 Valor de mercado total: {market_value:.2f}')

print('\\n✅ Sistema de Economia Emocional funcionando!')
        """], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao testar economia emocional: {e}")

def run_full_demo():
    """Executa uma demonstração completa do sistema"""
    print("🎭 Iniciando Demonstração Completa...")
    
    try:
        subprocess.run([sys.executable, "-c", """
import sys
sys.path.append('.')
from agent_dna import AgentDNA
from agent_name_generator import AgentNameGenerator
from neural_web import NeuralWeb
from social_agent import SocialAgent
from emotional_economy import *

print('\\n🌟 LORE N.A. - DEMONSTRAÇÃO COMPLETA')
print('=' * 60)

# 1. Criar agentes com DNA e identidades
print('\\n1️⃣ CRIANDO AGENTES NEURAIS')
name_gen = AgentNameGenerator()
agents = []

for i in range(3):
    # DNA único para cada agente
    dna = AgentDNA.generate_random(f'demo_agent_{i+1:02d}')
    
    # Identidade única
    identity = name_gen.generate_identity(
        dna.agent_id, 
        'Demo Agent', 
        dna.genes
    )
    
    # Agente social
    agent = SocialAgent(dna.agent_id, dna, identity)
    agents.append(agent)
    
    print(f'   👤 {identity.full_name} ({identity.personality_archetype})')
    print(f'      🧬 Fitness: {dna.calculate_fitness()["overall"]:.2f}')

# 2. Criar rede neural social
print('\\n2️⃣ CRIANDO REDE NEURAL SOCIAL')
neural_web = NeuralWeb()

for agent in agents:
    neural_web.add_agent(agent.agent_id, agent.identity.personality_archetype)

print(f'   🌐 Rede criada com {len(neural_web.agents)} agentes')

# 3. Estabelecer conexões
print('\\n3️⃣ ESTABELECENDO CONEXÕES NEURAIS')
# Conectar agentes baseado em compatibilidade
for i, agent1 in enumerate(agents):
    for j, agent2 in enumerate(agents[i+1:], i+1):
        compatibility = agent1.dna.calculate_compatibility(agent2.dna)
        if compatibility > 0.6:  # Threshold para conexão
            neural_web.connect_agents(agent1.agent_id, agent2.agent_id, compatibility)
            print(f'   🔗 {agent1.identity.full_name} ↔ {agent2.identity.full_name} (compatibilidade: {compatibility:.2f})')

# 4. Sistema de economia emocional
print('\\n4️⃣ ECONOMIA EMOCIONAL')
marketplace = EmotionalMarketplace()

for agent in agents:
    # Criar wallet para cada agente
    wallet = EmotionalWallet(agent.agent_id)
    
    # Gerar tokens baseado na personalidade
    if 'Visionário' in agent.identity.personality_archetype:
        token = EmotionToken(EmotionType.JOY, 100.0, 0.8, agent.agent_id)
    elif 'Líder' in agent.identity.personality_archetype:
        token = EmotionToken(EmotionType.TRUST, 80.0, 0.9, agent.agent_id)
    else:
        token = EmotionToken(EmotionType.ANTICIPATION, 60.0, 0.7, agent.agent_id)
    
    wallet.add_token(token)
    marketplace.wallets[agent.agent_id] = wallet
    
    print(f'   💳 {agent.identity.full_name}: {wallet.total_balance:.1f} tokens')

# 5. Métricas da rede
print('\\n5️⃣ MÉTRICAS DA REDE NEURAL')
metrics = neural_web.get_network_metrics()
print(f'   📊 Densidade: {metrics["density"]:.2f}')
print(f'   🎯 Centralidade média: {metrics["avg_centrality"]:.2f}')
print(f'   🏘️ Comunidades: {metrics["communities"]}')

print('\\n✨ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!')
print('🎯 Sistema Lore N.A. totalmente funcional!')
        """], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na demonstração: {e}")

def show_menu():
    """Exibe o menu principal"""
    clear_screen()
    print("🌟" + "=" * 58 + "🌟")
    print("🚀" + " " * 15 + "LORE N.A. - LAUNCHER AVANÇADO" + " " * 15 + "🚀")
    print("🌟" + "=" * 58 + "🌟")
    print()
    print("📋 OPÇÕES DISPONÍVEIS:")
    print()
    print("   1️⃣  🌐 API Server (FastAPI)")
    print("   2️⃣  📊 Dashboard (Streamlit)")
    print("   3️⃣  💰 Testar Economia Emocional")
    print("   4️⃣  🎭 Demonstração Completa")
    print("   5️⃣  🧪 Teste Rápido (quick_test.py)")
    print("   6️⃣  📊 Status do Sistema")
    print("   7️⃣  🔗 Menu Neural Web")
    print("   8️⃣  📚 Documentação")
    print("   0️⃣  🚪 Sair")
    print()
    print("🌟" + "=" * 58 + "🌟")

def show_documentation():
    """Mostra informações de documentação"""
    clear_screen()
    print("📚 DOCUMENTAÇÃO LORE N.A.")
    print("=" * 50)
    print()
    print("📖 DOCUMENTOS PRINCIPAIS:")
    print("   • README.md                    - Visão geral do projeto")
    print("   • GENESIS-PROTOCOL.md          - Protocolo de DNA digital")
    print("   • SESSAO-COMPLETA-REPORT.md    - Relatório completo da sessão")
    print()
    print("🧪 TESTES E VALIDAÇÃO:")
    print("   • python3 quick_test.py       - Teste rápido sem API")
    print("   • python3 test_neural_web.py  - Teste completo Neural Web")
    print("   • python3 test_agent_identity.py - Teste sistema de identidade")
    print()
    print("🚀 EXECUÇÃO:")
    print("   • ./neural_web_runner.sh       - Menu interativo completo")
    print("   • python3 system_status.py    - Status atual do sistema")
    print()
    print("🌐 MÓDULOS AVANÇADOS:")
    print("   • api_server.py                - API REST para agentes")
    print("   • dashboard.py                 - Dashboard visual")
    print("   • emotional_economy.py         - Sistema de tokens emocionais")
    print()
    print("Pressione ENTER para voltar...")
    input()

def main():
    """Função principal do launcher"""
    while True:
        show_menu()
        
        try:
            choice = input("🎯 Escolha uma opção: ").strip()
            
            if choice == "1":
                clear_screen()
                run_api_server()
                input("\nPressione ENTER para continuar...")
                
            elif choice == "2":
                clear_screen()
                run_dashboard()
                input("\nPressione ENTER para continuar...")
                
            elif choice == "3":
                clear_screen()
                test_emotional_economy()
                input("\nPressione ENTER para continuar...")
                
            elif choice == "4":
                clear_screen()
                run_full_demo()
                input("\nPressione ENTER para continuar...")
                
            elif choice == "5":
                clear_screen()
                print("🧪 Executando teste rápido...")
                subprocess.run([sys.executable, "quick_test.py"])
                input("\nPressione ENTER para continuar...")
                
            elif choice == "6":
                clear_screen()
                print("📊 Verificando status do sistema...")
                subprocess.run([sys.executable, "system_status.py"])
                input("\nPressione ENTER para continuar...")
                
            elif choice == "7":
                clear_screen()
                print("🔗 Abrindo menu Neural Web...")
                subprocess.run(["./neural_web_runner.sh"])
                input("\nPressione ENTER para continuar...")
                
            elif choice == "8":
                show_documentation()
                
            elif choice == "0":
                clear_screen()
                print("🌟 Obrigado por usar o Lore N.A.!")
                print("🚀 Até a próxima aventura na vida artificial!")
                break
                
            else:
                print("❌ Opção inválida. Tente novamente.")
                sleep(1)
                
        except KeyboardInterrupt:
            clear_screen()
            print("\n🛑 Programa interrompido pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()
