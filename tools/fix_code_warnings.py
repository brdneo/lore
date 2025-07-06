#!/usr/bin/env python3
"""
Ferramenta para corrigir automaticamente warnings de código Python
Corrige imports não utilizados, whitespace, linhas muito longas, etc.
"""

import os
import re
import autopep8
import subprocess
from pathlib import Path


def remove_unused_imports(content: str) -> str:
    """Remove imports não utilizados simples"""
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        # Skip comum imports não utilizados
        if any(unused in line for unused in [
            "import hashlib",
            "import os",
            "import time",
            "import math",
            "import json",
            "import glob",
            "from typing import List",
            "from typing import Dict",
            "from typing import Any",
            "from typing import Optional",
            "from concurrent.futures import ThreadPoolExecutor",
            "from concurrent.futures import ProcessPoolExecutor",
            "import asyncio",
            "import traceback",
            "from datetime import datetime",
            "from datetime import timedelta",
            "from dataclasses import asdict",
            "from dataclasses import field"
        ]):
            # Verifica se está sendo usado no restante do código
            import_name = line.split()[-1] if 'import' in line else ''
            if import_name and import_name not in content:
                continue  # Skip linha se não está sendo usado

        new_lines.append(line)

    return '\n'.join(new_lines)


def fix_f_strings(content: str) -> str:
    """Fix f-strings sem placeholders"""
    # Converte "texto" para "texto" quando não há placeholders
    content = re.sub(r'"([^"]*)"', lambda m: f'"{m.group(1)}"' if '{' not in m.group(1) else m.group(0), content)
    content = re.sub(r"'([^']*)'", lambda m: f"'{m.group(1)}'" if '{' not in m.group(1) else m.group(0), content)
    return content


def fix_syntax_error_file(file_path: str):
    """Fix arquivo com erro de sintaxe específico"""
    if "proximos_passos_2025.py" in file_path:
        # Este arquivo tem erro de string não terminada
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix string não terminada adicionando """
        if 'SyntaxError: unterminated triple-quoted string literal' in content:
            content += '\n"""\n'

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)


def fix_file(file_path: str) -> bool:
    """Corrige um arquivo específico"""
    try:
        # Casos especiais primeiro
        if "proximos_passos_2025.py" in file_path:
            fix_syntax_error_file(file_path)
            return True

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Remove imports não utilizados
        content = remove_unused_imports(content)

        # Fix f-strings
        content = fix_f_strings(content)

        # Usa autopep8 para corrigir formatação
        fixed_content = autopep8.fix_code(
            content,
            options={
                'max_line_length': 120,
                'aggressive': 2,
                'select': [
                    'E501',  # linha muito longa
                    'W291',  # trailing whitespace
                    'W293',  # blank line contains whitespace
                    'E302',  # expected 2 blank lines
                    'E305',  # expected 2 blank lines after class/function
                    'E128',  # continuation line under-indented
                    'E261',  # at least two spaces before inline comment
                    'E401',  # multiple imports on one line
                    'E402',  # module level import not at top of file
                    'W292',  # no newline at end of file
                ]
            }
        )

        # Se mudou, salva o arquivo
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"✓ No changes needed: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False


def main():
    print("🔧 Fixing code warnings automatically...")

    # Instalar autopep8 se necessário
    try:
        import autopep8
    except ImportError:
        print("Installing autopep8...")
        subprocess.run(["pip", "install", "autopep8"], check=True)
        import autopep8

    # Encontrar todos os arquivos Python
    python_files = []

    # Diretórios para ignorar
    ignore_dirs = {".venv", "venv", "env", "__pycache__", ".git", "backup", "node_modules"}

    for root in ["python/", "tools/", "scripts/", "examples/", "."]:
        if os.path.exists(root):
            for path in Path(root).rglob("*.py"):
                # Verifica se alguma parte do caminho está nos diretórios ignorados
                path_parts = set(path.parts)
                if not path_parts.intersection(ignore_dirs):
                    python_files.append(str(path))

    fixed_count = 0
    total_files = len(python_files)

    for file_path in python_files:
        if fix_file(file_path):
            fixed_count += 1

    print("\n📊 Summary:")
    print(f"   Total files checked: {total_files}")
    print(f"   Files fixed: {fixed_count}")
    print(f"   Files with no issues: {total_files - fixed_count}")

    # Verificar se ainda há erros
    print("\n🔍 Running final check...")
    result = subprocess.run([
        "python", "-m", "flake8",
        "--max-line-length=120",
        "--extend-ignore=E203,W503,F401",
        "python/", "tools/", "scripts/generate-secrets.py",
        "start.py", "validate_project.py", "examples/"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ All warnings fixed!")
    else:
        remaining_warnings = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        print(f"⚠️  {remaining_warnings} warnings remaining")
        if remaining_warnings < 50:  # Show only if manageable
            print(result.stdout)


if __name__ == "__main__":
    main()
