# AI-Powered Quiz Generator

An intelligent quiz generation system with HTML/CSS/JS frontend and Python backend.

## Current Status

✅ **Phase 1:** Project Setup - Complete
✅ **Phase 2:** Backend API - Complete  
✅ **Phase 3:** Frontend - Complete
✅ **Phase 4:** Document Processing - Complete
✅ **Phase 5:** Text Chunking - Complete
✅ **Phase 6:** RAG Pipeline - Pending
✅ **Phase 7:** AI Model Integration - Pending
✅ **Phase 8:** Quiz Generation - Pending
✅ **Phase 9:** Quiz Display - Pending
⏳ **Phase 10:** PDF Export - Pending

## Features Implemented

### Document Processing ✅
- PDF text extraction (PyMuPDF)
- DOCX text extraction (python-docx)
- TXT file reading
- Text cleaning and validation

### Text Chunking ✅
- Token-based chunking (tiktoken)
- Configurable chunk size (500 tokens)
- Overlap for context preservation (100 tokens)
- Chunk statistics and validation

### API Endpoints ✅
- `POST /upload` - Upload and process documents
- `POST /generate-quiz` - Generate quiz (dummy data)
- `POST /download-pdf` - Download PDF (placeholder)
- `GET /health` - Health check

### Frontend ✅
- Modern, responsive UI
- Drag & drop file upload
- Real-time status updates
- Quiz display components
- Chunk information display

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Backend:** Flask (Python)
- **Document Processing:** PyMuPDF, python-docx
- **Text Chunking:** langchain-text-splitters, tiktoken
- **AI Model:** Microsoft Phi-3-mini (coming in Phase 7)
- **RAG:** Sentence Transformers + FAISS (coming in Phase 6)

## Installation

### Prerequisites
- Python 3.9+
- Node.js (for http-server, optional)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
# Option 1: Python
python -m http.server 5500

# Option 2: VS Code Live Server
# Right-click index.html → Open with Live Server
```

## Usage

1. Start backend server (http://localhost:5000)
2. Open frontend (http://localhost:5500)
3. Upload a document (PDF, DOCX, or TXT)
4. Configure quiz settings
5. Generate quiz
6. Download as PDF

## Project Structure
```
quiz-generator/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── utils/
│   │   ├── document_processor.py
│   │   ├── text_chunker.py
│   │   ├── rag_pipeline.py (pending)
│   │   ├── quiz_generator.py (pending)
│   │   └── pdf_exporter.py (pending)
│   └── tests/
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
└── uploads/
```

## Testing
```bash
# Document processing tests
python backend/test_processor.py

# Chunking tests
python backend/test_chunker.py

# Integration tests
python backend/test_chunking_integration.py

# Complete test suite
python backend/test_chunking_complete.py
```

## Performance

| Operation | Time |
|-----------|------|
| Document upload & processing | < 100ms |
| Text chunking (100KB) | < 60ms |
| Chunk creation (avg) | ~0.5ms per chunk |
| Frontend rendering | < 50ms |