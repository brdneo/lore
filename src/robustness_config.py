"""
Configuração Global de Robustez - Lore N.A.
==========================================

Configurações para tratamento de erros, logging e recovery automático.
"""

import logging
import sys
from pathlib import Path

# Configurações de robustez
ROBUSTNESS_CONFIG = {
    "max_retries": 3,
    "retry_delay": 1.0,
    "enable_auto_recovery": True,
    "log_level": "INFO",
    "log_file": "/home/brendo/lore/logs/robustness.log",
    "health_check_interval": 30,
    "graceful_shutdown_timeout": 10
}

def setup_global_error_handling():
    """Configura tratamento de erros global"""
    
    # Criar diretório de logs
    log_dir = Path("/home/brendo/lore/logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logging global
    logging.basicConfig(
        level=getattr(logging, ROBUSTNESS_CONFIG["log_level"]),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(ROBUSTNESS_CONFIG["log_file"]),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Handler para exceções não capturadas
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logging.critical(
            "Exceção não capturada",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    
    sys.excepthook = handle_exception
    
    print("🛡️ Sistema global de robustez ativado!")

if __name__ == "__main__":
    setup_global_error_handling()
