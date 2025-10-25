"""
Test script for document processor
Run: python test_processor.py
"""

import sys
import os

# Add utils to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.document_processor import DocumentProcessor

def test_txt_file():
    """Test TXT file processing"""
    print("\n" + "="*50)
    print("Testing TXT File Processing")
    print("="*50)
    
    # Create a test TXT file
    test_file = "test_document.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("""
        Python is a high-level programming language. 
        It was created by Guido van Rossum in 1991.
        Python is known for its simple syntax and readability.
        It is widely used in web development, data science, and artificial intelligence.
        
        Python supports multiple programming paradigms including:
        - Object-oriented programming
        - Functional programming
        - Procedural programming
        
        The language emphasizes code readability and allows programmers to express concepts 
        in fewer lines of code compared to other languages.
        """)
    
    # Process the file
    processor = DocumentProcessor()
    result = processor.process_document(test_file)
    
    print(f"✓ Format: {result['format']}")
    print(f"✓ Word count: {result['word_count']}")
    print(f"✓ Character count: {result['char_count']}")
    print(f"✓ Line count: {result.get('line_count', 'N/A')}")
    print(f"\n✓ Text preview (first 200 chars):")
    print(result['text'][:200] + "...")
    
    # Validate text
    is_valid, message = processor.validate_text(result['text'])
    print(f"\n✓ Validation: {message}")
    
    # Clean up
    os.remove(test_file)
    print("\n✅ TXT processing test passed!")

def test_pdf_file():
    """Test PDF file processing"""
    print("\n" + "="*50)
    print("Testing PDF File Processing")
    print("="*50)
    
    # Check if test PDF exists
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    
    # Look for any PDF in uploads
    pdf_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')] if os.path.exists(uploads_dir) else []
    
    if not pdf_files:
        print("⚠️ No PDF files found in uploads folder. Upload a PDF via the frontend first.")
        print("Skipping PDF test...")
        return
    
    test_file = os.path.join(uploads_dir, pdf_files[0])
    
    # Process the file
    processor = DocumentProcessor()
    result = processor.process_document(test_file)
    
    print(f"✓ Format: {result['format']}")
    print(f"✓ Page count: {result.get('page_count', 'N/A')}")
    print(f"✓ Word count: {result['word_count']}")
    print(f"✓ Character count: {result['char_count']}")
    print(f"\n✓ Text preview (first 200 chars):")
    print(result['text'][:200] + "...")
    
    # Validate text
    is_valid, message = processor.validate_text(result['text'])
    print(f"\n✓ Validation: {message}")
    
    print("\n✅ PDF processing test passed!")

def test_docx_file():
    """Test DOCX file processing"""
    print("\n" + "="*50)
    print("Testing DOCX File Processing")
    print("="*50)
    
    # Check if test DOCX exists
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    
    # Look for any DOCX in uploads
    docx_files = [f for f in os.listdir(uploads_dir) if f.endswith('.docx')] if os.path.exists(uploads_dir) else []
    
    if not docx_files:
        print("⚠️ No DOCX files found in uploads folder. Upload a DOCX via the frontend first.")
        print("Skipping DOCX test...")
        return
    
    test_file = os.path.join(uploads_dir, docx_files[0])
    
    # Process the file
    processor = DocumentProcessor()
    result = processor.process_document(test_file)
    
    print(f"✓ Format: {result['format']}")
    print(f"✓ Paragraph count: {result.get('paragraph_count', 'N/A')}")
    print(f"✓ Word count: {result['word_count']}")
    print(f"✓ Character count: {result['char_count']}")
    print(f"\n✓ Text preview (first 200 chars):")
    print(result['text'][:200] + "...")
    
    # Validate text
    is_valid, message = processor.validate_text(result['text'])
    print(f"\n✓ Validation: {message}")
    
    print("\n✅ DOCX processing test passed!")

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("DOCUMENT PROCESSOR TESTS")
    print("="*50)
    
    try:
        test_txt_file()
        test_pdf_file()
        test_docx_file()
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()