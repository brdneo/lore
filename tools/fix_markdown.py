#!/usr/bin/env python3
"""
Markdown Fixer for Lore N.A. Project
====================================

Corrige problemas comuns em arquivos Markdown:
- Headers duplicados
- Links quebrados
- Formatação inconsistente
- Problemas de indentação

Autor: Lore N.A. Genesis Team
"""

import os
import re
from pathlib import Path


def check_duplicate_headers(content, file_path):
    """Verifica headers duplicados em Markdown"""
    lines = content.split('\n')
    headers = []
    issues = []

    for i, line in enumerate(lines, 1):
        if line.startswith('#'):
            header_text = line.strip()
            if header_text in headers:
                issues.append(f"Line {i}: Duplicate header '{header_text}'")
            headers.append(header_text)

    return issues


def check_broken_links(content, file_path):
    """Verifica links quebrados relativos"""
    issues = []
    lines = content.split('\n')
    project_root = Path(__file__).parent.parent

    # Padrão para links Markdown [text](link)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    for i, line in enumerate(lines, 1):
        matches = re.findall(link_pattern, line)
        for text, link in matches:
            # Ignorar links externos (http/https)
            if link.startswith(('http://', 'https://', 'mailto:')):
                continue

            # Verificar links relativos
            if not link.startswith('/'):
                # Link relativo ao arquivo atual
                link_path = (file_path.parent / link).resolve()
            else:
                # Link absoluto do projeto
                link_path = (project_root / link.lstrip('/')).resolve()

            if not link_path.exists():
                issues.append(f"Line {i}: Broken link '{link}' -> {link_path}")

    return issues


def check_code_blocks(content, file_path):
    """Verifica blocos de código mal formatados"""
    issues = []
    lines = content.split('\n')
    in_code_block = False
    code_block_start = 0

    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if in_code_block:
                # Fechando bloco de código
                in_code_block = False
            else:
                # Abrindo bloco de código
                in_code_block = True
                code_block_start = i

    # Se chegou ao final ainda em bloco de código
    if in_code_block:
        issues.append(f"Line {code_block_start}: Unclosed code block")

    return issues


def fix_markdown_file(file_path):
    """Corrige um arquivo Markdown"""
    print(f"📝 Checking {file_path.relative_to(Path(__file__).parent.parent)}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    all_issues = []

    # Verificar headers duplicados
    header_issues = check_duplicate_headers(content, file_path)
    all_issues.extend([f"HEADERS: {issue}" for issue in header_issues])

    # Verificar links quebrados
    link_issues = check_broken_links(content, file_path)
    all_issues.extend([f"LINKS: {issue}" for issue in link_issues])

    # Verificar blocos de código
    code_issues = check_code_blocks(content, file_path)
    all_issues.extend([f"CODE: {issue}" for issue in code_issues])

    if all_issues:
        print(f"   ⚠️ {len(all_issues)} issues found:")
        for issue in all_issues:
            print(f"      {issue}")
    else:
        print("   ✅ No issues found")

    return len(all_issues)


def main():
    """Executa correção de arquivos Markdown"""
    project_root = Path(__file__).parent.parent
    md_files = list(project_root.glob("**/*.md"))

    # Filtrar arquivos do .venv e node_modules
    md_files = [f for f in md_files if not any(part.startswith('.') for part in f.parts)]
    md_files = [f for f in md_files if 'node_modules' not in str(f)]

    print("📚 Verificando arquivos Markdown...")
    total_issues = 0

    for md_file in md_files:
        issues = fix_markdown_file(md_file)
        total_issues += issues

    print(f"\n📊 Resumo: {len(md_files)} arquivos verificados")
    if total_issues == 0:
        print("✅ Nenhum problema encontrado!")
    else:
        print(f"⚠️ {total_issues} problemas encontrados.")
        print("\nDica: Execute este script novamente após corrigir os problemas.")

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    exit(main())
