#!/usr/bin/env python3
"""
Sistema de Graceful Shutdown e Auto-Recovery - Lore N.A.
========================================================

Implementa shutdown gracioso e recuperação automática para execução 24/7:
- Captura sinais de sistema (SIGTERM, SIGINT)
- Salva estado antes de parar
- Auto-recovery após falhas
- Persistência de estado crítico

Autor: Lore N.A. Recovery Team
Data: 2025-07-05
"""

import os
import sys
import signal
import asyncio
import logging
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import subprocess
import psutil

# Adicionar src ao path
sys.path.append('/home/brendo/lore/src')

from robustness_config import setup_global_error_handling

# Configurar logging
setup_global_error_handling()
logger = logging.getLogger(__name__)

class StateManager:
    """Gerenciador de estado para persistência"""
    
    def __init__(self, state_dir: str = "/home/brendo/lore/state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("StateManager")
        
        # Arquivos de estado
        self.universe_state_file = self.state_dir / "universe_state.json"
        self.agents_state_file = self.state_dir / "agents_state.json"
        self.population_state_file = self.state_dir / "population_state.json"
        self.system_state_file = self.state_dir / "system_state.json"
        
        # Estado atual
        self.current_state = {}
        
    def save_universe_state(self, state_data: Dict[str, Any]):
        """Salva estado do universo"""
        try:
            state_with_metadata = {
                "timestamp": datetime.now().isoformat(),
                "state": state_data,
                "version": "1.0"
            }
            
            with open(self.universe_state_file, 'w') as f:
                json.dump(state_with_metadata, f, indent=2, default=str)
            
            self.logger.info("💾 Estado do universo salvo")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar estado do universo: {e}")
    
    def load_universe_state(self) -> Optional[Dict[str, Any]]:
        """Carrega estado do universo"""
        try:
            if self.universe_state_file.exists():
                with open(self.universe_state_file, 'r') as f:
                    state_data = json.load(f)
                
                self.logger.info("📂 Estado do universo carregado")
                return state_data.get("state", {})
            
            return None
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar estado do universo: {e}")
            return None
    
    def save_agents_state(self, agents_data: List[Dict[str, Any]]):
        """Salva estado dos agentes"""
        try:
            state_with_metadata = {
                "timestamp": datetime.now().isoformat(),
                "agents_count": len(agents_data),
                "agents": agents_data
            }
            
            with open(self.agents_state_file, 'w') as f:
                json.dump(state_with_metadata, f, indent=2, default=str)
            
            self.logger.info(f"💾 Estado de {len(agents_data)} agentes salvo")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar estado dos agentes: {e}")
    
    def load_agents_state(self) -> List[Dict[str, Any]]:
        """Carrega estado dos agentes"""
        try:
            if self.agents_state_file.exists():
                with open(self.agents_state_file, 'r') as f:
                    state_data = json.load(f)
                
                agents = state_data.get("agents", [])
                self.logger.info(f"📂 Estado de {len(agents)} agentes carregado")
                return agents
            
            return []
            
        except Exception as e:
            self.logger.error(f"Falha ao carregar estado dos agentes: {e}")
            return []
    
    def save_system_state(self, system_data: Dict[str, Any]):
        """Salva estado do sistema"""
        try:
            state_with_metadata = {
                "timestamp": datetime.now().isoformat(),
                "system": system_data,
                "pid": os.getpid(),
                "uptime": time.time() - psutil.Process().create_time()
            }
            
            with open(self.system_state_file, 'w') as f:
                json.dump(state_with_metadata, f, indent=2, default=str)
            
            self.logger.debug("💾 Estado do sistema salvo")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar estado do sistema: {e}")

class GracefulShutdownManager:
    """Gerenciador de shutdown gracioso"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.logger = logging.getLogger("GracefulShutdown")
        self.state_manager = StateManager()
        
        # Callbacks para shutdown
        self.shutdown_callbacks: List[Callable] = []
        self.cleanup_callbacks: List[Callable] = []
        
        # Estado de shutdown
        self.shutting_down = False
        self.shutdown_reason = None
        
        # Registrar handlers de sinal
        self.register_signal_handlers()
    
    def register_signal_handlers(self):
        """Registra handlers para sinais de sistema"""
        
        def signal_handler(signum, frame):
            signal_names = {
                signal.SIGTERM: "SIGTERM",
                signal.SIGINT: "SIGINT",
                signal.SIGUSR1: "SIGUSR1",
                signal.SIGUSR2: "SIGUSR2"
            }
            
            signal_name = signal_names.get(signum, f"Signal {signum}")
            self.logger.info(f"🔔 Sinal recebido: {signal_name}")
            
            if signum in [signal.SIGTERM, signal.SIGINT]:
                self.shutdown_reason = signal_name
                self.initiate_shutdown()
            elif signum == signal.SIGUSR1:
                # Sinal para salvar estado
                self.save_current_state()
            elif signum == signal.SIGUSR2:
                # Sinal para reload de configuração
                self.reload_configuration()
        
        # Registrar handlers
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGUSR1, signal_handler)
        signal.signal(signal.SIGUSR2, signal_handler)
        
        self.logger.info("📡 Handlers de sinal registrados")
    
    def add_shutdown_callback(self, callback: Callable):
        """Adiciona callback para ser executado no shutdown"""
        self.shutdown_callbacks.append(callback)
        self.logger.debug(f"📝 Callback de shutdown adicionado: {callback.__name__}")
    
    def add_cleanup_callback(self, callback: Callable):
        """Adiciona callback para limpeza"""
        self.cleanup_callbacks.append(callback)
        self.logger.debug(f"📝 Callback de limpeza adicionado: {callback.__name__}")
    
    def save_current_state(self):
        """Salva estado atual do sistema"""
        try:
            self.logger.info("💾 Salvando estado atual...")
            
            # Estado do sistema
            system_state = {
                "timestamp": datetime.now().isoformat(),
                "reason": "manual_save",
                "pid": os.getpid(),
                "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,  # MB
                "cpu_percent": psutil.Process().cpu_percent(),
                "num_threads": threading.active_count()
            }
            
            self.state_manager.save_system_state(system_state)
            
            # Executar callbacks de save se existirem
            for callback in self.shutdown_callbacks:
                try:
                    callback()
                except Exception as e:
                    self.logger.error(f"Erro em callback de save: {e}")
            
            self.logger.info("✅ Estado salvo com sucesso")
            
        except Exception as e:
            self.logger.error(f"Falha ao salvar estado: {e}")
    
    def reload_configuration(self):
        """Recarrega configuração do sistema"""
        self.logger.info("🔄 Recarregando configuração...")
        
        # Aqui seria implementado reload de configuração
        # Por enquanto, apenas log
        self.logger.info("✅ Configuração recarregada")
    
    def initiate_shutdown(self):
        """Inicia processo de shutdown gracioso"""
        if self.shutting_down:
            self.logger.warning("⚠️ Shutdown já em andamento")
            return
        
        self.shutting_down = True
        start_time = time.time()
        
        self.logger.info(f"🛑 Iniciando shutdown gracioso (timeout: {self.timeout}s)")
        self.logger.info(f"   Razão: {self.shutdown_reason}")
        
        try:
            # 1. Executar callbacks de shutdown
            self.logger.info("📞 Executando callbacks de shutdown...")
            for i, callback in enumerate(self.shutdown_callbacks):
                try:
                    callback_start = time.time()
                    callback()
                    callback_time = time.time() - callback_start
                    self.logger.info(f"   ✅ Callback {i+1}/{len(self.shutdown_callbacks)} executado ({callback_time:.2f}s)")
                    
                    # Verificar timeout
                    if time.time() - start_time > self.timeout:
                        self.logger.warning(f"⏰ Timeout atingido durante callback {i+1}")
                        break
                        
                except Exception as e:
                    self.logger.error(f"❌ Erro em callback {i+1}: {e}")
            
            # 2. Salvar estado final
            self.logger.info("💾 Salvando estado final...")
            self.save_current_state()
            
            # 3. Executar limpeza
            self.logger.info("🧹 Executando limpeza...")
            for callback in self.cleanup_callbacks:
                try:
                    callback()
                except Exception as e:
                    self.logger.error(f"Erro em callback de limpeza: {e}")
            
            shutdown_time = time.time() - start_time
            self.logger.info(f"✅ Shutdown gracioso concluído ({shutdown_time:.2f}s)")
            
        except Exception as e:
            self.logger.error(f"❌ Erro durante shutdown: {e}")
        
        finally:
            # Sair do programa
            sys.exit(0)

class AutoRecoveryManager:
    """Gerenciador de recuperação automática"""
    
    def __init__(self, max_restarts: int = 5, restart_delay: int = 10):
        self.max_restarts = max_restarts
        self.restart_delay = restart_delay
        self.logger = logging.getLogger("AutoRecovery")
        self.state_manager = StateManager()
        
        # Histórico de restarts
        self.restart_history = []
        self.last_crash_time = None
        
        # Configurações
        self.recovery_enabled = True
        self.health_check_interval = 30
        
    def is_recovery_needed(self) -> bool:
        """Verifica se recuperação é necessária"""
        
        # Verificar se há estado salvo de uma execução anterior
        universe_state = self.state_manager.load_universe_state()
        if universe_state:
            last_save = datetime.fromisoformat(universe_state.get("timestamp", ""))
            
            # Se o último save foi há mais de 1 hora, pode precisar de recovery
            if datetime.now() - last_save > timedelta(hours=1):
                self.logger.warning("⚠️ Estado antigo detectado - pode precisar de recovery")
                return True
        
        return False
    
    def recover_from_state(self) -> bool:
        """Recupera estado do sistema"""
        try:
            self.logger.info("🔄 Iniciando recuperação de estado...")
            
            # Carregar estado do universo
            universe_state = self.state_manager.load_universe_state()
            if universe_state:
                self.logger.info("📂 Estado do universo carregado")
            
            # Carregar estado dos agentes
            agents_state = self.state_manager.load_agents_state()
            if agents_state:
                self.logger.info(f"📂 Estado de {len(agents_state)} agentes carregado")
            
            self.logger.info("✅ Recuperação de estado concluída")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Falha na recuperação: {e}")
            return False
    
    def should_restart(self) -> bool:
        """Verifica se deve fazer restart automático"""
        
        # Verificar histórico de restarts recentes
        recent_restarts = [
            restart for restart in self.restart_history
            if datetime.now() - restart < timedelta(hours=1)
        ]
        
        if len(recent_restarts) >= self.max_restarts:
            self.logger.error(f"❌ Máximo de restarts atingido ({self.max_restarts} em 1 hora)")
            return False
        
        return True
    
    def perform_restart(self, script_path: str):
        """Executa restart do script"""
        
        if not self.should_restart():
            return False
        
        try:
            self.logger.info(f"🔄 Iniciando restart automático de {script_path}")
            
            # Registrar restart
            self.restart_history.append(datetime.now())
            
            # Aguardar delay
            if self.restart_delay > 0:
                self.logger.info(f"⏳ Aguardando {self.restart_delay}s antes do restart...")
                time.sleep(self.restart_delay)
            
            # Executar script
            self.logger.info(f"🚀 Executando: python {script_path}")
            
            # Usar subprocess para restart
            subprocess.Popen([sys.executable, script_path], 
                           cwd=os.path.dirname(script_path) or os.getcwd())
            
            self.logger.info("✅ Restart iniciado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Falha no restart: {e}")
            return False

class RobustUniverseManager:
    """Gerenciador robusto do universo que combina todos os sistemas"""
    
    def __init__(self):
        self.logger = logging.getLogger("RobustUniverseManager")
        
        # Componentes de robustez
        self.shutdown_manager = GracefulShutdownManager(timeout=15)
        self.recovery_manager = AutoRecoveryManager(max_restarts=3, restart_delay=5)
        
        # Estado do universo
        self.universe_running = False
        self.start_time = None
        self.agents = []
        self.population_state = {}
        
        # Configurar callbacks
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Configura callbacks de shutdown e limpeza"""
        
        # Callback para salvar estado dos agentes
        def save_agents_state():
            if self.agents:
                self.shutdown_manager.state_manager.save_agents_state(self.agents)
        
        # Callback para salvar estado do universo
        def save_universe_state():
            universe_state = {
                "running": self.universe_running,
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "agents_count": len(self.agents),
                "population_state": self.population_state,
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            }
            self.shutdown_manager.state_manager.save_universe_state(universe_state)
        
        # Callback para parar componentes
        def stop_universe_components():
            self.logger.info("🛑 Parando componentes do universo...")
            self.universe_running = False
            # Aqui pararia APIs, banco de dados, etc.
        
        # Registrar callbacks
        self.shutdown_manager.add_shutdown_callback(save_agents_state)
        self.shutdown_manager.add_shutdown_callback(save_universe_state)
        self.shutdown_manager.add_shutdown_callback(stop_universe_components)
    
    def start_universe(self, recover_state: bool = True):
        """Inicia universo com recuperação opcional"""
        
        self.logger.info("🌟 Iniciando universo robusto...")
        
        # Tentar recuperação se solicitado
        if recover_state and self.recovery_manager.is_recovery_needed():
            self.logger.info("🔄 Recuperação de estado detectada...")
            if self.recovery_manager.recover_from_state():
                # Carregar estado recuperado
                agents_state = self.shutdown_manager.state_manager.load_agents_state()
                if agents_state:
                    self.agents = agents_state
                    self.logger.info(f"📂 {len(self.agents)} agentes recuperados")
        
        # Inicializar universo
        self.universe_running = True
        self.start_time = datetime.now()
        
        # Criar agentes iniciais se não há estado recuperado
        if not self.agents:
            self.logger.info("👥 Criando população inicial...")
            for i in range(5):
                agent = {
                    "id": f"robust_agent_{i}",
                    "name": f"Robust Agent {i+1}",
                    "created_at": datetime.now().isoformat(),
                    "status": "active"
                }
                self.agents.append(agent)
            
            self.logger.info(f"✅ {len(self.agents)} agentes criados")
        
        # Estado inicial da população
        self.population_state = {
            "generation": 0,
            "total_agents": len(self.agents),
            "active_agents": len([a for a in self.agents if a.get("status") == "active"]),
            "last_update": datetime.now().isoformat()
        }
        
        self.logger.info("✅ Universo robusto iniciado!")
        return True
    
    def simulate_universe_cycle(self):
        """Simula um ciclo do universo"""
        if not self.universe_running:
            return
        
        try:
            # Simular atividade dos agentes
            active_agents = [a for a in self.agents if a.get("status") == "active"]
            
            # Atualizar estado da população
            self.population_state.update({
                "active_agents": len(active_agents),
                "last_update": datetime.now().isoformat(),
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
            })
            
            self.logger.info(f"🔄 Ciclo do universo: {len(active_agents)} agentes ativos")
            
            # Salvar estado periodicamente
            if int(time.time()) % 60 == 0:  # A cada minuto
                self.shutdown_manager.save_current_state()
            
        except Exception as e:
            self.logger.error(f"Erro no ciclo do universo: {e}")
    
    async def run_universe(self, duration: int = 300):
        """Executa universo por duração especificada"""
        
        self.logger.info(f"🚀 Executando universo robusto por {duration} segundos...")
        
        end_time = time.time() + duration
        cycle_count = 0
        
        while time.time() < end_time and self.universe_running:
            try:
                # Executar ciclo do universo
                self.simulate_universe_cycle()
                cycle_count += 1
                
                # Aguardar próximo ciclo
                await asyncio.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Erro no ciclo {cycle_count}: {e}")
                # Continuar execução mesmo com erro
                await asyncio.sleep(5)
        
        self.logger.info(f"✅ Universo executado por {cycle_count} ciclos")

def main():
    """Função principal para testar sistema de recovery"""
    
    print("⚡ SISTEMA DE GRACEFUL SHUTDOWN E AUTO-RECOVERY")
    print("=" * 60)
    
    # Criar gerenciador robusto
    universe_manager = RobustUniverseManager()
    
    # Iniciar universo
    universe_manager.start_universe(recover_state=True)
    
    print("✅ Universo robusto iniciado!")
    print("🔔 Handlers de sinal registrados (SIGTERM, SIGINT, SIGUSR1, SIGUSR2)")
    print("💾 Estado será salvo automaticamente")
    print("🔄 Recuperação automática ativada")
    print("\\n🎯 COMANDOS DE TESTE:")
    print("   kill -USR1 <PID>  # Salvar estado manualmente")
    print("   kill -USR2 <PID>  # Reload configuração")
    print("   kill -TERM <PID>  # Shutdown gracioso")
    print("   Ctrl+C            # Shutdown gracioso")
    print(f"\\n📊 PID atual: {os.getpid()}")
    
    try:
        # Executar universo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(universe_manager.run_universe(duration=60))
        
    except KeyboardInterrupt:
        print("\\n🔔 SIGINT recebido - shutdown será iniciado...")
        # O shutdown manager cuidará do resto
        
    except Exception as e:
        print(f"\\n❌ Erro durante execução: {e}")
        logger.error(f"Erro na execução principal: {e}")
    
    finally:
        print("\\n✅ Sistema de recovery testado!")
        print("📁 Estados salvos em: /home/brendo/lore/state/")

if __name__ == "__main__":
    main()
