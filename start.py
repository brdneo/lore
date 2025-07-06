#!/usr/bin/env python3
"""
Wrapper script para iniciar o projeto Lore N.A.
Redireciona para scripts/maintenance/start.py
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Executa o script principal de start"""
    project_root = Path(__file__).parent
    main_script = project_root / "scripts" / "maintenance" / "start.py"

    if not main_script.exists():
        print(f"❌ Arquivo principal não encontrado: {main_script}")
        sys.exit(1)

    # Executar o script principal
    try:
        result = subprocess.run([sys.executable, str(main_script)] + sys.argv[1:],
                                cwd=project_root)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️  Execução interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
