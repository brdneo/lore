//! # Lore Engine - Evolving Architecture
//! 
//! A Rust-based engine for genetic evolution with gradual feature introduction.

use pyo3::prelude::*;
use tracing::info;

// Modules
pub mod utils;
pub mod types;
pub mod genetic;
pub mod neural;
pub mod agent;

/// Simple evolution engine for testing
#[pyclass]
pub struct EvolutionEngine {
    population_size: usize,
}

#[pymethods]
impl EvolutionEngine {
    #[new]
    pub fn new(population_size: usize) -> Self {
        Self { population_size }
    }
    
    /// Get population size
    pub fn get_population_size(&self) -> usize {
        self.population_size
    }
}

/// Initialize the Rust engine with Python - evolving version
#[pymodule]
fn lore_engine(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Initialize tracing
    tracing_subscriber::fmt().init();
    
    info!("Lore Engine evolving version initialized");
    
    // Register utilities
    utils::register_util_functions(py, m)?;
    
    // Register types
    types::register_types(py, m)?;
    
    // Register genetic algorithms
    genetic::register_genetic_functions(py, m)?;
    
    // Register neural networks
    neural::register_neural_functions(py, m)?;
    
    // Register agent system
    agent::register_agent_functions(py, m)?;
    
    // Register the evolution engine (minimal for now)
    m.add_class::<EvolutionEngine>()?;
    
    // Add metadata
    m.add("__version__", "0.1.0")?;
    m.add("__author__", "Lore N.A. Genesis Team")?;
    m.add("__license__", "MIT")?;
    
    Ok(())
}
