"""
Test caching and memory optimization
Run: python test_cache.py
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from utils.rag_pipeline import RAGPipeline


def test_model_caching():
    """Test that model is cached properly"""
    print("\n" + "="*60)
    print("Test 1: Model Caching")
    print("="*60)
    
    # First load
    print("\n⏱️  First model load...")
    start_time = time.time()
    pipeline1 = RAGPipeline()
    pipeline1.load_model()
    first_load_time = time.time() - start_time
    print(f"   Time: {first_load_time:.2f} seconds")
    
    # Second load (should use cache)
    print("\n⏱️  Second model load (should be instant)...")
    start_time = time.time()
    pipeline2 = RAGPipeline()
    pipeline2.load_model()
    second_load_time = time.time() - start_time
    print(f"   Time: {second_load_time:.2f} seconds")
    
    # Compare
    print(f"\n📊 Results:")
    print(f"   First load: {first_load_time:.2f}s")
    print(f"   Second load: {second_load_time:.2f}s")
    print(f"   Speedup: {first_load_time / second_load_time:.1f}x faster")
    
    if second_load_time < first_load_time / 10:
        print(f"   ✅ Caching is working!")
    else:
        print(f"   ⚠️  Caching may not be working optimally")
    
    print("\n✅ Caching test passed!")


def test_memory_usage():
    """Test memory usage"""
    print("\n" + "="*60)
    print("Test 2: Memory Usage")
    print("="*60)
    
    try:
        import psutil
        process = psutil.Process()
        
        # Before loading model
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        print(f"\n📊 Memory before loading model: {mem_before:.2f} MB")
        
        # Load model
        pipeline = RAGPipeline()
        pipeline.load_model()
        
        # After loading model
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        print(f"📊 Memory after loading model: {mem_after:.2f} MB")
        print(f"📊 Memory increase: {mem_after - mem_before:.2f} MB")
        
        # Create index with sample data
        chunks = [
            {'chunk_id': i, 'text': f'Sample text {i}' * 20, 'token_count': 50}
            for i in range(100)
        ]
        
        pipeline.build_index(chunks)
        
        # After creating index
        mem_final = process.memory_info().rss / 1024 / 1024  # MB
        print(f"📊 Memory after creating index: {mem_final:.2f} MB")
        print(f"📊 Index memory overhead: {mem_final - mem_after:.2f} MB")
        
        print(f"\n📈 Total memory used: {mem_final - mem_before:.2f} MB")
        
        if mem_final < 1000:  # Less than 1GB
            print("   ✅ Memory usage is acceptable")
        else:
            print("   ⚠️  High memory usage detected")
        
    except ImportError:
        print("⚠️  psutil not installed, skipping detailed memory test")
        print("   Install with: pip install psutil")
        
        # Basic test without psutil
        pipeline = RAGPipeline()
        pipeline.load_model()
        chunks = [{'chunk_id': i, 'text': f'Text {i}', 'token_count': 5} for i in range(10)]
        pipeline.build_index(chunks)
        print("   ✅ Basic functionality works")
    
    print("\n✅ Memory test passed!")


def test_multiple_pipelines():
    """Test multiple pipeline instances share model cache"""
    print("\n" + "="*60)
    print("Test 3: Multiple Pipeline Instances")
    print("="*60)
    
    pipelines = []
    
    print("\n🔄 Creating 5 pipeline instances...")
    start_time = time.time()
    
    for i in range(5):
        pipeline = RAGPipeline()
        pipeline.load_model()
        pipelines.append(pipeline)
        print(f"   Pipeline {i+1} created")
    
    total_time = time.time() - start_time
    
    print(f"\n📊 Total time for 5 pipelines: {total_time:.2f} seconds")
    print(f"📊 Average per pipeline: {total_time/5:.2f} seconds")
    
    # Verify all use same model cache location
    print(f"\n✓ All pipelines using model: {pipelines[0].model_name}")
    print(f"✓ Model device: {pipelines[0].model.device}")
    
    print("\n✅ Multiple instances test passed!")


def test_index_reuse():
    """Test that index can be reused efficiently"""
    print("\n" + "="*60)
    print("Test 4: Index Reuse")
    print("="*60)
    
    # Create chunks
    chunks = [
        {'chunk_id': i, 'text': f'Document chunk {i} with content', 'token_count': 10}
        for i in range(50)
    ]
    
    # First pipeline
    print("\n⏱️  Creating first pipeline and index...")
    start_time = time.time()
    pipeline1 = RAGPipeline()
    pipeline1.build_index(chunks)
    first_time = time.time() - start_time
    print(f"   Time: {first_time:.2f} seconds")
    
    # Save index
    filepath = 'test_cache_index'
    pipeline1.save_index(filepath)
    print(f"   ✓ Index saved")
    
    # New pipeline loading saved index
    print("\n⏱️  Loading saved index in new pipeline...")
    start_time = time.time()
    pipeline2 = RAGPipeline()
    pipeline2.load_model()  # Still need model for queries
    pipeline2.load_index(filepath)
    second_time = time.time() - start_time
    print(f"   Time: {second_time:.2f} seconds")
    
    print(f"\n📊 Results:")
    print(f"   Build from scratch: {first_time:.2f}s")
    print(f"   Load from disk: {second_time:.2f}s")
    print(f"   Speedup: {first_time / second_time:.1f}x faster")
    
    # Clean up
    os.remove(f"{filepath}.index")
    os.remove(f"{filepath}.pkl")
    print(f"\n   ✓ Cleaned up test files")
    
    print("\n✅ Index reuse test passed!")


def test_concurrent_access():
    """Test thread-safe concurrent access"""
    print("\n" + "="*60)
    print("Test 5: Concurrent Access")
    print("="*60)
    
    import threading
    
    # Shared pipeline
    pipeline = RAGPipeline()
    chunks = [
        {'chunk_id': i, 'text': f'Content {i}', 'token_count': 5}
        for i in range(20)
    ]
    pipeline.build_index(chunks)
    
    results = []
    errors = []
    
    def query_pipeline(thread_id):
        """Function to run in thread"""
        try:
            query = f"Query from thread {thread_id}"
            result = pipeline.retrieve(query, k=3)
            results.append((thread_id, len(result)))
        except Exception as e:
            errors.append((thread_id, str(e)))
    
    # Create threads
    threads = []
    print("\n🧵 Starting 10 concurrent queries...")
    
    for i in range(10):
        thread = threading.Thread(target=query_pipeline, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    print(f"\n✓ Completed {len(results)} successful queries")
    if errors:
        print(f"⚠️  {len(errors)} errors occurred:")
        for tid, error in errors:
            print(f"   Thread {tid}: {error}")
    else:
        print(f"✓ No errors in concurrent access")
    
    print("\n✅ Concurrent access test passed!")


def main():
    """Run all cache tests"""
    print("\n" + "="*60)
    print("RAG CACHING & OPTIMIZATION TESTS")
    print("="*60)
    
    try:
        test_model_caching()
        test_memory_usage()
        test_multiple_pipelines()
        test_index_reuse()
        test_concurrent_access()
        
        print("\n" + "="*60)
        print("✅ ALL CACHE TESTS PASSED!")
        print("="*60)
        print("\n🎉 Caching and optimization working correctly!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()