//! # Common Types and Data Structures
//! 
//! This module defines all shared types, constants, and data structures
//! used across the Lore Engine for maximum type safety and performance.

use pyo3::prelude::*;
use pyo3::exceptions::{PyValueError, PyRuntimeError, PyIOError};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;
use ordered_float::OrderedFloat;

/// Type alias for high-precision floating point numbers
pub type Float = f64;

/// Type alias for ordered floats (can be used as HashMap keys)
pub type OrderedFloat64 = OrderedFloat<f64>;

/// Type alias for agent IDs
pub type AgentId = Uuid;

/// Type alias for generation numbers
pub type Generation = u64;

/// Type alias for fitness scores
pub type Fitness = OrderedFloat64;

/// Agent DNA representation with metadata
#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentDNA {
    #[pyo3(get, set)]
    pub id: String,
    
    #[pyo3(get, set)]
    pub genes: Vec<Float>,
    
    pub fitness: Option<Float>,
    
    #[pyo3(get, set)]
    pub generation: u64,
    
    #[pyo3(get, set)]
    pub parent_ids: Vec<String>,
    
    #[pyo3(get, set)]
    pub creation_time: u64,
    
    #[pyo3(get, set)]
    pub mutations: u32,
    
    #[pyo3(get, set)]
    pub metadata: HashMap<String, String>,
}

#[pymethods]
impl AgentDNA {
    #[new]
    pub fn new(genes: Vec<Float>) -> Self {
        Self {
            id: Uuid::new_v4().to_string(),
            genes,
            fitness: None,
            generation: 0,
            parent_ids: Vec::new(),
            creation_time: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            mutations: 0,
            metadata: HashMap::new(),
        }
    }
    
    /// Get the gene count
    pub fn gene_count(&self) -> usize {
        self.genes.len()
    }
    
    /// Clone the DNA with a new ID
    pub fn clone_with_new_id(&self) -> Self {
        let mut clone = self.clone();
        clone.id = Uuid::new_v4().to_string();
        clone
    }
    
    /// Update fitness score
    pub fn set_fitness(&mut self, fitness: Float) {
        self.fitness = Some(fitness);
    }
    
    /// Check if DNA has valid fitness
    pub fn has_fitness(&self) -> bool {
        self.fitness.is_some()
    }
    
    /// Get fitness or return default
    pub fn get_fitness(&self) -> Float {
        self.fitness.unwrap_or(0.0)
    }
    
    /// Get fitness for Python
    #[getter(fitness)]
    pub fn get_fitness_py(&self) -> Option<Float> {
        self.fitness
    }
    
    /// Set fitness for Python
    #[setter(fitness)]
    pub fn set_fitness_py(&mut self, fitness: Float) {
        self.fitness = Some(fitness);
    }
}

/// Evolution parameters for genetic algorithms
#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvolutionParams {
    #[pyo3(get, set)]
    pub population_size: usize,
    
    #[pyo3(get, set)]
    pub mutation_rate: Float,
    
    #[pyo3(get, set)]
    pub crossover_rate: Float,
    
    #[pyo3(get, set)]
    pub selection_pressure: Float,
    
    #[pyo3(get, set)]
    pub elitism_count: usize,
    
    #[pyo3(get, set)]
    pub max_generations: u64,
    
    #[pyo3(get, set)]
    pub target_fitness: Option<Float>,
    
    #[pyo3(get, set)]
    pub parallel_threads: Option<usize>,
    
    #[pyo3(get, set)]
    pub tournament_size: usize,
}

#[pymethods]
impl EvolutionParams {
    #[new]
    #[pyo3(signature = (
        population_size = 100,
        mutation_rate = 0.1,
        crossover_rate = 0.8,
        selection_pressure = 0.7,
        elitism_count = 5,
        max_generations = 1000,
        target_fitness = None,
        parallel_threads = None,
        tournament_size = 3
    ))]
    pub fn new(
        population_size: usize,
        mutation_rate: Float,
        crossover_rate: Float,
        selection_pressure: Float,
        elitism_count: usize,
        max_generations: u64,
        target_fitness: Option<Float>,
        parallel_threads: Option<usize>,
        tournament_size: usize,
    ) -> Self {
        Self {
            population_size,
            mutation_rate,
            crossover_rate,
            selection_pressure,
            elitism_count,
            max_generations,
            target_fitness,
            parallel_threads,
            tournament_size,
        }
    }
    
    /// Validate parameters for safety
    pub fn validate(&self) -> PyResult<()> {
        if self.population_size == 0 {
            return Err(PyValueError::new_err("Population size must be > 0"));
        }
        if !(0.0..=1.0).contains(&self.mutation_rate) {
            return Err(PyValueError::new_err("Mutation rate must be between 0.0 and 1.0"));
        }
        if !(0.0..=1.0).contains(&self.crossover_rate) {
            return Err(PyValueError::new_err("Crossover rate must be between 0.0 and 1.0"));
        }
        if !(0.0..=1.0).contains(&self.selection_pressure) {
            return Err(PyValueError::new_err("Selection pressure must be between 0.0 and 1.0"));
        }
        if self.elitism_count >= self.population_size {
            return Err(PyValueError::new_err("Elitism count must be < population size"));
        }
        if self.tournament_size == 0 {
            return Err(PyValueError::new_err("Tournament size must be > 0"));
        }
        Ok(())
    }
}

/// Evolution result with detailed metrics
#[pyclass]
#[derive(Debug, Clone)]
pub struct EvolutionResult {
    #[pyo3(get)]
    pub generation: u64,
    
    #[pyo3(get)]
    pub best_fitness: Float,
    
    #[pyo3(get)]
    pub average_fitness: Float,
    
    #[pyo3(get)]
    pub fitness_std: Float,
    
    #[pyo3(get)]
    pub convergence_rate: Float,
    
    #[pyo3(get)]
    pub elapsed_ms: u64,
    
    #[pyo3(get)]
    pub evaluations: u64,
    
    #[pyo3(get)]
    pub best_agent: Option<Py<AgentDNA>>,
    
    #[pyo3(get)]
    pub population: Vec<Py<AgentDNA>>,
    
    #[pyo3(get)]
    pub diversity_index: Float,
    
    #[pyo3(get)]
    pub success: bool,
}

/// Neural network node representation
#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NeuralNode {
    #[pyo3(get, set)]
    pub id: String,
    
    #[pyo3(get, set)]
    pub weights: Vec<Float>,
    
    #[pyo3(get, set)]
    pub bias: Float,
    
    #[pyo3(get, set)]
    pub activation: String,
    
    #[pyo3(get, set)]
    pub connections: Vec<String>,
    
    #[pyo3(get, set)]
    pub layer: usize,
}

/// Social network graph metrics
#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkMetrics {
    #[pyo3(get)]
    pub node_count: usize,
    
    #[pyo3(get)]
    pub edge_count: usize,
    
    #[pyo3(get)]
    pub density: Float,
    
    #[pyo3(get)]
    pub clustering_coefficient: Float,
    
    #[pyo3(get)]
    pub average_path_length: Float,
    
    #[pyo3(get)]
    pub diameter: usize,
    
    #[pyo3(get)]
    pub components: usize,
    
    #[pyo3(get)]
    pub modularity: Float,
    
    #[pyo3(get)]
    pub small_world_coefficient: Float,
}

/// Performance profiling result
#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProfileResult {
    #[pyo3(get)]
    pub function_name: String,
    
    #[pyo3(get)]
    pub elapsed_ns: u64,
    
    #[pyo3(get)]
    pub memory_peak_kb: u64,
    
    #[pyo3(get)]
    pub cpu_usage_percent: Float,
    
    #[pyo3(get)]
    pub thread_count: usize,
    
    #[pyo3(get)]
    pub iterations: u64,
    
    #[pyo3(get)]
    pub throughput_ops_per_sec: Float,
}

/// Error types for robust error handling
#[derive(thiserror::Error, Debug)]
pub enum LoreError {
    #[error("Genetic algorithm error: {0}")]
    Genetic(String),
    
    #[error("Neural network error: {0}")]
    Neural(String),
    
    #[error("Agent simulation error: {0}")]
    Agent(String),
    
    #[error("Performance error: {0}")]
    Performance(String),
    
    #[error("Validation error: {0}")]
    Validation(String),
    
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("JSON serialization error: {0}")]
    Json(#[from] serde_json::Error),
}

impl From<LoreError> for PyErr {
    fn from(err: LoreError) -> PyErr {
        match err {
            LoreError::Genetic(msg) => PyRuntimeError::new_err(format!("Genetic: {}", msg)),
            LoreError::Neural(msg) => PyRuntimeError::new_err(format!("Neural: {}", msg)),
            LoreError::Agent(msg) => PyRuntimeError::new_err(format!("Agent: {}", msg)),
            LoreError::Performance(msg) => PyRuntimeError::new_err(format!("Performance: {}", msg)),
            LoreError::Validation(msg) => PyValueError::new_err(format!("Validation: {}", msg)),
            LoreError::Io(err) => PyIOError::new_err(format!("IO: {}", err)),
            LoreError::Json(err) => PyValueError::new_err(format!("JSON: {}", err)),
        }
    }
}

/// Result type for all operations
pub type LoreResult<T> = Result<T, LoreError>;

/// Register all types with Python module
pub fn register_types(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<AgentDNA>()?;
    m.add_class::<EvolutionParams>()?;
    m.add_class::<EvolutionResult>()?;
    m.add_class::<NeuralNode>()?;
    m.add_class::<NetworkMetrics>()?;
    m.add_class::<ProfileResult>()?;
    
    // Add constants
    m.add("DEFAULT_POPULATION_SIZE", 100)?;
    m.add("DEFAULT_MUTATION_RATE", 0.1)?;
    m.add("DEFAULT_CROSSOVER_RATE", 0.8)?;
    m.add("DEFAULT_SELECTION_PRESSURE", 0.7)?;
    m.add("MAX_GENE_COUNT", 10000)?;
    m.add("MIN_POPULATION_SIZE", 10)?;
    
    Ok(())
}
