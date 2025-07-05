# Dockerfile for Lore N.A. Project
# Multi-stage build for production optimization

# ================================
# Stage 1: Rust Build Environment
# ================================
FROM rust:1.75-slim AS rust-builder

WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Rust workspace configuration
COPY Cargo.toml Cargo.lock ./
COPY crates/ ./crates/

# Build Rust libraries
RUN cargo build --release

# ====================================
# Stage 2: Python Build Environment  
# ====================================
FROM python:3.11-slim AS python-builder

WORKDIR /app

# Install Python build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Python package configuration
COPY python/requirements.txt ./
COPY python/pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python source code
COPY python/ ./python/
COPY scripts/ ./scripts/
COPY config/ ./config/

# ==============================
# Stage 3: Production Runtime
# ==============================
FROM python:3.11-slim AS runtime

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash lore

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy built artifacts from previous stages
COPY --from=rust-builder /usr/src/app/target/release/ ./target/release/
COPY --from=python-builder /app/ ./

# Copy additional project files
COPY README.md ./
COPY LICENSE ./
COPY Makefile ./

# Install Python package in development mode
RUN pip install -e ./python/

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/cache \
    && chown -R lore:lore /app

# Switch to non-root user
USER lore

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - can be overridden
CMD ["python", "scripts/maintenance/start.py", "--full"]

# ===========================
# Build Labels and Metadata
# ===========================
LABEL maintainer="Lore N.A. Team"
LABEL version="2.0.0"
LABEL description="Lore N.A. - Neural Artificial Life System"
LABEL org.opencontainers.image.source="https://github.com/brdneo/lore"
LABEL org.opencontainers.image.title="Lore N.A."
LABEL org.opencontainers.image.description="Advanced artificial life simulation with neural agents"
