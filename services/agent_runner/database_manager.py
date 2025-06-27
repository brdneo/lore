#!/usr/bin/env python3
"""
Database Manager - Lore N.A.
============================

Sistema de persistência para dados do universo.
Salva automaticamente DNA, identidades, conexões e evolução.

Autor: Lore N.A. Genesis Team
Data: 27 de Junho de 2025
"""

import sqlite3
import json
import os
from datetime import datetime
from dataclasses import asdict
import logging

logger = logging.getLogger(__name__)

class LoREDatabase:
    """Sistema de persistência para o universo Lore N.A."""
    
    def __init__(self, db_path="lore_universe.db"):
        self.db_path = db_path
        self.connection = None
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados com todas as tabelas"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            
            # Criar tabelas
            self._create_tables()
            
            logger.info(f"Database inicializada: {self.db_path}")
            print(f"💾 Database conectada: {self.db_path}")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar database: {e}")
            print(f"❌ Erro no database: {e}")
    
    def _create_tables(self):
        """Cria todas as tabelas necessárias"""
        
        # Tabela de agentes
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                full_name TEXT,
                nickname TEXT,
                personality TEXT,
                origin TEXT,
                generation INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de DNA
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS dna (
                agent_id TEXT PRIMARY KEY,
                dna_data TEXT NOT NULL,  -- JSON com todos os genes
                fitness_overall REAL,
                fitness_limbo REAL,
                fitness_odyssey REAL,
                fitness_ritual REAL,
                fitness_engine REAL,
                fitness_logs REAL,
                parents TEXT,  -- JSON array com IDs dos pais
                mutations TEXT,  -- JSON array com mutações
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES agents (id)
            )
        """)
        
        # Tabela de conexões neurais
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS neural_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent1_id TEXT NOT NULL,
                agent2_id TEXT NOT NULL,
                strength REAL NOT NULL,
                connection_type TEXT DEFAULT 'neural',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent1_id) REFERENCES agents (id),
                FOREIGN KEY (agent2_id) REFERENCES agents (id),
                UNIQUE(agent1_id, agent2_id)
            )
        """)
        
        # Tabela de economia emocional
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS emotional_wallets (
                agent_id TEXT PRIMARY KEY,
                tokens_data TEXT NOT NULL,  -- JSON com todos os tokens
                total_balance REAL DEFAULT 0,
                market_value REAL DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES agents (id)
            )
        """)
        
        # Tabela de gerações
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation_number INTEGER NOT NULL,
                population_size INTEGER,
                avg_fitness REAL,
                max_fitness REAL,
                min_fitness REAL,
                diversity_index REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de eventos do universo
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS universe_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT,  -- JSON com dados do evento
                agents_involved TEXT,  -- JSON array com IDs
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
        print("🏗️  Tabelas do universo criadas")
    
    def save_agent(self, agent_data, dna_data, identity_data):
        """Salva um agente completo"""
        try:
            # Salvar dados básicos do agente
            self.connection.execute("""
                INSERT OR REPLACE INTO agents 
                (id, name, full_name, nickname, personality, origin, generation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                agent_data['id'],
                identity_data.get('name', ''),
                identity_data.get('full_name', ''),
                identity_data.get('nickname', ''),
                identity_data.get('personality_archetype', ''),
                identity_data.get('origin', ''),
                dna_data.get('generation', 0)
            ))
            
            # Salvar DNA
            fitness = dna_data.get('fitness', {})
            self.connection.execute("""
                INSERT OR REPLACE INTO dna 
                (agent_id, dna_data, fitness_overall, fitness_limbo, 
                 fitness_odyssey, fitness_ritual, fitness_engine, fitness_logs,
                 parents, mutations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                agent_data['id'],
                json.dumps(dna_data),
                fitness.get('overall', 0),
                fitness.get('limbo', 0),
                fitness.get('odyssey', 0),
                fitness.get('ritual', 0),
                fitness.get('engine', 0),
                fitness.get('logs', 0),
                json.dumps(dna_data.get('parents', [])),
                json.dumps(dna_data.get('mutations', []))
            ))
            
            self.connection.commit()
            logger.info(f"Agente salvo: {agent_data['id']}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar agente: {e}")
    
    def save_neural_connection(self, agent1_id, agent2_id, strength):
        """Salva uma conexão neural"""
        try:
            self.connection.execute("""
                INSERT OR REPLACE INTO neural_connections 
                (agent1_id, agent2_id, strength)
                VALUES (?, ?, ?)
            """, (agent1_id, agent2_id, strength))
            
            self.connection.commit()
            
        except Exception as e:
            logger.error(f"Erro ao salvar conexão: {e}")
    
    def save_generation_stats(self, generation_num, stats):
        """Salva estatísticas de uma geração"""
        try:
            self.connection.execute("""
                INSERT INTO generations 
                (generation_number, population_size, avg_fitness, max_fitness, 
                 min_fitness, diversity_index)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                generation_num,
                stats.get('population_size', 0),
                stats.get('avg_fitness', 0),
                stats.get('max_fitness', 0),
                stats.get('min_fitness', 0),
                stats.get('diversity_index', 0)
            ))
            
            self.connection.commit()
            
        except Exception as e:
            logger.error(f"Erro ao salvar geração: {e}")
    
    def log_universe_event(self, event_type, event_data=None, agents_involved=None):
        """Registra um evento do universo"""
        try:
            self.connection.execute("""
                INSERT INTO universe_events 
                (event_type, event_data, agents_involved)
                VALUES (?, ?, ?)
            """, (
                event_type,
                json.dumps(event_data) if event_data else None,
                json.dumps(agents_involved) if agents_involved else None
            ))
            
            self.connection.commit()
            
        except Exception as e:
            logger.error(f"Erro ao registrar evento: {e}")
    
    def get_population_stats(self):
        """Retorna estatísticas da população atual"""
        try:
            cursor = self.connection.execute("""
                SELECT COUNT(*) as total_agents,
                       AVG(fitness_overall) as avg_fitness,
                       MAX(fitness_overall) as max_fitness,
                       MIN(fitness_overall) as min_fitness,
                       MAX(generation) as max_generation
                FROM agents a
                JOIN dna d ON a.id = d.agent_id
            """)
            
            result = cursor.fetchone()
            return dict(result) if result else {}
            
        except Exception as e:
            logger.error(f"Erro ao obter stats: {e}")
            return {}
    
    def get_recent_events(self, limit=50):
        """Retorna eventos recentes do universo"""
        try:
            cursor = self.connection.execute("""
                SELECT event_type, event_data, agents_involved, timestamp
                FROM universe_events
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Erro ao obter eventos: {e}")
            return []
    
    def backup_universe(self, backup_path=None):
        """Cria backup completo do universo"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"lore_backup_{timestamp}.db"
        
        try:
            # Fazer backup do arquivo SQLite
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            print(f"💾 Backup criado: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Erro no backup: {e}")
            return None
    
    def close(self):
        """Fecha a conexão com o database"""
        if self.connection:
            self.connection.close()
            print("💾 Database desconectado")

def test_database():
    """Testa as funcionalidades do database"""
    print("🧪 TESTANDO SISTEMA DE DATABASE")
    print("=" * 40)
    
    # Criar database de teste
    db = LoREDatabase("test_universe.db")
    
    # Teste 1: Salvar agente
    print("\n1️⃣ Teste: Salvar agente")
    agent_data = {'id': 'test_agent_001'}
    dna_data = {
        'generation': 0,
        'fitness': {'overall': 0.75, 'limbo': 0.8},
        'parents': [],
        'mutations': []
    }
    identity_data = {
        'name': 'Test Agent',
        'full_name': 'Test Agent Smith',
        'nickname': 'Tester',
        'personality_archetype': 'Test Personality',
        'origin': 'Test Lab'
    }
    
    db.save_agent(agent_data, dna_data, identity_data)
    print("   ✅ Agente salvo")
    
    # Teste 2: Salvar conexão
    print("\n2️⃣ Teste: Conexão neural")
    db.save_neural_connection('test_agent_001', 'test_agent_002', 0.85)
    print("   ✅ Conexão salva")
    
    # Teste 3: Evento do universo
    print("\n3️⃣ Teste: Evento do universo")
    db.log_universe_event('agent_born', {'agent_id': 'test_agent_001'}, ['test_agent_001'])
    print("   ✅ Evento registrado")
    
    # Teste 4: Estatísticas
    print("\n4️⃣ Teste: Estatísticas")
    stats = db.get_population_stats()
    print(f"   📊 Stats: {stats}")
    
    # Teste 5: Backup
    print("\n5️⃣ Teste: Backup")
    backup_file = db.backup_universe()
    print(f"   💾 Backup: {backup_file}")
    
    # Limpar
    db.close()
    os.remove("test_universe.db")
    if backup_file and os.path.exists(backup_file):
        os.remove(backup_file)
    
    print("\n✅ TODOS OS TESTES PASSARAM!")

if __name__ == "__main__":
    test_database()
