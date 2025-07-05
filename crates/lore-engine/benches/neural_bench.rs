use criterion::{black_box, criterion_group, criterion_main, Criterion};
use lore_engine::neural::*;
use rand::Rng;

fn benchmark_neural_forward(c: &mut Criterion) {
    let mut rng = rand::thread_rng();
    let network = NeuralData::random(&mut rng, 10, 5, 3);
    let input = vec![0.5; 10];
    
    c.bench_function("neural forward pass", |b| {
        b.iter(|| {
            network.forward_pass(black_box(&input))
        })
    });
}

fn benchmark_neural_mutation(c: &mut Criterion) {
    let mut rng = rand::thread_rng();
    let mut network = NeuralData::random(&mut rng, 10, 5, 3);
    
    c.bench_function("neural mutation", |b| {
        b.iter(|| {
            let mut rng = rand::thread_rng();
            network.mutate(black_box(0.1), black_box(&mut rng))
        })
    });
}

criterion_group!(benches, benchmark_neural_forward, benchmark_neural_mutation);
criterion_main!(benches);
