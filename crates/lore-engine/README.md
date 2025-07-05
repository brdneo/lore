# Lore Engine - Rust Core

High-performance Rust core for the Lore N.A. intelligent agent simulation platform.

## Features

-   🚀 **Ultra-fast genetic algorithms** with parallel processing
-   🧠 **Optimized neural networks** for agent cognition
-   🤖 **Intelligent agent systems** with emergent behaviors
-   🔗 **Seamless Python integration** via PyO3
-   📊 **Advanced performance monitoring** and profiling

## Architecture

The Rust core handles all performance-critical operations:

-   **Genetic Operations**: Population creation, evolution, selection
-   **Neural Processing**: Feedforward networks, backpropagation, inference
-   **Agent Cognition**: Decision making, memory, learning
-   **Parallel Processing**: Multi-threaded operations with Rayon
-   **Memory Management**: Zero-copy operations where possible

## Building

```bash
# Development build
cargo build

# Release build (optimized)
cargo build --release

# Run tests
cargo test

# Run benchmarks
cargo bench
```

## Python Integration

This crate is designed to be used from Python via PyO3:

```python
import lore_engine

# Create genetic engine
params = lore_engine.EvolutionParams(population_size=100)
engine = lore_engine.GeneticEngine(params)

# Create agents
population = engine.create_random_population(100)

# Neural networks
network = lore_engine.create_feedforward_network(10, [20, 15], 5, "relu")
result = network.forward([0.1, 0.2, 0.3, 0.4, 0.5])
```

## Performance

Benchmarks on modern hardware show:

-   10-100x faster genetic operations vs pure Python
-   50-200x faster neural network inference
-   Linear scaling with CPU cores via Rayon
-   Memory-efficient operations with minimal allocations
