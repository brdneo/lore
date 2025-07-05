//! # High-Performance Genetic Algorithms
//! 
//! This module implements ultra-fast genetic algorithms with:
//! - Parallel processing with Rayon
//! - Memory-efficient data structures
//! - Advanced selection strategies

use crate::types::*;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use rayon::prelude::*;
use rand::prelude::*;
use rand_distr::Normal;
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::Instant;
use tracing::info;

/// High-performance genetic evolution engine
#[pyclass]
pub struct GeneticEngine {
    params: EvolutionParams,
    generation_counter: AtomicU64,
    evaluation_counter: AtomicU64,
}

#[pymethods]
impl GeneticEngine {
    #[new]
    pub fn new(params: EvolutionParams) -> PyResult<Self> {
        params.validate()?;
        
        info!("GeneticEngine initialized with population size: {}", params.population_size);
        
        Ok(Self {
            params,
            generation_counter: AtomicU64::new(0),
            evaluation_counter: AtomicU64::new(0),
        })
    }
    
    /// Get current generation
    pub fn get_generation(&self) -> u64 {
        self.generation_counter.load(Ordering::Relaxed)
    }
    
    /// Get total evaluations performed
    pub fn get_evaluations(&self) -> u64 {
        self.evaluation_counter.load(Ordering::Relaxed)
    }
    
    /// Get population size
    pub fn get_population_size(&self) -> usize {
        self.params.population_size
    }
    
    /// Create a random population with parallel generation
    pub fn create_random_population(&self, gene_count: usize) -> PyResult<Vec<AgentDNA>> {
        if gene_count == 0 || gene_count > 10000 {
            return Err(PyValueError::new_err("Gene count must be between 1 and 10000"));
        }
        
        info!("Creating random population of {} agents with {} genes", 
              self.params.population_size, gene_count);
        
        let timer = Instant::now();
        
        // Parallel population generation using Rayon
        let population: Vec<AgentDNA> = (0..self.params.population_size)
            .into_par_iter()
            .map(|_| {
                let mut rng = thread_rng();
                let genes: Vec<Float> = (0..gene_count)
                    .map(|_| rng.gen_range(-1.0..1.0))
                    .collect();
                AgentDNA::new(genes)
            })
            .collect();
        
        let elapsed = timer.elapsed().as_millis();
        info!("Random population created in {}ms using parallel processing", elapsed);
        
        Ok(population)
    }
    
    /// Gaussian mutation with adaptive strength
    pub fn mutate(&self, agent: &mut AgentDNA) -> PyResult<()> {
        let mut rng = thread_rng();
        let normal = Normal::new(0.0, 0.1).map_err(|e| 
            PyValueError::new_err(format!("Failed to create normal distribution: {}", e)))?;
        
        for gene in &mut agent.genes {
            if rng.gen::<Float>() < self.params.mutation_rate {
                *gene += normal.sample(&mut rng);
                *gene = gene.clamp(-2.0, 2.0); // Keep genes in reasonable bounds
                agent.mutations += 1;
            }
        }
        
        Ok(())
    }
}

/// Parallel crossover function for batch operations
#[pyfunction]
pub fn parallel_crossover(
    parents1: Vec<AgentDNA>,
    parents2: Vec<AgentDNA>,
    crossover_rate: Float,
) -> PyResult<Vec<AgentDNA>> {
    if parents1.len() != parents2.len() {
        return Err(PyValueError::new_err("Parent arrays must have same length"));
    }
    
    let offspring: Vec<AgentDNA> = parents1
        .par_iter()
        .zip(parents2.par_iter())
        .map(|(p1, p2)| {
            if thread_rng().gen::<Float>() < crossover_rate {
                // Perform uniform crossover
                let mut genes = Vec::with_capacity(p1.genes.len());
                for (g1, g2) in p1.genes.iter().zip(p2.genes.iter()) {
                    genes.push(if thread_rng().gen::<bool>() { *g1 } else { *g2 });
                }
                
                let mut child = AgentDNA::new(genes);
                child.parent_ids = vec![p1.id.clone(), p2.id.clone()];
                child
            } else {
                p1.clone_with_new_id()
            }
        })
        .collect();
    
    Ok(offspring)
}

/// Parallel mutation function for batch operations
#[pyfunction]
pub fn parallel_mutation(
    mut population: Vec<AgentDNA>,
    mutation_rate: Float,
    mutation_strength: Float,
) -> PyResult<Vec<AgentDNA>> {
    population.par_iter_mut().for_each(|agent| {
        if thread_rng().gen::<Float>() < mutation_rate {
            let normal = Normal::new(0.0, mutation_strength).unwrap();
            
            for gene in &mut agent.genes {
                if thread_rng().gen::<Float>() < 0.1 { // Per-gene mutation probability
                    *gene += normal.sample(&mut thread_rng());
                    *gene = gene.clamp(-5.0, 5.0); // Reasonable bounds
                }
            }
            
            agent.mutations += 1;
        }
    });
    
    Ok(population)
}

/// Register genetic algorithm functions with Python
pub fn register_genetic_functions(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<GeneticEngine>()?;
    m.add_function(wrap_pyfunction!(parallel_crossover, m)?)?;
    m.add_function(wrap_pyfunction!(parallel_mutation, m)?)?;
    
    info!("Genetic algorithm functions registered successfully");
    Ok(())
}
