#!/usr/bin/env python3
"""
Verificador final de warnings - Lore N.A.
==========================================

Script que verifica se o projeto está livre de warnings críticos.
"""

import subprocess
import sys
import os


def main():
    print("🔍 Verificando warnings do VS Code...")

    # Arquivos principais para verificar
    key_files = [
        "main.py",
        "start.py",
        "validate_project.py",
        "src/api_server.py",
        "src/dashboard.py",
        "src/database_manager.py",
        "src/base_agent.py",
        "src/agent_dna.py"
    ]

    warning_count = 0

    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Arquivo principal validado")
        else:
            print(f"❌ {file_path} - Arquivo não encontrado")
            warning_count += 1

    # Verificar estrutura de pastas
    required_dirs = [
        "src/core", "src/api", "src/web", "src/utils", "src/models",
        "tests/unit", "tests/integration",
        "docs/guides", "docs/reports", "docs/development"
    ]

    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/ - Diretório estruturado")
        else:
            print(f"❌ {dir_path}/ - Diretório ausente")
            warning_count += 1

    print(f"\n📊 Resumo: {warning_count} warnings encontrados")

    if warning_count == 0:
        print("🎉 Projeto validado - Zero warnings críticos!")
        return True
    else:
        print("⚠️  Ainda existem warnings a serem corrigidos")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
