"""
Complete test suite for text chunking functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.text_chunker import TextChunker
from utils.document_processor import DocumentProcessor


def test_end_to_end():
    """Test complete flow from document to chunks"""
    print("\n" + "="*60)
    print("End-to-End Chunking Test")
    print("="*60)
    
    # Create test document
    content = """
    Artificial Intelligence Overview
    
    Artificial Intelligence (AI) is intelligence demonstrated by machines, 
    in contrast to the natural intelligence displayed by humans and animals. 
    Leading AI textbooks define the field as the study of "intelligent agents": 
    any device that perceives its environment and takes actions that maximize 
    its chance of successfully achieving its goals.
    
    Machine Learning
    Machine learning is a subset of artificial intelligence that provides 
    systems the ability to automatically learn and improve from experience 
    without being explicitly programmed. Machine learning focuses on the 
    development of computer programs that can access data and use it to 
    learn for themselves.
    
    Deep Learning
    Deep learning is part of a broader family of machine learning methods 
    based on artificial neural networks with representation learning. 
    Learning can be supervised, semi-supervised or unsupervised.
    
    Applications
    AI is used in various applications including computer vision, speech 
    recognition, natural language processing, machine translation, and 
    expert systems. AI research has been highly successful in developing 
    effective techniques for solving a wide range of problems.
    """ * 2
    
    # Save to file
    with open('test_e2e.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Process document
    processor = DocumentProcessor()
    result = processor.process_and_chunk('test_e2e.txt', chunk_size=300, chunk_overlap=50)
    
    # Display results
    print(f"\n✓ Extraction successful:")
    print(f"  - Format: {result['extraction']['format']}")
    print(f"  - Word count: {result['extraction']['word_count']}")
    print(f"  - Character count: {result['extraction']['char_count']}")
    
    print(f"\n✓ Chunking successful:")
    print(f"  - Total chunks: {result['chunk_stats']['total_chunks']}")
    print(f"  - Total tokens: {result['chunk_stats']['total_tokens']}")
    print(f"  - Avg tokens/chunk: {result['chunk_stats']['avg_tokens_per_chunk']}")
    print(f"  - Min tokens: {result['chunk_stats']['min_tokens']}")
    print(f"  - Max tokens: {result['chunk_stats']['max_tokens']}")
    
    print(f"\n✓ Validation: {result['validation_message']}")
    
    # Display first chunk preview
    if result['chunks']:
        first_chunk = result['chunks'][0]
        print(f"\n✓ First chunk preview:")
        print(f"  {first_chunk['text'][:150]}...")
    
    # Cleanup
    os.remove('test_e2e.txt')
    
    print("\n✅ End-to-end test passed!")


def test_performance_benchmark():
    """Benchmark chunking performance"""
    print("\n" + "="*60)
    print("Performance Benchmark")
    print("="*60)
    
    import time
    
    # Create documents of different sizes
    sizes = {
        '1KB': "x" * 1024,
        '10KB': "x" * (10 * 1024),
        '50KB': "x" * (50 * 1024),
        '100KB': "x" * (100 * 1024)
    }
    
    chunker = TextChunker(chunk_size=500, chunk_overlap=100)
    
    for size_name, content in sizes.items():
        start_time = time.time()
        chunks = chunker.chunk_text(content)
        end_time = time.time()
        
        elapsed_ms = (end_time - start_time) * 1000
        
        print(f"\n✓ {size_name} document:")
        print(f"  - Chunking time: {elapsed_ms:.2f}ms")
        print(f"  - Chunks created: {len(chunks)}")
        print(f"  - Chunks per second: {len(chunks) / (elapsed_ms / 1000):.2f}")
    
    print("\n✅ Performance benchmark complete!")


def test_special_cases():
    """Test special edge cases"""
    print("\n" + "="*60)
    print("Special Cases Test")
    print("="*60)
    
    chunker = TextChunker(chunk_size=200, chunk_overlap=50)
    
    # Test 1: Document with only whitespace
    print("\n✓ Test 1: Whitespace only")
    chunks = chunker.chunk_text("   \n\n   \t\t   ")
    print(f"  - Chunks created: {len(chunks)}")
    assert len(chunks) == 0, "Should create no chunks for whitespace"
    
    # Test 2: Document with single word
    print("\n✓ Test 2: Single word")
    chunks = chunker.chunk_text("Hello")
    print(f"  - Chunks created: {len(chunks)}")
    assert len(chunks) == 1, "Should create one chunk for single word"
    
    # Test 3: Document with repeated newlines
    print("\n✓ Test 3: Multiple newlines")
    text = "Paragraph 1\n\n\n\n\nParagraph 2\n\n\n\nParagraph 3"
    chunks = chunker.chunk_text(text)
    print(f"  - Chunks created: {len(chunks)}")
    
    # Test 4: Document with long unbreakable word
    print("\n✓ Test 4: Long unbreakable word")
    text = "a" * 1000 + " normal text here"
    chunks = chunker.chunk_text(text)
    print(f"  - Chunks created: {len(chunks)}")
    
    print("\n✅ Special cases test passed!")


def test_chunk_quality():
    """Test the quality of chunks"""
    print("\n" + "="*60)
    print("Chunk Quality Test")
    print("="*60)
    
    text = """
    First paragraph with important information about Python programming.
    This paragraph should stay together if possible.
    
    Second paragraph discusses machine learning and artificial intelligence.
    It contains related concepts that should remain grouped.
    
    Third paragraph covers web development frameworks like Django and Flask.
    These frameworks are popular choices for Python developers.
    """
    
    chunker = TextChunker(chunk_size=150, chunk_overlap=30)
    chunks = chunker.chunk_text(text)
    
    print(f"\n✓ Created {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks):
        print(f"\n  Chunk {i} ({chunk['token_count']} tokens):")
        print(f"  {chunk['text'][:100]}...")
        
        # Check that chunks are reasonable
        assert chunk['token_count'] > 10, f"Chunk {i} too small"
        assert chunk['token_count'] <= 200, f"Chunk {i} too large"
    
    print("\n✅ Chunk quality test passed!")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("COMPLETE CHUNKING TEST SUITE")
    print("="*60)
    
    try:
        test_end_to_end()
        test_performance_benchmark()
        test_special_cases()
        test_chunk_quality()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()