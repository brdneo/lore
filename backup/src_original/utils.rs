//! # Performance Utilities and Profiling
//! 
//! This module provides high-performance utilities, benchmarking tools,
//! and profiling helpers for the Lore Engine.

use pyo3::prelude::*;
use std::time::Instant;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use tracing::{info, debug};

/// High-resolution timer for performance benchmarking
#[pyclass]
pub struct Timer {
    start: Instant,
    label: String,
}

#[pymethods]
impl Timer {
    #[new]
    pub fn new(label: String) -> Self {
        debug!("Starting timer: {}", label);
        Self {
            start: Instant::now(),
            label,
        }
    }
    
    /// Get elapsed time in microseconds
    pub fn elapsed_micros(&self) -> u64 {
        self.start.elapsed().as_micros() as u64
    }
    
    /// Get elapsed time in milliseconds
    pub fn elapsed_millis(&self) -> u64 {
        self.start.elapsed().as_millis() as u64
    }
    
    /// Stop timer and log the result
    pub fn stop(&self) -> f64 {
        let elapsed = self.start.elapsed();
        let millis = elapsed.as_millis() as f64;
        info!("Timer '{}' elapsed: {:.2}ms", self.label, millis);
        millis
    }
}

/// Performance counter for tracking operations
#[pyclass]
pub struct PerformanceCounter {
    counter: Arc<AtomicU64>,
    label: String,
}

#[pymethods]
impl PerformanceCounter {
    #[new]
    pub fn new(label: String) -> Self {
        Self {
            counter: Arc::new(AtomicU64::new(0)),
            label,
        }
    }
    
    /// Increment counter
    pub fn increment(&self) {
        self.counter.fetch_add(1, Ordering::Relaxed);
    }
    
    /// Add value to counter
    pub fn add(&self, value: u64) {
        self.counter.fetch_add(value, Ordering::Relaxed);
    }
    
    /// Get current count
    pub fn count(&self) -> u64 {
        self.counter.load(Ordering::Relaxed)
    }
    
    /// Reset counter
    pub fn reset(&self) {
        self.counter.store(0, Ordering::Relaxed);
    }
}

/// Memory usage information
#[pyclass]
#[derive(Debug, Clone)]
pub struct MemoryInfo {
    #[pyo3(get)]
    pub allocated_bytes: u64,
    #[pyo3(get)]
    pub deallocated_bytes: u64,
    #[pyo3(get)]
    pub current_usage: u64,
    #[pyo3(get)]
    pub peak_usage: u64,
}

#[pymethods]
impl MemoryInfo {
    #[new]
    pub fn new() -> Self {
        Self {
            allocated_bytes: 0,
            deallocated_bytes: 0,
            current_usage: 0,
            peak_usage: 0,
        }
    }
}

/// Get system information
#[pyfunction]
pub fn get_system_info() -> PyResult<String> {
    let num_threads = num_cpus::get();
    let info = format!(
        "Lore Engine System Info:\n\
         - CPU cores: {}\n\
         - Rayon threads: {}\n\
         - Rust version: {}\n\
         - Build: {}",
        num_threads,
        rayon::current_num_threads(),
        env!("CARGO_PKG_VERSION"),
        if cfg!(debug_assertions) { "Debug" } else { "Release" }
    );
    Ok(info)
}

/// Benchmark a Python function
#[pyfunction]
pub fn benchmark_function(py: Python<'_>, func: PyObject, iterations: usize) -> PyResult<f64> {
    let timer = Instant::now();
    
    for _ in 0..iterations {
        func.call0(py)?;
    }
    
    let elapsed = timer.elapsed().as_millis() as f64;
    let avg_time = elapsed / iterations as f64;
    
    info!("Benchmarked {} iterations in {:.2}ms (avg: {:.4}ms)", 
          iterations, elapsed, avg_time);
    
    Ok(avg_time)
}

/// Register utility functions with Python
pub fn register_util_functions(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Timer>()?;
    m.add_class::<PerformanceCounter>()?;
    m.add_class::<MemoryInfo>()?;
    m.add_function(wrap_pyfunction!(get_system_info, m)?)?;
    m.add_function(wrap_pyfunction!(benchmark_function, m)?)?;
    Ok(())
}
