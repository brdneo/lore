"""
Lore N.A. - High-Performance Intelligent Agent Simulation Platform
================================================================

A hybrid Rust+Python platform for creating, evolving, and simulating
intelligent agents with advanced genetic algorithms and neural networks.

Features:
- Ultra-fast Rust core for performance-critical operations
- Intuitive Python interface for ease of use
- Advanced genetic algorithms with parallel processing
- Neural networks for agent cognition
- Real-time simulation and visualization
- Scalable from single machine to distributed clusters

Example:
    >>> import lore_na
    >>> universe = lore_na.Universe()
    >>> universe.create_population(100)
    >>> universe.run_simulation(generations=50)
    >>> universe.get_best_agents(10)
"""

__version__ = "0.1.0"
__author__ = "Lore N.A. Team"
__email__ = "contact@lore-na.com"
__license__ = "MIT"

# Import main modules
from .core.simulation import Universe, Simulation
from .core.population import PopulationManager
from .models.agent import Agent, AgentDNA
from .utils.config import Config
from .utils.logging import setup_logging

# Import Rust engine
try:
    import lore_engine
    RUST_ENGINE_AVAILABLE = True
except ImportError:
    RUST_ENGINE_AVAILABLE = False
    import warnings
    warnings.warn(
        "Rust engine not available. Install with: maturin develop --release",
        ImportWarning
    )

__all__ = [
    "Universe",
    "Simulation",
    "PopulationManager",
    "Agent",
    "AgentDNA",
    "Config",
    "setup_logging",
    "RUST_ENGINE_AVAILABLE",
]

# Version info
VERSION_INFO = {
    "version": __version__,
    "rust_engine": RUST_ENGINE_AVAILABLE,
    "python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
}


def get_version_info():
    """Get detailed version information."""
    return VERSION_INFO.copy()


def health_check():
    """Perform system health check."""
    checks = {
        "python_version": True,
        "rust_engine": RUST_ENGINE_AVAILABLE,
        "dependencies": True,
    }

    try:
        import numpy
        import pandas
        import matplotlib
        checks["scientific_libraries"] = True
    except ImportError:
        checks["scientific_libraries"] = False

    return checks
