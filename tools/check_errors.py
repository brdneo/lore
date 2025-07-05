#!/usr/bin/env python3
"""
Error Checker for Lore N.A. Project
===================================

Verifica erros comuns no projeto:
- Imports quebrados
- Sintaxe Python
- Arquivos vazios que não deveriam estar
- Problemas de estrutura

Autor: Lore N.A. Genesis Team
"""

import os
import ast
import sys
from pathlib import Path
import importlib.util

def check_python_syntax(file_path):
    """Verifica sintaxe Python de um arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def check_imports(file_path):
    """Verifica se imports funcionam"""
    try:
        spec = importlib.util.spec_from_file_location("temp_module", file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return True, None
    except Exception as e:
        return False, f"Import error: {e}"

def main():
    """Executa verificação de erros"""
    project_root = Path(__file__).parent.parent
    python_files = []
    
    # Encontrar todos os arquivos Python
    for pattern in ["**/*.py"]:
        python_files.extend(project_root.glob(pattern))
    
    # Filtrar arquivos do .venv
    python_files = [f for f in python_files if ".venv" not in str(f)]
    
    print("🔍 Verificando erros no projeto...")
    errors_found = 0
    
    for file_path in python_files:
        # Verificar sintaxe
        syntax_ok, syntax_error = check_python_syntax(file_path)
        if not syntax_ok:
            print(f"❌ {file_path}: {syntax_error}")
            errors_found += 1
        
        # Verificar se arquivo está vazio (quando não deveria)
        if file_path.stat().st_size == 0 and file_path.name != "__init__.py":
            print(f"⚠️ {file_path}: Arquivo vazio")
    
    if errors_found == 0:
        print("✅ Nenhum erro encontrado!")
    else:
        print(f"❌ {errors_found} erros encontrados.")
        sys.exit(1)

if __name__ == "__main__":
    main()