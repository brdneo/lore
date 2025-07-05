#!/usr/bin/env python3
"""
Análise Completa do Roadmap PROXIMOS-PASSOS.md - Lore N.A.
=========================================================

Verifica o status de implementação de cada etapa do roadmap definido
no documento PROXIMOS-PASSOS.md, comparando com o código existente.

Autor: Lore N.A. Roadmap Analysis Team
Data: 2025-07-05
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Adicionar src ao path
sys.path.append('/home/brendo/lore/src')

class RoadmapAnalyzer:
    """Analisador de aderência ao roadmap dos próximos passos"""
    
    def __init__(self, project_root: str = "/home/brendo/lore"):
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        
        # Roadmap estruturado baseado no PROXIMOS-PASSOS.md
        self.roadmap = self._load_roadmap_structure()
        
        # Resultados da análise
        self.implementation_status = {}
        
    def _load_roadmap_structure(self) -> Dict[str, Any]:
        """Carrega estrutura do roadmap do PROXIMOS-PASSOS.md"""
        
        return {
            "sistema_nucleo": {
                "description": "SISTEMA NÚCLEO COMPLETO ✅",
                "items": {
                    "dna_digital": {
                        "description": "Sistema de DNA Digital Completo",
                        "requirements": [
                            "Genesis Protocol com 5 universos",
                            "25+ traits genéticos comportamentais", 
                            "Herança, crossover, mutação e fitness scoring"
                        ],
                        "files": ["agent_dna.py", "evolved_agent.py"],
                        "status": "unknown"
                    },
                    "identidades_unicas": {
                        "description": "Sistema de Identidades Únicas",
                        "requirements": [
                            "Gerador de nomes únicos (1000+ combinações)",
                            "Personalidades emergentes baseadas em DNA",
                            "Títulos, origens culturais e apresentações"
                        ],
                        "files": ["agent_name_generator.py", "base_agent.py"],
                        "status": "unknown"
                    },
                    "rede_social_neural": {
                        "description": "Rede Social Neural",
                        "requirements": [
                            "Neural Web com conexões dinâmicas",
                            "Compatibilidade genética para conexões",
                            "Formação natural de comunidades",
                            "Métricas sociais avançadas"
                        ],
                        "files": ["neural_web.py", "social_network_manager.py"],
                        "status": "unknown"
                    },
                    "motor_evolucao": {
                        "description": "Motor de Evolução",
                        "requirements": [
                            "Seleção natural baseada em fitness",
                            "Reprodução sexual com crossover genético",
                            "Mutações gaussianas controladas",
                            "Gerenciamento de gerações"
                        ],
                        "files": ["population_manager.py", "agent_dna.py"],
                        "status": "unknown"
                    },
                    "modulos_avancados": {
                        "description": "Módulos Avançados",
                        "requirements": [
                            "API Server (FastAPI) com documentação automática",
                            "Dashboard visual (Streamlit) para visualizações",
                            "Sistema de economia emocional com tokens",
                            "Launcher unificado para todos os módulos"
                        ],
                        "files": ["api_server.py", "dashboard.py", "emotional_economy.py", "advanced_launcher.py"],
                        "status": "unknown"
                    }
                }
            },
            "fase1_consolidacao": {
                "description": "FASE 1: CONSOLIDAÇÃO (Próximas 2-4 semanas)",
                "items": {
                    "otimizacao_performance": {
                        "description": "Otimização de Performance",
                        "requirements": [
                            "Algoritmos mais eficientes para populações grandes",
                            "Cache inteligente para cálculos genéticos",
                            "Paralelização de processamento"
                        ],
                        "files": ["caching", "async", "parallel"],
                        "status": "unknown"
                    },
                    "robustez_sistema": {
                        "description": "Robustez do Sistema",
                        "requirements": [
                            "Tratamento de erros mais abrangente",
                            "Logs estruturados para debugging",
                            "Testes automatizados mais completos"
                        ],
                        "files": ["error_handling", "logging", "tests"],
                        "status": "unknown"
                    },
                    "analytics_avancadas": {
                        "description": "Analytics Avançadas",
                        "requirements": [
                            "Métricas de comportamento emergente",
                            "Análise de tendências evolutivas",
                            "Predição de formação de comunidades"
                        ],
                        "files": ["analytics", "metrics", "predictions"],
                        "status": "unknown"
                    }
                }
            },
            "fase2_expansao": {
                "description": "FASE 2: EXPANSÃO DE FUNCIONALIDADES (1-3 meses)",
                "items": {
                    "ia_conversacional": {
                        "description": "IA Conversacional",
                        "requirements": [
                            "Integração com modelos de linguagem",
                            "Cada agente com personalidade conversacional única",
                            "Sistema de memória e aprendizado"
                        ],
                        "files": ["llm_integration", "conversation", "memory"],
                        "status": "unknown"
                    },
                    "governo_democratico": {
                        "description": "Governo Digital Democrático",
                        "requirements": [
                            "Sistema de votação entre agentes",
                            "Políticas emergentes baseadas em consenso",
                            "Hierarquias dinâmicas de liderança"
                        ],
                        "files": ["voting_system", "democracy", "governance"],
                        "status": "unknown"
                    },
                    "persistencia_distribuida": {
                        "description": "Persistência Distribuída",
                        "requirements": [
                            "Database para histórico de populações",
                            "Backup automático de DNA crítico",
                            "Sincronização entre instâncias"
                        ],
                        "files": ["distributed_db", "backup", "sync"],
                        "status": "unknown"
                    }
                }
            },
            "fase3_inovacoes": {
                "description": "FASE 3: INOVAÇÕES CONCEITUAIS (3-6 meses)",
                "items": {
                    "multiverse_system": {
                        "description": "Multiverse System",
                        "requirements": [
                            "Universos paralelos com leis diferentes",
                            "Migração inter-dimensional de agentes",
                            "Eventos cósmicos que afetam múltiplas realidades"
                        ],
                        "files": ["multiverse", "dimensions", "cosmic_events"],
                        "status": "unknown"
                    },
                    "evolucao_dirigida": {
                        "description": "Evolução Dirigida",
                        "requirements": [
                            "Machine learning para otimização genética",
                            "Objetivos evolutivos configuráveis",
                            "Experimentos científicos automatizados"
                        ],
                        "files": ["ml_evolution", "objectives", "experiments"],
                        "status": "unknown"
                    },
                    "gamificacao_interacao": {
                        "description": "Gamificação e Interação",
                        "requirements": [
                            "Interface de \"criador de mundos\"",
                            "Competições entre populações",
                            "Visualização em realidade virtual"
                        ],
                        "files": ["world_creator", "competitions", "vr"],
                        "status": "unknown"
                    }
                }
            },
            "fase4_expansao_tecnica": {
                "description": "FASE 4: EXPANSÃO TÉCNICA (6-12 meses)",
                "items": {
                    "plataformas_multiplas": {
                        "description": "Plataformas Múltiplas",
                        "requirements": [
                            "App móvel para monitoramento",
                            "API pública para desenvolvedores",
                            "Plugins para outras plataformas"
                        ],
                        "files": ["mobile_app", "public_api", "plugins"],
                        "status": "unknown"
                    },
                    "blockchain_nfts": {
                        "description": "Blockchain e NFTs",
                        "requirements": [
                            "DNA único como NFT",
                            "Histórico imutável de linhagens",
                            "Marketplace de agentes raros"
                        ],
                        "files": ["blockchain", "nft", "marketplace"],
                        "status": "unknown"
                    },
                    "ia_coletiva": {
                        "description": "IA Coletiva Emergente",
                        "requirements": [
                            "Inteligência de enxame",
                            "Resolução coletiva de problemas",
                            "Criatividade emergente colaborativa"
                        ],
                        "files": ["swarm_intelligence", "collective_ai", "emergence"],
                        "status": "unknown"
                    }
                }
            }
        }
    
    def analyze_file_implementation(self, file_path: Path) -> Dict[str, Any]:
        """Analisa implementação de um arquivo específico"""
        
        if not file_path.exists():
            return {
                "exists": False,
                "lines": 0,
                "functions": 0,
                "classes": 0,
                "complexity_score": 0
            }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = len(content.split('\n'))
            functions = content.count('def ')
            classes = content.count('class ')
            
            # Score de complexidade baseado em tamanho e estrutura
            complexity_score = min(100, (lines / 10) + (functions * 5) + (classes * 10))
            
            # Verificar imports e dependências avançadas
            advanced_imports = [
                'asyncio', 'typing', 'dataclass', 'json', 'logging',
                'requests', 'fastapi', 'streamlit', 'sqlite3', 'threading'
            ]
            
            imports_found = sum(1 for imp in advanced_imports if imp in content)
            
            return {
                "exists": True,
                "lines": lines,
                "functions": functions,
                "classes": classes,
                "complexity_score": complexity_score,
                "advanced_imports": imports_found,
                "content_preview": content[:200] + "..." if len(content) > 200 else content
            }
            
        except Exception as e:
            return {
                "exists": True,
                "error": str(e),
                "lines": 0,
                "functions": 0,
                "classes": 0,
                "complexity_score": 0
            }
    
    def check_concept_implementation(self, concepts: List[str]) -> Dict[str, Any]:
        """Verifica implementação de conceitos no código"""
        
        python_files = list(self.src_dir.glob("*.py"))
        concept_evidence = {}
        
        for concept in concepts:
            concept_evidence[concept] = {
                "files_with_concept": [],
                "total_occurrences": 0,
                "implemented": False
            }
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                for concept in concepts:
                    concept_lower = concept.lower()
                    occurrences = content.count(concept_lower)
                    
                    if occurrences > 0:
                        concept_evidence[concept]["files_with_concept"].append({
                            "file": py_file.name,
                            "occurrences": occurrences
                        })
                        concept_evidence[concept]["total_occurrences"] += occurrences
                        concept_evidence[concept]["implemented"] = True
                        
            except Exception:
                continue
        
        return concept_evidence
    
    def analyze_requirements_implementation(self, requirements: List[str]) -> Dict[str, Any]:
        """Analisa implementação de requisitos específicos"""
        
        requirement_status = {}
        
        for req in requirements:
            # Extrair palavras-chave do requisito
            keywords = self._extract_keywords(req)
            
            # Verificar implementação dos conceitos
            concept_evidence = self.check_concept_implementation(keywords)
            
            # Determinar status baseado na evidência
            implemented_concepts = sum(1 for evidence in concept_evidence.values() if evidence["implemented"])
            total_concepts = len(keywords)
            
            implementation_percentage = (implemented_concepts / total_concepts * 100) if total_concepts > 0 else 0
            
            requirement_status[req] = {
                "keywords": keywords,
                "implementation_percentage": implementation_percentage,
                "concept_evidence": concept_evidence,
                "status": "implemented" if implementation_percentage >= 70 else "partial" if implementation_percentage >= 30 else "missing"
            }
        
        return requirement_status
    
    def _extract_keywords(self, requirement: str) -> List[str]:
        """Extrai palavras-chave de um requisito"""
        
        # Mapear conceitos para palavras-chave
        keyword_mapping = {
            "Genesis Protocol": ["genesis", "protocol"],
            "universos": ["universe", "limbo", "odyssey", "ritual", "engine", "logs"],
            "traits genéticos": ["traits", "genetic", "genes"],
            "herança": ["inheritance", "parent", "crossover"],
            "crossover": ["crossover", "reproduction"],
            "mutação": ["mutation", "mutate"],
            "fitness": ["fitness", "score"],
            "nomes únicos": ["name", "generator", "unique"],
            "personalidades": ["personality", "archetype"],
            "Neural Web": ["neural", "web", "network"],
            "conexões dinâmicas": ["connection", "dynamic", "link"],
            "compatibilidade genética": ["compatibility", "genetic"],
            "comunidades": ["community", "group", "cluster"],
            "seleção natural": ["selection", "natural", "fitness"],
            "reprodução sexual": ["reproduction", "sexual", "mate"],
            "gerações": ["generation", "evolve"],
            "API Server": ["api", "server", "fastapi"],
            "FastAPI": ["fastapi", "api"],
            "Dashboard": ["dashboard", "streamlit"],
            "Streamlit": ["streamlit"],
            "economia emocional": ["emotional", "economy", "token"],
            "Launcher": ["launcher", "advanced"],
            "algoritmos eficientes": ["algorithm", "efficient", "optimize"],
            "cache": ["cache", "caching"],
            "paralelização": ["parallel", "async", "thread"],
            "tratamento de erros": ["error", "exception", "try"],
            "logs estruturados": ["logging", "logger", "log"],
            "testes automatizados": ["test", "unittest", "pytest"],
            "métricas": ["metrics", "measure", "analytics"],
            "comportamento emergente": ["emergent", "behavior", "emergence"],
            "tendências evolutivas": ["trend", "evolution", "analysis"],
            "predição": ["prediction", "predict", "forecast"],
            "modelos de linguagem": ["llm", "language", "model"],
            "conversacional": ["conversation", "chat", "dialogue"],
            "memória": ["memory", "remember", "recall"],
            "aprendizado": ["learning", "learn", "train"],
            "votação": ["voting", "vote", "ballot"],
            "consenso": ["consensus", "agreement"],
            "liderança": ["leadership", "leader", "hierarchy"],
            "database": ["database", "db", "storage"],
            "backup": ["backup", "save", "persist"],
            "sincronização": ["sync", "synchronize"],
            "universos paralelos": ["multiverse", "parallel", "dimension"],
            "migração": ["migration", "migrate", "transfer"],
            "eventos cósmicos": ["cosmic", "event", "universal"],
            "machine learning": ["ml", "machine", "learning"],
            "objetivos evolutivos": ["objective", "goal", "target"],
            "experimentos": ["experiment", "test", "trial"],
            "criador de mundos": ["world", "creator", "builder"],
            "competições": ["competition", "contest", "tournament"],
            "realidade virtual": ["vr", "virtual", "reality"],
            "app móvel": ["mobile", "app", "android", "ios"],
            "API pública": ["public", "api", "external"],
            "plugins": ["plugin", "extension", "addon"],
            "blockchain": ["blockchain", "chain", "crypto"],
            "NFT": ["nft", "token", "digital"],
            "marketplace": ["marketplace", "market", "trade"],
            "inteligência de enxame": ["swarm", "collective", "hive"],
            "resolução coletiva": ["collective", "solve", "group"],
            "criatividade emergente": ["creativity", "creative", "emergent"]
        }
        
        keywords = []
        requirement_lower = requirement.lower()
        
        for concept, concept_keywords in keyword_mapping.items():
            if concept.lower() in requirement_lower:
                keywords.extend(concept_keywords)
        
        # Adicionar palavras-chave diretas do requisito
        words = requirement_lower.split()
        for word in words:
            if len(word) > 3 and word not in ['com', 'para', 'que', 'uma', 'dos', 'das', 'entre']:
                keywords.append(word)
        
        return list(set(keywords))  # Remover duplicatas
    
    def analyze_roadmap_implementation(self) -> Dict[str, Any]:
        """Análise completa da implementação do roadmap"""
        
        print("🔍 ANÁLISE COMPLETA DO ROADMAP PROXIMOS-PASSOS.md")
        print("=" * 70)
        
        for phase_key, phase in self.roadmap.items():
            print(f"\n📋 {phase['description']}")
            print("-" * 50)
            
            phase_results = {}
            
            for item_key, item in phase["items"].items():
                print(f"\n🔎 Analisando: {item['description']}")
                
                # Verificar arquivos específicos se existirem
                if "files" in item and item["files"][0].endswith('.py'):
                    file_analysis = {}
                    for file_name in item["files"]:
                        file_path = self.src_dir / file_name
                        analysis = self.analyze_file_implementation(file_path)
                        file_analysis[file_name] = analysis
                        
                        if analysis["exists"]:
                            print(f"   ✅ {file_name}: {analysis['lines']} linhas, {analysis['functions']} funções")
                        else:
                            print(f"   ❌ {file_name}: Arquivo não encontrado")
                    
                    item["file_analysis"] = file_analysis
                
                # Analisar requisitos
                requirements_analysis = self.analyze_requirements_implementation(item["requirements"])
                item["requirements_analysis"] = requirements_analysis
                
                # Calcular score geral do item
                if "file_analysis" in item:
                    # Items com arquivos específicos
                    existing_files = sum(1 for analysis in item["file_analysis"].values() if analysis["exists"])
                    total_files = len(item["file_analysis"])
                    file_score = (existing_files / total_files * 100) if total_files > 0 else 0
                    
                    avg_complexity = sum(analysis.get("complexity_score", 0) for analysis in item["file_analysis"].values()) / total_files
                    
                    # Score baseado na existência de arquivos e complexidade
                    item_score = (file_score * 0.6) + (min(avg_complexity, 100) * 0.4)
                else:
                    # Items conceituais - baseado na implementação de requisitos
                    req_scores = [req_analysis["implementation_percentage"] for req_analysis in requirements_analysis.values()]
                    item_score = sum(req_scores) / len(req_scores) if req_scores else 0
                
                # Determinar status
                if item_score >= 80:
                    item["status"] = "implemented"
                    status_icon = "✅"
                elif item_score >= 40:
                    item["status"] = "partial"
                    status_icon = "⚠️"
                else:
                    item["status"] = "missing"
                    status_icon = "❌"
                
                item["implementation_score"] = item_score
                print(f"   {status_icon} Score de implementação: {item_score:.1f}%")
                
                # Mostrar detalhes dos requisitos
                for req, req_analysis in requirements_analysis.items():
                    if req_analysis["implementation_percentage"] >= 70:
                        print(f"      ✅ {req}: {req_analysis['implementation_percentage']:.0f}%")
                    elif req_analysis["implementation_percentage"] >= 30:
                        print(f"      ⚠️ {req}: {req_analysis['implementation_percentage']:.0f}%")
                    else:
                        print(f"      ❌ {req}: {req_analysis['implementation_percentage']:.0f}%")
                
                phase_results[item_key] = item
            
            # Calcular score da fase
            phase_scores = [item["implementation_score"] for item in phase_results.values()]
            phase["implementation_score"] = sum(phase_scores) / len(phase_scores) if phase_scores else 0
            
            print(f"\n📊 SCORE DA FASE: {phase['implementation_score']:.1f}%")
            
            self.implementation_status[phase_key] = phase
    
    def generate_roadmap_report(self) -> str:
        """Gera relatório completo da análise do roadmap"""
        
        report = []
        report.append("# 📋 RELATÓRIO COMPLETO - ANÁLISE DO ROADMAP PROXIMOS-PASSOS.md")
        report.append(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Calcular estatísticas gerais
        total_items = 0
        implemented_items = 0
        partial_items = 0
        missing_items = 0
        
        phase_scores = []
        
        for phase_key, phase in self.implementation_status.items():
            phase_scores.append(phase["implementation_score"])
            
            for item_key, item in phase["items"].items():
                total_items += 1
                if item["status"] == "implemented":
                    implemented_items += 1
                elif item["status"] == "partial":
                    partial_items += 1
                else:
                    missing_items += 1
        
        overall_score = sum(phase_scores) / len(phase_scores) if phase_scores else 0
        
        # Resumo executivo
        report.append("## 🎯 RESUMO EXECUTIVO")
        report.append("")
        report.append(f"**Score Geral de Implementação:** {overall_score:.1f}%")
        report.append("")
        report.append(f"**Estatísticas do Roadmap:**")
        report.append(f"- 📊 Total de itens analisados: {total_items}")
        report.append(f"- ✅ Implementados: {implemented_items} ({implemented_items/total_items*100:.1f}%)")
        report.append(f"- ⚠️ Parcialmente implementados: {partial_items} ({partial_items/total_items*100:.1f}%)")
        report.append(f"- ❌ Não implementados: {missing_items} ({missing_items/total_items*100:.1f}%)")
        report.append("")
        
        # Status por fase
        report.append("## 📋 STATUS POR FASE")
        report.append("")
        
        for phase_key, phase in self.implementation_status.items():
            score = phase["implementation_score"]
            
            if score >= 80:
                status_icon = "✅ COMPLETA"
            elif score >= 60:
                status_icon = "🔄 EM ANDAMENTO"
            elif score >= 30:
                status_icon = "⚠️ INICIADA"
            else:
                status_icon = "❌ NÃO INICIADA"
            
            report.append(f"### {phase['description']}")
            report.append(f"**Status:** {status_icon} ({score:.1f}%)")
            report.append("")
            
            # Listar itens da fase
            for item_key, item in phase["items"].items():
                item_score = item["implementation_score"]
                
                if item["status"] == "implemented":
                    item_icon = "✅"
                elif item["status"] == "partial":
                    item_icon = "⚠️"
                else:
                    item_icon = "❌"
                
                report.append(f"- {item_icon} **{item['description']}**: {item_score:.1f}%")
                
                # Mostrar requisitos críticos
                if item["status"] != "implemented":
                    missing_reqs = []
                    for req, req_analysis in item["requirements_analysis"].items():
                        if req_analysis["implementation_percentage"] < 30:
                            missing_reqs.append(req)
                    
                    if missing_reqs:
                        report.append(f"  - 🔴 Requisitos ausentes: {len(missing_reqs)}")
                        for req in missing_reqs[:2]:  # Mostrar apenas os 2 primeiros
                            report.append(f"    - {req}")
                        if len(missing_reqs) > 2:
                            report.append(f"    - ... e mais {len(missing_reqs) - 2}")
            
            report.append("")
        
        # Próximos passos recomendados
        report.append("## 🚀 PRÓXIMOS PASSOS RECOMENDADOS")
        report.append("")
        
        # Identificar prioridades baseadas no roadmap
        priorities = []
        
        # Itens da Fase 1 com baixa implementação
        fase1 = self.implementation_status.get("fase1_consolidacao", {})
        if fase1.get("implementation_score", 0) < 80:
            priorities.append("1. 🔧 **Completar Fase 1 (Consolidação)** - Otimização, robustez e analytics")
        
        # Sistema núcleo com lacunas
        nucleo = self.implementation_status.get("sistema_nucleo", {})
        if nucleo.get("implementation_score", 0) < 95:
            priorities.append("2. 🌟 **Finalizar Sistema Núcleo** - Completar funcionalidades básicas")
        
        # Próximas fases
        fase2 = self.implementation_status.get("fase2_expansao", {})
        if fase2.get("implementation_score", 0) < 20:
            priorities.append("3. 🤖 **Iniciar Fase 2** - IA conversacional e governo democrático")
        
        if not priorities:
            priorities.append("🎉 **Roadmap bem avançado!** Considerar Fase 3 - Inovações conceituais")
        
        for priority in priorities:
            report.append(priority)
        
        report.append("")
        
        # Conclusão
        report.append("## 📊 CONCLUSÃO")
        report.append("")
        
        if overall_score >= 80:
            conclusion = "🎉 **EXCELENTE** - Roadmap muito bem implementado"
        elif overall_score >= 60:
            conclusion = "✅ **BOM** - Boa aderência ao roadmap, algumas lacunas"
        elif overall_score >= 40:
            conclusion = "⚠️ **REGULAR** - Implementação parcial, precisa de foco"
        else:
            conclusion = "❌ **BAIXO** - Roadmap pouco implementado"
        
        report.append(f"**Avaliação Geral:** {conclusion}")
        report.append(f"**Score:** {overall_score:.1f}% de aderência ao roadmap")
        report.append("")
        
        report.append("---")
        report.append("*Relatório gerado automaticamente pela análise do roadmap Lore N.A.*")
        
        return "\n".join(report)

def main():
    """Função principal"""
    print("📋 LORE N.A. - ANÁLISE COMPLETA DO ROADMAP")
    print("=" * 60)
    
    analyzer = RoadmapAnalyzer()
    
    # Executar análise
    analyzer.analyze_roadmap_implementation()
    
    # Gerar relatório
    report = analyzer.generate_roadmap_report()
    
    # Salvar relatório
    report_file = Path("/home/brendo/lore/docs/reports/ANALISE-ROADMAP-COMPLETA.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Relatório salvo em: {report_file}")
    
    # Resumo final
    phase_scores = [phase["implementation_score"] for phase in analyzer.implementation_status.values()]
    overall_score = sum(phase_scores) / len(phase_scores) if phase_scores else 0
    
    print(f"\n🎯 RESULTADO FINAL:")
    print(f"   📊 Score geral do roadmap: {overall_score:.1f}%")
    
    for phase_key, phase in analyzer.implementation_status.items():
        score = phase["implementation_score"]
        if score >= 80:
            status = "✅ COMPLETA"
        elif score >= 60:
            status = "🔄 EM ANDAMENTO"
        elif score >= 30:
            status = "⚠️ INICIADA"
        else:
            status = "❌ NÃO INICIADA"
        
        print(f"   {status}: {phase['description']} ({score:.1f}%)")

if __name__ == "__main__":
    main()
