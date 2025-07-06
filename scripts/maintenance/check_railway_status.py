#!/usr/bin/env python3
"""
Railway Deploy Status Checker
Verifica o status atual do deploy Railway com os dados reais fornecidos
"""

import requests
import json
import time
from typing import Dict, Any


def check_railway_status() -> Dict[str, Any]:
    """Verifica o status do deploy Railway"""

    railway_config = {
        "projectId": "e20bef32-6bb9-4670-8a79-c60fa4939e71",
        "serviceId": "e5b3e063-be8f-409a-8c78-26dc34fbfa51",
        "environmentId": "9c86a94e-8c19-47e6-a5e0-5c6a9e27b4b8",
        "privateDomain": "lore-na-production.railway.internal",
        "publicDomain": "lore-na-production.up.railway.app",
        "sshConnection": "ssh root@containers-us-west1.railway.app -p 30625"
    }

    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "railway_config": railway_config,
        "status_checks": {}
    }

    # URLs para testar
    urls_to_test = [
        f"https://{railway_config['publicDomain']}",
        f"https://{railway_config['publicDomain']}/health",
        f"https://{railway_config['publicDomain']}/api/status"
    ]

    print("🚂 Railway Deploy Status Checker")
    print("=" * 50)
    print(f"Projeto ID: {railway_config['projectId']}")
    print(f"Serviço ID: {railway_config['serviceId']}")
    print(f"Ambiente ID: {railway_config['environmentId']}")
    print(f"Domínio Público: {railway_config['publicDomain']}")
    print(f"SSH: {railway_config['sshConnection']}")
    print()

    # Testar cada URL
    for url in urls_to_test:
        print(f"Testando: {url}")
        try:
            response = requests.get(url, timeout=10)
            status = {
                "url": url,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "accessible": True,
                "content_length": len(response.content),
                "headers": dict(response.headers)
            }

            if response.status_code == 200:
                print(f"  ✅ {response.status_code} - {response.elapsed.total_seconds():.2f}s")
                # Se for o endpoint de saúde, tentar parsear JSON
                if "/health" in url:
                    try:
                        status["health_data"] = response.json()
                        print(f"  📊 Health Data: {json.dumps(status['health_data'], indent=2)}")
                    except:
                        status["health_data"] = response.text[:200]
                        print(f"  📊 Health Response: {response.text[:200]}")
            else:
                print(f"  ❌ {response.status_code} - {response.reason}")
                status["error"] = response.reason

        except requests.exceptions.Timeout:
            status = {"url": url, "accessible": False, "error": "Timeout"}
            print("  ⏰ Timeout")

        except requests.exceptions.ConnectionError:
            status = {"url": url, "accessible": False, "error": "Connection Error"}
            print("  🔌 Connection Error")

        except Exception as e:
            status = {"url": url, "accessible": False, "error": str(e)}
            print(f"  ❌ Error: {e}")

        results["status_checks"][url] = status
        print()

    # Verificar se alguma URL está funcionando
    working_urls = [url for url, status in results["status_checks"].items()
                    if status.get("accessible") and status.get("status_code") == 200]

    if working_urls:
        print("✅ DEPLOY ATIVO!")
        print(f"URLs funcionando: {working_urls}")
        results["deploy_status"] = "ACTIVE"
    else:
        print("❌ DEPLOY INATIVO")
        print("Nenhuma URL está respondendo corretamente")
        results["deploy_status"] = "INACTIVE"

    return results


def save_status_report(results: Dict[str, Any]):
    """Salva relatório de status"""

    report_content = """# Railway Deploy Status Report
*Gerado em: {results['timestamp']}*

## Configuração Railway
- **Projeto ID**: `{results['railway_config']['projectId']}`
- **Serviço ID**: `{results['railway_config']['serviceId']}`
- **Ambiente ID**: `{results['railway_config']['environmentId']}`
- **Domínio Público**: `{results['railway_config']['publicDomain']}`
- **Domínio Privado**: `{results['railway_config']['privateDomain']}`
- **SSH**: `{results['railway_config']['sshConnection']}`

## Status do Deploy: {results['deploy_status']}

## Testes de Conectividade

"""

    for url, status in results['status_checks'].items():
        report_content += f"### {url}\n"
        if status.get('accessible'):
            report_content += f"- ✅ **Status**: {status['status_code']}\n"
            report_content += f"- ⏱️ **Tempo**: {status.get('response_time', 'N/A')}s\n"
            report_content += f"- 📦 **Tamanho**: {status.get('content_length', 'N/A')} bytes\n"

            if 'health_data' in status:
                report_content += f"- 🏥 **Health Data**: ```json\n{json.dumps(status['health_data'], indent=2)}\n```\n"
        else:
            report_content += f"- ❌ **Erro**: {status.get('error', 'Desconhecido')}\n"
        report_content += "\n"

    # Salvar arquivo
    with open("/home/brendo/lore/docs/reports/RAILWAY-STATUS-ATUAL.md", "w", encoding="utf-8") as f:
        f.write(report_content)

    print("📄 Relatório salvo em: docs/reports/RAILWAY-STATUS-ATUAL.md")


if __name__ == "__main__":
    try:
        results = check_railway_status()
        save_status_report(results)

        # Também salvar JSON para uso programático
        with open("/home/brendo/lore/docs/reports/railway-status.json", "w") as f:
            json.dump(results, f, indent=2)

    except Exception as e:
        print(f"❌ Erro ao verificar status: {e}")
