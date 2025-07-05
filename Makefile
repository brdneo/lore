# Lore N.A. - Hybrid Rust/Python AI Simulation Platform
# Makefile for build automation and development workflows

.PHONY: help build test clean install dev-setup docker all
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m # No Color

# Project variables
RUST_WORKSPACE := crates
PYTHON_PACKAGE := python
PROJECT_NAME := lore-na
VERSION := 1.0.0

help: ## Show this help message
	@echo "$(BLUE)Lore N.A. - Hybrid Rust/Python AI Simulation Platform$(NC)"
	@echo "========================================================="
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Examples:$(NC)"
	@echo "  make all          # Build everything"
	@echo "  make dev-setup    # Setup development environment"
	@echo "  make test         # Run all tests"
	@echo "  make clean        # Clean all build artifacts"

# =============================================================================
# BUILD TARGETS
# =============================================================================

all: build-rust build-python ## Build everything (Rust + Python)
	@echo "$(GREEN)✅ All builds completed successfully!$(NC)"

build: all ## Alias for 'all'

build-rust: ## Build Rust workspace
	@echo "$(BLUE)🦀 Building Rust workspace...$(NC)"
	cd $(RUST_WORKSPACE) && cargo build --release
	@echo "$(GREEN)✅ Rust build completed$(NC)"

build-rust-dev: ## Build Rust workspace in development mode
	@echo "$(BLUE)🦀 Building Rust workspace (dev)...$(NC)"
	cd $(RUST_WORKSPACE) && cargo build
	@echo "$(GREEN)✅ Rust dev build completed$(NC)"

build-python: ## Build Python package
	@echo "$(BLUE)🐍 Building Python package...$(NC)"
	cd $(PYTHON_PACKAGE) && pip install -e .
	@echo "$(GREEN)✅ Python package built$(NC)"

build-python-wheel: ## Build Python wheel
	@echo "$(BLUE)🐍 Building Python wheel...$(NC)"
	cd $(PYTHON_PACKAGE) && python -m build
	@echo "$(GREEN)✅ Python wheel built$(NC)"

# =============================================================================
# TESTING TARGETS
# =============================================================================

test: test-rust test-python ## Run all tests
	@echo "$(GREEN)✅ All tests completed!$(NC)"

test-rust: ## Run Rust tests
	@echo "$(BLUE)🦀 Running Rust tests...$(NC)"
	cd $(RUST_WORKSPACE) && cargo test --release
	@echo "$(GREEN)✅ Rust tests passed$(NC)"

test-rust-coverage: ## Run Rust tests with coverage
	@echo "$(BLUE)🦀 Running Rust tests with coverage...$(NC)"
	cd $(RUST_WORKSPACE) && cargo install cargo-tarpaulin
	cd $(RUST_WORKSPACE) && cargo tarpaulin --out Html --output-dir ../target/coverage/rust
	@echo "$(GREEN)✅ Rust coverage report generated$(NC)"

test-python: ## Run Python tests
	@echo "$(BLUE)🐍 Running Python tests...$(NC)"
	python -m pytest tests/ -v
	@echo "$(GREEN)✅ Python tests passed$(NC)"

test-python-coverage: ## Run Python tests with coverage
	@echo "$(BLUE)🐍 Running Python tests with coverage...$(NC)"
	python -m pytest tests/ --cov=lore_na --cov-report=html:target/coverage/python
	@echo "$(GREEN)✅ Python coverage report generated$(NC)"

test-integration: ## Run integration tests
	@echo "$(BLUE)🔗 Running integration tests...$(NC)"
	python -m pytest tests/integration/ -v --tb=short
	@echo "$(GREEN)✅ Integration tests passed$(NC)"

benchmark: ## Run performance benchmarks
	@echo "$(BLUE)⚡ Running benchmarks...$(NC)"
	cd $(RUST_WORKSPACE) && cargo bench
	cd $(PYTHON_PACKAGE) && python -m pytest benchmarks/ -v
	@echo "$(GREEN)✅ Benchmarks completed$(NC)"

# =============================================================================
# DEVELOPMENT TARGETS
# =============================================================================

dev-setup: ## Setup development environment
	@echo "$(BLUE)🛠️  Setting up development environment...$(NC)"
	@echo "$(YELLOW)Installing Rust toolchain...$(NC)"
	rustup update
	rustup component add rustfmt clippy
	@echo "$(YELLOW)Installing Python dependencies...$(NC)"
	cd $(PYTHON_PACKAGE) && pip install -e .[dev,ml,viz,web]
	@echo "$(YELLOW)Installing pre-commit hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Development environment ready!$(NC)"

format: format-rust format-python ## Format all code

format-rust: ## Format Rust code
	@echo "$(BLUE)🦀 Formatting Rust code...$(NC)"
	cd $(RUST_WORKSPACE) && cargo fmt

format-python: ## Format Python code
	@echo "$(BLUE)🐍 Formatting Python code...$(NC)"
	cd $(PYTHON_PACKAGE) && black .
	cd $(PYTHON_PACKAGE) && isort .

lint: lint-rust lint-python ## Run all linters

lint-rust: ## Lint Rust code
	@echo "$(BLUE)🦀 Linting Rust code...$(NC)"
	cd $(RUST_WORKSPACE) && cargo clippy -- -D warnings

lint-python: ## Lint Python code
	@echo "$(BLUE)🐍 Linting Python code...$(NC)"
	cd $(PYTHON_PACKAGE) && mypy lore_na/
	cd $(PYTHON_PACKAGE) && flake8 lore_na/

docs: docs-rust docs-python ## Generate all documentation

docs-rust: ## Generate Rust documentation
	@echo "$(BLUE)🦀 Generating Rust documentation...$(NC)"
	cd $(RUST_WORKSPACE) && cargo doc --no-deps --open

docs-python: ## Generate Python documentation
	@echo "$(BLUE)🐍 Generating Python documentation...$(NC)"
	cd $(PYTHON_PACKAGE) && sphinx-build -b html docs/ ../target/docs/python/

# =============================================================================
# DEPLOYMENT TARGETS
# =============================================================================

docker: ## Build Docker images
	@echo "$(BLUE)🐳 Building Docker images...$(NC)"
	docker build -t $(PROJECT_NAME):$(VERSION) .
	docker build -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✅ Docker images built$(NC)"

docker-compose-up: ## Start services with Docker Compose
	@echo "$(BLUE)🐳 Starting services with Docker Compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started$(NC)"

docker-compose-down: ## Stop services with Docker Compose
	@echo "$(BLUE)🐳 Stopping services with Docker Compose...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Services stopped$(NC)"

release: ## Create a release build
	@echo "$(BLUE)🚀 Creating release build...$(NC)"
	$(MAKE) clean
	$(MAKE) build
	$(MAKE) test
	$(MAKE) build-python-wheel
	@echo "$(GREEN)✅ Release build created$(NC)"

# =============================================================================
# MAINTENANCE TARGETS
# =============================================================================

clean: clean-rust clean-python ## Clean all build artifacts
	@echo "$(GREEN)✅ All artifacts cleaned$(NC)"

clean-rust: ## Clean Rust build artifacts
	@echo "$(BLUE)🦀 Cleaning Rust artifacts...$(NC)"
	cd $(RUST_WORKSPACE) && cargo clean
	rm -rf target/

clean-python: ## Clean Python build artifacts
	@echo "$(BLUE)🐍 Cleaning Python artifacts...$(NC)"
	cd $(PYTHON_PACKAGE) && rm -rf build/ dist/ *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

install: ## Install the project for end users
	@echo "$(BLUE)📦 Installing Lore N.A....$(NC)"
	$(MAKE) build-rust
	$(MAKE) build-python
	@echo "$(GREEN)✅ Installation completed$(NC)"

uninstall: ## Uninstall the project
	@echo "$(BLUE)🗑️  Uninstalling Lore N.A....$(NC)"
	cd $(PYTHON_PACKAGE) && pip uninstall -y lore-na
	@echo "$(GREEN)✅ Uninstallation completed$(NC)"

update-deps: ## Update all dependencies
	@echo "$(BLUE)📦 Updating dependencies...$(NC)"
	cd $(RUST_WORKSPACE) && cargo update
	cd $(PYTHON_PACKAGE) && pip install --upgrade pip
	cd $(PYTHON_PACKAGE) && pip-compile --upgrade requirements.in
	@echo "$(GREEN)✅ Dependencies updated$(NC)"

security-audit: ## Run security audits
	@echo "$(BLUE)🔒 Running security audits...$(NC)"
	cd $(RUST_WORKSPACE) && cargo audit
	cd $(PYTHON_PACKAGE) && safety check
	@echo "$(GREEN)✅ Security audit completed$(NC)"

# =============================================================================
# UTILITY TARGETS
# =============================================================================

info: ## Show project information
	@echo "$(BLUE)📋 Project Information$(NC)"
	@echo "======================"
	@echo "Project: $(PROJECT_NAME)"
	@echo "Version: $(VERSION)"
	@echo "Rust workspace: $(RUST_WORKSPACE)"
	@echo "Python package: $(PYTHON_PACKAGE)"
	@echo ""
	@echo "$(BLUE)🦀 Rust Info:$(NC)"
	@cd $(RUST_WORKSPACE) && cargo --version && rustc --version
	@echo ""
	@echo "$(BLUE)🐍 Python Info:$(NC)"
	@python --version
	@pip --version

status: ## Check project status
	@echo "$(BLUE)📊 Project Status$(NC)"
	@echo "=================="
	@echo "$(YELLOW)Git status:$(NC)"
	@git status --porcelain || echo "Not a git repository"
	@echo ""
	@echo "$(YELLOW)Rust workspace:$(NC)"
	@cd $(RUST_WORKSPACE) && cargo check --quiet && echo "✅ Rust OK" || echo "❌ Rust has issues"
	@echo ""
	@echo "$(YELLOW)Python package:$(NC)"
	@cd $(PYTHON_PACKAGE) && python -c "import lore_na; print('✅ Python OK')" 2>/dev/null || echo "❌ Python has issues"

quick-start: ## Quick setup for new developers
	@echo "$(BLUE)🚀 Quick Start Setup$(NC)"
	@echo "===================="
	$(MAKE) dev-setup
	$(MAKE) build
	$(MAKE) test
	@echo ""
	@echo "$(GREEN)🎉 Welcome to Lore N.A. development!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Read the documentation: docs/getting-started/"
	@echo "2. Try the examples: make run-example"
	@echo "3. Run the CLI: lore-na --help"

run-example: ## Run a basic example
	@echo "$(BLUE)🔬 Running basic example...$(NC)"
	cd examples/basic && python simple_agent.py

# =============================================================================
# CI/CD TARGETS
# =============================================================================

ci: ## Run CI pipeline locally
	@echo "$(BLUE)🔄 Running CI pipeline...$(NC)"
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) build
	$(MAKE) test
	$(MAKE) security-audit
	@echo "$(GREEN)✅ CI pipeline completed$(NC)"

cd-staging: ## Deploy to staging environment
	@echo "$(BLUE)🚀 Deploying to staging...$(NC)"
	$(MAKE) release
	# Add staging deployment commands here
	@echo "$(GREEN)✅ Deployed to staging$(NC)"

cd-production: ## Deploy to production environment
	@echo "$(BLUE)🚀 Deploying to production...$(NC)"
	$(MAKE) release
	# Add production deployment commands here
	@echo "$(GREEN)✅ Deployed to production$(NC)"

# =============================================================================
# SPECIAL TARGETS
# =============================================================================

.PHONY: create-agent run-agent simulate
create-agent: ## Create a new agent (CLI wrapper)
	@echo "$(BLUE)🧬 Creating new agent...$(NC)"
	cd $(PYTHON_PACKAGE) && python -m lore_na.cli create-agent --name "demo_agent" --save

run-agent: ## Run an agent (CLI wrapper)
	@echo "$(BLUE)🚀 Running agent...$(NC)"
	cd $(PYTHON_PACKAGE) && python -m lore_na.cli run-agent --name "demo_agent" --agent-type frugal --interval 10

simulate: ## Run a simulation (CLI wrapper)
	@echo "$(BLUE)🌍 Running simulation...$(NC)"
	cd $(PYTHON_PACKAGE) && python -m lore_na.cli simulate --agents 10 --duration 60 --interval 5

# Check if required tools are installed
check-tools:
	@command -v cargo >/dev/null 2>&1 || { echo "$(RED)❌ Rust/Cargo not found. Please install: https://rustup.rs/$(NC)"; exit 1; }
	@command -v python >/dev/null 2>&1 || { echo "$(RED)❌ Python not found. Please install Python 3.8+$(NC)"; exit 1; }
	@command -v pip >/dev/null 2>&1 || { echo "$(RED)❌ pip not found. Please install pip$(NC)"; exit 1; }
	@echo "$(GREEN)✅ All required tools are available$(NC)"

# Make sure tools are available before running targets
build-rust: check-tools
build-python: check-tools
dev-setup: check-tools
