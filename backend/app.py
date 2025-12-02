from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from config import Config
from utils.document_processor import DocumentProcessor
chunks_storage = {}
# Add these imports at the top
from utils.rag_pipeline import RAGPipeline
import threading

# Add global variables for model caching (after chunks_storage)
_rag_pipeline = None
_rag_lock = threading.Lock()

def get_rag_pipeline():
    """
    Get or create RAG pipeline (singleton pattern with thread safety)
    
    Returns:
        RAGPipeline: Cached RAG pipeline instance
    """
    global _rag_pipeline
    
    with _rag_lock:
        if _rag_pipeline is None:
            print("🔄 Initializing RAG pipeline...")
            _rag_pipeline = RAGPipeline(model_name='all-MiniLM-L6-v2')
            _rag_pipeline.load_model()
            print("✅ RAG pipeline initialized and cached")
        else:
            print("♻️  Using cached RAG pipeline")
    
    return _rag_pipeline


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
        
        # Extract text from document
        
        # Extract text and create chunks
        
        processor = DocumentProcessor()
        
        # Process document and chunk it
        processing_result = processor.process_and_chunk(
            filepath,
            chunk_size=500,
            chunk_overlap=100
        )
        
        extraction_result = processing_result['extraction']
        chunks = processing_result['chunks']
        chunk_stats = processing_result['chunk_stats']
        
        # Validate extracted text
        is_valid, validation_message = processor.validate_text(extraction_result['text'])
        
        if not is_valid:
            # Remove invalid file
            os.remove(filepath)
            return jsonify({
                "success": False,
                "error": validation_message
            }), 400
        
        # Validate chunks
        if not processing_result['chunks_valid']:
            os.remove(filepath)
            return jsonify({
                "success": False,
                "error": f"Chunking failed: {processing_result['validation_message']}"
            }), 400
        
        extracted_text = extraction_result['text']
        text_preview = processor.get_text_preview(extracted_text, 300)

   
        # Generate embeddings and create RAG index
        try:
            print(f"🔍 Creating RAG index for {unique_filename}...")
            rag_pipeline = get_rag_pipeline()
            
            # Build index for this document's chunks
            rag_pipeline.build_index(chunks)
            
            # Get RAG stats
            rag_stats = rag_pipeline.get_stats()
            
            print(f"✅ RAG index created: {rag_stats['index_size']} vectors")
            
        except Exception as e:
            print(f"⚠️  RAG indexing failed: {str(e)}")
            # Continue without RAG (graceful degradation)
            rag_stats = None
        
        # Store chunks, embeddings, and RAG pipeline for later use
        chunks_storage[unique_filename] = {
            'chunks': chunks,
            'extraction_result': extraction_result,
            'timestamp': timestamp,
            'rag_pipeline': rag_pipeline if rag_stats else None
        }

        
        
        return jsonify({
            "success": True,
            "message": "File uploaded, processed, and chunked successfully",
            "data": {
                "filename": filename,
                "saved_as": unique_filename,
                "size": file_size,
                "size_mb": round(file_size / (1024*1024), 2),
                "type": filename.rsplit('.', 1)[1].lower(),
                "upload_time": timestamp,
                "text_preview": text_preview,
                "text_length": len(extracted_text),
                "word_count": extraction_result['word_count'],
                "metadata": {
                    "format": extraction_result['format'],
                    "page_count": extraction_result.get('page_count'),
                    "paragraph_count": extraction_result.get('paragraph_count'),
                    "line_count": extraction_result.get('line_count')
                },
                "chunking": {
                    "total_chunks": chunk_stats['total_chunks'],
                    "total_tokens": chunk_stats['total_tokens'],
                    "avg_tokens_per_chunk": chunk_stats['avg_tokens_per_chunk'],
                    "chunk_size_config": 500,
                    "chunk_overlap_config": 100
                },
                "rag": {
                    "embeddings_generated": rag_stats is not None,
                    "index_size": rag_stats['index_size'] if rag_stats else 0,
                    "embedding_dimension": rag_stats['embedding_dimension'] if rag_stats else 0,
                    "model_name": rag_stats['model_name'] if rag_stats else None
                } if rag_stats else {
                    "embeddings_generated": False,
                    "error": "RAG indexing was skipped"
                }
            }
        }), 200
    
    except Exception as e:
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500
    

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data"}), 400

        filename = data.get('filename')
        quiz_mode = data.get('quiz_mode', 'mcq').lower()
        num_questions = int(data.get('num_questions', 5))
        difficulty = data.get('difficulty', 'medium').lower()

        if not filename or filename not in chunks_storage:
            return jsonify({"success": False, "error": "File not found"}), 404

        if quiz_mode not in ['mcq', 'qa']:
            return jsonify({"success": False, "error": "quiz_mode must be 'mcq' or 'qa'"}), 400

        if not 1 <= num_questions <= 20:
            return jsonify({"success": False, "error": "num_questions must be 1-20"}), 400

        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'

        stored_data = chunks_storage[filename]
        rag_pipeline = stored_data.get('rag_pipeline')
        if not rag_pipeline:
            return jsonify({"success": False, "error": "No RAG index"}), 500

        from utils.quiz_generator import QuizGenerator
        generator = QuizGenerator()

        if not generator.test_connection():
            return jsonify({"success": False, "error": "Llama server not running"}), 503

        # Get rich context
        query = "important concepts definitions facts examples"
        context = rag_pipeline.retrieve_context(query, k=10, max_tokens=4000)

        result = generator.generate_quiz(
            context=context,
            quiz_mode=quiz_mode,
            num_questions=num_questions,
            difficulty=difficulty
        )

        return jsonify({
            "success": True,
            "message": f"Generated {len(result['questions'])} questions",
            "data": {
                "quiz_mode": quiz_mode,
                "num_questions": len(result['questions']),
                "difficulty": difficulty,
                "questions": result['questions'],
                "generated_at": datetime.now().isoformat()
            }
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": f"Failed: {str(e)}"}), 500



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


@app.route('/test-rag', methods=['POST'])
def test_rag():
    """
    Test RAG retrieval with a query
    
    Expected JSON data:
        - filename: Name of uploaded file
        - query: Search query
        - k: Number of chunks to retrieve (optional, default 5)
    
    Returns:
        JSON with retrieved chunks
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        filename = data.get('filename')
        query = data.get('query')
        k = data.get('k', 5)
        
        # Validate inputs
        if not filename or not query:
            return jsonify({
                "success": False,
                "error": "Both filename and query are required"
            }), 400
        
        # Check if file exists in storage
        if filename not in chunks_storage:
            return jsonify({
                "success": False,
                "error": "File not found in storage. Please upload first."
            }), 404
        
        # Get RAG pipeline for this file
        stored_data = chunks_storage[filename]
        rag_pipeline = stored_data.get('rag_pipeline')
        
        if not rag_pipeline:
            return jsonify({
                "success": False,
                "error": "RAG pipeline not available for this file"
            }), 400
        
        # Retrieve relevant chunks
        results = rag_pipeline.retrieve(query, k=k)
        
        # Format results for response
        formatted_results = []
        for result in results:
            formatted_results.append({
                'chunk_id': result['chunk_id'],
                'text': result['text'],
                'text_preview': result['text'][:200] + '...' if len(result['text']) > 200 else result['text'],
                'token_count': result['token_count'],
                'retrieval_score': result['retrieval_score'],
                'distance': result['distance'],
                'rank': result['rank']
            })
        
        return jsonify({
            "success": True,
            "message": f"Retrieved {len(formatted_results)} chunks",
            "data": {
                "query": query,
                "k_requested": k,
                "k_returned": len(formatted_results),
                "results": formatted_results
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

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
    
    # Pre-load RAG model to cache it
    print("\n🚀 Pre-loading RAG model...")
    try:
        pipeline = get_rag_pipeline()
        print(f"✅ Model pre-loaded: {pipeline.model_name}")
        print(f"   Device: {pipeline.model.device}")
    except Exception as e:
        print(f"⚠️  Model pre-loading failed: {str(e)}")
        print("   Model will be loaded on first request")
    
    print("\n" + "=" * 50)
    print("🎉 Server ready!")
    print("=" * 50 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')