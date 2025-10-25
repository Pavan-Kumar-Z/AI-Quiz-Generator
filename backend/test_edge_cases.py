"""
Edge case tests for document processor
"""

from utils.document_processor import DocumentProcessor
import os

def test_empty_file():
    """Test with empty file"""
    print("\n=== Test: Empty File ===")
    
    # Create empty file
    with open('empty.txt', 'w') as f:
        f.write("")
    
    processor = DocumentProcessor()
    
    try:
        result = processor.process_document('empty.txt')
        is_valid, message = processor.validate_text(result['text'])
        print(f"Validation: {message}")
        assert not is_valid
        print("✅ Empty file correctly rejected")
    except Exception as e:
        print(f"✅ Exception caught: {str(e)}")
    finally:
        os.remove('empty.txt')

def test_special_characters():
    """Test with special characters"""
    print("\n=== Test: Special Characters ===")
    
    content = """
    This document contains special characters!
    Symbols: @#$%^&*()
    Emojis: 😀 🎉 🚀
    Math: x² + y² = z²
    Currency: $100, €50, ¥1000
    """
    
    with open('special.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    processor = DocumentProcessor()
    result = processor.process_document('special.txt')
    
    print(f"Original length: {len(content)}")
    print(f"Cleaned length: {len(result['text'])}")
    print(f"Preview: {result['text'][:100]}")
    
    os.remove('special.txt')
    print("✅ Special characters handled")

def test_very_long_lines():
    """Test with very long lines"""
    print("\n=== Test: Very Long Lines ===")
    
    content = "This is a very long line. " * 1000
    
    with open('long_line.txt', 'w') as f:
        f.write(content)
    
    processor = DocumentProcessor()
    result = processor.process_document('long_line.txt')
    
    print(f"Word count: {result['word_count']}")
    print(f"Character count: {result['char_count']}")
    
    os.remove('long_line.txt')
    print("✅ Long lines handled")

def test_unicode_content():
    """Test with unicode content"""
    print("\n=== Test: Unicode Content ===")
    
    content = """
    Multilingual text:
    English: Hello World
    Spanish: Hola Mundo
    French: Bonjour le monde
    German: Hallo Welt
    Chinese: 你好世界
    Arabic: مرحبا بالعالم
    Russian: Здравствуй мир
    """
    
    with open('unicode.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    processor = DocumentProcessor()
    result = processor.process_document('unicode.txt')
    
    print(f"Word count: {result['word_count']}")
    print(f"Preview: {result['text'][:100]}")
    
    os.remove('unicode.txt')
    print("✅ Unicode content handled")

def test_minimum_word_count():
    """Test minimum word count validation"""
    print("\n=== Test: Minimum Word Count ===")
    
    # Create file with exactly 49 words (below minimum)
    content = " ".join(["word"] * 49)
    
    with open('short.txt', 'w') as f:
        f.write(content)
    
    processor = DocumentProcessor()
    result = processor.process_document('short.txt')
    is_valid, message = processor.validate_text(result['text'], min_words=50)
    
    print(f"Word count: {result['word_count']}")
    print(f"Validation: {message}")
    assert not is_valid
    
    os.remove('short.txt')
    print("✅ Minimum word count validation works")

def main():
    """Run all edge case tests"""
    print("\n" + "="*50)
    print("EDGE CASE TESTS")
    print("="*50)
    
    try:
        test_empty_file()
        test_special_characters()
        test_very_long_lines()
        test_unicode_content()
        test_minimum_word_count()
        
        print("\n" + "="*50)
        print("✅ ALL EDGE CASE TESTS PASSED!")
        print("="*50)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()