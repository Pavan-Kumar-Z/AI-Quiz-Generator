// ============================================
// Main Application Logic
// ============================================

// Application state
const AppState = {
    uploadedFile: null,
    uploadedFileData: null,
    quizData: null,
    answersVisible: false
};

// DOM Elements
const elements = {
    fileInput: document.getElementById('fileInput'),
    uploadArea: document.getElementById('uploadArea'),
    browseBtn: document.getElementById('browseBtn'),
    removeFileBtn: document.getElementById('removeFile'),
    generateBtn: document.getElementById('generateBtn'),
    downloadBtn: document.getElementById('downloadBtn'),
    toggleAnswersBtn: document.getElementById('toggleAnswersBtn'),
    statusClose: document.getElementById('statusClose'),
    instructionsToggle: document.getElementById('instructionsToggle'),
    instructionsContent: document.getElementById('instructionsContent'),
    numQuestions: document.getElementById('numQuestions'),
    numQuestionsValue: document.getElementById('numQuestionsValue')
};

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎓 AI Quiz Generator initialized');
    
    initializeEventListeners();
    checkBackendHealth();
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // File upload events
    elements.browseBtn.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);
    elements.removeFileBtn.addEventListener('click', removeFile);

    // Drag and drop events
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);

    // Button events
    elements.generateBtn.addEventListener('click', generateQuiz);
    elements.downloadBtn.addEventListener('click', downloadPDF);
    elements.toggleAnswersBtn.addEventListener('click', toggleAnswers);

    // UI events
    elements.statusClose.addEventListener('click', () => UI.hideStatus());
    elements.instructionsToggle.addEventListener('click', toggleInstructions);

    // Slider update
    elements.numQuestions.addEventListener('input', (e) => {
        elements.numQuestionsValue.textContent = e.target.value;
    });
}

/**
 * Check if backend is running
 */
async function checkBackendHealth() {
    try {
        await API.checkHealth();
        console.log('✅ Backend is connected');
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        UI.showStatus('Cannot connect to backend server. Please ensure it is running on http://localhost:5000', 'error');
    }
}

// ============================================
// FILE UPLOAD HANDLERS
// ============================================

/**
 * Handle file selection from input
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

/**
 * Handle drag over event
 */
function handleDragOver(event) {
    event.preventDefault();
    elements.uploadArea.classList.add('dragover');
}

/**
 * Handle drag leave event
 */
function handleDragLeave(event) {
    event.preventDefault();
    elements.uploadArea.classList.remove('dragover');
}

/**
 * Handle file drop
 */
function handleDrop(event) {
    event.preventDefault();
    elements.uploadArea.classList.remove('dragover');

    const file = event.dataTransfer.files[0];
    if (file) {
        processFile(file);
    }
}

/**
 * Process and validate uploaded file
 */
async function processFile(file) {
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const allowedExtensions = ['.pdf', '.docx', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        UI.showStatus('Invalid file type. Please upload PDF, DOCX, or TXT files only.', 'error');
        return;
    }

    // Validate file size (10 MB)
    const maxSize = 10 * 1024 * 1024; // 10 MB in bytes
    if (file.size > maxSize) {
        UI.showStatus('File is too large. Maximum size is 10 MB.', 'error');
        return;
    }

    // Store file
    AppState.uploadedFile = file;

    // Show file info
    UI.showFileInfo({
        name: file.name,
        sizeText: UI.formatFileSize(file.size)
    });

    // Upload file to backend
    await uploadFile(file);
}

/**
 * Upload file to backend
 */
async function uploadFile(file) {
    try {
        UI.showStatus('Uploading file...', 'info');

        const response = await API.uploadFile(file);

        if (response.success) {
            AppState.uploadedFileData = response.data;
            UI.showStatus('File uploaded successfully!', 'success');
            UI.setGenerateButton(true);
            
            console.log('Upload response:', response);
            
            // Display chunk information if available
            if (response.data.chunking) {
                const chunkInfo = response.data.chunking;
                console.log(`📊 Document chunked into ${chunkInfo.total_chunks} chunks`);
                console.log(`📊 Total tokens: ${chunkInfo.total_tokens}`);
                console.log(`📊 Average tokens per chunk: ${chunkInfo.avg_tokens_per_chunk}`);
            }
        }
    } catch (error) {
        UI.showStatus(error.message || 'Failed to upload file', 'error');
        removeFile();
    }
}

/**
 * Remove uploaded file
 */
function removeFile() {
    // Reset state
    AppState.uploadedFile = null;
    AppState.uploadedFileData = null;
    AppState.quizData = null;

    // Reset UI
    elements.fileInput.value = '';
    UI.hideFileInfo();
    UI.setGenerateButton(false);
    UI.hideResults();
    
    console.log('File removed');
}

// ============================================
// QUIZ GENERATION
// ============================================

/**
 * Generate quiz from uploaded document
 */
async function generateQuiz() {
    if (!AppState.uploadedFileData) {
        UI.showStatus('Please upload a file first', 'warning');
        return;
    }

    // Get settings
    const quizMode = document.querySelector('input[name="quizMode"]:checked').value;
    const numQuestions = parseInt(elements.numQuestions.value);
    const difficulty = document.getElementById('difficulty').value;

    const params = {
        filename: AppState.uploadedFileData.saved_as,
        quiz_mode: quizMode,
        num_questions: numQuestions,
        difficulty: difficulty
    };

    console.log('Generating quiz with params:', params);

    try {
        // Show progress
        UI.hideResults();
        UI.showProgress();

        // Simulate progress steps
        await simulateProgress();

        // Call API
        const response = await API.generateQuiz(params);

        if (response.success) {
            AppState.quizData = response.data;
            
            // Hide progress
            UI.hideProgress();

            // Render quiz based on mode
            if (quizMode === 'mcq') {
                UI.renderMCQ(response.data.questions);
            } else {
                UI.renderQA(response.data.questions);
            }

            // Show results
            UI.showResults();
            UI.showStatus('Quiz generated successfully!', 'success');

            console.log('Quiz data:', response.data);
        }
    } catch (error) {
        UI.hideProgress();
        UI.showStatus(error.message || 'Failed to generate quiz', 'error');
    }
}

/**
 * Simulate progress steps
 */
async function simulateProgress() {
    const steps = [
        { percent: 20, message: '📄 Extracting text from document...' },
        { percent: 40, message: '✂️ Chunking document...' },
        { percent: 60, message: '🔍 Creating embeddings...' },
        { percent: 80, message: '🤖 Generating questions...' },
        { percent: 100, message: '✅ Finalizing quiz...' }
    ];

    for (const step of steps) {
        UI.updateProgress(step.percent, step.message);
        await sleep(800); // Wait 800ms between steps
    }
}

/**
 * Sleep utility function
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================
// QUIZ DISPLAY
// ============================================

/**
 * Toggle answer visibility
 */
function toggleAnswers() {
    AppState.answersVisible = !AppState.answersVisible;
    UI.toggleAnswers(AppState.answersVisible);
}

// ============================================
// PDF DOWNLOAD
// ============================================

/**
 * Download quiz as PDF
 */
async function downloadPDF() {
    if (!AppState.quizData) {
        UI.showStatus('No quiz to download', 'warning');
        return;
    }

    try {
        UI.showStatus('Preparing PDF download...', 'info');

        const response = await API.downloadPDF(AppState.quizData);

        if (response.success) {
            UI.showStatus(response.message, 'info');
            console.log('PDF download response:', response);
            
            // Note: Actual PDF download will be implemented in Phase 10
            UI.showStatus('PDF generation feature will be available in Phase 10', 'info');
        }
    } catch (error) {
        UI.showStatus(error.message || 'Failed to download PDF', 'error');
    }
}

// ============================================
// UI INTERACTIONS
// ============================================

/**
 * Toggle instructions visibility
 */
function toggleInstructions() {
    const content = elements.instructionsContent;
    const toggle = elements.instructionsToggle;

    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        content.classList.add('show');
        toggle.classList.add('active');
    } else {
        content.classList.add('hidden');
        content.classList.remove('show');
        toggle.classList.remove('active');
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Get current quiz settings
 */
function getQuizSettings() {
    return {
        mode: document.querySelector('input[name="quizMode"]:checked').value,
        numQuestions: parseInt(elements.numQuestions.value),
        difficulty: document.getElementById('difficulty').value
    };
}

/**
 * Log application state (for debugging)
 */
function logState() {
    console.log('Current App State:', AppState);
}

// Expose logState for debugging in console
window.logState = logState;

// ============================================
// ERROR HANDLING
// ============================================

window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

console.log('✅ Main.js loaded successfully');