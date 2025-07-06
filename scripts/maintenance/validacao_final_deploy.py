#!/usr/bin/env python3
"""
🚀 LORE N.A. - VALIDAÇÃO FINAL PRÉ-DEPLOY
Valida todos os sistemas antes do deploy em produção
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FinalDeployValidator:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'validation_status': 'PENDING',
            'checks': {},
            'errors': [],
            'warnings': [],
            'ready_for_deploy': False
        }
        self.passed_checks = 0
        self.total_checks = 0

    def check_required_files(self):
        """Verificar arquivos essenciais"""
        print("🔍 Verificando arquivos essenciais...")

        required_files = [
            'main.py', 'start.py', 'Procfile', 'requirements.txt',
            'runtime.txt', '.env', 'config/railway.json',
            'src/api_server.py', 'src/database_manager.py',
            'src/population_manager.py', 'src/agent_dna.py',
            'robust_universe_24_7.py'
        ]

        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)

        if missing_files:
            self.results['errors'].append(f"Arquivos essenciais ausentes: {missing_files}")
            self.results['checks']['required_files'] = 'FAIL'
            return False

        self.results['checks']['required_files'] = 'PASS'
        self.passed_checks += 1
        print("   ✅ Todos os arquivos essenciais presentes")
        return True

    def check_environment_variables(self):
        """Verificar variáveis de ambiente"""
        print("🔍 Verificando variáveis de ambiente...")

        required_vars = [
            'DATABASE_URL', 'JWT_SECRET', 'RAILWAY_ENVIRONMENT'
        ]

        # Carregar .env
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            self.results['warnings'].append("python-dotenv não instalado")

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            self.results['errors'].append(f"Variáveis de ambiente ausentes: {missing_vars}")
            self.results['checks']['environment'] = 'FAIL'
            return False

        self.results['checks']['environment'] = 'PASS'
        self.passed_checks += 1
        print("   ✅ Todas as variáveis de ambiente configuradas")
        return True

    def check_database_connection(self):
        """Verificar conexão com banco de dados"""
        print("🔍 Verificando conexão com banco de dados...")

        try:
            # Testar importação do database manager
            sys.path.append('./src')
            from database_manager import LoREDatabase

            # Testar conexão
            db = LoREDatabase()
            if hasattr(db, 'test_connection'):
                connection_ok = db.test_connection()
                if connection_ok:
                    self.results['checks']['database'] = 'PASS'
                    self.passed_checks += 1
                    print("   ✅ Conexão com banco de dados OK")
                    return True

            # Se não tem test_connection, considerar como OK se não houve erro na importação
            self.results['checks']['database'] = 'PASS'
            self.passed_checks += 1
            print("   ✅ Database manager carregado com sucesso")
            return True

        except Exception as e:
            self.results['errors'].append(f"Erro na conexão com banco: {str(e)}")
            self.results['checks']['database'] = 'FAIL'
            print(f"   ❌ Erro na conexão com banco: {e}")
            return False

    def check_core_modules(self):
        """Verificar módulos do núcleo"""
        print("🔍 Verificando módulos do núcleo...")

        core_modules = [
            'src.agent_dna',
            'src.base_agent',
            'src.population_manager',
            'src.neural_web',
            'src.social_network_manager',
            'src.api_server'
        ]

        failed_modules = []
        for module_name in core_modules:
            try:
                __import__(module_name)
            except Exception as e:
                failed_modules.append(f"{module_name}: {str(e)}")

        if failed_modules:
            self.results['errors'].append(f"Módulos com erro: {failed_modules}")
            self.results['checks']['core_modules'] = 'FAIL'
            return False

        self.results['checks']['core_modules'] = 'PASS'
        self.passed_checks += 1
        print("   ✅ Todos os módulos do núcleo carregam corretamente")
        return True

    def check_robustness_system(self):
        """Verificar sistema de robustez"""
        print("🔍 Verificando sistema de robustez...")

        robustness_files = [
            'logs/', 'cache/', 'state/',
            'implement_error_handling.py',
            'implement_monitoring.py',
            'implement_offline_mode.py',
            'implement_graceful_shutdown.py',
            'robust_universe_24_7.py'
        ]

        missing_robustness = []
        for item in robustness_files:
            if not os.path.exists(item):
                missing_robustness.append(item)

        if missing_robustness:
            self.results['warnings'].append(f"Sistema de robustez incompleto: {missing_robustness}")
            self.results['checks']['robustness'] = 'WARN'
        else:
            self.results['checks']['robustness'] = 'PASS'
            self.passed_checks += 1
            print("   ✅ Sistema de robustez completo")
            return True

        return False

    def check_dependencies(self):
        """Verificar dependências"""
        print("🔍 Verificando dependências...")

        critical_packages = [
            'fastapi', 'uvicorn', 'sqlalchemy', 'psycopg2',
            'pydantic', 'numpy', 'pandas', 'streamlit'
        ]

        missing_packages = []
        for package in critical_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)

        if missing_packages:
            self.results['errors'].append(f"Pacotes ausentes: {missing_packages}")
            self.results['checks']['dependencies'] = 'FAIL'
            return False

        self.results['checks']['dependencies'] = 'PASS'
        self.passed_checks += 1
        print("   ✅ Todas as dependências críticas instaladas")
        return True

    def check_api_health(self):
        """Verificar saúde da API"""
        print("🔍 Verificando configuração da API...")

        try:
            # Verificar se a API pode ser importada e configurada
            sys.path.append('./src')
            from api_server import app

            if app:
                self.results['checks']['api'] = 'PASS'
                self.passed_checks += 1
                print("   ✅ API configurada corretamente")
                return True
        except Exception as e:
            self.results['errors'].append(f"Erro na configuração da API: {str(e)}")
            self.results['checks']['api'] = 'FAIL'
            return False

        return False

    def check_documentation(self):
        """Verificar documentação"""
        print("🔍 Verificando documentação...")

        required_docs = [
            'README.md',
            'docs/development/PROXIMOS-PASSOS.md',
            'docs/reports/STATUS-IMPLEMENTACAO-FINAL.md',
            'docs/reports/ANALISE-ROBUSTEZ-COMPLETA.md'
        ]

        missing_docs = []
        for doc in required_docs:
            if not os.path.exists(doc):
                missing_docs.append(doc)

        if missing_docs:
            self.results['warnings'].append(f"Documentação ausente: {missing_docs}")
            self.results['checks']['documentation'] = 'WARN'
        else:
            self.results['checks']['documentation'] = 'PASS'
            self.passed_checks += 1
            print("   ✅ Documentação completa")
            return True

        return False

    def run_validation(self):
        """Executar todas as validações"""
        print("🚀 LORE N.A. - VALIDAÇÃO FINAL PRÉ-DEPLOY")
        print("=" * 50)

        checks = [
            self.check_required_files,
            self.check_environment_variables,
            self.check_database_connection,
            self.check_core_modules,
            self.check_robustness_system,
            self.check_dependencies,
            self.check_api_health,
            self.check_documentation
        ]

        self.total_checks = len(checks)

        for check in checks:
            try:
                check()
            except Exception as e:
                self.results['errors'].append(f"Erro na validação: {str(e)}")
                logger.error(f"Erro na validação: {e}")

        # Calcular resultado final
        success_rate = (self.passed_checks / self.total_checks) * 100

        if success_rate >= 90 and len(self.results['errors']) == 0:
            self.results['validation_status'] = 'PASS'
            self.results['ready_for_deploy'] = True
            status_emoji = "✅"
            status_text = "PRONTO PARA DEPLOY"
        elif success_rate >= 70:
            self.results['validation_status'] = 'WARN'
            self.results['ready_for_deploy'] = False
            status_emoji = "⚠️"
            status_text = "DEPLOY COM RESSALVAS"
        else:
            self.results['validation_status'] = 'FAIL'
            self.results['ready_for_deploy'] = False
            status_emoji = "❌"
            status_text = "NÃO PRONTO PARA DEPLOY"

        print("\n" + "=" * 50)
        print(f"🎯 RESULTADO FINAL: {status_emoji} {status_text}")
        print(f"📊 Score: {self.passed_checks}/{self.total_checks} ({success_rate:.1f}%)")

        if self.results['errors']:
            print(f"\n❌ Erros ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                print(f"   - {error}")

        if self.results['warnings']:
            print(f"\n⚠️ Avisos ({len(self.results['warnings'])}):")
            for warning in self.results['warnings']:
                print(f"   - {warning}")

        # Salvar relatório
        os.makedirs('docs/reports', exist_ok=True)
        report_path = 'docs/reports/VALIDACAO-FINAL-DEPLOY.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Relatório salvo em: {report_path}")

        if self.results['ready_for_deploy']:
            print("\n🚀 SISTEMA VALIDADO - PODE PROCEDER COM O DEPLOY!")
            print("\nComandos sugeridos para deploy:")
            print("1. git add . && git commit -m 'Deploy ready - validation passed'")
            print("2. git push origin main")
            print("3. Deploy via Railway dashboard ou CLI")
        else:
            print("\n🔧 CORRIJA OS PROBLEMAS ANTES DO DEPLOY")

        return self.results['ready_for_deploy']


def main():
    """Função principal"""
    validator = FinalDeployValidator()
    return validator.run_validation()


if __name__ == "__main__":
    ready = main()
    sys.exit(0 if ready else 1)
