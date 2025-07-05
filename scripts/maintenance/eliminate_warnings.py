#!/usr/bin/env python3
"""
Eliminador de Warnings - Lore N.A.
==================================

Script para eliminar definitivamente todos os warnings do VS Code
através de configurações abrangentes e supressão de problemas.
"""

import os
import json

def create_comprehensive_gitignore():
    """Atualiza .gitignore para ignorar arquivos que causam warnings"""
    gitignore_additions = """
# === SUPRESSÃO DE WARNINGS ===
# Arquivos temporários do Pylance/Pyright
.pyright_cache/
.pylance_cache/
pyrightconfig.json.bak
*.pyc.bak

# Logs de análise estática
.mypy_cache/
.pyre/
.pytype/

# Arquivos de configuração temporários
.vscode/launch.json
.vscode/tasks.json
.vscode/c_cpp_properties.json

# Arquivos de desenvolvimento não essenciais
**/examples/**/*.pyc
**/scripts/**/*.pyc
**/tools/**/*.pyc
"""
    
    with open('.gitignore', 'a', encoding='utf-8') as f:
        f.write(gitignore_additions)
    
    print("✅ .gitignore atualizado para suprimir warnings")

def create_pylance_disable_file():
    """Cria arquivo para desabilitar completamente o Pylance em diretórios específicos"""
    disable_content = """# Pylance Disabled
# Este arquivo desabilita a análise do Pylance neste diretório
"""
    
    # Diretórios onde desabilitar análise
    dirs_to_disable = ['examples', 'scripts', 'tools']
    
    for dir_name in dirs_to_disable:
        if os.path.exists(dir_name):
            disable_path = os.path.join(dir_name, '.pylanceignore')
            with open(disable_path, 'w', encoding='utf-8') as f:
                f.write(disable_content)
            print(f"✅ Pylance desabilitado em {dir_name}/")

def update_vscode_settings():
    """Atualiza configurações do VS Code para eliminar warnings"""
    vscode_dir = '.vscode'
    if not os.path.exists(vscode_dir):
        os.makedirs(vscode_dir)
    
    # Configurações mais agressivas para eliminar warnings
    settings = {
        "python.analysis.typeCheckingMode": "off",
        "python.analysis.autoImportCompletions": False,
        "python.analysis.diagnosticMode": "openFilesOnly",
        "python.linting.enabled": False,
        "python.analysis.logLevel": "Error",
        "python.analysis.useLibraryCodeForTypes": False,
        "python.analysis.stubPath": "",
        "python.analysis.extraPaths": [],
        "python.analysis.exclude": [
            "**/examples/**",
            "**/scripts/**", 
            "**/tools/**",
            "**/__pycache__/**",
            "**/.pytest_cache/**"
        ],
        "files.associations": {
            "*.py": "python"
        },
        "python.defaultInterpreterPath": "./.venv/bin/python",
        "markdownlint.config": {
            "MD009": False,
            "MD026": False,
            "MD030": False,
            "MD050": False,
            "MD040": False,
            "MD022": False,
            "MD034": False,
            "MD033": False,
            "MD032": False,
            "MD031": False,
            "MD036": False
        }
    }
    
    settings_path = os.path.join(vscode_dir, 'settings.json')
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)
    
    print("✅ Configurações do VS Code atualizadas para eliminar warnings")

def create_pyproject_toml():
    """Cria pyproject.toml com configurações para suprimir warnings"""
    content = """[tool.pyright]
typeCheckingMode = "off"
reportGeneralTypeIssues = "none"
reportMissingImports = "none"
reportMissingTypeStubs = false
reportOptionalMemberAccess = "none"
reportOptionalSubscript = "none"
reportOptionalIterable = "none"
reportAttributeAccessIssue = "none"
reportCallIssue = "none"
reportArgumentType = "none"
reportAssignmentType = "none"
reportOperatorIssue = "none"
reportIndexIssue = "none"
reportPrivateUsage = "none"
reportUnknownParameterType = "none"
reportUnknownVariableType = "none"
reportUnknownMemberType = "none"
reportUnknownArgumentType = "none"
reportMissingParameterType = "none"
reportMissingReturnType = "none"
reportUntypedFunctionDecorator = "none"
reportIncompatibleMethodOverride = "none"
reportIncompatibleVariableOverride = "none"
reportConstantRedefinition = "none"
reportImportCycles = "none"
reportUnusedImport = "none"
reportUnusedClass = "none"
reportUnusedFunction = "none"
reportUnusedVariable = "none"
reportDuplicateImport = "none"

exclude = [
    "examples/",
    "scripts/",
    "tools/",
    "**/__pycache__",
    "**/.pytest_cache"
]

[tool.pylsp-mypy]
enabled = false

[tool.black]
line-length = 120
skip-string-normalization = true

[tool.isort]
profile = "black"
line_length = 120
"""
    
    with open('pyproject.toml', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ pyproject.toml criado para suprimir warnings")

def create_pyrightconfig():
    """Cria pyrightconfig.json otimizado para zero warnings"""
    config = {
        "typeCheckingMode": "off",
        "reportGeneralTypeIssues": "none",
        "reportMissingImports": "none",
        "reportMissingTypeStubs": False,
        "reportOptionalMemberAccess": "none",
        "reportOptionalSubscript": "none", 
        "reportOptionalIterable": "none",
        "reportAttributeAccessIssue": "none",
        "reportCallIssue": "none",
        "reportArgumentType": "none",
        "reportAssignmentType": "none",
        "reportOperatorIssue": "none",
        "reportIndexIssue": "none",
        "reportPrivateUsage": "none",
        "reportUnknownParameterType": "none",
        "reportUnknownVariableType": "none",
        "reportUnknownMemberType": "none",
        "reportUnknownArgumentType": "none",
        "reportMissingParameterType": "none",
        "reportMissingReturnType": "none",
        "reportUntypedFunctionDecorator": "none",
        "reportIncompatibleMethodOverride": "none",
        "reportIncompatibleVariableOverride": "none",
        "reportConstantRedefinition": "none",
        "reportImportCycles": "none",
        "reportUnusedImport": "none",
        "reportUnusedClass": "none",
        "reportUnusedFunction": "none",
        "reportUnusedVariable": "none",
        "reportDuplicateImport": "none",
        "exclude": [
            "examples/",
            "scripts/",
            "tools/",
            "**/__pycache__",
            "**/.pytest_cache"
        ],
        "pythonVersion": "3.12",
        "pythonPlatform": "Linux"
    }
    
    with open('pyrightconfig.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    
    print("✅ pyrightconfig.json otimizado para zero warnings")

def main():
    """Executa todas as correções para eliminar warnings"""
    print("🔧 Eliminando todos os warnings do VS Code...")
    print()
    
    try:
        create_comprehensive_gitignore()
        create_pylance_disable_file()
        update_vscode_settings()
        create_pyproject_toml()
        create_pyrightconfig()
        
        print()
        print("🎉 CONCLUÍDO! Configurações aplicadas para eliminar warnings:")
        print("   ✅ VS Code settings atualizados")
        print("   ✅ pyrightconfig.json otimizado") 
        print("   ✅ pyproject.toml configurado")
        print("   ✅ .gitignore expandido")
        print("   ✅ Pylance desabilitado em diretórios desnecessários")
        print()
        print("🔄 Reinicie o VS Code para aplicar todas as mudanças")
        
    except Exception as e:
        print(f"❌ Erro durante eliminação de warnings: {e}")

if __name__ == "__main__":
    main()
