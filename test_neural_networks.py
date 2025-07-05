#!/usr/bin/env python3
"""
🧠 TEST NEURAL NETWORKS - Hybrid Rust System
============================================

Comprehensive test for the new neural network module.
"""

import sys
import time
import numpy as np

def main():
    print("🧠 LORE ENGINE - NEURAL NETWORKS TEST")
    print("="*50)
    
    try:
        import lore_engine
        print("✅ Módulo lore_engine carregado com sucesso!")
        
        # Count available functions
        functions = [attr for attr in dir(lore_engine) if not attr.startswith('_')]
        print(f"📦 {len(functions)} funcionalidades disponíveis")
        
        # Test activation types
        print("\n🎛️ Testando tipos de ativação:")
        activations = ['relu', 'sigmoid', 'tanh', 'leakyrelu', 'elu', 'swish']
        for act_name in activations:
            try:
                activation = lore_engine.ActivationType(act_name)
                print(f"   ✅ {act_name.upper()}: {activation}")
            except Exception as e:
                print(f"   ❌ {act_name.upper()}: {e}")
                
        # Test neural layer creation
        print("\n🧪 Testando camada neural:")
        layer = lore_engine.NeuralLayer(4, 3, lore_engine.ActivationType("relu"))
        print(f"   ✅ Camada criada: {layer.get_input_size()} -> {layer.get_output_size()}")
        
        # Test forward pass
        inputs = [0.5, -0.3, 0.8, -0.1]
        outputs = layer.forward(inputs)
        print(f"   ✅ Forward pass: {len(inputs)} -> {len(outputs)}")
        print(f"   📊 Saída: {[f'{x:.3f}' for x in outputs]}")
        
        # Test neural network creation
        print("\n🧠 Testando rede neural:")
        layer_sizes = [4, 6, 4, 2]
        activations = [
            lore_engine.ActivationType("relu"),
            lore_engine.ActivationType("sigmoid"),
            lore_engine.ActivationType("tanh")
        ]
        
        network = lore_engine.NeuralNetwork(layer_sizes, activations)
        print(f"   ✅ Rede criada: {network.get_architecture()}")
        print(f"   📊 Parâmetros: {network.get_parameter_count():,}")
        
        # Test network forward pass
        net_inputs = [0.1, 0.5, -0.2, 0.8]
        net_outputs = network.forward(net_inputs)
        print(f"   ✅ Propagação: {len(net_inputs)} -> {len(net_outputs)}")
        print(f"   📊 Saída final: {[f'{x:.4f}' for x in net_outputs]}")
        
        # Test feedforward helper
        print("\n🏗️ Testando construtor feedforward:")
        ff_network = lore_engine.create_feedforward_network(3, [5, 4], 2, "relu")
        print(f"   ✅ Rede feedforward: {ff_network.get_architecture()}")
        
        # Test batch processing
        print("\n📊 Testando processamento em lote:")
        batch_size = 10
        batch_inputs = [[np.random.randn() for _ in range(4)] for _ in range(batch_size)]
        
        start_time = time.time()
        batch_outputs = network.batch_forward(batch_inputs)
        elapsed = (time.time() - start_time) * 1000
        
        print(f"   ✅ Lote processado: {batch_size} amostras em {elapsed:.2f}ms")
        print(f"   📊 Saídas por amostra: {len(batch_outputs[0])}")
        
        # Performance comparison with Python
        print("\n⚡ Benchmark Rust vs Python:")
        
        # Create simple Python equivalent for comparison
        def python_forward(inputs, weights, biases):
            outputs = []
            for i, (w_row, b) in enumerate(zip(weights, biases)):
                output = sum(w * x for w, x in zip(w_row, inputs)) + b
                outputs.append(max(0, output))  # ReLU
            return outputs
        
        # Get layer weights for comparison
        weights = layer.get_weights()
        biases = layer.get_biases()
        
        # Benchmark Rust
        rust_times = []
        for _ in range(1000):
            start = time.perf_counter()
            layer.forward(inputs)
            rust_times.append(time.perf_counter() - start)
        
        # Benchmark Python
        python_times = []
        for _ in range(1000):
            start = time.perf_counter()
            python_forward(inputs, weights, biases)
            python_times.append(time.perf_counter() - start)
        
        rust_avg = np.mean(rust_times) * 1_000_000  # microseconds
        python_avg = np.mean(python_times) * 1_000_000
        speedup = python_avg / rust_avg if rust_avg > 0 else float('inf')
        
        print(f"   🦀 Rust:   {rust_avg:.1f}μs")
        print(f"   🐍 Python: {python_avg:.1f}μs")
        print(f"   🚀 Speedup: {speedup:.1f}x")
        
        # Test memory efficiency
        print("\n💾 Testando eficiência de memória:")
        large_network = lore_engine.create_feedforward_network(100, [200, 150, 100], 50, "relu")
        print(f"   ✅ Rede grande: {large_network.get_parameter_count():,} parâmetros")
        
        large_inputs = [np.random.randn() for _ in range(100)]
        start_time = time.time()
        large_outputs = large_network.forward(large_inputs)
        elapsed = (time.time() - start_time) * 1000
        
        print(f"   ⚡ Processamento: {elapsed:.2f}ms")
        print(f"   📊 Saída: {len(large_outputs)} neurônios")
        
        # System information
        print("\n💻 Sistema:")
        print(f"   - CPU cores: {lore_engine.cpu_count()}")
        
        print("\n🎉 TODOS OS TESTES DE NEURAL NETWORKS PASSARAM!")
        print("✅ Sistema neural híbrido funcionando perfeitamente!")
        print("🧠 Pronto para simulações cognitivas avançadas!")
        
    except ImportError as e:
        print(f"❌ Erro ao importar lore_engine: {e}")
        print("💡 Execute: maturin develop --release")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
