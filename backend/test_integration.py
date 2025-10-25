"""
Integration test for document processing with API
"""

import requests
import os

API_BASE = "http://localhost:5000"

def test_health():
    """Test API health"""
    print("\n=== Testing API Health ===")
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✅ Health check passed")

def test_upload_txt():
    """Test TXT file upload"""
    print("\n=== Testing TXT Upload ===")
    
    # Create test file
    test_content = """
    Artificial Intelligence (AI) is transforming the world. Machine learning algorithms 
    can now recognize patterns, make predictions, and even generate creative content.
    Deep learning models power applications from image recognition to natural language processing.
    The future of AI holds immense potential for solving complex problems across various domains.
    """ * 3  # Repeat to ensure enough words
    
    with open('test_ai.txt', 'w') as f:
        f.write(test_content)
    
    # Upload file
    with open('test_ai.txt', 'rb') as f:
        files = {'file': ('test_ai.txt', f, 'text/plain')}
        response = requests.post(f"{API_BASE}/upload", files=files)
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data['success']}")
    print(f"Word count: {data['data']['word_count']}")
    print(f"Text preview: {data['data']['text_preview'][:100]}...")
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['data']['word_count'] > 50
    
    # Cleanup
    os.remove('test_ai.txt')
    print("✅ TXT upload test passed")
    
    return data['data']['saved_as']

def test_generate_quiz(filename):
    """Test quiz generation with extracted text"""
    print("\n=== Testing Quiz Generation ===")
    
    payload = {
        "filename": filename,
        "quiz_mode": "mcq",
        "num_questions": 5,
        "difficulty": "medium"
    }
    
    response = requests.post(f"{API_BASE}/generate-quiz", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data['success']}")
    print(f"Questions generated: {len(data['data']['questions'])}")
    
    assert response.status_code == 200
    assert data['success'] == True
    assert len(data['data']['questions']) == 5
    print("✅ Quiz generation test passed")

def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("DOCUMENT PROCESSING INTEGRATION TESTS")
    print("="*60)
    
    try:
        test_health()
        filename = test_upload_txt()
        test_generate_quiz(filename)
        
        print("\n" + "="*60)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Check if server is running
    try:
        requests.get(f"{API_BASE}/health", timeout=2)
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Backend server is not running!")
        print("Please start the server first:")
        print("  cd backend")
        print("  python app.py")