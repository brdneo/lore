//! # Lore Engine - High-Performance Genetic Evolution System
//! 
//! A Rust-based engine for ultra-fast genetic algorithms, neural networks,
//! and agent simulation designed to work seamlessly with Python.
//! 
//! ## Features
//! - Ultra-fast genetic algorithms with parallel processing
//! - Scalable neural network graphs for millions of connections
//! - Memory-safe concurrent operations
//! - Zero-copy integration with Python via PyO3
//! - SIMD optimizations and lock-free data structures
//! - Async/await support for I/O intensive operations
//! 
//! ## Architecture
//! - `genetic`: Core genetic algorithm implementations with SIMD
//! - `neural`: Neural network and graph processing for massive graphs
//! - `agent`: Agent behavior simulation with parallel execution
//! - `utils`: High-performance utilities and profiling tools
//! - `python_bindings`: PyO3 bindings optimized for zero-copy transfers
//! - `types`: Common type definitions and shared data structures

use pyo3::prelude::*;
use std::sync::OnceLock;
use tracing::{info, error};

// Modules
pub mod genetic;
pub mod neural;
pub mod agent;
pub mod utils;
pub mod python_bindings;
pub mod types;

// Global initialization
static INIT: OnceLock<()> = OnceLock::new();

/// Initialize global resources once
fn init_globals() {
    INIT.get_or_init(|| {
        // Initialize tracing with simple configuration
        tracing_subscriber::fmt()
            .init();
            
        // Set global allocator for better performance
        #[cfg(feature = "mimalloc")]
        {
            info!("Using mimalloc for optimal memory performance");
        }
        
        // Initialize thread pool with optimal core count
        let num_threads = num_cpus::get();
        rayon::ThreadPoolBuilder::new()
            .num_threads(num_threads)
            .thread_name(|index| format!("lore-worker-{}", index))
            .build_global()
            .expect("Failed to initialize thread pool");
            
        info!("Lore Engine initialized with {} threads", num_threads);
    });
}

/// Initialize the Rust engine with Python
#[pymodule]
fn lore_engine(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Initialize global resources
    init_globals();
    
    info!("Initializing Lore Engine Python bindings");
    
    // Register all module functions with error handling
    if let Err(e) = types::register_types(py, m) {
        error!("Failed to register types: {}", e);
        return Err(e);
    }
    
    if let Err(e) = genetic::register_genetic_functions(py, m) {
        error!("Failed to register genetic functions: {}", e);
        return Err(e);
    }
    
    if let Err(e) = neural::register_neural_functions(py, m) {
        error!("Failed to register neural functions: {}", e);
        return Err(e);
    }
    
    if let Err(e) = agent::register_agent_functions(py, m) {
        error!("Failed to register agent functions: {}", e);
        return Err(e);
    }
    
    if let Err(e) = utils::register_util_functions(py, m) {
        error!("Failed to register utility functions: {}", e);
        return Err(e);
    }
    
    if let Err(e) = python_bindings::register_python_functions(py, m) {
        error!("Failed to register Python binding functions: {}", e);
        return Err(e);
    }
    
    // Add metadata
    m.add("__version__", "0.1.0")?;
    m.add("__author__", "Lore N.A. Genesis Team")?;
    m.add("__license__", "MIT")?;
    m.add("__doc__", "High-performance genetic evolution engine")?;
    
    // Runtime information
    m.add("num_threads", num_cpus::get())?;
    
    info!("Lore Engine Python bindings initialized successfully");
    Ok(())
}
