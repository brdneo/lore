#!/usr/bin/env python3
"""
Script de Inicialização Simples - Lore N.A.
==========================================

Script simplificado para iniciar o projeto Lore N.A.
Inicializa apenas o servidor API por padrão.

Para usar:
- python start.py           -> Inicia apenas API
- python start.py --full    -> Inicia API + Dashboard
- python start.py --dash    -> Inicia apenas Dashboard

Autor: Lore N.A. Genesis Team
Data: 03 de Julho de 2025
"""

import sys
import os
import subprocess
import webbrowser
from time import sleep
import argparse

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def start_api_server(port=8000):
    """Inicia o servidor API"""
    try:
        # Import with proper error handling
        import importlib.util

        # Import api_server module
        src_path = os.path.join(os.path.dirname(__file__), 'src')
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

        host = "0.0.0.0"
        print(f"🚀 Iniciando Lore N.A. API Server")
        print(f"🌐 URL: http://{host}:{port}")
        print(f"📖 Docs: http://{host}:{port}/docs")
        print("🔥 Pressione Ctrl+C para parar")

        uvicorn.run(app, host=host, port=port, log_level="info")

    except Exception as e:
        print(f"❌ Erro ao iniciar API server: {e}")
        return False

def start_dashboard(port=8501):
    """Inicia o dashboard Streamlit"""
    try:
        dashboard_path = os.path.join("src", "dashboard.py")
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            dashboard_path, "--server.port", str(port),
            "--server.headless", "true"
        ]

        print(f"📊 Iniciando Dashboard Streamlit")
        print(f"🌐 URL: http://localhost:{port}")

        process = subprocess.Popen(cmd)
        return process

    except Exception as e:
        print(f"❌ Erro ao iniciar dashboard: {e}")
        return None

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Lore N.A. - Sistema de Vida Artificial')
    parser.add_argument('--full', action='store_true', help='Iniciar API + Dashboard')
    parser.add_argument('--dash', action='store_true', help='Iniciar apenas Dashboard')
    parser.add_argument('--api-port', type=int, default=8000, help='Porta do API (padrão: 8000)')
    parser.add_argument('--dash-port', type=int, default=8501, help='Porta do Dashboard (padrão: 8501)')

    args = parser.parse_args()

    print("🌟 Lore N.A. - Neural Artificial Life")
    print("====================================")

    if args.dash:
        # Iniciar apenas dashboard
        process = start_dashboard(args.dash_port)
        if process:
            try:
                sleep(3)
                webbrowser.open(f"http://localhost:{args.dash_port}")
                process.wait()
            except KeyboardInterrupt:
                print("\n👋 Encerrando Dashboard...")
                process.terminate()

    elif args.full:
        # Iniciar dashboard e API
        print("🚀 Modo Completo: API + Dashboard")

        # Iniciar dashboard em background
        dashboard_process = start_dashboard(args.dash_port)
        if dashboard_process:
            sleep(3)
            try:
                webbrowser.open(f"http://localhost:{args.dash_port}")
            except:
                pass

        # Iniciar API (bloqueia thread principal)
        try:
            start_api_server(args.api_port)
        except KeyboardInterrupt:
            print("\n👋 Encerrando serviços...")
            if dashboard_process:
                dashboard_process.terminate()

    else:
        # Iniciar apenas API (padrão)
        start_api_server(args.api_port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Encerrando Lore N.A...")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)
