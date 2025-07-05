#!/usr/bin/env python3
"""
Main entry point for Lore N.A.
==============================

Sistema de inicialização principal para o projeto Lore N.A.
Suporta API server e dashboard integrados.

Autor: Lore N.A. Genesis Team
Data: 03 de Julho de 2025
"""

import sys
import os
import subprocess
import webbrowser
from time import sleep
import threading

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import fastapi
        import uvicorn
        import streamlit
        return True
    except ImportError:
        return False

def install_dependencies():
    """Instala dependências automaticamente"""
    print("🔧 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False

def start_api_server():
    """Inicia o servidor API"""
    try:
        # Import with proper error handling
        import sys
        import os
        import importlib.util

        # Add src to path
        src_path = os.path.join(os.path.dirname(__file__), 'src')
        sys.path.insert(0, src_path)

        # Import api_server module
        spec = importlib.util.spec_from_file_location(
            "api_server",
            os.path.join(src_path, "api_server.py")
        )
        if spec is not None and spec.loader is not None:
            api_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(api_module)
            app = api_module.app  # type: ignore
        else:
            raise ImportError("Could not load api_server module")

        import uvicorn

        port = int(os.getenv("PORT", 8000))
        host = "0.0.0.0"

        print(f"🚀 Iniciando API Server em http://{host}:{port}")
        uvicorn.run(app, host=host, port=port, log_level="info")

    except Exception as e:
        print(f"❌ Erro ao iniciar API server: {e}")
        return False

def start_dashboard():
    """Inicia o dashboard Streamlit"""
    try:
        dashboard_path = os.path.join("src", "dashboard.py")
        cmd = [sys.executable, "-m", "streamlit", "run", dashboard_path, "--server.port", "8501"]
        subprocess.Popen(cmd)
        print("📊 Dashboard iniciado em http://localhost:8501")
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar dashboard: {e}")
        return False

def main():
    """Função principal"""
    print("🌟 Lore N.A. - Neural Artificial Life")
    print("=====================================")

    # Verificar dependências
    if not check_dependencies():
        print("📦 Instalando dependências...")
        if not install_dependencies():
            print("❌ Falha ao instalar dependências")
            return

    # Iniciar serviços
    print("🚀 Iniciando serviços...")

    # Iniciar dashboard em thread separada
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()

    sleep(2)  # Aguardar dashboard iniciar

    # Abrir browser automaticamente
    try:
        webbrowser.open("http://localhost:8501")
    except:
        pass

    # Iniciar API server (bloqueia thread principal)
    start_api_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Encerrando Lore N.A...")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
