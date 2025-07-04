#!/usr/bin/env python3
"""
Validador Completo do Projeto Lore N.A.
=======================================

Script para validar e testar todo o projeto Lore N.A.
- Verifica dependências
- Testa imports
- Executa testes unitários
- Valida estrutura de arquivos

Autor: Lore N.A. Genesis Team
Data: 03 de Julho de 2025
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def print_header(title):
    """Imprime cabeçalho formatado"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"❌ {message}")

def print_warning(message):
    """Imprime mensagem de aviso"""
    print(f"⚠️ {message}")

def check_file_exists(file_path):
    """Verifica se arquivo existe"""
    return Path(file_path).exists()

def check_directory_structure():
    """Verifica estrutura de diretórios"""
    print_header("VERIFICAÇÃO DA ESTRUTURA")

    required_dirs = [
        "src",
        "src/core",
        "src/api",
        "src/web",
        "src/utils",
        "src/models",
        "tests",
        "tests/unit",
        "tests/integration",
        "docs",
        "config",
        "scripts"
    ]

    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print_success(f"Diretório {dir_path}")
        else:
            print_error(f"Diretório {dir_path} não encontrado")

    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/api_server.py",
        "src/database_manager.py",
        "src/dashboard.py"
    ]

    for file_path in required_files:
        if check_file_exists(file_path):
            print_success(f"Arquivo {file_path}")
        else:
            print_error(f"Arquivo {file_path} não encontrado")

def check_python_imports():
    """Verifica se os imports principais funcionam"""
    print_header("VERIFICAÇÃO DE IMPORTS")

    # Adicionar src ao path
    sys.path.insert(0, "src")

    modules_to_test = [
        "api_server",
        "database_manager",
        "dashboard",
        "advanced_launcher",
        "cloud_deployment_config"
    ]

    for module_name in modules_to_test:
        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                f"src/{module_name}.py"
            )
            if spec is None:
                print_error(f"Módulo {module_name}.py não encontrado")
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print_success(f"Import {module_name}")

        except Exception as e:
            print_error(f"Import {module_name}: {str(e)}")

def check_dependencies():
    """Verifica dependências instaladas"""
    print_header("VERIFICAÇÃO DE DEPENDÊNCIAS")

    required_packages = [
        "fastapi",
        "uvicorn",
        "streamlit",
        "plotly",
        "sqlalchemy",
        "requests",
        "jwt"  # PyJWT instala como 'jwt'
    ]

    for package in required_packages:
        try:
            __import__(package)
            print_success(f"Pacote {package}")
        except ImportError:
            print_error(f"Pacote {package} não instalado")

def run_tests():
    """Executa testes unitários"""
    print_header("EXECUÇÃO DE TESTES")

    test_files = [
        "tests/unit/test_sentiment_service.py",
        "tests/unit/test_sentiment_libs.py"
    ]

    for test_file in test_files:
        if check_file_exists(test_file):
            try:
                result = subprocess.run(
                    [sys.executable, test_file],
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                if result.returncode == 0:
                    print_success(f"Teste {test_file}")
                else:
                    print_error(f"Teste {test_file} falhou")
                    if result.stderr:
                        print(f"  Erro: {result.stderr}")
            except Exception as e:
                print_error(f"Erro ao executar teste {test_file}: {e}")
        else:
            print_warning(f"Arquivo de teste {test_file} não encontrado")

def check_config_files():
    """Verifica arquivos de configuração"""
    print_header("VERIFICAÇÃO DE CONFIGURAÇÕES")

    config_files = [
        "config/app.json",
        "config/railway.json",
        "config/docker-compose.yml",
        "Procfile",
        "runtime.txt"
    ]

    for config_file in config_files:
        if check_file_exists(config_file):
            print_success(f"Config {config_file}")
        else:
            print_warning(f"Config {config_file} não encontrado")

def validate_api_server():
    """Valida se o servidor API pode ser iniciado"""
    print_header("VALIDAÇÃO DO SERVIDOR API")

    try:
        # Test import
        sys.path.insert(0, "src")
        from api_server import app
        print_success("API server pode ser importado")

        # Check if FastAPI app exists
        if hasattr(app, 'routes'):
            print_success(f"API tem {len(app.routes)} rotas configuradas")
        else:
            print_error("Aplicação FastAPI não configurada corretamente")

    except Exception as e:
        print_error(f"Erro na validação do API server: {e}")

def main():
    """Função principal de validação"""
    print("🌟 Lore N.A. - Validador de Projeto")
    print("===================================")

    # Mudar para diretório do projeto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Executar todas as verificações
    check_directory_structure()
    check_dependencies()
    check_python_imports()
    check_config_files()
    validate_api_server()
    run_tests()

    print_header("RESUMO DA VALIDAÇÃO")
    print("✅ Validação completa executada!")
    print("📊 Verifique os resultados acima para identificar problemas")
    print("🚀 Se tudo estiver verde, o projeto está pronto para execução!")

if __name__ == "__main__":
    main()
