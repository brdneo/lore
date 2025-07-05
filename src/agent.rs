//! # Advanced Agent System
//! 
//! This module implements intelligent agents with:
//! - Cognitive architectures
//! - Decision-making systems
//! - Social interaction capabilities
//! - Learning and adaptation

use crate::types::*;
use crate::neural::NeuralNetwork;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use rand::prelude::*;
use std::collections::HashMap;
use std::time::Instant;
use tracing::{debug, info};

/// Agent behavior types
#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub enum BehaviorType {
    Explorer,
    Socializer,
    Optimizer,
    Creator,
    Analyzer,
}

#[pymethods]
impl BehaviorType {
    #[new]
    pub fn new(name: String) -> PyResult<Self> {
        match name.to_lowercase().as_str() {
            "explorer" => Ok(BehaviorType::Explorer),
            "socializer" => Ok(BehaviorType::Socializer),
            "optimizer" => Ok(BehaviorType::Optimizer),
            "creator" => Ok(BehaviorType::Creator),
            "analyzer" => Ok(BehaviorType::Analyzer),
            _ => Err(PyValueError::new_err(format!("Unknown behavior: {}", name))),
        }
    }
    
    pub fn __str__(&self) -> String {
        format!("{:?}", self)
    }
}

/// Cognitive state of an agent
#[pyclass]
#[derive(Clone, Debug)]
pub struct CognitiveState {
    pub attention: Float,
    pub memory_capacity: Float,
    pub processing_speed: Float,
    pub creativity: Float,
    pub social_awareness: Float,
    pub emotional_stability: Float,
}

#[pymethods]
impl CognitiveState {
    #[new]
    pub fn new(
        attention: Float,
        memory_capacity: Float,
        processing_speed: Float,
        creativity: Float,
        social_awareness: Float,
        emotional_stability: Float,
    ) -> PyResult<Self> {
        // Validate ranges (0.0 to 1.0)
        for (name, value) in [
            ("attention", attention),
            ("memory_capacity", memory_capacity),
            ("processing_speed", processing_speed),
            ("creativity", creativity),
            ("social_awareness", social_awareness),
            ("emotional_stability", emotional_stability),
        ] {
            if !(0.0..=1.0).contains(&value) {
                return Err(PyValueError::new_err(
                    format!("{} must be between 0.0 and 1.0, got {}", name, value)
                ));
            }
        }
        
        Ok(Self {
            attention,
            memory_capacity,
            processing_speed,
            creativity,
            social_awareness,
            emotional_stability,
        })
    }
    
    /// Get overall cognitive capacity
    pub fn get_capacity(&self) -> Float {
        (self.attention + self.memory_capacity + self.processing_speed + 
         self.creativity + self.social_awareness + self.emotional_stability) / 6.0
    }
    
    /// Update cognitive state based on experience
    pub fn update(&mut self, experience_type: String, intensity: Float) -> PyResult<()> {
        let adjustment = intensity.clamp(-0.1, 0.1);
        
        match experience_type.as_str() {
            "learning" => {
                self.memory_capacity = (self.memory_capacity + adjustment).clamp(0.0, 1.0);
                self.processing_speed = (self.processing_speed + adjustment * 0.5).clamp(0.0, 1.0);
            },
            "social" => {
                self.social_awareness = (self.social_awareness + adjustment).clamp(0.0, 1.0);
                self.emotional_stability = (self.emotional_stability + adjustment * 0.3).clamp(0.0, 1.0);
            },
            "creative" => {
                self.creativity = (self.creativity + adjustment).clamp(0.0, 1.0);
                self.attention = (self.attention + adjustment * 0.2).clamp(0.0, 1.0);
            },
            "stress" => {
                self.emotional_stability = (self.emotional_stability - adjustment.abs()).clamp(0.0, 1.0);
                self.attention = (self.attention - adjustment.abs() * 0.5).clamp(0.0, 1.0);
            },
            _ => return Err(PyValueError::new_err(format!("Unknown experience type: {}", experience_type))),
        }
        
        Ok(())
    }
}

/// Advanced intelligent agent
#[pyclass]
#[derive(Clone)]
pub struct IntelligentAgent {
    pub id: String,
    pub dna: AgentDNA,
    pub behavior_type: BehaviorType,
    pub cognitive_state: CognitiveState,
    decision_network: Option<NeuralNetwork>,
    memory: HashMap<String, Float>,
    social_connections: Vec<String>,
    experience_points: u64,
    age: u64,
}

#[pymethods]
impl IntelligentAgent {
    #[new]
    pub fn new(
        id: String,
        dna: AgentDNA,
        behavior_type: BehaviorType,
        cognitive_state: CognitiveState,
    ) -> PyResult<Self> {
        info!("Creating intelligent agent: {} with behavior {:?}", id, behavior_type);
        
        Ok(Self {
            id,
            dna,
            behavior_type,
            cognitive_state,
            decision_network: None,
            memory: HashMap::new(),
            social_connections: Vec::new(),
            experience_points: 0,
            age: 0,
        })
    }
    
    /// Set decision-making neural network
    pub fn set_decision_network(&mut self, network: NeuralNetwork) {
        self.decision_network = Some(network);
        info!("Decision network set for agent {}", self.id);
    }
    
    /// Make a decision based on current state and inputs
    pub fn make_decision(&self, situation_inputs: Vec<Float>) -> PyResult<Vec<Float>> {
        let timer = Instant::now();
        
        // Combine situation inputs with agent's internal state
        let mut decision_inputs = situation_inputs.clone();
        
        // Add cognitive state as context
        decision_inputs.extend(vec![
            self.cognitive_state.attention,
            self.cognitive_state.memory_capacity,
            self.cognitive_state.processing_speed,
            self.cognitive_state.creativity,
            self.cognitive_state.social_awareness,
            self.cognitive_state.emotional_stability,
        ]);
        
        // Add some DNA genes as personality factors
        decision_inputs.extend(self.dna.genes.iter().take(4).cloned());
        
        // Use decision network if available
        let decision = if let Some(ref network) = self.decision_network {
            network.forward(decision_inputs)?
        } else {
            // Fallback: simple rule-based decision
            self.simple_decision_making(situation_inputs)?
        };
        
        let elapsed = timer.elapsed().as_micros();
        debug!("Agent {} made decision in {}μs", self.id, elapsed);
        
        Ok(decision)
    }
    
    /// Simple rule-based decision making (fallback)
    fn simple_decision_making(&self, inputs: Vec<Float>) -> PyResult<Vec<Float>> {
        let mut decision = vec![0.0; 3]; // [action_intensity, social_tendency, risk_taking]
        
        let input_sum: Float = inputs.iter().sum();
        let input_avg = if !inputs.is_empty() { input_sum / inputs.len() as Float } else { 0.0 };
        
        match self.behavior_type {
            BehaviorType::Explorer => {
                decision[0] = (input_avg + self.cognitive_state.creativity).min(1.0);
                decision[2] = self.cognitive_state.attention; // Higher risk tolerance
            },
            BehaviorType::Socializer => {
                decision[1] = self.cognitive_state.social_awareness;
                decision[0] = input_avg * 0.7; // Moderate action
            },
            BehaviorType::Optimizer => {
                decision[0] = self.cognitive_state.processing_speed;
                decision[2] = 1.0 - self.cognitive_state.emotional_stability; // Lower risk
            },
            BehaviorType::Creator => {
                decision[0] = self.cognitive_state.creativity;
                decision[1] = input_avg * 0.5; // Some social tendency
            },
            BehaviorType::Analyzer => {
                decision[0] = self.cognitive_state.processing_speed * 0.8;
                decision[2] = 0.2; // Very conservative
            },
        }
        
        Ok(decision)
    }
    
    /// Add social connection
    pub fn add_social_connection(&mut self, other_agent_id: String) {
        if !self.social_connections.contains(&other_agent_id) {
            self.social_connections.push(other_agent_id);
        }
    }
    
    /// Get social network size
    pub fn get_social_network_size(&self) -> usize {
        self.social_connections.len()
    }
    
    /// Store memory
    pub fn store_memory(&mut self, key: String, value: Float) {
        let memory_limit = (self.cognitive_state.memory_capacity * 100.0) as usize;
        
        if self.memory.len() >= memory_limit {
            // Remove oldest memory (simple implementation)
            if let Some(first_key) = self.memory.keys().next().cloned() {
                self.memory.remove(&first_key);
            }
        }
        
        self.memory.insert(key, value);
    }
    
    /// Retrieve memory
    pub fn get_memory(&self, key: String) -> Option<Float> {
        self.memory.get(&key).copied()
    }
    
    /// Gain experience and potentially level up
    pub fn gain_experience(&mut self, points: u64, experience_type: String) -> PyResult<bool> {
        self.experience_points += points;
        self.age += 1;
        
        // Update cognitive state based on experience
        let intensity = (points as Float / 100.0).min(0.1);
        self.cognitive_state.update(experience_type, intensity)?;
        
        // Check for level up (every 1000 experience points)
        let level_up = self.experience_points % 1000 == 0 && points > 0;
        
        if level_up {
            info!("Agent {} leveled up! Total XP: {}", self.id, self.experience_points);
        }
        
        Ok(level_up)
    }
    
    /// Get agent statistics
    pub fn get_stats(&self) -> HashMap<String, Float> {
        let mut stats = HashMap::new();
        
        stats.insert("experience_points".to_string(), self.experience_points as Float);
        stats.insert("age".to_string(), self.age as Float);
        stats.insert("cognitive_capacity".to_string(), self.cognitive_state.get_capacity());
        stats.insert("social_connections".to_string(), self.social_connections.len() as Float);
        stats.insert("memory_usage".to_string(), self.memory.len() as Float);
        stats.insert("fitness".to_string(), self.dna.fitness.unwrap_or(0.0));
        
        stats
    }
    
    /// Get agent ID
    pub fn get_id(&self) -> String {
        self.id.clone()
    }
    
    /// Get behavior type as string
    pub fn get_behavior(&self) -> String {
        format!("{:?}", self.behavior_type)
    }
}

/// Agent society for managing multiple agents
#[pyclass]
pub struct AgentSociety {
    agents: Vec<IntelligentAgent>,
    interaction_history: Vec<(String, String, Float)>, // (agent1, agent2, strength)
}

#[pymethods]
impl AgentSociety {
    #[new]
    pub fn new() -> Self {
        info!("Creating new agent society");
        
        Self {
            agents: Vec::new(),
            interaction_history: Vec::new(),
        }
    }
    
    /// Add agent to society
    pub fn add_agent(&mut self, agent: IntelligentAgent) {
        info!("Adding agent {} to society", agent.id);
        self.agents.push(agent);
    }
    
    /// Get society size
    pub fn get_size(&self) -> usize {
        self.agents.len()
    }
    
    /// Simulate social interactions
    pub fn simulate_interactions(&mut self, num_interactions: usize) -> PyResult<usize> {
        if self.agents.len() < 2 {
            return Ok(0);
        }
        
        let mut rng = thread_rng();
        let mut interactions_created = 0;
        
        for _ in 0..num_interactions {
            // Select two random agents
            let agent1_idx = rng.gen_range(0..self.agents.len());
            let mut agent2_idx = rng.gen_range(0..self.agents.len());
            
            while agent2_idx == agent1_idx {
                agent2_idx = rng.gen_range(0..self.agents.len());
            }
            
            let agent1_id = self.agents[agent1_idx].id.clone();
            let agent2_id = self.agents[agent2_idx].id.clone();
            
            // Calculate interaction strength based on compatibility
            let agent1_social = self.agents[agent1_idx].cognitive_state.social_awareness;
            let agent2_social = self.agents[agent2_idx].cognitive_state.social_awareness;
            
            let interaction_strength = (agent1_social + agent2_social) / 2.0 * rng.gen::<Float>();
            
            // Create mutual connections if strong enough
            if interaction_strength > 0.5 {
                self.agents[agent1_idx].add_social_connection(agent2_id.clone());
                self.agents[agent2_idx].add_social_connection(agent1_id.clone());
                
                // Both agents gain social experience
                let _ = self.agents[agent1_idx].gain_experience(10, "social".to_string());
                let _ = self.agents[agent2_idx].gain_experience(10, "social".to_string());
                
                interactions_created += 1;
            }
            
            // Record interaction
            self.interaction_history.push((agent1_id, agent2_id, interaction_strength));
        }
        
        info!("Simulated {} interactions, {} connections created", num_interactions, interactions_created);
        Ok(interactions_created)
    }
    
    /// Get society statistics
    pub fn get_society_stats(&self) -> HashMap<String, Float> {
        let mut stats = HashMap::new();
        
        if self.agents.is_empty() {
            return stats;
        }
        
        let total_connections: usize = self.agents.iter()
            .map(|agent| agent.get_social_network_size())
            .sum();
        
        let avg_connections = total_connections as Float / self.agents.len() as Float;
        
        let total_experience: u64 = self.agents.iter()
            .map(|agent| agent.experience_points)
            .sum();
        
        let avg_experience = total_experience as Float / self.agents.len() as Float;
        
        let avg_cognitive_capacity: Float = self.agents.iter()
            .map(|agent| agent.cognitive_state.get_capacity())
            .sum::<Float>() / self.agents.len() as Float;
        
        stats.insert("total_agents".to_string(), self.agents.len() as Float);
        stats.insert("total_connections".to_string(), total_connections as Float);
        stats.insert("avg_connections".to_string(), avg_connections);
        stats.insert("avg_experience".to_string(), avg_experience);
        stats.insert("avg_cognitive_capacity".to_string(), avg_cognitive_capacity);
        stats.insert("total_interactions".to_string(), self.interaction_history.len() as Float);
        
        stats
    }
    
    /// Run collective decision making
    pub fn collective_decision(&self, situation: Vec<Float>) -> PyResult<Vec<Float>> {
        if self.agents.is_empty() {
            return Ok(vec![0.0; 3]);
        }
        
        let timer = Instant::now();
        
        // Collect decisions from all agents
        let decisions: Result<Vec<Vec<Float>>, _> = self.agents
            .iter()
            .map(|agent| agent.make_decision(situation.clone()))
            .collect();
        
        let all_decisions = decisions?;
        
        // Average the decisions (simple consensus)
        let decision_size = all_decisions[0].len();
        let mut collective_decision = vec![0.0; decision_size];
        
        for decision in &all_decisions {
            for (i, &value) in decision.iter().enumerate() {
                collective_decision[i] += value;
            }
        }
        
        for value in &mut collective_decision {
            *value /= self.agents.len() as Float;
        }
        
        let elapsed = timer.elapsed().as_millis();
        info!("Collective decision made by {} agents in {}ms", self.agents.len(), elapsed);
        
        Ok(collective_decision)
    }
}

/// Generate random cognitive state
#[pyfunction]
pub fn generate_random_cognitive_state() -> PyResult<CognitiveState> {
    let mut rng = thread_rng();
    
    CognitiveState::new(
        rng.gen_range(0.3..0.9),  // attention
        rng.gen_range(0.4..0.9),  // memory_capacity
        rng.gen_range(0.3..0.8),  // processing_speed
        rng.gen_range(0.2..0.9),  // creativity
        rng.gen_range(0.3..0.8),  // social_awareness
        rng.gen_range(0.4..0.9),  // emotional_stability
    )
}

/// Create agent with neural decision network
#[pyfunction]
pub fn create_agent_with_neural_brain(
    id: String,
    dna: AgentDNA,
    behavior: String,
    brain_architecture: Vec<usize>,
) -> PyResult<IntelligentAgent> {
    use crate::neural::{ActivationType, NeuralNetwork};
    
    // Create cognitive state based on DNA
    let cognitive_state = CognitiveState::new(
        dna.genes.get(0).copied().unwrap_or(0.5).abs().min(1.0),
        dna.genes.get(1).copied().unwrap_or(0.5).abs().min(1.0),
        dna.genes.get(2).copied().unwrap_or(0.5).abs().min(1.0),
        dna.genes.get(3).copied().unwrap_or(0.5).abs().min(1.0),
        dna.genes.get(4).copied().unwrap_or(0.5).abs().min(1.0),
        dna.genes.get(5).copied().unwrap_or(0.5).abs().min(1.0),
    )?;
    
    let behavior_type = BehaviorType::new(behavior)?;
    
    // Create agent
    let mut agent = IntelligentAgent::new(id, dna, behavior_type, cognitive_state)?;
    
    // Create neural decision network
    if brain_architecture.len() >= 2 {
        let activations = vec![ActivationType::ReLU; brain_architecture.len() - 1];
        let network = NeuralNetwork::new(brain_architecture, activations)?;
        agent.set_decision_network(network);
    }
    
    Ok(agent)
}

/// Register agent system functions with Python
pub fn register_agent_functions(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<BehaviorType>()?;
    m.add_class::<CognitiveState>()?;
    m.add_class::<IntelligentAgent>()?;
    m.add_class::<AgentSociety>()?;
    m.add_function(wrap_pyfunction!(generate_random_cognitive_state, m)?)?;
    m.add_function(wrap_pyfunction!(create_agent_with_neural_brain, m)?)?;
    
    info!("Agent system functions registered successfully");
    Ok(())
}
