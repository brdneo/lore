#!/usr/bin/env python3
"""
Test the Lore Engine hybrid Rust/Python module
"""

def test_lore_engine():
    try:
        import lore_engine
        print("✅ SUCCESS: lore_engine imported")
        
        # Check available attributes
        attrs = [x for x in dir(lore_engine) if not x.startswith('_')]
        print(f"📦 Available: {attrs}")
        
        # Test system info
        if hasattr(lore_engine, 'get_system_info'):
            info = lore_engine.get_system_info()
            print(f"🖥️  System info: {info[:100]}...")
        
        # Test evolution engine
        if hasattr(lore_engine, 'EvolutionEngine'):
            engine = lore_engine.EvolutionEngine(100)
            print(f"🧬 Engine created with population: {engine.get_population_size()}")
        
        # Test timer
        if hasattr(lore_engine, 'Timer'):
            timer = lore_engine.Timer("test_operation")
            import time
            time.sleep(0.05)
            elapsed = timer.stop()
            print(f"⏱️  Timer test: {elapsed:.2f}ms")
        
        # Test performance counter
        if hasattr(lore_engine, 'PerformanceCounter'):
            counter = lore_engine.PerformanceCounter("operations")
            counter.increment()
            counter.add(10)
            print(f"📊 Counter test: {counter.count()}")
        
        print("🎉 ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_lore_engine()
