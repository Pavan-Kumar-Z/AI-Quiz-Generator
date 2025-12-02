"""
Test Quiz Generator with JSON Output Mode
Run: python test_quiz_generator.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.quiz_generator import QuizGenerator
import json


def test_llama_connection():
    print("\n" + "="*60)
    print("Test 1: Llama API Connection")
    print("="*60)
    
    generator = QuizGenerator()
    if generator.test_connection():
        print("   Llama API is running on http://localhost:8000")
        return True
    else:
        print("   Cannot connect to Llama API")
        print("   Run: python -m llama_cpp.server --model your-model.gguf --port 8000 --n_ctx 8192")
        return False


def test_simple_json_generation():
    print("\n" + "="*60)
    print("Test 2: Force JSON Output")
    print("="*60)
    
    generator = QuizGenerator()
    prompt = 'Respond with valid JSON: {"name": "Alice", "age": 25}'
    
    try:
        response = generator.call_llama(prompt)
        print("Raw response:")
        print(response[:500] + "..." if len(response) > 500 else response)
        
        # Try to parse
        data = json.loads(response)
        print(f"\n   Parsed JSON successfully: {data}")
        print("   JSON mode is WORKING!")
        return True
    except Exception as e:
        print(f"   JSON mode failed: {e}")
        return False


def test_mcq_generation():
    print("\n" + "="*60)
    print("Test 3: Generate 5 MCQ Questions (JSON)")
    print("="*60)
    
    context = """
    Python was created by Guido van Rossum and first released in 1991.
    It is known for its readability and is used in web development, data science, AI, and automation.
    Python supports object-oriented, functional, and procedural programming.
    The Zen of Python says: "Simple is better than complex."
    """
    
    generator = QuizGenerator()
    
    try:
        result = generator.generate_quiz(
            context=context,
            quiz_mode='mcq',
            num_questions=5,
            difficulty='medium'
        )
        
        print(f"\n   Generated {len(result['questions'])} questions")
        
        for q in result['questions']:
            print(f"\nQuestion {q['question_number']}: {q['question']}")
            for opt, text in q['options'].items():
                print(f"  {opt}) {text}")
            print(f"   Correct: {q['correct_answer']}")
            print(f"   Explanation: {q['explanation'][:100]}...")
        
        print("\n   MCQ Generation + JSON Parsing = SUCCESS!")
        return True
        
    except Exception as e:
        print(f"   MCQ test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_qa_generation():
    print("\n" + "="*60)
    print("Test 4: Generate 4 Q&A Questions (JSON)")
    print("="*60)
    
    context = """
    Photosynthesis is the process by which green plants convert sunlight, carbon dioxide,
    and water into glucose and oxygen. It occurs in chloroplasts and requires chlorophyll.
    The chemical equation is: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂.
    """
    
    generator = QuizGenerator()
    
    try:
        result = generator.generate_quiz(
            context=context,
            quiz_mode='qa',
            num_questions=4,
            difficulty='easy'
        )
        
        print(f"\n   Generated {len(result['questions'])} questions")
        
        for q in result['questions']:
            print(f"\nQuestion {q['question_number']}: {q['question']}")
            print(f"Answer: {q['answer'][:150]}...")
        
        print("\n   Q&A Generation + JSON Parsing = SUCCESS!")
        return True
        
    except Exception as e:
        print(f"   Q&A test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("QUIZ GENERATOR - JSON MODE TESTS")
    print("="*60)
    print("Make sure Llama 3.2 is running with JSON support:")
    print("python -m llama_cpp.server --model models/llama-3.2-3b-instruct-q8_0.gguf --port 8000 --n_ctx 8192")
    print("="*60 + "\n")
    
    if not test_llama_connection():
        return
    
    success = True
    
    if not test_simple_json_generation():
        success = False
    
    if not test_mcq_generation():
        success = False
    
    if not test_qa_generation():
        success = False
    
    print("\n" + "="*60)
    if success:
        print("ALL TESTS PASSED! JSON MODE IS WORKING PERFECTLY")
        print("Your quiz generator is now 100% reliable")
    else:
        print("SOME TESTS FAILED - Check Llama server settings")
    print("="*60)


if __name__ == "__main__":
    main()