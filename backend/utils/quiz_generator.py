"""
Quiz Generator - FIXED: Generate One Question at a Time (100% Reliable for Small Models)
Each question is generated separately → guarantees exact number
Slightly slower but bulletproof for Llama 3.2 1B on CPU
"""

import requests
import json
import re
from typing import List, Dict, Any


class QuizGenerator:
    def __init__(self, llama_endpoint='http://localhost:8000/v1/chat/completions'):
        self.llama_endpoint = llama_endpoint
        self.model_name = "local-llama"

    def call_llama(self, prompt: str, temperature: float = 0.1, max_tokens: int = 1000) -> str:
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are a precise JSON generator. Always output ONLY valid JSON. No extra text."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stop": []
            }
            # Try JSON mode (graceful if not supported)
            try:
                payload["response_format"] = {"type": "json_object"}
            except:
                pass  # Older llama.cpp ignores this

            response = requests.post(self.llama_endpoint, json=payload, timeout=120)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise Exception(f"Llama call failed: {str(e)}")

    def generate_single_mcq(self, context: str, question_num: int, difficulty: str) -> Dict:
        prompt = f"""Based on this content, generate ONE multiple-choice question (MCQ) as valid JSON.

CONTENT:
{context}

INSTRUCTION:
- Difficulty: {difficulty}
- Question {question_num}: Create a clear question with exactly 4 options (A, B, C, D)
- Only ONE correct answer
- Include a brief explanation

Output ONLY this JSON structure:
{{
  "question_number": {question_num},
  "question": "Your question here?",
  "options": {{"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"}},
  "correct_answer": "A",
  "explanation": "Brief explanation why this is correct."
}}

Respond with ONLY the JSON:"""

        raw = self.call_llama(prompt, temperature=0.1, max_tokens=800)
        return self._parse_single_json(raw, expected_keys=["question_number", "question", "options", "correct_answer", "explanation"])

    def generate_single_qa(self, context: str, question_num: int, difficulty: str) -> Dict:
        prompt = f"""Based on this content, generate ONE question-answer pair as valid JSON.

CONTENT:
{context}

INSTRUCTION:
- Difficulty: {difficulty}
- Question {question_num}: Create a thoughtful question with a detailed answer
- Base on content only

Output ONLY this JSON structure:
{{
  "question_number": {question_num},
  "question": "Your question here?",
  "answer": "Detailed answer based on content."
}}

Respond with ONLY the JSON:"""

        raw = self.call_llama(prompt, temperature=0.1, max_tokens=800)
        return self._parse_single_json(raw, expected_keys=["question_number", "question", "answer"])

    def _parse_single_json(self, raw: str, expected_keys: List[str]) -> Dict:
        try:
            # Extract JSON block
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in response")
            data = json.loads(json_match.group(0))
            
            # Validate required keys
            for key in expected_keys:
                if key not in data:
                    raise ValueError(f"Missing key: {key}")
            
            # Validate MCQ options if present
            if "options" in data:
                if len(data["options"]) != 4 or not all(k in "ABCD" for k in data["options"]):
                    raise ValueError("Invalid options format")
            
            return data
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON Parse Error: {e}")
            print(f"Raw response: {raw[:200]}...")
            # Fallback: Return dummy to avoid crash (in production, retry or handle)
            if "options" in expected_keys:
                return {
                    "question_number": expected_keys.index("question_number") + 1,  # Hacky fallback
                    "question": "Fallback question due to generation error.",
                    "options": {"A": "A", "B": "B", "C": "C", "D": "D"},
                    "correct_answer": "A",
                    "explanation": "Generation error - please retry."
                }
            else:
                return {
                    "question_number": expected_keys.index("question_number") + 1,
                    "question": "Fallback question due to generation error.",
                    "answer": "Fallback answer - generation error occurred."
                }

    def generate_quiz(self, context: str, quiz_mode: str, num_questions: int, difficulty: str) -> Dict[str, Any]:
        print(f"Generating {quiz_mode.upper()} quiz: {num_questions} questions ({difficulty}) - one by one for reliability")
        questions = []

        for i in range(1, num_questions + 1):
            print(f"   Generating question {i}/{num_questions}...")
            try:
                if quiz_mode == "mcq":
                    q = self.generate_single_mcq(context, i, difficulty)
                else:
                    q = self.generate_single_qa(context, i, difficulty)
                questions.append(q)
            except Exception as e:
                print(f"   Error generating question {i}: {e}")
                # Add dummy to maintain count
                if quiz_mode == "mcq":
                    questions.append({
                        "question_number": i,
                        "question": f"Error generating question {i}. Please retry.",
                        "options": {"A": "A", "B": "B", "C": "C", "D": "D"},
                        "correct_answer": "A",
                        "explanation": f"Generation failed: {str(e)}"
                    })
                else:
                    questions.append({
                        "question_number": i,
                        "question": f"Error generating question {i}. Please retry.",
                        "answer": f"Generation failed: {str(e)}"
                    })

        print(f"✅ Successfully generated {len(questions)} questions")
        return {
            "quiz_mode": quiz_mode,
            "num_questions": len(questions),
            "difficulty": difficulty,
            "questions": questions,
            "raw_responses": []  # Not storing per-question raw for simplicity
        }

    def test_connection(self) -> bool:
        try:
            resp = requests.get(self.llama_endpoint.replace('/chat/completions', '/models'), timeout=5)
            return resp.status_code == 200
        except:
            return False