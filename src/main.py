# services/agent_runner/main.py
# Ponto de entrada para o serviço que executa os Agentes Neurais.

import os
import logging
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from frugal_agent import FrugalBuyerAgent

# --- Configuração do Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - (%(agent_name)s) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class HealthHandler(BaseHTTPRequestHandler):
    """Handler simples para health checks"""
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "healthy", "service": "agent_runner"}')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Silencia logs do servidor HTTP para não poluir os logs do agente
        pass

def start_health_server():
    """Inicia servidor HTTP para health checks em thread separada"""
    try:
        server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
        server.serve_forever()
    except Exception as e:
        logger.warning(f"Falha ao iniciar servidor de health check: {e}")

def main():
    """
    Função principal que configura e inicia o agente.
    """
    system_log_extra = {'agent_name': 'SYSTEM'}

    # --- Leitura das Variáveis de Ambiente ---
    api_base_url = os.getenv("API_BASE_URL")
    tick_interval = int(os.getenv("TICK_INTERVAL_SECONDS", "10"))
    agent_name = os.getenv("AGENT_NAME", "Agente Gênesis")

    # Validação crítica
    if not api_base_url:
        logger.error(
            "FATAL: A variável de ambiente API_BASE_URL não foi definida. Encerrando.",
            extra=system_log_extra
        )
        return

    # Validação das credenciais JWT
    kong_jwt_secret = os.getenv("KONG_JWT_SECRET")
    if not kong_jwt_secret:
        logger.error(
            "FATAL: A variável de ambiente KONG_JWT_SECRET não foi definida. Encerrando.",
            extra=system_log_extra
        )
        return

    # --- Instanciação do Agente ---
    try:
        # Inicia servidor de health check em thread separada
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        logger.info("Servidor de health check iniciado na porta 8080", extra=system_log_extra)
        
        agent = FrugalBuyerAgent(
            name=agent_name,
            api_base_url=api_base_url
        )
        
        # --- Execução do Ciclo de Vida ---
        agent.run_life_cycle(tick_interval)

    except Exception as e:
        logger.error(
            f"FATAL: Ocorreu um erro não tratado ao iniciar o agente: {e}",
            extra=system_log_extra
        )


if __name__ == "__main__":
    main()
