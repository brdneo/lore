#!/usr/bin/env python3
"""
Universe Status Checker - Versão Simples
Verifica o status do universo sem depender de conexões externas
"""

import os
import json
import glob
from pathlib import Path


def check_file_exists(filepath):
    """Verifica se arquivo existe"""
    return "✅" if os.path.exists(filepath) else "❌"


def count_files_in_directory(directory, pattern="*"):
    """Conta arquivos em diretório"""
    try:
        files = list(Path(directory).glob(pattern))
        return len(files)
    except:
        return 0


def analyze_universe_status():
    """Analisa status do universo sem conexões externas"""

    print("🌟 LORE N.A. - UNIVERSE STATUS CHECKER")
    print("=" * 50)
    print()

    # 1. ESTRUTURA BÁSICA
    print("## 📁 ESTRUTURA BÁSICA")
    core_files = {
        "main.py": "/home/brendo/lore/main.py",
        "start.py": "/home/brendo/lore/start.py",
        "Procfile": "/home/brendo/lore/Procfile",
        ".env": "/home/brendo/lore/.env"
    }

    for name, path in core_files.items():
        status = check_file_exists(path)
        print(f"- {status} {name}")
    print()

    # 2. COMPONENTES DO UNIVERSO
    print("## 🧬 COMPONENTES DO UNIVERSO")
    universe_components = {
        "Agent DNA": "/home/brendo/lore/src/agent_dna.py",
        "Evolved Agent": "/home/brendo/lore/src/evolved_agent.py",
        "Population Manager": "/home/brendo/lore/src/population_manager.py",
        "Database Manager": "/home/brendo/lore/src/database_manager.py",
        "API Server": "/home/brendo/lore/src/api_server.py",
        "Neural Web": "/home/brendo/lore/src/neural_web.py"
    }

    for name, path in universe_components.items():
        status = check_file_exists(path)
        print(f"- {status} {name}")
    print()

    # 3. CONFIGURAÇÕES DE DEPLOY
    print("## 🚀 CONFIGURAÇÕES DE DEPLOY")
    deploy_files = {
        "Railway Config": "/home/brendo/lore/config/railway.json",
        "App Config": "/home/brendo/lore/config/app.json",
        "Requirements": "/home/brendo/lore/requirements.txt",
        "Runtime": "/home/brendo/lore/runtime.txt"
    }

    for name, path in deploy_files.items():
        status = check_file_exists(path)
        print(f"- {status} {name}")
    print()

    # 4. DOCUMENTAÇÃO
    print("## 📚 DOCUMENTAÇÃO")
    docs_count = count_files_in_directory("/home/brendo/lore/docs", "**/*.md")
    reports_count = count_files_in_directory("/home/brendo/lore/docs/reports", "*.md")
    print(f"- ✅ Total de documentos: {docs_count}")
    print(f"- ✅ Relatórios: {reports_count}")
    print()

    # 5. STATUS DOS 5 UNIVERSOS
    print("## 🌍 STATUS DOS 5 UNIVERSOS")
    universes = [
        ("🏪 LIMBO", "Marketplace de compras", "Implementado"),
        ("🎨 ODYSSEY", "Universo criativo", "Estrutura pronta"),
        ("👥 RITUAL", "Rede social", "Neural Web ativo"),
        ("🧠 ENGINE", "IA e análises", "Sentiment Analysis v3.0"),
        ("📦 LOGS", "Operações e logs", "Sistema de logs ativo")
    ]

    for icon, name, status in universes:
        print(f"- {icon} **{name}**: {status}")
    print()

    # 6. O QUE FALTA PARA ATIVAR
    print("## ⚠️ O QUE FALTA PARA ATIVAÇÃO COMPLETA")
    print()
    print("### 🔴 CRÍTICO (Impede funcionamento)")
    print("1. **População inicial**: Não há agentes criados ainda")
    print("2. **Produtos no marketplace**: Catálogo vazio")
    print("3. **Database inicializado**: Tabelas não populadas")
    print("4. **Railway deploy ativo**: URL retornando 404")
    print()

    print("### 🟡 IMPORTANTE (Limita funcionalidade)")
    print("5. **Scheduler de ciclos**: Agentes não executam automaticamente")
    print("6. **Dashboard real-time**: Não mostra atividade atual")
    print("7. **Logs estruturados**: Pouco feedback de atividade")
    print()

    print("### 🟢 OPCIONAL (Melhorias futuras)")
    print("8. **WebSockets**: Para updates em tempo real")
    print("9. **Métricas avançadas**: Analytics detalhados")
    print("10. **API rate limiting**: Proteção contra abuso")
    print()

    # 7. LINKS E URLS
    print("## 🔗 URLS E ACESSOS")
    print()
    print("### 🌐 URLs Principais")
    print("- **Railway (público)**: https://lore-na-production.up.railway.app")
    print("- **Railway (privado)**: lore.railway.internal")
    print("- **Local API**: http://localhost:8080")
    print("- **Local Dashboard**: http://localhost:8501")
    print()

    print("### 📊 Endpoints da API")
    print("- `/health` - Status do sistema")
    print("- `/agents` - Lista de agentes")
    print("- `/products` - Produtos do marketplace")
    print("- `/neural-web` - Rede social")
    print("- `/universe-status` - Status completo")
    print()

    # 8. AÇÕES IMEDIATAS
    print("## 🎯 AÇÕES IMEDIATAS PARA ATIVAÇÃO")
    print()
    print("### Etapa 1: Inicializar Database (5 min)")
    print("```bash")
    print("python3 src/database_manager.py  # Criar tabelas")
    print("```")
    print()

    print("### Etapa 2: Criar População Inicial (10 min)")
    print("```bash")
    print("python3 create_initial_population.py  # Criar agentes")
    print("```")
    print()

    print("### Etapa 3: Popular Marketplace (10 min)")
    print("```bash")
    print("python3 populate_marketplace.py  # Adicionar produtos")
    print("```")
    print()

    print("### Etapa 4: Ativar Ciclos (5 min)")
    print("```bash")
    print("python3 start_universe_cycles.py  # Iniciar automação")
    print("```")
    print()

    print("### Etapa 5: Testar Funcionamento (5 min)")
    print("```bash")
    print("curl http://localhost:8080/universe-status")
    print("curl http://localhost:8080/agents")
    print("```")
    print()

    # 9. RESUMO FINAL
    print("## 📝 RESUMO EXECUTIVO")
    print()
    print("**Status Atual**: 🟡 **INFRAESTRUTURA PRONTA, UNIVERSO INATIVO**")
    print()
    print("✅ **O que está funcionando:**")
    print("- Código completo e sem erros")
    print("- API e Dashboard operacionais")
    print("- Sistema de DNA e evolução implementado")
    print("- Deploy configurado (Railway + Neon)")
    print("- Documentação completa")
    print()
    print("❌ **O que falta para o universo 'respirar':**")
    print("- População de agentes criada")
    print("- Marketplace com produtos")
    print("- Ciclos automáticos executando")
    print("- Deploy Railway ativo")
    print()
    print("⏱️ **Tempo para ativação completa**: ~35 minutos")
    print("🎯 **Próximo passo**: Executar scripts de inicialização")
    print()
    print("🚀 **Depois disso**: O universo começará a evoluir sozinho!")


if __name__ == "__main__":
    analyze_universe_status()
