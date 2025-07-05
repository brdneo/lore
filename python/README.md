# Lore N.A. Python Package

The Python package for the Lore N.A. neural agent simulation platform. This package provides high-level APIs, agent implementations, and utilities for working with the Lore N.A. ecosystem.

## 🚀 Features

-   **Neural Agents**: Complete agent lifecycle management with genetic evolution
-   **Genesis Protocol**: Digital DNA system for agent inheritance and evolution
-   **Multi-Universe Simulation**: Support for Limbo, Odyssey, Ritual, Engine, and Logs universes
-   **API Integration**: Seamless communication with Lore N.A. backend services
-   **Performance Monitoring**: Built-in metrics and fitness tracking
-   **Identity System**: Unique agent identities with cultural origins

## 📦 Installation

### From Source

```bash
cd python/
pip install -e .
```

### With Optional Dependencies

```bash
# For machine learning features
pip install -e .[ml]

# For visualization
pip install -e .[viz]

# For web features
pip install -e .[web]

# For development
pip install -e .[dev]

# All features
pip install -e .[ml,viz,web,dev]
```

## 🏗️ Architecture

```
lore_na/
├── core/           # Core simulation components
├── agents/         # Agent implementations
├── genetics/       # Genesis Protocol (DNA system)
├── models/         # Data models and schemas
├── api/            # API clients and servers
├── utils/          # Utilities and helpers
└── web/            # Web interfaces
```

## 🧬 Quick Start

### Basic Agent Creation

```python
from lore_na.agents import BaseAgent
from lore_na.genetics import DNAGenerator

# Generate genetic DNA
dna_gen = DNAGenerator()
agent_dna = dna_gen.generate_random_dna("my_agent")

# Create agent
agent = BaseAgent(
    name="my_agent",
    api_base_url="http://localhost:8000",
    dna=agent_dna
)

# Run agent lifecycle
agent.run_life_cycle(tick_interval=5)
```

### Genetic Evolution

```python
from lore_na.genetics import EvolutionEngine, AgentDNA

# Create evolution engine
evolution = EvolutionEngine(population_size=100)

# Calculate fitness
performance_data = {
    "limbo": {"profit_ratio": 0.8, "decision_accuracy": 0.9},
    "odyssey": {"creativity_score": 0.7},
    # ... other universe metrics
}

updated_dna = evolution.calculate_fitness(agent_dna, performance_data)
```

### Agent Identity System

```python
from lore_na.genetics import AgentNameGenerator

name_gen = AgentNameGenerator()
identity = name_gen.generate_identity(
    agent_id="agent_001",
    personality="Innovative Artist",
    dna_genes=agent_dna.genes
)

print(f"Agent: {identity.full_name}")
print(f"Origin: {identity.origin}")
print(f"Introduction: {name_gen.generate_introduction(identity)}")
```

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
LORE_API_BASE_URL=http://localhost:8000
KONG_JWT_SECRET=your_jwt_secret
KONG_JWT_ISS=agent_genesis

# Database
DATABASE_URL=postgresql://user:pass@localhost/lore_na

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Configuration Files

```python
from lore_na.utils.config import LoreConfig

config = LoreConfig.from_env()
# or
config = LoreConfig.from_file("config/development.toml")
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m slow

# With coverage
pytest --cov=lore_na --cov-report=html
```

## 📊 Monitoring

### Performance Metrics

```python
from lore_na.core.monitoring import AgentMonitor

monitor = AgentMonitor()
monitor.track_agent_performance(agent)
monitor.export_metrics()  # Prometheus format
```

### Logging

```python
import structlog

logger = structlog.get_logger("lore_na.agents")
logger.info("Agent action", agent_id="001", action="purchase", universe="limbo")
```

## 🌐 API Server

Start the FastAPI server:

```bash
cd python/
python -m lore_na.api.server
```

Or programmatically:

```python
from lore_na.api.server import create_app
import uvicorn

app = create_app()
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## 🔬 Examples

### Frugal Agent

```python
from lore_na.agents import FrugalBuyerAgent

agent = FrugalBuyerAgent(
    name="bargain_hunter_001",
    api_base_url="http://localhost:8000"
)

# Agent will automatically buy cheapest available items
agent.run_life_cycle(tick_interval=10)
```

### Custom Agent

```python
from lore_na.agents import BaseAgent

class CustomAgent(BaseAgent):
    def decide_and_act(self):
        # Custom decision logic
        decision_factors = self.perceive_environment()
        influenced_decision = self.make_decision_with_genes(
            decision_factors,
            "limbo"  # Universe context
        )
        self.execute_action(influenced_decision)

agent = CustomAgent("custom_001", "http://localhost:8000")
```

## 📚 Documentation

-   [Getting Started Guide](../../docs/getting-started/)
-   [Architecture Overview](../../docs/architecture/)
-   [API Reference](../../docs/api/)
-   [Tutorials](../../docs/tutorials/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/username/lore-na.git
cd lore-na/python

# Install in development mode
pip install -e .[dev]

# Run pre-commit hooks
pre-commit install

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## 🙏 Acknowledgments

-   Rust community for the powerful core engine
-   Python ecosystem for rich libraries
-   Contributors and beta testers

## 🔗 Related Projects

-   [Lore Engine (Rust)](../crates/lore-engine/) - High-performance core engine
-   [Lore N.A. Documentation](../../docs/) - Complete documentation
-   [Deployment Configs](../../config/) - Production deployment configurations
