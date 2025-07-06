#!/usr/bin/env python3
"""
Structure Checker for Lore N.A. Project
=======================================

Verifica se a estrutura do projeto está correta:
- Diretórios obrigatórios existem
- Arquivos essenciais estão presentes
- Estrutura modular está íntegra

Autor: Lore N.A. Genesis Team
"""

import os
from pathlib import Path

# Estrutura esperada do projeto
EXPECTED_STRUCTURE = {
    "directories": [
        "crates/lore-engine/src",
        "python/lore_na/agents",
        "python/lore_na/core",
        "python/lore_na/genetics",
        "python/lore_na/models",
        "python/lore_na/utils",
        "docs/getting-started",
        "docs/guides",
        "docs/reports",
        "docs/strategy",
        "docs/internal",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "tests/benchmarks",
        "scripts/setup",
        "scripts/build",
        "scripts/deployment",
        "scripts/maintenance",
        "config",
        "examples/basic",
        "examples/advanced",
        "examples/enterprise",
        "backup",
        "assets"
    ],
    "files": [
        "README.md",
        "LICENSE",
        "Makefile",
        "Dockerfile",
        "Cargo.toml",
        ".gitignore",
        ".env.example",
        "start.py",
        "validate_project.py",
        "crates/lore-engine/Cargo.toml",
        "python/pyproject.toml",
        "python/requirements.txt"
    ]
}


def check_directory_structure():
    """Verifica se diretórios obrigatórios existem"""
    project_root = Path(__file__).parent.parent
    missing_dirs = []

    for directory in EXPECTED_STRUCTURE["directories"]:
        dir_path = project_root / directory
        if not dir_path.exists():
            missing_dirs.append(directory)
        elif not dir_path.is_dir():
            missing_dirs.append(f"{directory} (não é diretório)")

    return missing_dirs


def check_essential_files():
    """Verifica se arquivos essenciais existem"""
    project_root = Path(__file__).parent.parent
    missing_files = []

    for file_path in EXPECTED_STRUCTURE["files"]:
        full_path = project_root / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        elif full_path.is_dir():
            missing_files.append(f"{file_path} (é diretório, deveria ser arquivo)")

    return missing_files


def check_wrapper_files():
    """Verifica se os wrappers na raiz estão implementados"""
    project_root = Path(__file__).parent.parent
    issues = []

    # Verificar start.py
    start_py = project_root / "start.py"
    if start_py.exists():
        with open(start_py, 'r') as f:
            content = f.read()
            if len(content.strip()) < 200:  # Ajustado o limite
                issues.append("start.py parece estar muito pequeno (esperado wrapper)")
            elif "scripts/maintenance/start.py" not in content:
                issues.append("start.py não parece ser um wrapper válido")

    # Verificar validate_project.py
    validate_py = project_root / "validate_project.py"
    if validate_py.exists():
        with open(validate_py, 'r') as f:
            content = f.read()
            if len(content.strip()) < 200:  # Ajustado o limite
                issues.append("validate_project.py parece estar muito pequeno (esperado wrapper)")
            elif "scripts/maintenance/validate_project.py" not in content:
                issues.append("validate_project.py não parece ser um wrapper válido")

    return issues


def main():
    """Executa verificação da estrutura"""
    print("🏗️ Verificando estrutura do projeto...")

    # Verificar diretórios
    missing_dirs = check_directory_structure()
    if missing_dirs:
        print("❌ Diretórios ausentes:")
        for dir_name in missing_dirs:
            print(f"   - {dir_name}")
    else:
        print("✅ Todos os diretórios obrigatórios existem")

    # Verificar arquivos
    missing_files = check_essential_files()
    if missing_files:
        print("❌ Arquivos ausentes:")
        for file_name in missing_files:
            print(f"   - {file_name}")
    else:
        print("✅ Todos os arquivos essenciais existem")

    # Verificar wrappers
    wrapper_issues = check_wrapper_files()
    if wrapper_issues:
        print("⚠️ Problemas com wrappers:")
        for issue in wrapper_issues:
            print(f"   - {issue}")
    else:
        print("✅ Wrappers da raiz estão OK")

    # Resultado final
    total_issues = len(missing_dirs) + len(missing_files) + len(wrapper_issues)
    if total_issues == 0:
        print("\n🎉 Estrutura do projeto está perfeita!")
    else:
        print(f"\n⚠️ {total_issues} problemas encontrados na estrutura.")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
