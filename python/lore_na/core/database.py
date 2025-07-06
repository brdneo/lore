"""
Database management for Lore N.A.
================================

Handles persistence of agents, populations, and simulation data.
Supports both SQLite (development) and PostgreSQL (production).
"""

import sqlite3
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from datetime import datetime

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database operations for agent persistence."""

    def __init__(self, db_path: str = "lore_universe.db"):
        """Initialize database manager."""
        self.db_path = db_path
        self.connection = None
        self._init_database()

    def _init_database(self):
        """Initialize database connection and tables."""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
            logger.info(f"Database initialized: {self.db_path}")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def _create_tables(self):
        """Create database tables."""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT,
                dna_data TEXT,
                fitness REAL,
                behavior TEXT,
                cognitive_capacity REAL,
                generation INTEGER,
                resources INTEGER,
                emotional_state TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS populations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation INTEGER,
                population_size INTEGER,
                average_fitness REAL,
                best_fitness REAL,
                parameters TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                config TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT,
                results TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS evolution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation INTEGER,
                agent_id TEXT,
                parent_ids TEXT,
                mutation_type TEXT,
                fitness_before REAL,
                fitness_after REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]

        cursor = self.connection.cursor()
        for table_sql in tables:
            cursor.execute(table_sql)
        self.connection.commit()

        logger.info("Database tables created successfully")

    def save_agent(self, agent_data: Dict[str, Any]) -> bool:
        """Save agent to database."""
        try:
            sql = """
            INSERT OR REPLACE INTO agents
            (id, name, dna_data, fitness, behavior, cognitive_capacity,
             generation, resources, emotional_state, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params = (
                agent_data.get('id'),
                agent_data.get('name', agent_data.get('id')),
                json.dumps(agent_data.get('dna', {})),
                agent_data.get('fitness', 0.5),
                agent_data.get('behavior', 'explorer'),
                agent_data.get('cognitive_capacity', 0.5),
                agent_data.get('generation', 0),
                agent_data.get('resources', 0),
                json.dumps(agent_data.get('emotional_state', {})),
                datetime.now().isoformat()
            )

            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            self.connection.commit()

            logger.debug(f"Agent saved: {agent_data.get('id')}")
            return True

        except Exception as e:
            logger.error(f"Failed to save agent: {e}")
            return False

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve agent by ID."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
            result = cursor.fetchone()

            if result:
                agent_dict = dict(result)
                agent_dict['dna'] = json.loads(agent_dict.get('dna_data', '{}'))
                agent_dict['emotional_state'] = json.loads(agent_dict.get('emotional_state', '{}'))
                return agent_dict

            return None

        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {e}")
            return None

    def get_all_agents(self, generation: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all agents, optionally filtered by generation."""
        try:
            sql = "SELECT * FROM agents"
            params = []

            if generation is not None:
                sql += " WHERE generation = ?"
                params.append(generation)

            sql += " ORDER BY fitness DESC"

            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            results = cursor.fetchall()

            agents = []
            for result in results:
                agent_dict = dict(result)
                agent_dict['dna'] = json.loads(agent_dict.get('dna_data', '{}'))
                agent_dict['emotional_state'] = json.loads(agent_dict.get('emotional_state', '{}'))
                agents.append(agent_dict)

            return agents

        except Exception as e:
            logger.error(f"Failed to get agents: {e}")
            return []

    def save_population(self, generation: int, agents: List[Dict[str, Any]], parameters: Dict[str, Any]) -> bool:
        """Save population statistics."""
        try:
            fitness_scores = [agent.get('fitness', 0) for agent in agents]

            sql = """
            INSERT INTO populations
            (generation, population_size, average_fitness, best_fitness, parameters)
            VALUES (?, ?, ?, ?, ?)
            """

            params = (
                generation,
                len(agents),
                sum(fitness_scores) / len(fitness_scores) if fitness_scores else 0,
                max(fitness_scores) if fitness_scores else 0,
                json.dumps(parameters)
            )

            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            self.connection.commit()

            logger.debug(f"Population saved for generation {generation}")
            return True

        except Exception as e:
            logger.error(f"Failed to save population: {e}")
            return False

    def count_agents(self) -> int:
        """Count total number of agents."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM agents")
            result = cursor.fetchone()
            return int(result['total']) if result else 0
        except Exception as e:
            logger.error(f"Failed to count agents: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            cursor = self.connection.cursor()

            # Agent statistics
            cursor.execute("SELECT COUNT(*) as total FROM agents")
            total_agents = cursor.fetchone()['total']

            cursor.execute("SELECT MAX(generation) as max_gen FROM agents")
            max_generation = cursor.fetchone()['max_gen'] or 0

            cursor.execute("SELECT AVG(fitness) as avg_fitness FROM agents")
            avg_fitness = cursor.fetchone()['avg_fitness'] or 0

            # Population statistics
            cursor.execute("SELECT COUNT(*) as total FROM populations")
            total_populations = cursor.fetchone()['total']

            return {
                "total_agents": total_agents,
                "max_generation": max_generation,
                "average_fitness": avg_fitness,
                "total_populations": total_populations,
                "database_path": self.db_path
            }

        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}

    def cleanup_old_data(self, keep_generations: int = 10):
        """Clean up old generation data."""
        try:
            cursor = self.connection.cursor()

            # Get current max generation
            cursor.execute("SELECT MAX(generation) as max_gen FROM agents")
            max_gen = cursor.fetchone()['max_gen'] or 0

            # Delete agents from old generations
            cutoff_gen = max_gen - keep_generations
            if cutoff_gen > 0:
                cursor.execute("DELETE FROM agents WHERE generation < ?", (cutoff_gen,))
                deleted = cursor.rowcount

                self.connection.commit()
                logger.info(f"Cleaned up {deleted} agents from generations < {cutoff_gen}")

        except Exception as e:
            logger.error(f"Failed to cleanup data: {e}")

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
