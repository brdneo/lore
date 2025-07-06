"""
Configuration management for Lore N.A.
=====================================

Centralized configuration handling with environment variable support
and validation for all system parameters.
"""

import os
import toml
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Main configuration class for Lore N.A."""

    # Simulation parameters
    population_size: int = 100
    max_generations: int = 1000
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    selection_pressure: float = 0.7
    elitism_rate: float = 0.2

    # Database settings
    database_path: str = "lore_universe.db"
    database_url: Optional[str] = None

    # Performance settings
    parallel_threads: Optional[int] = None
    use_rust_engine: bool = True
    batch_size: int = 1000

    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None

    # API settings
    api_host: str = "localhost"
    api_port: int = 8000
    api_debug: bool = False

    # Web interface settings
    web_host: str = "localhost"
    web_port: int = 8501
    web_debug: bool = False

    # Advanced settings
    gpu_acceleration: bool = False
    distributed_mode: bool = False
    backup_interval: int = 3600  # seconds
    cleanup_interval: int = 86400  # seconds

    # Environment
    environment: str = "development"

    def __post_init__(self):
        """Validate configuration after initialization."""
        self._load_from_env()
        self._validate()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Database
        if os.getenv("DATABASE_URL"):
            self.database_url = os.getenv("DATABASE_URL")

        if os.getenv("DATABASE_PATH"):
            self.database_path = os.getenv("DATABASE_PATH")

        # Simulation
        if os.getenv("POPULATION_SIZE"):
            self.population_size = int(os.getenv("POPULATION_SIZE"))

        if os.getenv("MAX_GENERATIONS"):
            self.max_generations = int(os.getenv("MAX_GENERATIONS"))

        # API
        if os.getenv("API_HOST"):
            self.api_host = os.getenv("API_HOST")

        if os.getenv("API_PORT"):
            self.api_port = int(os.getenv("API_PORT"))

        # Environment
        if os.getenv("ENVIRONMENT"):
            self.environment = os.getenv("ENVIRONMENT")

        # Logging
        if os.getenv("LOG_LEVEL"):
            self.log_level = os.getenv("LOG_LEVEL")

        logger.debug("Configuration loaded from environment variables")

    def _validate(self):
        """Validate configuration values."""
        if self.population_size <= 0:
            raise ValueError("population_size must be positive")

        if not 0 <= self.mutation_rate <= 1:
            raise ValueError("mutation_rate must be between 0 and 1")

        if not 0 <= self.crossover_rate <= 1:
            raise ValueError("crossover_rate must be between 0 and 1")

        if not 0 <= self.selection_pressure <= 1:
            raise ValueError("selection_pressure must be between 0 and 1")

        if not 0 <= self.elitism_rate <= 1:
            raise ValueError("elitism_rate must be between 0 and 1")

        if self.api_port <= 0 or self.api_port > 65535:
            raise ValueError("api_port must be between 1 and 65535")

        if self.web_port <= 0 or self.web_port > 65535:
            raise ValueError("web_port must be between 1 and 65535")

        logger.debug("Configuration validation passed")

    @classmethod
    def from_file(cls, config_path: str) -> "Config":
        """Load configuration from TOML file."""
        try:
            with open(config_path, 'r') as f:
                data = toml.load(f)

            config = cls(**data)
            logger.info(f"Configuration loaded from {config_path}")
            return config

        except Exception as e:
            logger.error(f"Failed to load config from {config_path}: {e}")
            raise

    @classmethod
    def default(cls) -> "Config":
        """Get default configuration."""
        return cls()

    @classmethod
    def development(cls) -> "Config":
        """Get development configuration."""
        return cls(
            environment="development",
            log_level="DEBUG",
            api_debug=True,
            web_debug=True,
            population_size=50,
            max_generations=10
        )

    @classmethod
    def production(cls) -> "Config":
        """Get production configuration."""
        return cls(
            environment="production",
            log_level="WARNING",
            api_debug=False,
            web_debug=False,
            population_size=1000,
            max_generations=1000,
            parallel_threads=None,  # Use all available cores
            use_rust_engine=True
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    def save_to_file(self, config_path: str):
        """Save configuration to TOML file."""
        try:
            with open(config_path, 'w') as f:
                toml.dump(self.to_dict(), f)
            logger.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save config to {config_path}: {e}")
            raise


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration with automatic environment detection.

    Args:
        config_path: Optional path to config file

    Returns:
        Loaded configuration
    """
    if config_path and os.path.exists(config_path):
        return Config.from_file(config_path)

    # Try to load based on environment
    env = os.getenv("ENVIRONMENT", "development")

    if env == "production":
        config_file = "config/production.toml"
        if os.path.exists(config_file):
            return Config.from_file(config_file)
        return Config.production()

    elif env == "development":
        config_file = "config/development.toml"
        if os.path.exists(config_file):
            return Config.from_file(config_file)
        return Config.development()

    else:
        return Config.default()
