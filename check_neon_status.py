#!/usr/bin/env python3
"""
Neon Database Status Checker
Verifica o status e detalhes do banco Neon PostgreSQL
"""

import psycopg2
import os
import json
from urllib.parse import urlparse
import time

def get_neon_info_from_url(database_url):
    """Extrai informações da URL de conexão do Neon"""
    
    try:
        parsed = urlparse(database_url)
        
        return {
            "host": parsed.hostname,
            "port": parsed.port or 5432,
            "database": parsed.path.lstrip('/'),
            "username": parsed.username,
            "password_length": len(parsed.password) if parsed.password else 0,
            "ssl_mode": "require" if "sslmode=require" in database_url else "unknown",
            "channel_binding": "require" if "channel_binding=require" in database_url else "unknown",
            "pooler_detected": "pooler" in parsed.hostname,
            "region": "us-east-2" if "us-east-2" in parsed.hostname else "unknown",
            "provider": "neon" if "neon.tech" in parsed.hostname else "unknown"
        }
    except Exception as e:
        return {"error": f"Erro ao parsear URL: {e}"}

def test_neon_connection(database_url):
    """Testa conexão com o Neon"""
    
    try:
        print("🔌 Testando conexão com Neon...")
        
        # Conectar
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Informações básicas
        cursor.execute("SELECT version();")
        pg_version = cursor.fetchone()[0]
        
        # Estatísticas do banco
        cursor.execute("""
            SELECT 
                pg_database.datname,
                pg_size_pretty(pg_database_size(pg_database.datname)) as size
            FROM pg_database 
            WHERE datname = current_database();
        """)
        db_info = cursor.fetchone()
        
        # Tabelas do projeto
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE';
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        # Contagem de registros por tabela
        table_counts = {}
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                table_counts[table] = cursor.fetchone()[0]
            except:
                table_counts[table] = "erro"
        
        # Configurações de conexão
        cursor.execute("SHOW max_connections;")
        max_connections = cursor.fetchone()[0]
        
        cursor.execute("SELECT count(*) FROM pg_stat_activity;")
        current_connections = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "status": "success",
            "postgresql_version": pg_version,
            "database_name": db_info[0],
            "database_size": db_info[1],
            "tables": tables,
            "table_counts": table_counts,
            "max_connections": max_connections,
            "current_connections": current_connections,
            "connection_test": "✅ Sucesso"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "connection_test": f"❌ Erro: {e}"
        }

def generate_neon_report():
    """Gera relatório completo do Neon"""
    
    # Ler DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Tentar ler do .env
        try:
            with open('/home/brendo/lore/.env', 'r') as f:
                for line in f:
                    if line.startswith('DATABASE_URL='):
                        database_url = line.split('=', 1)[1].strip()
                        break
        except:
            pass
    
    if not database_url:
        print("❌ DATABASE_URL não encontrado")
        return
    
    print("🐘 NEON DATABASE STATUS CHECKER")
    print("=" * 50)
    
    # Informações da URL
    print("\n## 📋 CONFIGURAÇÃO DETECTADA")
    url_info = get_neon_info_from_url(database_url)
    
    for key, value in url_info.items():
        if key == "password_length":
            print(f"- {key}: {value} caracteres")
        elif "password" not in key.lower():
            print(f"- {key}: {value}")
    
    # Teste de conexão
    print("\n## 🔍 TESTE DE CONEXÃO")
    connection_result = test_neon_connection(database_url)
    
    if connection_result["status"] == "success":
        print("✅ Conexão bem-sucedida!")
        print(f"- PostgreSQL: {connection_result['postgresql_version']}")
        print(f"- Database: {connection_result['database_name']}")
        print(f"- Tamanho: {connection_result['database_size']}")
        print(f"- Conexões: {connection_result['current_connections']}/{connection_result['max_connections']}")
        
        print(f"\n## 📊 TABELAS ENCONTRADAS ({len(connection_result['tables'])})")
        for table in connection_result['tables']:
            count = connection_result['table_counts'].get(table, 0)
            print(f"- {table}: {count} registros")
            
    else:
        print(f"❌ Erro na conexão: {connection_result['error']}")
    
    # Gerar relatório em arquivo
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url_info": url_info,
        "connection_result": connection_result
    }
    
    # Markdown report
    markdown_content = f"""# Neon Database Status Report
*Gerado em: {report_data['timestamp']}*

## 🔧 Configuração

### Connection Details
- **Host**: `{url_info.get('host', 'N/A')}`
- **Database**: `{url_info.get('database', 'N/A')}`
- **Username**: `{url_info.get('username', 'N/A')}`
- **Port**: `{url_info.get('port', 'N/A')}`
- **Region**: `{url_info.get('region', 'N/A')}`
- **SSL Mode**: `{url_info.get('ssl_mode', 'N/A')}`
- **Pooler**: {'✅ Sim' if url_info.get('pooler_detected') else '❌ Não'}

## 🏥 Status de Saúde

### Connection Test
{connection_result.get('connection_test', 'N/A')}

"""
    
    if connection_result["status"] == "success":
        markdown_content += f"""### Database Info
- **PostgreSQL Version**: `{connection_result['postgresql_version']}`
- **Database Name**: `{connection_result['database_name']}`
- **Database Size**: `{connection_result['database_size']}`
- **Max Connections**: `{connection_result['max_connections']}`
- **Current Connections**: `{connection_result['current_connections']}`

### Tables ({len(connection_result['tables'])})
"""
        for table in connection_result['tables']:
            count = connection_result['table_counts'].get(table, 0)
            markdown_content += f"- **{table}**: {count} registros\n"
    
    else:
        markdown_content += f"""### Error Details
```
{connection_result['error']}
```
"""
    
    # Salvar arquivos
    with open('/home/brendo/lore/docs/reports/NEON-STATUS.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    with open('/home/brendo/lore/docs/reports/neon-status.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Relatórios salvos:")
    print(f"- docs/reports/NEON-STATUS.md")
    print(f"- docs/reports/neon-status.json")

if __name__ == "__main__":
    generate_neon_report()
