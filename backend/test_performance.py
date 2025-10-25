"""
Performance tests for document processing
"""

import time
import os
from utils.document_processor import DocumentProcessor

def test_processing_speed():
    """Test processing speed for different file sizes"""
    print("\n=== Document Processing Performance Test ===\n")
    
    processor = DocumentProcessor()
    
    # Create test files of different sizes
    sizes = {
        "Small (1KB)": "x" * 1024,
        "Medium (10KB)": "x" * (10 * 1024),
        "Large (100KB)": "x" * (100 * 1024)
    }
    
    for size_name, content in sizes.items():
        # Create test file
        filename = f"test_{size_name.replace(' ', '_')}.txt"
        with open(filename, 'w') as f:
            f.write(content)
        
        # Measure processing time
        start_time = time.time()
        result = processor.process_document(filename)
        end_time = time.time()
        
        elapsed = (end_time - start_time) * 1000  # Convert to ms
        
        print(f"{size_name}:")
        print(f"  - Processing time: {elapsed:.2f}ms")
        print(f"  - Word count: {result['word_count']}")
        print(f"  - Characters: {result['char_count']}\n")
        
        # Cleanup
        os.remove(filename)
    
    print("✅ Performance test complete")

if __name__ == "__main__":
    test_processing_speed()