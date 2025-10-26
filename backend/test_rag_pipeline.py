"""
Test script for RAG pipeline
Run: python test_rag_pipeline.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.rag_pipeline import RAGPipeline


def test_model_loading():
    """Test model loading"""
    print("\n" + "="*60)
    print("Test 1: Model Loading")
    print("="*60)
    
    pipeline = RAGPipeline()
    model = pipeline.load_model()
    
    print(f"✓ Model name: {pipeline.model_name}")
    print(f"✓ Model device: {model.device}")
    print(f"✓ Max sequence length: {model.max_seq_length}")
    
    print("\n✅ Model loading test passed!")
    return pipeline


def test_embedding_generation():
    """Test embedding generation"""
    print("\n" + "="*60)
    print("Test 2: Embedding Generation")
    print("="*60)
    
    # Create sample chunks
    chunks = [
        {
            'chunk_id': 0,
            'text': 'Python is a high-level programming language created by Guido van Rossum.',
            'token_count': 15
        },
        {
            'chunk_id': 1,
            'text': 'Machine learning is a subset of artificial intelligence that enables systems to learn.',
            'token_count': 16
        },
        {
            'chunk_id': 2,
            'text': 'Data science combines statistics, programming, and domain expertise.',
            'token_count': 12
        },
        {
            'chunk_id': 3,
            'text': 'Neural networks are computational models inspired by biological neural networks.',
            'token_count': 13
        },
        {
            'chunk_id': 4,
            'text': 'Web development involves creating websites using HTML, CSS, and JavaScript.',
            'token_count': 13
        }
    ]
    
    pipeline = RAGPipeline()
    embeddings = pipeline.generate_embeddings(chunks)
    
    print(f"\n✓ Number of chunks: {len(chunks)}")
    print(f"✓ Embeddings shape: {embeddings.shape}")
    print(f"✓ Embedding dimension: {embeddings.shape[1]}")
    print(f"✓ Data type: {embeddings.dtype}")
    
    print("\n✅ Embedding generation test passed!")
    return pipeline, chunks, embeddings


def test_index_creation():
    """Test FAISS index creation"""
    print("\n" + "="*60)
    print("Test 3: Index Creation")
    print("="*60)
    
    # Create sample chunks
    chunks = [
        {'chunk_id': i, 'text': f'Sample text {i}', 'token_count': 10}
        for i in range(10)
    ]
    
    pipeline = RAGPipeline()
    pipeline.build_index(chunks)
    
    print(f"\n✓ Index created: {pipeline.index is not None}")
    print(f"✓ Index size: {pipeline.index.ntotal}")
    print(f"✓ Index dimension: {pipeline.embeddings.shape[1]}")
    
    print("\n✅ Index creation test passed!")
    return pipeline


def test_retrieval():
    """Test chunk retrieval"""
    print("\n" + "="*60)
    print("Test 4: Chunk Retrieval")
    print("="*60)
    
    # Create chunks about different topics
    chunks = [
        {
            'chunk_id': 0,
            'text': 'Python is a programming language used for web development, data science, and automation.',
            'token_count': 15
        },
        {
            'chunk_id': 1,
            'text': 'Machine learning algorithms can classify images, predict outcomes, and recognize patterns.',
            'token_count': 14
        },
        {
            'chunk_id': 2,
            'text': 'JavaScript is the programming language of the web, used for interactive websites.',
            'token_count': 14
        },
        {
            'chunk_id': 3,
            'text': 'Deep learning uses neural networks with multiple layers to process complex data.',
            'token_count': 14
        },
        {
            'chunk_id': 4,
            'text': 'HTML and CSS are used together to structure and style web pages.',
            'token_count': 14
        }
    ]
    
    # Build pipeline
    pipeline = RAGPipeline()
    pipeline.build_index(chunks)
    
    # Test queries
    queries = [
        "What is Python used for?",
        "How does machine learning work?",
        "What is web development?"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        results = pipeline.retrieve(query, k=3)
        
        print(f"   Top 3 results:")
        for result in results:
            print(f"      Rank {result['rank']}: [Score: {result['retrieval_score']:.4f}]")
            print(f"         {result['text'][:80]}...")
    
    print("\n✅ Retrieval test passed!")
    return pipeline


def test_context_retrieval():
    """Test context retrieval"""
    print("\n" + "="*60)
    print("Test 5: Context Retrieval")
    print("="*60)
    
    chunks = [
        {
            'chunk_id': 0,
            'text': 'Python was created by Guido van Rossum in 1991. It emphasizes code readability.',
            'token_count': 15
        },
        {
            'chunk_id': 1,
            'text': 'Python supports multiple programming paradigms including object-oriented and functional.',
            'token_count': 12
        },
        {
            'chunk_id': 2,
            'text': 'The Python standard library is extensive and includes modules for various tasks.',
            'token_count': 14
        }
    ]
    
    pipeline = RAGPipeline()
    pipeline.build_index(chunks)
    
    query = "Tell me about Python"
    context = pipeline.retrieve_context(query, k=3, max_tokens=500)
    
    print(f"\n🔍 Query: '{query}'")
    print(f"\n📝 Retrieved context:")
    print(f"{context}")
    print(f"\n✓ Context length: {len(context)} characters")
    
    print("\n✅ Context retrieval test passed!")


def test_pipeline_stats():
    """Test pipeline statistics"""
    print("\n" + "="*60)
    print("Test 6: Pipeline Statistics")
    print("="*60)
    
    chunks = [
        {'chunk_id': i, 'text': f'Chunk {i} with some text content', 'token_count': 8}
        for i in range(5)
    ]
    
    pipeline = RAGPipeline()
    pipeline.build_index(chunks)
    
    stats = pipeline.get_stats()
    
    print(f"\n📊 Pipeline Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Statistics test passed!")


def test_save_load_index():
    """Test saving and loading index"""
    print("\n" + "="*60)
    print("Test 7: Save and Load Index")
    print("="*60)
    
    # Create and build pipeline
    chunks = [
        {'chunk_id': i, 'text': f'Test chunk {i}', 'token_count': 5}
        for i in range(5)
    ]
    
    pipeline1 = RAGPipeline()
    pipeline1.build_index(chunks)
    
    # Save index
    filepath = 'test_index'
    pipeline1.save_index(filepath)
    
    print(f"\n✓ Index saved")
    
    # Load index in new pipeline
    pipeline2 = RAGPipeline()
    pipeline2.load_index(filepath)
    
    print(f"✓ Index loaded")
    print(f"✓ Loaded {len(pipeline2.chunks)} chunks")
    
    # Clean up
    import os
    os.remove(f"{filepath}.index")
    os.remove(f"{filepath}.pkl")
    print(f"\n✓ Cleaned up test files")
    
    print("\n✅ Save/Load test passed!")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("RAG PIPELINE TESTS")
    print("="*60)
    
    try:
        test_model_loading()
        test_embedding_generation()
        test_index_creation()
        test_retrieval()
        test_context_retrieval()
        test_pipeline_stats()
        test_save_load_index()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 RAG Pipeline is working correctly!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()