from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, origins=Config.CORS_ORIGINS)

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file types
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Helper function to get file size
def get_file_size(file):
    """Get file size in bytes"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset file pointer
    return size


# ============== ROUTES ==============

@app.route('/')
def home():
    """Home endpoint - API information"""
    return jsonify({
        "message": "AI Quiz Generator API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/upload (POST)",
            "generate": "/generate-quiz (POST)",
            "download": "/download-pdf (GET)"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload and process document
    
    Expected form data:
        - file: The document file (PDF, DOCX, or TXT)
    
    Returns:
        JSON with file info and extracted text preview
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file provided"
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": f"Invalid file type. Allowed types: {', '.join(Config.ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Check file size
        file_size = get_file_size(file)
        if file_size > Config.MAX_FILE_SIZE:
            return jsonify({
                "success": False,
                "error": f"File too large. Maximum size: {Config.MAX_FILE_SIZE / (1024*1024):.0f} MB"
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # TODO: Extract text from document (Phase 4)
        # For now, return dummy data
        extracted_text = "Document text will be extracted here..."
        
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "data": {
                "filename": filename,
                "saved_as": unique_filename,
                "size": file_size,
                "size_mb": round(file_size / (1024*1024), 2),
                "type": filename.rsplit('.', 1)[1].lower(),
                "upload_time": timestamp,
                "text_preview": extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text,
                "text_length": len(extracted_text)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    """
    Generate quiz from uploaded document
    
    Expected JSON data:
        - filename: Name of uploaded file
        - quiz_mode: "mcq" or "qa"
        - num_questions: Number of questions (5-20)
        - difficulty: "easy", "medium", or "hard"
    
    Returns:
        JSON with generated quiz
    """
    try:
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        filename = data.get('filename')
        quiz_mode = data.get('quiz_mode', 'mcq')
        num_questions = data.get('num_questions', Config.DEFAULT_QUESTIONS)
        difficulty = data.get('difficulty', 'medium')
        
        # Validate inputs
        if not filename:
            return jsonify({
                "success": False,
                "error": "Filename is required"
            }), 400
        
        if num_questions < Config.MIN_QUESTIONS or num_questions > Config.MAX_QUESTIONS:
            return jsonify({
                "success": False,
                "error": f"Number of questions must be between {Config.MIN_QUESTIONS} and {Config.MAX_QUESTIONS}"
            }), 400
        
        if quiz_mode not in ['mcq', 'qa']:
            return jsonify({
                "success": False,
                "error": "Quiz mode must be 'mcq' or 'qa'"
            }), 400
        
        # TODO: Generate quiz using AI (Phase 8)
        # For now, return dummy quiz data
        
        if quiz_mode == 'mcq':
            quiz_data = generate_dummy_mcq(num_questions)
        else:
            quiz_data = generate_dummy_qa(num_questions)
        
        return jsonify({
            "success": True,
            "message": "Quiz generated successfully",
            "data": {
                "quiz_mode": quiz_mode,
                "num_questions": num_questions,
                "difficulty": difficulty,
                "questions": quiz_data,
                "generated_at": datetime.now().isoformat()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    """
    Generate and download quiz as PDF
    
    Expected JSON data:
        - quiz_data: The quiz data to convert to PDF
    
    Returns:
        PDF file
    """
    try:
        # Get quiz data
        data = request.get_json()
        
        if not data or 'quiz_data' not in data:
            return jsonify({
                "success": False,
                "error": "No quiz data provided"
            }), 400
        
        quiz_data = data.get('quiz_data')
        
        # TODO: Generate PDF (Phase 10)
        # For now, return a message
        
        return jsonify({
            "success": True,
            "message": "PDF generation will be implemented in Phase 10",
            "data": {
                "note": "This endpoint will return a PDF file"
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


# ============== HELPER FUNCTIONS ==============

def generate_dummy_mcq(num_questions):
    """Generate dummy MCQ data for testing"""
    questions = []
    for i in range(num_questions):
        questions.append({
            "question_number": i + 1,
            "question": f"Sample MCQ Question {i + 1}?",
            "options": {
                "A": f"Option A for question {i + 1}",
                "B": f"Option B for question {i + 1}",
                "C": f"Option C for question {i + 1}",
                "D": f"Option D for question {i + 1}"
            },
            "correct_answer": "B",
            "explanation": f"This is a sample explanation for question {i + 1}"
        })
    return questions


def generate_dummy_qa(num_questions):
    """Generate dummy Q&A data for testing"""
    questions = []
    for i in range(num_questions):
        questions.append({
            "question_number": i + 1,
            "question": f"Sample Q&A Question {i + 1}?",
            "answer": f"This is a detailed answer to question {i + 1}. It provides comprehensive information about the topic."
        })
    return questions


# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ============== RUN SERVER ==============

if __name__ == '__main__':
    print("=" * 50)
    print("AI Quiz Generator API Server")
    print("=" * 50)
    print(f"Server running on: http://localhost:5000")
    print(f"Upload folder: {Config.UPLOAD_FOLDER}")
    print(f"Max file size: {Config.MAX_FILE_SIZE / (1024*1024):.0f} MB")
    print(f"Allowed extensions: {', '.join(Config.ALLOWED_EXTENSIONS)}")
    print("=" * 50)
    
    app.run(debug=True, port=5000, host='0.0.0.0')