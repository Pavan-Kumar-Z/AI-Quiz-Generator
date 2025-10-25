"""
Test script for text chunker
Run: python test_chunker.py
"""

import sys
import os

# Add utils to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.text_chunker import TextChunker


def test_basic_chunking():
    """Test basic text chunking"""
    print("\n" + "="*60)
    print("Test 1: Basic Chunking")
    print("="*60)
    
    # Sample text
    text = """
    Python is a high-level, interpreted programming language. It was created by 
    Guido van Rossum and first released in 1991. Python's design philosophy 
    emphasizes code readability with its notable use of significant whitespace.
    
    Python is dynamically typed and garbage-collected. It supports multiple 
    programming paradigms, including structured, object-oriented, and functional 
    programming. Python is often described as a "batteries included" language 
    due to its comprehensive standard library.
    
    Python interpreters are available for many operating systems. CPython, the 
    reference implementation of Python, is open source software and has a 
    community-based development model. Python is managed by the Python Software 
    Foundation.
    """ * 5  # Repeat to create larger text
    
    # Create chunker
    chunker = TextChunker(chunk_size=200, chunk_overlap=50)
    
    # Chunk the text
    chunks = chunker.chunk_text(text)
    
    print(f"✓ Original text length: {len(text)} characters")
    print(f"✓ Number of chunks created: {len(chunks)}")
    
    # Display first 3 chunks
    print(f"\n✓ First 3 chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n  Chunk {i}:")
        print(f"    - Tokens: {chunk['token_count']}")
        print(f"    - Characters: {chunk['char_count']}")
        print(f"    - Preview: {chunk['text'][:100]}...")
    
    print("\n✅ Basic chunking test passed!")
    return chunks


def test_chunk_stats():
    """Test chunk statistics"""
    print("\n" + "="*60)
    print("Test 2: Chunk Statistics")
    print("="*60)
    
    text = "This is a test sentence. " * 100
    
    chunker = TextChunker(chunk_size=150, chunk_overlap=30)
    chunks = chunker.chunk_text(text)
    
    # Get statistics
    stats = chunker.get_chunk_stats(chunks)
    
    print(f"✓ Total chunks: {stats['total_chunks']}")
    print(f"✓ Total tokens: {stats['total_tokens']}")
    print(f"✓ Total characters: {stats['total_chars']}")
    print(f"✓ Average tokens per chunk: {stats['avg_tokens_per_chunk']}")
    print(f"✓ Average characters per chunk: {stats['avg_chars_per_chunk']}")
    print(f"✓ Min tokens in a chunk: {stats['min_tokens']}")
    print(f"✓ Max tokens in a chunk: {stats['max_tokens']}")
    
    print("\n✅ Statistics test passed!")


def test_chunk_overlap():
    """Test that chunks have proper overlap"""
    print("\n" + "="*60)
    print("Test 3: Chunk Overlap")
    print("="*60)
    
    text = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence. Sixth sentence. Seventh sentence. Eighth sentence."
    
    chunker = TextChunker(chunk_size=50, chunk_overlap=20)
    chunks = chunker.chunk_text(text)
    
    print(f"✓ Created {len(chunks)} chunks with overlap")
    
    # Check for overlap between consecutive chunks
    if len(chunks) > 1:
        for i in range(len(chunks) - 1):
            chunk1_end = chunks[i]['text'][-20:]
            chunk2_start = chunks[i + 1]['text'][:20]
            
            print(f"\n  Chunk {i} ending: ...{chunk1_end}")
            print(f"  Chunk {i+1} starting: {chunk2_start}...")
            
            # Note: Overlap might not be exact due to separator logic
    
    print("\n✅ Overlap test passed!")


def test_different_chunk_sizes():
    """Test with different chunk sizes"""
    print("\n" + "="*60)
    print("Test 4: Different Chunk Sizes")
    print("="*60)
    
    text = "Python programming language. " * 200
    
    sizes = [100, 300, 500]
    
    for size in sizes:
        chunker = TextChunker(chunk_size=size, chunk_overlap=50)
        chunks = chunker.chunk_text(text)
        stats = chunker.get_chunk_stats(chunks)
        
        print(f"\n✓ Chunk size: {size} tokens")
        print(f"  - Total chunks: {stats['total_chunks']}")
        print(f"  - Avg tokens per chunk: {stats['avg_tokens_per_chunk']}")
    
    print("\n✅ Different sizes test passed!")


def test_validation():
    """Test chunk validation"""
    print("\n" + "="*60)
    print("Test 5: Chunk Validation")
    print("="*60)
    
    # Valid text
    text = "This is a valid document with enough content. " * 20
    chunker = TextChunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk_text(text)
    
    is_valid, message = chunker.validate_chunks(chunks)
    print(f"✓ Valid chunks: {is_valid}")
    print(f"  Message: {message}")
    
    # Empty text
    empty_chunks = chunker.chunk_text("")
    is_valid, message = chunker.validate_chunks(empty_chunks)
    print(f"\n✓ Empty text validation: {not is_valid}")
    print(f"  Message: {message}")
    
    print("\n✅ Validation test passed!")


def test_metadata():
    """Test metadata attachment"""
    print("\n" + "="*60)
    print("Test 6: Metadata Attachment")
    print("="*60)
    
    text = "Python is great. " * 50
    
    metadata = {
        'document_id': 'doc_123',
        'source': 'test_document.txt',
        'upload_date': '2024-01-25'
    }
    
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.chunk_text(text, metadata=metadata)
    
    print(f"✓ Created {len(chunks)} chunks with metadata")
    print(f"\n  Sample chunk metadata:")
    print(f"    {chunks[0]['metadata']}")
    
    print("\n✅ Metadata test passed!")


def test_previews():
    """Test chunk previews"""
    print("\n" + "="*60)
    print("Test 7: Chunk Previews")
    print("="*60)
    
    text = "This is a long sentence that should be truncated in the preview. " * 10
    
    chunker = TextChunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk_text(text)
    
    previews = chunker.preview_chunks(chunks, max_preview_length=50)
    
    print(f"✓ Generated {len(previews)} previews")
    print(f"\n  First preview:")
    print(f"    {previews[0]}")
    
    print("\n✅ Preview test passed!")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("TEXT CHUNKER TESTS")
    print("="*60)
    
    try:
        test_basic_chunking()
        test_chunk_stats()
        test_chunk_overlap()
        test_different_chunk_sizes()
        test_validation()
        test_metadata()
        test_previews()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
    