#!/usr/bin/env python3
"""
Database Manager - Lore N.A.
============================

Sistema de persistência para dados do universo.
Salva automaticamente DNA, identidades, conexões e evolução.
Suporta SQLite (desenvolvimento) e PostgreSQL (produção).

Autor: Lore N.A. Genesis Team
Data: 27 de Junho de 2025
"""

import sqlite3
import json
import os
from datetime import datetime
from dataclasses import asdict
import logging
from typing import Dict, List, Optional, Any, Union, cast

logger = logging.getLogger(__name__)

# Detectar ambiente e configurar database
DATABASE_URL = os.getenv("DATABASE_URL")
# Forçar SQLite para desenvolvimento
USE_POSTGRESQL = DATABASE_URL is not None and DATABASE_URL.strip() != ""

if USE_POSTGRESQL:
    try:
        import psycopg2
        import psycopg2.extras
        from psycopg2 import pool
        HAS_POSTGRESQL = True
    except ImportError:
        logger.warning("psycopg2 não disponível, usando SQLite")
        USE_POSTGRESQL = False
        HAS_POSTGRESQL = False
else:
    HAS_POSTGRESQL = False

class LoREDatabase:
    """Sistema de persistência para o universo Lore N.A."""
    
    def __init__(self, db_path="lore_universe.db"):
        self.db_path = db_path
        self.connection = None
        self.is_postgresql = USE_POSTGRESQL and HAS_POSTGRESQL
        self.DATABASE_URL = DATABASE_URL
        self._init_database()
    
    def _get_connection(self):
        """Obtém uma conexão válida, reconectando se necessário"""
        if self.is_postgresql:
            try:
                # Testa se a conexão está ativa
                if self.connection:
                    # Para PostgreSQL, verificamos fazendo uma query rápida
                    cursor = self.connection.cursor()
                    cursor.execute("SELECT 1")
                    cursor.close()
                    return self.connection
            except (Exception, psycopg2.Error):  # type: ignore
                pass
            
            # Reconecta se necessário
            try:
                if self.connection:
                    self.connection.close()
                self.connection = psycopg2.connect(
                    self.DATABASE_URL,
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
                self.connection.autocommit = True
                logger.info("PostgreSQL reconectado")
                return self.connection
            except Exception as e:
                logger.error(f"Erro ao reconectar PostgreSQL: {e}")
                raise
        else:
            # SQLite
            if not self.connection:
                self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
                self.connection.row_factory = sqlite3.Row
            return self.connection
    
    def _init_database(self):
        """Inicializa o banco de dados com todas as tabelas"""
        try:
            if self.is_postgresql:
                # Conexão PostgreSQL para produção
                self.connection = psycopg2.connect(
                    self.DATABASE_URL,
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
                self.connection.autocommit = True
                logger.info(f"PostgreSQL conectado: {str(self.DATABASE_URL)[:50]}...")
                print(f"💾 PostgreSQL conectado (produção)")
            else:
                # Conexão SQLite para desenvolvimento
                self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
                self.connection.row_factory = sqlite3.Row
                logger.info(f"SQLite inicializada: {self.db_path}")
                print(f"💾 SQLite conectada: {self.db_path}")
            
            # Criar tabelas
            self._create_tables()
            
        except Exception as e:
            logger.error(f"Erro ao inicializar database: {e}")
            print(f"❌ Erro no database: {e}")
            # Fallback para SQLite se PostgreSQL falhar
            if self.is_postgresql:
                logger.info("Fallback para SQLite...")
                self.is_postgresql = False
                self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
                self.connection.row_factory = sqlite3.Row
                self._create_tables()
    
    def _execute_sql(self, sql, params=None):
        """Executa SQL de forma compatível com ambos os databases"""
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            if not self.is_postgresql:
                connection.commit()
            
            return cursor
        except Exception as e:
            logger.error(f"Erro SQL: {e}")
            print(f"Erro SQL: {e}")
            if not self.is_postgresql and self.connection:
                self.connection.rollback()
            raise
    
    def _create_tables(self):
        """Cria todas as tabelas necessárias"""
        
        if self.is_postgresql:
            # SQL PostgreSQL
            tables = [
                """
                CREATE TABLE IF NOT EXISTS agents (
                    id VARCHAR(50) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    full_name VARCHAR(200),
                    personality TEXT,
                    dna_data JSONB,
                    generation INTEGER DEFAULT 0,
                    fitness_scores JSONB DEFAULT '{}',
                    emotional_state JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS neural_connections (
                    id SERIAL PRIMARY KEY,
                    agent_a_id VARCHAR(50) REFERENCES agents(id),
                    agent_b_id VARCHAR(50) REFERENCES agents(id),
                    connection_type VARCHAR(50),
                    strength REAL DEFAULT 0.5,
                    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    interaction_count INTEGER DEFAULT 0,
                    metadata JSONB DEFAULT '{}'
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS evolution_history (
                    id SERIAL PRIMARY KEY,
                    generation INTEGER NOT NULL,
                    agent_id VARCHAR(50) REFERENCES agents(id),
                    parent_ids JSONB,
                    mutation_type VARCHAR(50),
                    fitness_before REAL,
                    fitness_after REAL,
                    evolution_data JSONB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS products (
                    id VARCHAR(100) PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    price REAL DEFAULT 0,
                    category VARCHAR(100),
                    universe VARCHAR(50),
                    description TEXT,
                    rating REAL DEFAULT 0,
                    stock INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            ]
            
        else:
            # SQL SQLite
            tables = [
                """
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    full_name TEXT,
                    personality TEXT,
                    dna_data TEXT,
                    generation INTEGER DEFAULT 0,
                    fitness_scores TEXT DEFAULT '{}',
                    emotional_state TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS neural_connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_a_id TEXT REFERENCES agents(id),
                    agent_b_id TEXT REFERENCES agents(id),
                    connection_type TEXT,
                    strength REAL DEFAULT 0.5,
                    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    interaction_count INTEGER DEFAULT 0,
                    metadata TEXT DEFAULT '{}'
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS evolution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    generation INTEGER NOT NULL,
                    agent_id TEXT REFERENCES agents(id),
                    parent_ids TEXT,
                    mutation_type TEXT,
                    fitness_before REAL,
                    fitness_after REAL,
                    evolution_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL DEFAULT 0,
                    category TEXT,
                    universe TEXT,
                    description TEXT,
                    rating REAL DEFAULT 0,
                    stock INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            ]
        
        # Executar criação de tabelas
        for table_sql in tables:
            self._execute_sql(table_sql)
            
        logger.info("Tabelas criadas com sucesso")
        print("✅ Tabelas do database criadas")
    
    def save_agent(self, agent_data):
        """Salva dados de um agente"""
        try:
            if self.is_postgresql:
                sql = """
                INSERT INTO agents (id, name, full_name, personality, dna_data, generation, fitness_scores, emotional_state)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    full_name = EXCLUDED.full_name,
                    personality = EXCLUDED.personality,
                    dna_data = EXCLUDED.dna_data,
                    generation = EXCLUDED.generation,
                    fitness_scores = EXCLUDED.fitness_scores,
                    emotional_state = EXCLUDED.emotional_state,
                    updated_at = CURRENT_TIMESTAMP
                """
                params = (
                    agent_data.get('id'),
                    agent_data.get('name'),
                    agent_data.get('full_name'),
                    agent_data.get('personality'),
                    json.dumps(agent_data.get('dna', {})),
                    agent_data.get('generation', 0),
                    json.dumps(agent_data.get('fitness_scores', {})),
                    json.dumps(agent_data.get('emotional_state', {}))
                )
            else:
                sql = """
                INSERT OR REPLACE INTO agents 
                (id, name, full_name, personality, dna_data, generation, fitness_scores, emotional_state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    agent_data.get('id'),
                    agent_data.get('name'),
                    agent_data.get('full_name'),
                    agent_data.get('personality'),
                    json.dumps(agent_data.get('dna', {})),
                    agent_data.get('generation', 0),
                    json.dumps(agent_data.get('fitness_scores', {})),
                    json.dumps(agent_data.get('emotional_state', {}))
                )
            
            self._execute_sql(sql, params)
            logger.info(f"Agente salvo: {agent_data.get('name')}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar agente: {e}")
            print(f"Erro ao salvar agente: {e}")
            return False
    
    def get_agent(self, agent_id):
        """Recupera dados de um agente"""
        try:
            if self.is_postgresql:
                sql = "SELECT * FROM agents WHERE id = %s"
            else:
                sql = "SELECT * FROM agents WHERE id = ?"
            
            cursor = self._execute_sql(sql, (agent_id,))
            result = cursor.fetchone()
            
            if result:
                agent_dict = dict(result)
                
                # Handle JSON fields - PostgreSQL returns objects, SQLite returns strings  
                if self.is_postgresql:
                    agent_dict['dna'] = agent_dict.get('dna_data', {})
                    agent_dict['fitness_scores'] = agent_dict.get('fitness_scores', {})
                    agent_dict['emotional_state'] = agent_dict.get('emotional_state', {})
                else:
                    agent_dict['dna'] = json.loads(agent_dict.get('dna_data', '{}'))
                    agent_dict['fitness_scores'] = json.loads(agent_dict.get('fitness_scores', '{}'))
                    agent_dict['emotional_state'] = json.loads(agent_dict.get('emotional_state', '{}'))
                
                return agent_dict
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar agente: {e}")
            return None
    
    def get_all_agents(self):
        """Recupera todos os agentes"""
        try:
            sql = "SELECT * FROM agents ORDER BY created_at DESC"
            cursor = self._execute_sql(sql)
            results = cursor.fetchall()
            
            agents = []
            for result in results:
                agent_dict = dict(result)
                
                # Handle JSON fields - PostgreSQL returns objects, SQLite returns strings
                if self.is_postgresql:
                    agent_dict['dna'] = agent_dict.get('dna_data', {})
                    agent_dict['fitness_scores'] = agent_dict.get('fitness_scores', {})
                    agent_dict['emotional_state'] = agent_dict.get('emotional_state', {})
                else:
                    agent_dict['dna'] = json.loads(agent_dict.get('dna_data', '{}'))
                    agent_dict['fitness_scores'] = json.loads(agent_dict.get('fitness_scores', '{}'))
                    agent_dict['emotional_state'] = json.loads(agent_dict.get('emotional_state', '{}'))
                
                agents.append(agent_dict)
            
            return agents
            
        except Exception as e:
            logger.error(f"Erro ao buscar agentes: {e}")
            print(f"Erro ao buscar agentes: {e}")
            return []
    
    def save_connection(self, agent_a_id, agent_b_id, connection_type="neural", strength=0.5, metadata=None):
        """Salva uma conexão neural entre agentes"""
        try:
            if self.is_postgresql:
                sql = """
                INSERT INTO neural_connections (agent_a_id, agent_b_id, connection_type, strength, metadata)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (agent_a_id, agent_b_id) DO UPDATE SET
                    strength = EXCLUDED.strength,
                    metadata = EXCLUDED.metadata,
                    interaction_count = neural_connections.interaction_count + 1,
                    last_interaction = CURRENT_TIMESTAMP
                """
            else:
                sql = """
                INSERT OR REPLACE INTO neural_connections 
                (agent_a_id, agent_b_id, connection_type, strength, metadata)
                VALUES (?, ?, ?, ?, ?)
                """
            
            params = (
                agent_a_id,
                agent_b_id,
                connection_type,
                strength,
                json.dumps(metadata or {})
            )
            
            self._execute_sql(sql, params)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar conexão: {e}")
            return False
    
    def get_agent_connections(self, agent_id):
        """Recupera conexões de um agente"""
        try:
            if self.is_postgresql:
                sql = """
                SELECT * FROM neural_connections 
                WHERE agent_a_id = %s OR agent_b_id = %s
                ORDER BY strength DESC
                """
            else:
                sql = """
                SELECT * FROM neural_connections 
                WHERE agent_a_id = ? OR agent_b_id = ?
                ORDER BY strength DESC
                """
            
            cursor = self._execute_sql(sql, (agent_id, agent_id))
            results = cursor.fetchall()
            
            connections = []
            for result in results:
                conn_dict = dict(result)
                conn_dict['metadata'] = json.loads(conn_dict.get('metadata', '{}'))
                connections.append(conn_dict)
            
            return connections
            
        except Exception as e:
            logger.error(f"Erro ao buscar conexões: {e}")
            return []
    
    def save_evolution_record(self, evolution_data):
        """Salva registro de evolução"""
        try:
            if self.is_postgresql:
                sql = """
                INSERT INTO evolution_history 
                (generation, agent_id, parent_ids, mutation_type, fitness_before, fitness_after, evolution_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            else:
                sql = """
                INSERT INTO evolution_history 
                (generation, agent_id, parent_ids, mutation_type, fitness_before, fitness_after, evolution_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
            
            params = (
                evolution_data.get('generation'),
                evolution_data.get('agent_id'),
                json.dumps(evolution_data.get('parent_ids', [])),
                evolution_data.get('mutation_type'),
                evolution_data.get('fitness_before'),
                evolution_data.get('fitness_after'),
                json.dumps(evolution_data.get('data', {}))
            )
            
            self._execute_sql(sql, params)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar evolução: {e}")
            return False
    
    def get_evolution_history(self, agent_id=None, generation=None):
        """Recupera histórico de evolução"""
        try:
            sql = "SELECT * FROM evolution_history"
            params = []
            conditions = []
            
            if agent_id:
                conditions.append("agent_id = ?" if not self.is_postgresql else "agent_id = %s")
                params.append(agent_id)
            
            if generation:
                conditions.append("generation = ?" if not self.is_postgresql else "generation = %s")
                params.append(generation)
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            
            sql += " ORDER BY timestamp DESC"
            
            cursor = self._execute_sql(sql, params if params else None)
            results = cursor.fetchall()
            
            history = []
            for result in results:
                record = dict(result)
                record['parent_ids'] = json.loads(record.get('parent_ids', '[]'))
                record['evolution_data'] = json.loads(record.get('evolution_data', '{}'))
                history.append(record)
            
            return history
            
        except Exception as e:
            logger.error(f"Erro ao buscar histórico: {e}")
            return []
    
    def get_stats(self):
        """Estatísticas gerais do universo"""
        try:
            stats = {}
            
            # Total de agentes
            cursor = self._execute_sql("SELECT COUNT(*) as total FROM agents")
            result = cursor.fetchone()
            stats['total_agents'] = int(result['total']) if result else 0  # type: ignore
            
            # Geração atual máxima
            cursor = self._execute_sql("SELECT MAX(generation) as max_gen FROM agents")
            result = cursor.fetchone()
            stats['current_generation'] = int(result['max_gen']) if result and result['max_gen'] else 0  # type: ignore
            
            # Total de conexões
            cursor = self._execute_sql("SELECT COUNT(*) as total FROM neural_connections")
            result = cursor.fetchone()
            stats['total_connections'] = int(result['total']) if result else 0  # type: ignore
            
            # Total de evoluções
            cursor = self._execute_sql("SELECT COUNT(*) as total FROM evolution_history")
            result = cursor.fetchone()
            stats['total_evolutions'] = int(result['total']) if result else 0  # type: ignore
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            print(f"Erro ao calcular estatísticas: {e}")
            return {}
    
    def close(self):
        """Fecha conexão com database"""
        if self.connection:
            self.connection.close()
            logger.info("Database fechado")
    
    def save_hybrid_agent(self, agent_data):
        """Salva dados de um agente criado pelo sistema híbrido Rust+Python"""
        try:
            # Extrair dados específicos do sistema híbrido
            hybrid_data = {
                'id': agent_data.get('agent_id'),
                'name': agent_data.get('agent_id'),  # usar ID como nome temporário
                'full_name': f"Hybrid Agent {agent_data.get('agent_id')}",
                'personality': agent_data.get('behavior', 'explorer'),
                'dna': {
                    'genes': agent_data.get('dna_genes', []),
                    'fitness': agent_data.get('fitness', 0.5),
                    'generation': agent_data.get('generation', 0)
                },
                'generation': agent_data.get('generation', 0),
                'fitness_scores': {
                    'overall': agent_data.get('fitness', 0.5),
                    'cognitive_capacity': agent_data.get('cognitive_capacity', 0.5)
                },
                'emotional_state': agent_data.get('emotional_state', {}),
                'resources': agent_data.get('resources', 0),
                'behavior_type': agent_data.get('behavior', 'explorer'),
                'hybrid_engine': True  # Flag para identificar agentes híbridos
            }
            
            # Usar método save_agent existente
            return self.save_agent(hybrid_data)
            
        except Exception as e:
            logger.error(f"Erro ao salvar agente híbrido: {e}")
            print(f"Erro ao salvar agente híbrido: {e}")
            return False
    
    def count_agents(self):
        """Conta o número total de agentes no banco de dados"""
        try:
            cursor = self._execute_sql("SELECT COUNT(*) as total FROM agents")
            result = cursor.fetchone()
            return int(result['total']) if result else 0  # type: ignore
        except Exception as e:
            logger.error(f"Erro ao contar agentes: {e}")
            return 0
    
    def count_products(self):
        """Conta o número total de produtos no banco de dados"""
        try:
            # Assumindo que existe uma tabela de produtos
            cursor = self._execute_sql("SELECT COUNT(*) as total FROM products")
            result = cursor.fetchone()
            return int(result['total']) if result else 0  # type: ignore
        except Exception as e:
            logger.warning("Tabela de produtos não encontrada")
            return 0
    
    def save_product(self, product_data):
        """Salva dados de um produto"""
        try:
            if self.is_postgresql:
                sql = """
                INSERT INTO products (id, name, price, category, universe, description, rating, stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    price = EXCLUDED.price,
                    category = EXCLUDED.category,
                    universe = EXCLUDED.universe,
                    description = EXCLUDED.description,
                    rating = EXCLUDED.rating,
                    stock = EXCLUDED.stock,
                    updated_at = CURRENT_TIMESTAMP
                """
                params = (
                    product_data.get('id'),
                    product_data.get('name'),
                    product_data.get('price'),
                    product_data.get('category'),
                    product_data.get('universe'),
                    product_data.get('description'),
                    product_data.get('rating'),
                    product_data.get('stock')
                )
            else:
                sql = """
                INSERT OR REPLACE INTO products 
                (id, name, price, category, universe, description, rating, stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    product_data.get('id'),
                    product_data.get('name'),
                    product_data.get('price'),
                    product_data.get('category'),
                    product_data.get('universe'),
                    product_data.get('description'),
                    product_data.get('rating'),
                    product_data.get('stock')
                )
            
            self._execute_sql(sql, params)
            logger.info(f"Produto salvo: {product_data.get('name')}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar produto: {e}")
            print(f"Erro ao salvar produto: {e}")
            return False
