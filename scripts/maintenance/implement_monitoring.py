#!/usr/bin/env python3
"""
Sistema de Monitoramento e Health Checks - Lore N.A.
====================================================

Implementa monitoramento contínuo do universo para execução 24/7:
- Health checks automáticos de todos os componentes
- Métricas de performance em tempo real
- Alertas automáticos para falhas
- Dashboard de status do sistema

Autor: Lore N.A. Monitoring Team
Data: 2025-07-05
"""

from robustness_config import setup_global_error_handling
import asyncio
import logging
import time
import json
import psutil
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
import threading
import sys
import os

# Adicionar src ao path
sys.path.append('/home/brendo/lore/src')


# Configurar logging
setup_global_error_handling()
logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    """Status de saúde de um componente"""
    component: str
    status: str  # "healthy", "warning", "critical", "offline"
    response_time: float
    last_check: datetime
    details: Dict[str, Any]
    error_message: Optional[str] = None


@dataclass
class SystemMetrics:
    """Métricas do sistema"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    active_agents: int
    database_connections: int
    api_requests_per_minute: int
    neural_web_connections: int


class HealthChecker:
    """Verificador de saúde dos componentes"""

    def __init__(self):
        self.logger = logging.getLogger("HealthChecker")
        self.checks = {}
        self.alerts_sent = set()

    async def check_database(self) -> HealthStatus:
        """Verifica saúde do banco de dados"""
        start_time = time.time()

        try:
            # Verificar se arquivo de banco existe
            db_path = "/home/brendo/lore/data/lore_persistent_universe.db"

            if not os.path.exists(db_path):
                return HealthStatus(
                    component="database",
                    status="critical",
                    response_time=0,
                    last_check=datetime.now(),
                    details={"error": "Database file not found"},
                    error_message=f"Database file missing: {db_path}"
                )

            # Verificar tamanho do arquivo
            db_size = os.path.getsize(db_path)

            # Tentar conectar via sqlite3
            import sqlite3

            conn = sqlite3.connect(db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()

            response_time = time.time() - start_time

            return HealthStatus(
                component="database",
                status="healthy",
                response_time=response_time,
                last_check=datetime.now(),
                details={
                    "size_bytes": db_size,
                    "tables_count": len(tables),
                    "tables": [t[0] for t in tables]
                }
            )

        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error(f"Database health check failed: {e}")

            return HealthStatus(
                component="database",
                status="critical",
                response_time=response_time,
                last_check=datetime.now(),
                details={"error": str(e)},
                error_message=str(e)
            )

    async def check_api_server(self, base_url: str = "http://localhost:8000") -> HealthStatus:
        """Verifica saúde do servidor API"""
        start_time = time.time()

        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            response_time = time.time() - start_time

            if response.status_code == 200:
                return HealthStatus( component="api_server",
                                     status="healthy",
                                     response_time=response_time,
                                     last_check=datetime.now(),
                                     details={ "status_code": response.status_code,
                                               "response": response.json() if response.headers.get('content-type',
                                                                                                   '').startswith('application/json') else response.text[:200] } )
            else:
                return HealthStatus(
                    component="api_server",
                    status="warning",
                    response_time=response_time,
                    last_check=datetime.now(),
                    details={"status_code": response.status_code},
                    error_message=f"HTTP {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            response_time = time.time() - start_time
            return HealthStatus(
                component="api_server",
                status="offline",
                response_time=response_time,
                last_check=datetime.now(),
                details={"error": "Connection refused"},
                error_message="API server is offline"
            )

        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error(f"API health check failed: {e}")

            return HealthStatus(
                component="api_server",
                status="critical",
                response_time=response_time,
                last_check=datetime.now(),
                details={"error": str(e)},
                error_message=str(e)
            )

    async def check_dashboard(self, base_url: str = "http://localhost:8501") -> HealthStatus:
        """Verifica saúde do dashboard"""
        start_time = time.time()

        try:
            response = requests.get(base_url, timeout=10)
            response_time = time.time() - start_time

            if response.status_code == 200:
                return HealthStatus(
                    component="dashboard",
                    status="healthy",
                    response_time=response_time,
                    last_check=datetime.now(),
                    details={"status_code": response.status_code}
                )
            else:
                return HealthStatus(
                    component="dashboard",
                    status="warning",
                    response_time=response_time,
                    last_check=datetime.now(),
                    details={"status_code": response.status_code},
                    error_message=f"HTTP {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            response_time = time.time() - start_time
            return HealthStatus(
                component="dashboard",
                status="offline",
                response_time=response_time,
                last_check=datetime.now(),
                details={"error": "Connection refused"},
                error_message="Dashboard is offline"
            )

        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error(f"Dashboard health check failed: {e}")

            return HealthStatus(
                component="dashboard",
                status="critical",
                response_time=response_time,
                last_check=datetime.now(),
                details={"error": str(e)},
                error_message=str(e)
            )

    async def check_system_resources(self) -> HealthStatus:
        """Verifica recursos do sistema"""
        start_time = time.time()

        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Determinar status baseado nos recursos
            status = "healthy"
            warnings = []

            if cpu_percent > 80:
                status = "warning"
                warnings.append(f"High CPU usage: {cpu_percent}%")

            if memory.percent > 85:
                status = "warning" if status == "healthy" else "critical"
                warnings.append(f"High memory usage: {memory.percent}%")

            if disk.percent > 90:
                status = "critical"
                warnings.append(f"High disk usage: {disk.percent}%")

            response_time = time.time() - start_time

            return HealthStatus(
                component="system_resources",
                status=status,
                response_time=response_time,
                last_check=datetime.now(),
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "disk_percent": disk.percent,
                    "disk_free_gb": disk.free / (1024**3),
                    "warnings": warnings
                },
                error_message="; ".join(warnings) if warnings else None
            )

        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error(f"System resources check failed: {e}")

            return HealthStatus(
                component="system_resources",
                status="critical",
                response_time=response_time,
                last_check=datetime.now(),
                details={"error": str(e)},
                error_message=str(e)
            )

    async def check_universe_status(self) -> HealthStatus:
        """Verifica status do universo (agentes, população, etc.)"""
        start_time = time.time()

        try:
            # Verificar arquivos de log do universo
            log_dir = Path("/home/brendo/lore/logs")
            autonomous_log = log_dir / "universe_autonomous.log"

            details = {
                "log_dir_exists": log_dir.exists(),
                "autonomous_log_exists": autonomous_log.exists(),
                "last_activity": None,
                "estimated_agents": 0
            }

            if autonomous_log.exists():
                # Verificar atividade recente no log
                stat = autonomous_log.stat()
                last_modified = datetime.fromtimestamp(stat.st_mtime)
                details["last_activity"] = last_modified.isoformat()

                # Determinar se há atividade recente (últimos 5 minutos)
                if datetime.now() - last_modified < timedelta(minutes=5):
                    status = "healthy"
                elif datetime.now() - last_modified < timedelta(minutes=30):
                    status = "warning"
                else:
                    status = "critical"

                # Tentar ler últimas linhas do log para estimar agentes
                try:
                    with open(autonomous_log, 'r') as f:
                        lines = f.readlines()
                        # Buscar por linhas com informação de agentes
                        for line in reversed(lines[-50:]):  # Últimas 50 linhas
                            if "agentes" in line.lower() or "agents" in line.lower():
                                # Tentar extrair número
                                import re
                                numbers = re.findall(r'\\d+', line)
                                if numbers:
                                    details["estimated_agents"] = int(numbers[-1])
                                break
                except Exception:
                    pass
            else:
                status = "offline"
                details["error"] = "Universe not running (no log file)"

            response_time = time.time() - start_time

            return HealthStatus(
                component="universe_status",
                status=status,
                response_time=response_time,
                last_check=datetime.now(),
                details=details,
                error_message=details.get("error")
            )

        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error(f"Universe status check failed: {e}")

            return HealthStatus(
                component="universe_status",
                status="critical",
                response_time=response_time,
                last_check=datetime.now(),
                details={"error": str(e)},
                error_message=str(e)
            )


class SystemMonitor:
    """Monitor principal do sistema"""

    def __init__(self, check_interval: int = 30):
        self.check_interval = check_interval
        self.health_checker = HealthChecker()
        self.logger = logging.getLogger("SystemMonitor")
        self.running = False
        self.metrics_history = []
        self.health_history = {}

        # Criar diretórios necessários
        self.logs_dir = Path("/home/brendo/lore/logs")
        self.logs_dir.mkdir(exist_ok=True)

        self.monitoring_log = self.logs_dir / "monitoring.log"
        self.health_report = self.logs_dir / "health_report.json"

    async def collect_system_metrics(self) -> SystemMetrics:
        """Coleta métricas do sistema"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Métricas específicas do Lore (estimativas)
            active_agents = 0
            database_connections = 1 if os.path.exists("/home/brendo/lore/data/lore_persistent_universe.db") else 0
            api_requests_per_minute = 0  # Seria implementado com contador real
            neural_web_connections = 0  # Seria implementado com análise de log

            return SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_percent=disk.percent,
                active_agents=active_agents,
                database_connections=database_connections,
                api_requests_per_minute=api_requests_per_minute,
                neural_web_connections=neural_web_connections
            )

        except Exception as e:
            self.logger.error(f"Failed to collect metrics: {e}")
            raise

    async def run_health_checks(self) -> Dict[str, HealthStatus]:
        """Executa todos os health checks"""
        checks = {}

        try:
            # Executar checks em paralelo
            tasks = [
                self.health_checker.check_database(),
                self.health_checker.check_api_server(),
                self.health_checker.check_dashboard(),
                self.health_checker.check_system_resources(),
                self.health_checker.check_universe_status()
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, HealthStatus):
                    checks[result.component] = result
                elif isinstance(result, Exception):
                    self.logger.error(f"Health check failed: {result}")

            return checks

        except Exception as e:
            self.logger.error(f"Failed to run health checks: {e}")
            return {}

    def generate_health_report(self, checks: Dict[str, HealthStatus], metrics: SystemMetrics) -> Dict[str, Any]:
        """Gera relatório de saúde completo"""

        # Calcular status geral
        statuses = [check.status for check in checks.values()]

        if "critical" in statuses:
            overall_status = "critical"
        elif "warning" in statuses:
            overall_status = "warning"
        elif "offline" in statuses:
            overall_status = "degraded"
        elif all(status == "healthy" for status in statuses):
            overall_status = "healthy"
        else:
            overall_status = "unknown"

        # Contadores por status
        status_counts = {
            "healthy": statuses.count("healthy"),
            "warning": statuses.count("warning"),
            "critical": statuses.count("critical"),
            "offline": statuses.count("offline")
        }

        # Componentes com problemas
        problematic_components = [
            {
                "component": check.component,
                "status": check.status,
                "error": check.error_message,
                "response_time": check.response_time
            }
            for check in checks.values()
            if check.status in ["warning", "critical", "offline"]
        ]

        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "status_counts": status_counts,
            "problematic_components": problematic_components,
            "system_metrics": asdict(metrics),
            "component_details": {
                comp: asdict(status) for comp, status in checks.items()
            },
            "uptime_score": (status_counts["healthy"] / len(statuses)) * 100 if statuses else 0
        }

    def send_alert(self, report: Dict[str, Any]):
        """Envia alertas para problemas críticos"""

        critical_components = [
            comp for comp in report["problematic_components"]
            if comp["status"] == "critical"
        ]

        if critical_components:
            alert_key = f"critical_{len(critical_components)}_{datetime.now().date()}"

            if alert_key not in self.health_checker.alerts_sent:
                self.logger.critical(f"🚨 ALERT: {len(critical_components)} critical components detected!")

                for comp in critical_components:
                    self.logger.critical(f"   ❌ {comp['component']}: {comp['error']}")

                self.health_checker.alerts_sent.add(alert_key)

                # Limpar alertas antigos (manter apenas do dia atual)
                current_date = str(datetime.now().date())
                self.health_checker.alerts_sent = {
                    alert for alert in self.health_checker.alerts_sent
                    if current_date in alert
                }

    def save_health_report(self, report: Dict[str, Any]):
        """Salva relatório de saúde"""
        try:
            with open(self.health_report, 'w') as f:
                json.dump(report, f, indent=2, default=str)

            # Manter histórico
            self.health_history[report["timestamp"]] = report

            # Limitar histórico (últimas 24 horas)
            cutoff = datetime.now() - timedelta(hours=24)
            self.health_history = {
                ts: data for ts, data in self.health_history.items()
                if datetime.fromisoformat(ts.replace('Z', '+00:00')) > cutoff
            }

        except Exception as e:
            self.logger.error(f"Failed to save health report: {e}")

    async def monitoring_cycle(self):
        """Ciclo principal de monitoramento"""

        while self.running:
            try:
                self.logger.info("🔍 Executando ciclo de monitoramento...")

                # Coletar métricas
                metrics = await self.collect_system_metrics()
                self.metrics_history.append(metrics)

                # Limitar histórico de métricas
                if len(self.metrics_history) > 2880:  # 24h com checks a cada 30s
                    self.metrics_history = self.metrics_history[-2880:]

                # Executar health checks
                checks = await self.run_health_checks()

                # Gerar relatório
                report = self.generate_health_report(checks, metrics)

                # Log resumo
                self.logger.info(f"   📊 Status geral: {report['overall_status']}")
                self.logger.info(f"   ✅ Componentes saudáveis: {report['status_counts']['healthy']}")
                self.logger.info(f"   ⚠️ Componentes com warning: {report['status_counts']['warning']}")
                self.logger.info(f"   ❌ Componentes críticos: {report['status_counts']['critical']}")
                self.logger.info(f"   📈 Score de uptime: {report['uptime_score']:.1f}%")

                # Enviar alertas se necessário
                self.send_alert(report)

                # Salvar relatório
                self.save_health_report(report)

                # Aguardar próximo ciclo
                await asyncio.sleep(self.check_interval)

            except Exception as e:
                self.logger.error(f"Monitoring cycle failed: {e}")
                await asyncio.sleep(self.check_interval)

    def start(self):
        """Inicia o monitoramento"""
        self.logger.info("🚀 Iniciando sistema de monitoramento...")
        self.running = True

        # Executar em thread separada para não bloquear
        def run_monitoring():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.monitoring_cycle())
            finally:
                loop.close()

        monitoring_thread = threading.Thread(target=run_monitoring, daemon=True)
        monitoring_thread.start()

        self.logger.info("✅ Sistema de monitoramento iniciado!")
        return monitoring_thread

    def stop(self):
        """Para o monitoramento"""
        self.logger.info("🛑 Parando sistema de monitoramento...")
        self.running = False

    def get_latest_health_report(self) -> Optional[Dict[str, Any]]:
        """Retorna o último relatório de saúde"""
        try:
            if self.health_report.exists():
                with open(self.health_report, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to read health report: {e}")

        return None


def main():
    """Função principal para testar o sistema de monitoramento"""

    print("📊 SISTEMA DE MONITORAMENTO - Lore N.A.")
    print("=" * 50)

    # Instalar psutil se necessário
    try:
        import psutil
    except ImportError:
        print("⚠️ Instalando psutil...")
        os.system("pip install psutil")
        import psutil

    # Criar monitor
    monitor = SystemMonitor(check_interval=30)

    # Iniciar monitoramento
    thread = monitor.start()

    try:
        print("✅ Monitoramento iniciado!")
        print("📊 Relatórios salvos em: /home/brendo/lore/logs/")
        print("🔍 Health checks a cada 30 segundos")
        print("📈 Métricas coletadas continuamente")
        print("🚨 Alertas automáticos para componentes críticos")
        print("\\n⏳ Aguardando primeiro ciclo...")

        # Aguardar primeiro relatório
        time.sleep(35)

        # Mostrar último relatório
        latest_report = monitor.get_latest_health_report()
        if latest_report:
            print("\\n📋 ÚLTIMO RELATÓRIO DE SAÚDE:")
            print(f"   🎯 Status geral: {latest_report['overall_status']}")
            print(f"   ✅ Saudáveis: {latest_report['status_counts']['healthy']}")
            print(f"   ⚠️ Warnings: {latest_report['status_counts']['warning']}")
            print(f"   ❌ Críticos: {latest_report['status_counts']['critical']}")
            print(f"   📈 Uptime: {latest_report['uptime_score']:.1f}%")

            if latest_report['problematic_components']:
                print("\\n🔍 COMPONENTES COM PROBLEMAS:")
                for comp in latest_report['problematic_components']:
                    print(f"   {comp['component']}: {comp['status']} - {comp['error']}")

        print("\\n🎯 Sistema de monitoramento está funcionando!")
        print("📁 Arquivos de log: /home/brendo/lore/logs/")
        print("📊 Health report: /home/brendo/lore/logs/health_report.json")

    except KeyboardInterrupt:
        print("\\n🛑 Parando monitoramento...")
        monitor.stop()
        print("✅ Monitoramento parado!")


if __name__ == "__main__":
    main()
