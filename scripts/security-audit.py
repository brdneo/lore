#!/usr/bin/env python3
"""
Sistema de Auditoria de Segurança para Lore N.A.
Valida configurações, verifica vulnerabilidades e gera relatórios de segurança
"""
import os
import re
import json
import subprocess
import hashlib
from datetime import datetime
from pathlib import Path

class SecurityAuditor:
    def __init__(self, project_root="/home/brendo/lore"):
        self.project_root = Path(project_root)
        self.issues = []
        self.passed_checks = []
        
    def log_issue(self, severity, category, message, file_path=None):
        """Registra um problema de segurança"""
        self.issues.append({
            "severity": severity,
            "category": category,
            "message": message,
            "file": str(file_path) if file_path else None,
            "timestamp": datetime.now().isoformat()
        })
        
    def log_pass(self, check_name, message):
        """Registra um teste que passou"""
        self.passed_checks.append({
            "check": check_name,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def check_file_permissions(self):
        """Verifica permissões de arquivos sensíveis"""
        print("🔍 Verificando permissões de arquivos...")
        
        sensitive_files = [
            ".env", ".env.secure", ".env.production",
            "secrets.json", "infra/kong.yml"
        ]
        
        for file_name in sensitive_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                stat = file_path.stat()
                mode = oct(stat.st_mode)[-3:]
                
                if mode != "600":
                    self.log_issue("HIGH", "FILE_PERMISSIONS", 
                                 f"Arquivo {file_name} tem permissões inseguras: {mode}. Deveria ser 600.", 
                                 file_path)
                else:
                    self.log_pass("FILE_PERMISSIONS", f"Arquivo {file_name} tem permissões seguras (600)")
            else:
                self.log_pass("FILE_PERMISSIONS", f"Arquivo sensível {file_name} não encontrado (OK se não usado)")
    
    def check_weak_passwords(self):
        """Verifica senhas fracas em arquivos de configuração"""
        print("🔍 Verificando força das senhas...")
        
        weak_patterns = [
            r"password.*=.*123",
            r"secret.*=.*123", 
            r"key.*=.*test",
            r"MinhaChaveSecretaSuperSegura123"
        ]
        
        config_files = [".env", ".env.secure", "infra/kong.yml"]
        
        for file_name in config_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text()
                    for pattern in weak_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            self.log_issue("HIGH", "WEAK_CREDENTIALS", 
                                         f"Possível senha fraca detectada em {file_name}", 
                                         file_path)
                            break
                    else:
                        self.log_pass("WEAK_CREDENTIALS", f"Nenhuma senha fraca detectada em {file_name}")
                except Exception as e:
                    self.log_issue("MEDIUM", "FILE_ACCESS", f"Erro ao ler {file_name}: {e}", file_path)
    
    def check_secrets_exposure(self):
        """Verifica se secrets estão sendo expostos no Git"""
        print("🔍 Verificando exposição de secrets...")
        
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text()
            
            required_patterns = [".env", "secrets.json", "*.key", "*.pem"]
            missing_patterns = []
            
            for pattern in required_patterns:
                if pattern not in gitignore_content:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                self.log_issue("HIGH", "SECRET_EXPOSURE", 
                             f"Padrões faltando no .gitignore: {missing_patterns}")
            else:
                self.log_pass("SECRET_EXPOSURE", "Todos os padrões de secrets estão no .gitignore")
        else:
            self.log_issue("HIGH", "SECRET_EXPOSURE", ".gitignore não encontrado")
    
    def check_docker_security(self):
        """Verifica configurações de segurança do Docker"""
        print("🔍 Verificando segurança do Docker...")
        
        docker_compose_path = self.project_root / "docker-compose.yml"
        if docker_compose_path.exists():
            content = docker_compose_path.read_text()
            
            # Verificar se está executando como root
            if "user:" not in content:
                self.log_issue("MEDIUM", "DOCKER_SECURITY", 
                             "Containers podem estar executando como root")
            
            # Verificar se tem restart policy
            if "restart:" in content:
                self.log_pass("DOCKER_SECURITY", "Restart policies configuradas")
            else:
                self.log_issue("LOW", "DOCKER_SECURITY", "Restart policies não configuradas")
            
            # Verificar healthchecks
            if "healthcheck:" in content:
                self.log_pass("DOCKER_SECURITY", "Healthchecks configurados")
            else:
                self.log_issue("MEDIUM", "DOCKER_SECURITY", "Healthchecks não configurados")
    
    def check_network_security(self):
        """Verifica configurações de rede"""
        print("🔍 Verificando segurança de rede...")
        
        kong_config_path = self.project_root / "infra" / "kong.yml"
        if kong_config_path.exists():
            content = kong_config_path.read_text()
            
            # Verificar se JWT está habilitado
            if "jwt" in content:
                self.log_pass("NETWORK_SECURITY", "Plugin JWT configurado no Kong")
            else:
                self.log_issue("HIGH", "NETWORK_SECURITY", "JWT não configurado no Kong")
            
            # Verificar rate limiting
            if "rate-limiting" in content:
                self.log_pass("NETWORK_SECURITY", "Rate limiting configurado")
            else:
                self.log_issue("MEDIUM", "NETWORK_SECURITY", "Rate limiting não configurado")
            
            # Verificar CORS
            if "cors" in content:
                self.log_pass("NETWORK_SECURITY", "CORS configurado")
            else:
                self.log_issue("LOW", "NETWORK_SECURITY", "CORS não configurado")
    
    def generate_report(self):
        """Gera relatório de auditoria de segurança"""
        print("\n" + "="*60)
        print("🛡️  RELATÓRIO DE AUDITORIA DE SEGURANÇA")
        print("="*60)
        
        # Estatísticas
        high_issues = [i for i in self.issues if i["severity"] == "HIGH"]
        medium_issues = [i for i in self.issues if i["severity"] == "MEDIUM"]
        low_issues = [i for i in self.issues if i["severity"] == "LOW"]
        
        print(f"📊 RESUMO:")
        print(f"  ✅ Verificações aprovadas: {len(self.passed_checks)}")
        print(f"  🔴 Problemas CRÍTICOS: {len(high_issues)}")
        print(f"  🟡 Problemas MÉDIOS: {len(medium_issues)}")
        print(f"  🟠 Problemas BAIXOS: {len(low_issues)}")
        
        # Problemas críticos
        if high_issues:
            print(f"\n🔴 PROBLEMAS CRÍTICOS (requer ação imediata):")
            for issue in high_issues:
                print(f"  • {issue['category']}: {issue['message']}")
                if issue['file']:
                    print(f"    📁 Arquivo: {issue['file']}")
        
        # Problemas médios
        if medium_issues:
            print(f"\n🟡 PROBLEMAS MÉDIOS (recomendado corrigir):")
            for issue in medium_issues:
                print(f"  • {issue['category']}: {issue['message']}")
        
        # Problemas baixos
        if low_issues:
            print(f"\n🟠 MELHORIAS RECOMENDADAS:")
            for issue in low_issues:
                print(f"  • {issue['category']}: {issue['message']}")
        
        # Score de segurança
        total_checks = len(self.passed_checks) + len(self.issues)
        if total_checks > 0:
            # Peso dos problemas: HIGH=3, MEDIUM=2, LOW=1
            penalty = len(high_issues) * 3 + len(medium_issues) * 2 + len(low_issues) * 1
            max_penalty = total_checks * 3
            score = max(0, int(100 * (1 - penalty / max_penalty))) if max_penalty > 0 else 100
            
            print(f"\n🎯 SCORE DE SEGURANÇA: {score}/100")
            
            if score >= 90:
                print("   🟢 EXCELENTE - Sistema muito seguro")
            elif score >= 70:
                print("   🟡 BOM - Algumas melhorias recomendadas")
            elif score >= 50:
                print("   🟠 MÉDIO - Vários problemas a corrigir")
            else:
                print("   🔴 BAIXO - Requer atenção imediata")
        
        # Salvar relatório
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "passed_checks": self.passed_checks,
            "issues": self.issues,
            "summary": {
                "total_checks": len(self.passed_checks) + len(self.issues),
                "passed": len(self.passed_checks),
                "high_issues": len(high_issues),
                "medium_issues": len(medium_issues), 
                "low_issues": len(low_issues),
                "security_score": score if 'score' in locals() else 0
            }
        }
        
        report_path = self.project_root / "security-audit-report.json"
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Relatório detalhado salvo em: {report_path}")
        print("="*60)
    
    def run_full_audit(self):
        """Executa auditoria completa de segurança"""
        print("🛡️  Iniciando auditoria de segurança do Lore N.A...")
        print("="*60)
        
        self.check_file_permissions()
        self.check_weak_passwords()
        self.check_secrets_exposure()
        self.check_docker_security()
        self.check_network_security()
        
        self.generate_report()

def main():
    auditor = SecurityAuditor()
    auditor.run_full_audit()

if __name__ == "__main__":
    main()
