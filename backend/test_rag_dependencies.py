"""
Test script to verify RAG dependencies are working
Run: python test_rag_dependencies.py
"""

import sys


def test_imports():
    """Test that all required packages can be imported"""
    print("\n" + "="*60)
    print("Testing RAG Dependencies")
    print("="*60)
    
    # Test sentence-transformers
    print("\n1. Testing sentence-transformers...")
    try:
        from sentence_transformers import SentenceTransformer
        print("   ✅ sentence-transformers imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import sentence-transformers: {e}")
        return False
    
    # Test FAISS
    print("\n2. Testing FAISS...")
    try:
        import faiss
        print(f"   ✅ FAISS imported successfully (version {faiss.__version__})")
    except ImportError as e:
        print(f"   ❌ Failed to import FAISS: {e}")
        return False
    
    # Test numpy (required dependency)
    print("\n3. Testing numpy...")
    try:
        import numpy as np
        print(f"   ✅ numpy imported successfully (version {np.__version__})")
    except ImportError as e:
        print(f"   ❌ Failed to import numpy: {e}")
        return False
    
    # Test torch (required dependency)
    print("\n4. Testing torch...")
    try:
        import torch
        print(f"   ✅ torch imported successfully (version {torch.__version__})")
        print(f"   ℹ️  CUDA available: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"   ❌ Failed to import torch: {e}")
        return False
    
    return True


def test_model_loading():
    """Test loading a small embedding model"""
    print("\n" + "="*60)
    print("Testing Model Loading")
    print("="*60)
    
    try:
        from sentence_transformers import SentenceTransformer
        import time
        
        print("\n📥 Loading all-MiniLM-L6-v2 model...")
        print("   (This may take a moment on first run...)")
        
        start_time = time.time()
        model = SentenceTransformer('all-MiniLM-L6-v2')
        load_time = time.time() - start_time
        
        print(f"   ✅ Model loaded in {load_time:.2f} seconds")
        print(f"   ℹ️  Model device: {model.device}")
        print(f"   ℹ️  Max sequence length: {model.max_seq_length}")
        
        return True, model
        
    except Exception as e:
        print(f"   ❌ Failed to load model: {e}")
        return False, None


def test_embedding_generation():
    """Test generating embeddings"""
    print("\n" + "="*60)
    print("Testing Embedding Generation")
    print("="*60)
    
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
        
        # Load model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Test sentences
        sentences = [
            "Python is a programming language",
            "Machine learning is a subset of AI",
            "Data science uses Python extensively"
        ]
        
        print(f"\n📝 Generating embeddings for {len(sentences)} sentences...")
        
        # Generate embeddings
        embeddings = model.encode(sentences)
        
        print(f"   ✅ Embeddings generated successfully")
        print(f"   ℹ️  Shape: {embeddings.shape}")
        print(f"   ℹ️  Dimension: {embeddings.shape[1]}")
        print(f"   ℹ️  Data type: {embeddings.dtype}")
        
        # Show first embedding preview
        print(f"\n   📊 First embedding preview (first 10 values):")
        print(f"      {embeddings[0][:10]}")
        
        return True, embeddings
        
    except Exception as e:
        print(f"   ❌ Failed to generate embeddings: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_faiss_index():
    """Test creating a FAISS index"""
    print("\n" + "="*60)
    print("Testing FAISS Index Creation")
    print("="*60)
    
    try:
        import faiss
        import numpy as np
        
        # Create sample embeddings
        dimension = 384  # all-MiniLM-L6-v2 dimension
        num_vectors = 5
        
        print(f"\n🔨 Creating FAISS index...")
        print(f"   Dimension: {dimension}")
        print(f"   Number of vectors: {num_vectors}")
        
        # Create random embeddings for testing
        embeddings = np.random.random((num_vectors, dimension)).astype('float32')
        
        # Create FAISS index
        index = faiss.IndexFlatL2(dimension)
        
        print(f"   ✅ Index created successfully")
        print(f"   ℹ️  Index type: {type(index).__name__}")
        print(f"   ℹ️  Is trained: {index.is_trained}")
        
        # Add vectors to index
        index.add(embeddings)
        
        print(f"   ✅ Added {index.ntotal} vectors to index")
        
        # Test search
        query = embeddings[0:1]  # Use first embedding as query
        k = 3  # Find 3 nearest neighbors
        
        distances, indices = index.search(query, k)
        
        print(f"\n   🔍 Search test:")
        print(f"      Query shape: {query.shape}")
        print(f"      Found {k} nearest neighbors")
        print(f"      Indices: {indices[0]}")
        print(f"      Distances: {distances[0]}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to create FAISS index: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_similarity_search():
    """Test similarity search with real embeddings"""
    print("\n" + "="*60)
    print("Testing Similarity Search")
    print("="*60)
    
    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        import numpy as np
        
        # Load model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Sample documents
        documents = [
            "Python is a high-level programming language",
            "Machine learning uses algorithms to learn patterns",
            "JavaScript is used for web development",
            "Neural networks are inspired by the human brain",
            "HTML and CSS are used to create web pages"
        ]
        
        print(f"\n📚 Documents: {len(documents)}")
        
        # Generate embeddings
        embeddings = model.encode(documents)
        embeddings = np.array(embeddings).astype('float32')
        
        print(f"   ✅ Generated embeddings: {embeddings.shape}")
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        print(f"   ✅ Created FAISS index with {index.ntotal} vectors")
        
        # Query
        query = "What is artificial intelligence?"
        query_embedding = model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        print(f"\n   🔍 Query: '{query}'")
        
        # Search
        k = 3
        distances, indices = index.search(query_embedding, k)
        
        print(f"\n   📊 Top {k} most similar documents:")
        for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
            print(f"      {i+1}. [{distance:.4f}] {documents[idx]}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed similarity search: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("RAG DEPENDENCIES TEST SUITE")
    print("="*60)
    
    success = True
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install dependencies:")
        print("   pip install sentence-transformers faiss-cpu")
        return
    
    # Test 2: Model loading
    model_success, model = test_model_loading()
    if not model_success:
        success = False
    
    # Test 3: Embedding generation
    embed_success, embeddings = test_embedding_generation()
    if not embed_success:
        success = False
    
    # Test 4: FAISS index
    if not test_faiss_index():
        success = False
    
    # Test 5: Similarity search
    if not test_similarity_search():
        success = False
    
    # Final result
    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 RAG dependencies are ready!")
        print("   You can proceed to Step 6.2: Create RAG Pipeline")
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        print("\nPlease fix the issues before proceeding.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()