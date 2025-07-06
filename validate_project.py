#!/usr/bin/env python3
"""
Wrapper script para validação do projeto Lore N.A.
Redireciona para scripts/maintenance/validate_project.py
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Executa o script de validação"""
    project_root = Path(__file__).parent
    validation_script = project_root / "scripts" / "maintenance" / "validate_project.py"

    if not validation_script.exists():
        print(f"❌ Script de validação não encontrado: {validation_script}")
        sys.exit(1)

    # Executar o script de validação
    try:
        result = subprocess.run([sys.executable, str(validation_script)] + sys.argv[1:],
                                cwd=project_root)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️  Validação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao executar validação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
