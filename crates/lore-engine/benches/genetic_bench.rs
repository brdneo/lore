use criterion::{black_box, criterion_group, criterion_main, Criterion};
use lore_engine::genetic::*;
use rand::Rng;

fn benchmark_crossover(c: &mut Criterion) {
    let mut rng = rand::thread_rng();
    let parent1 = GeneticData::random(&mut rng);
    let parent2 = GeneticData::random(&mut rng);
    
    c.bench_function("genetic crossover", |b| {
        b.iter(|| {
            let mut rng = rand::thread_rng();
            GeneticData::crossover(
                black_box(&parent1),
                black_box(&parent2),
                black_box(&mut rng)
            )
        })
    });
}

fn benchmark_mutation(c: &mut Criterion) {
    let mut rng = rand::thread_rng();
    let mut data = GeneticData::random(&mut rng);
    
    c.bench_function("genetic mutation", |b| {
        b.iter(|| {
            let mut rng = rand::thread_rng();
            data.mutate(black_box(0.1), black_box(&mut rng))
        })
    });
}

criterion_group!(benches, benchmark_crossover, benchmark_mutation);
criterion_main!(benches);
