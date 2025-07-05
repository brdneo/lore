# REORGANIZAÇÃO DA ESTRUTURA DO PROJETO - LORE N.A.

## 🎯 OBJETIVO

Reorganizar completamente a estrutura de pastas seguindo melhores práticas para:

-   Facilitar onboarding de novos desenvolvedores
-   Melhorar manutenibilidade do código
-   Seguir padrões industriais
-   Organizar documentação e recursos

## 📁 NOVA ESTRUTURA PROPOSTA

```
lore-na/
├── 📂 .github/                    # GitHub workflows e templates
│   ├── workflows/
│   │   ├── rust-ci.yml
│   │   ├── python-tests.yml
│   │   └── release.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── 📂 crates/                     # Rust workspace (core engine)
│   ├── lore-engine/              # Main hybrid engine
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── genetic.rs
│   │   │   ├── neural.rs
│   │   │   ├── agent.rs
│   │   │   ├── types.rs
│   │   │   └── utils.rs
│   │   ├── Cargo.toml
│   │   ├── README.md
│   │   └── examples/
│   │
│   ├── lore-gpu/                 # GPU acceleration (future)
│   ├── lore-distributed/         # Distributed computing (future)
│   └── lore-ai/                  # Advanced AI features (future)
│
├── 📂 python/                     # Python package
│   ├── lore_na/                  # Main package
│   │   ├── __init__.py
│   │   ├── core/                 # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── population.py
│   │   │   └── simulation.py
│   │   ├── api/                  # REST API
│   │   │   ├── __init__.py
│   │   │   ├── server.py
│   │   │   └── routes/
│   │   ├── web/                  # Web interface
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py
│   │   │   └── templates/
│   │   ├── utils/                # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── logging.py
│   │   │   └── config.py
│   │   └── models/               # Data models
│   │       ├── __init__.py
│   │       ├── agent.py
│   │       └── universe.py
│   │
│   ├── setup.py
│   ├── pyproject.toml
│   └── requirements/
│       ├── base.txt
│       ├── dev.txt
│       └── prod.txt
│
├── 📂 docs/                       # Comprehensive documentation
│   ├── README.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   ├── quickstart.md
│   │   └── first-simulation.md
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── rust-core.md
│   │   ├── python-interface.md
│   │   └── hybrid-system.md
│   ├── api/
│   │   ├── rust-api.md
│   │   ├── python-api.md
│   │   └── rest-api.md
│   ├── tutorials/
│   │   ├── basic-usage.md
│   │   ├── advanced-features.md
│   │   └── custom-agents.md
│   ├── deployment/
│   │   ├── local.md
│   │   ├── cloud.md
│   │   └── production.md
│   └── development/
│       ├── contributing.md
│       ├── coding-standards.md
│       └── testing.md
│
├── 📂 examples/                   # Example applications
│   ├── basic/
│   │   ├── simple_simulation.py
│   │   ├── agent_creation.py
│   │   └── README.md
│   ├── advanced/
│   │   ├── custom_evolution.py
│   │   ├── neural_networks.py
│   │   └── README.md
│   └── enterprise/
│       ├── market_simulation/
│       ├── optimization/
│       └── README.md
│
├── 📂 tests/                      # Test suite
│   ├── unit/
│   │   ├── test_genetic.py
│   │   ├── test_neural.py
│   │   └── test_agents.py
│   ├── integration/
│   │   ├── test_hybrid_system.py
│   │   └── test_api.py
│   ├── e2e/
│   │   └── test_full_simulation.py
│   ├── benchmarks/
│   │   ├── performance_tests.py
│   │   └── comparison_tests.py
│   └── fixtures/
│       ├── sample_agents.json
│       └── test_data.json
│
├── 📂 scripts/                    # Utility scripts
│   ├── setup/
│   │   ├── install.sh
│   │   ├── setup_dev.sh
│   │   └── setup_prod.sh
│   ├── build/
│   │   ├── build_rust.sh
│   │   ├── build_python.sh
│   │   └── build_all.sh
│   ├── deploy/
│   │   ├── deploy_local.sh
│   │   ├── deploy_cloud.sh
│   │   └── docker_deploy.sh
│   └── maintenance/
│       ├── backup.sh
│       ├── cleanup.sh
│       └── health_check.sh
│
├── 📂 config/                     # Configuration files
│   ├── development.toml
│   ├── production.toml
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── docker-compose.prod.yml
│   └── kubernetes/
│       ├── deployment.yaml
│       └── service.yaml
│
├── 📂 data/                       # Data files
│   ├── samples/
│   │   ├── universe_catalog.json
│   │   └── sample_populations.json
│   ├── schemas/
│   │   ├── agent_schema.json
│   │   └── universe_schema.json
│   └── migrations/
│       └── 001_initial.sql
│
├── 📂 assets/                     # Static assets
│   ├── images/
│   │   ├── logo.png
│   │   └── architecture.png
│   ├── videos/
│   └── presentations/
│
├── 📂 benchmarks/                 # Performance benchmarks
│   ├── rust_vs_python.py
│   ├── gpu_acceleration.py
│   └── scalability_tests.py
│
├── 📂 tools/                      # Development tools
│   ├── linters/
│   ├── formatters/
│   └── analyzers/
│
├── 📄 README.md                   # Main project README
├── 📄 CHANGELOG.md                # Version history
├── 📄 CONTRIBUTING.md             # Contribution guidelines
├── 📄 LICENSE                     # MIT License
├── 📄 CODE_OF_CONDUCT.md          # Code of conduct
├── 📄 SECURITY.md                 # Security policy
├── 📄 Cargo.toml                  # Rust workspace
├── 📄 pyproject.toml              # Python project config
├── 📄 .gitignore                  # Git ignore rules
├── 📄 .editorconfig               # Editor configuration
└── 📄 Makefile                    # Build automation
```

## 🎨 PRINCIPIOS DA ORGANIZAÇÃO

### 1. **Separação por Linguagem**

-   `crates/` para código Rust (performance-critical)
-   `python/` para código Python (interface e orchestration)

### 2. **Documentação Centralizada**

-   `docs/` com documentação completa e estruturada
-   READMEs específicos em cada pasta

### 3. **Testes Organizados**

-   Separação por tipo: unit, integration, e2e
-   Benchmarks em pasta dedicada

### 4. **Configuração Flexível**

-   Configs por ambiente (dev, prod)
-   Docker e Kubernetes prontos

### 5. **Exemplos Práticos**

-   Organizados por nível de complexidade
-   READMEs explicativos

## 🚀 PRÓXIMOS PASSOS

1. **Criar nova estrutura de pastas**
2. **Mover arquivos existentes**
3. **Atualizar imports e referências**
4. **Criar documentação estruturada**
5. **Configurar CI/CD**
6. **Validar funcionamento**
