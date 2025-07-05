"""
Lore Engine - High-performance hybrid Python/Rust genetic evolution engine.

This module provides Python bindings for the Rust-based high-performance
components of the Lore N.A. project, including:

- Genetic algorithms with parallel evolution
- Neural network simulation and social graphs
- Multi-threaded agent simulation
- Performance utilities and benchmarking tools

The Rust engine is designed to accelerate the most computationally intensive
parts of the Lore N.A. ecosystem while maintaining seamless integration
with existing Python code.

Example:
    >>> import lore_engine
    >>> engine = lore_engine.EvolutionEngine(population_size=1000)
    >>> result = engine.evolve_generation(agents, selection_pressure=0.8)
    >>> print(f"Evolution completed in {result.elapsed_ms}ms")
"""

# Import native Rust module when available
try:
    from .lore_engine import *
    
    __version__ = "0.1.0"
    __author__ = "Lore N.A. Genesis Team"
    __license__ = "MIT"
    
    # Re-export main classes and functions for convenience
    __all__ = [
        "EvolutionEngine",
        "NeuralNetwork", 
        "SocialGraph",
        "AgentSimulator",
        "PerformanceProfiler",
        "benchmark_function",
        "parallel_crossover",
        "parallel_mutation",
        "parallel_selection",
        "create_social_network",
        "analyze_network_metrics",
        "simulate_agent_interactions",
        "profile_execution_time",
    ]
    
except ImportError as e:
    # Fallback when Rust module is not built
    import warnings
    warnings.warn(
        f"Rust engine not available: {e}. "
        "Please build the module with 'maturin develop' or 'pip install -e .'",
        ImportWarning
    )
    
    # Provide stub implementations for development
    class EvolutionEngine:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    class NeuralNetwork:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    class SocialGraph:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    class AgentSimulator:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    class PerformanceProfiler:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def benchmark_function(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def parallel_crossover(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def parallel_mutation(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def parallel_selection(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def create_social_network(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def analyze_network_metrics(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def simulate_agent_interactions(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    def profile_execution_time(*args, **kwargs):
        raise NotImplementedError("Rust engine not built. Run 'maturin develop'.")
    
    __all__ = [
        "EvolutionEngine",
        "NeuralNetwork", 
        "SocialGraph",
        "AgentSimulator",
        "PerformanceProfiler",
        "benchmark_function",
        "parallel_crossover",
        "parallel_mutation", 
        "parallel_selection",
        "create_social_network",
        "analyze_network_metrics",
        "simulate_agent_interactions",
        "profile_execution_time",
    ]
