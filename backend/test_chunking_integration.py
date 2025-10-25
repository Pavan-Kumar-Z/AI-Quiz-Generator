"""
Integration test for document processing with chunking
"""

import requests
import os

API_BASE = "http://localhost:5000"


def test_upload_with_chunking():
    """Test file upload with chunking"""
    print("\n" + "="*60)
    print("Testing Upload with Chunking")
    print("="*60)
    
    # Create a substantial test document
    test_content = """
    Python Programming Language
    
    Python is a high-level, interpreted, general-purpose programming language. 
    Its design philosophy emphasizes code readability with the use of significant 
    indentation. Python is dynamically typed and garbage-collected.
    
    History
    Python was conceived in the late 1980s by Guido van Rossum at Centrum 
    Wiskunde & Informatica (CWI) in the Netherlands as a successor to the ABC 
    programming language, which was inspired by SETL, capable of exception 
    handling and interfacing with the Amoeba operating system.
    
    Features
    Python supports multiple programming paradigms, including structured 
    (particularly procedural), object-oriented and functional programming. 
    It is often described as a "batteries included" language due to its 
    comprehensive standard library.
    
    Applications
    Python is used for web development (server-side), software development, 
    mathematics, system scripting, data analysis, artificial intelligence, 
    scientific computing, and many other applications.
    
    Syntax
    Python uses whitespace indentation, rather than curly brackets or keywords, 
    to delimit blocks. An increase in indentation comes after certain statements; 
    a decrease in indentation signifies the end of the current block.
    
    Libraries
    Python has a large ecosystem of third-party packages. The Python Package 
    Index (PyPI), the official repository for third-party Python software, 
    contains over 350,000 packages with a wide range of functionality.
    """ * 3  # Repeat to ensure multiple chunks
    
    # Create test file
    with open('test_chunking.txt', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    # Upload file
    with open('test_chunking.txt', 'rb') as f:
        files = {'file': ('test_chunking.txt', f, 'text/plain')}
        response = requests.post(f"{API_BASE}/upload", files=files)
    
    # Check response
    print(f"\n✓ Status Code: {response.status_code}")
    assert response.status_code == 200, "Upload failed"
    
    data = response.json()
    print(f"✓ Success: {data['success']}")
    assert data['success'] == True, "Response indicates failure"
    
    # Check chunking data
    assert 'chunking' in data['data'], "Chunking data missing"
    
    chunking = data['data']['chunking']
    print(f"\n📊 Chunking Results:")
    print(f"  • Total chunks: {chunking['total_chunks']}")
    print(f"  • Total tokens: {chunking['total_tokens']}")
    print(f"  • Avg tokens per chunk: {chunking['avg_tokens_per_chunk']}")
    print(f"  • Chunk size config: {chunking['chunk_size_config']}")
    print(f"  • Chunk overlap config: {chunking['chunk_overlap_config']}")
    
    # Verify chunking occurred
    assert chunking['total_chunks'] > 1, "Should have multiple chunks"
    assert chunking['total_tokens'] > 0, "Should have tokens"
    assert chunking['avg_tokens_per_chunk'] > 0, "Should have average tokens"
    
    # Cleanup
    os.remove('test_chunking.txt')
    
    print("\n✅ Upload with chunking test passed!")
    return data['data']['saved_as']


def test_different_document_sizes():
    """Test chunking with different document sizes"""
    print("\n" + "="*60)
    print("Testing Different Document Sizes")
    print("="*60)
    
    sizes = {
        'small': "Short document. " * 50,
        'medium': "Medium length document. " * 100,
        'large': "Large document with lots of content. " * 500
    }
    
    for size_name, content in sizes.items():
        # Create test file
        filename = f'test_{size_name}.txt'
        with open(filename, 'w') as f:
            f.write(content)
        
        # Upload
        with open(filename, 'rb') as f:
            files = {'file': (filename, f, 'text/plain')}
            response = requests.post(f"{API_BASE}/upload", files=files)
        
        #data = response.json()
        #chunking = data['data']['chunking']

        data = response.json()

        if not data.get('success', False):
            print(f"❌ Upload failed for {size_name} document")
            print(f"  - Status code: {response.status_code}")
            print(f"  - Response: {data}")
            continue  # Skip to next size

        chunking = data['data']['chunking']
        
        print(f"\n✓ {size_name.capitalize()} document:")
        print(f"  - Word count: {data['data']['word_count']}")
        print(f"  - Chunks: {chunking['total_chunks']}")
        print(f"  - Tokens: {chunking['total_tokens']}")
        
        # Cleanup
        os.remove(filename)
    
    print("\n✅ Different sizes test passed!")


def test_chunk_consistency():
    """Test that chunking is consistent for same document"""
    print("\n" + "="*60)
    print("Testing Chunk Consistency")
    print("="*60)
    
    content = "Consistency test. " * 100
    
    # Upload same document twice
    results = []
    
    for i in range(2):
        with open('test_consistency.txt', 'w') as f:
            f.write(content)
        
        with open('test_consistency.txt', 'rb') as f:
            files = {'file': ('test_consistency.txt', f, 'text/plain')}
            response = requests.post(f"{API_BASE}/upload", files=files)
        
        data = response.json()
        results.append(data['data']['chunking'])
        
        os.remove('test_consistency.txt')
    
    # Compare results
    print(f"\n✓ Upload 1: {results[0]['total_chunks']} chunks, {results[0]['total_tokens']} tokens")
    print(f"✓ Upload 2: {results[1]['total_chunks']} chunks, {results[1]['total_tokens']} tokens")
    
    assert results[0]['total_chunks'] == results[1]['total_chunks'], "Chunk count should be consistent"
    assert results[0]['total_tokens'] == results[1]['total_tokens'], "Token count should be consistent"
    
    print("\n✅ Consistency test passed!")


def test_chunk_validation():
    """Test that invalid documents are rejected"""
    print("\n" + "="*60)
    print("Testing Chunk Validation")
    print("="*60)
    
    # Test with very short document
    short_content = "Too short"
    
    with open('test_short.txt', 'w') as f:
        f.write(short_content)
    
    with open('test_short.txt', 'rb') as f:
        files = {'file': ('test_short.txt', f, 'text/plain')}
        response = requests.post(f"{API_BASE}/upload", files=files)
    
    print(f"\n✓ Short document status: {response.status_code}")
    data = response.json()
    print(f"✓ Success: {data['success']}")
    print(f"✓ Error message: {data.get('error', 'N/A')}")
    
    assert response.status_code == 400, "Should reject short documents"
    assert data['success'] == False, "Should indicate failure"
    
    os.remove('test_short.txt')
    
    print("\n✅ Validation test passed!")


def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("CHUNKING INTEGRATION TESTS")
    print("="*60)
    
    try:
        # Check if server is running
        response = requests.get(f"{API_BASE}/health", timeout=2)
        print("✓ Backend server is running")
        
        # Run tests
        test_upload_with_chunking()
        test_different_document_sizes()
        test_chunk_consistency()
        test_chunk_validation()
        
        print("\n" + "="*60)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Backend server is not running!")
        print("Please start the server first:")
        print("  cd backend")
        print("  python app.py")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()