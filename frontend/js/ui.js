// ============================================
// UI Utilities Module
// Handles UI updates and interactions
// ============================================

const UI = {
    /**
     * Show status banner
     * @param {string} message - The message to display
     * @param {string} type - Banner type: success, error, warning, info
     */
    showStatus(message, type = 'info') {
        const banner = document.getElementById('statusBanner');
        const icon = document.getElementById('statusIcon');
        const messageEl = document.getElementById('statusMessage');

        // Set icon based on type
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        icon.textContent = icons[type] || icons.info;
        messageEl.textContent = message;

        // Remove all type classes
        banner.classList.remove('success', 'error', 'warning', 'info');
        // Add new type class
        banner.classList.add(type);
        // Show banner
        banner.classList.remove('hidden');

        // Auto-hide after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(() => this.hideStatus(), 5000);
        }
    },

    /**
     * Hide status banner
     */
    hideStatus() {
        const banner = document.getElementById('statusBanner');
        banner.classList.add('hidden');
    },

    /**
     * Show file info
     * @param {Object} fileData - File information
     */
    showFileInfo(fileData) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');

        fileName.textContent = fileData.name;
        fileSize.textContent = fileData.sizeText;

        fileInfo.classList.remove('hidden');
    },

    /**
     * Hide file info
     */
    hideFileInfo() {
        const fileInfo = document.getElementById('fileInfo');
        fileInfo.classList.add('hidden');
    },

    /**
     * Update progress bar
     * @param {number} percent - Progress percentage (0-100)
     * @param {string} message - Progress message
     */
    updateProgress(percent, message) {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');

        progressFill.style.width = `${percent}%`;
        progressText.textContent = message;
    },

    /**
     * Show progress section
     */
    showProgress() {
        const progressSection = document.getElementById('progressSection');
        progressSection.classList.remove('hidden');
        this.updateProgress(0, 'Initializing...');
    },

    /**
     * Hide progress section
     */
    hideProgress() {
        const progressSection = document.getElementById('progressSection');
        progressSection.classList.add('hidden');
    },

    /**
     * Enable/disable generate button
     * @param {boolean} enabled - Whether button should be enabled
     */
    setGenerateButton(enabled) {
        const generateBtn = document.getElementById('generateBtn');
        const generateNote = document.getElementById('generateNote');

        generateBtn.disabled = !enabled;

        if (enabled) {
            generateNote.textContent = 'Ready to generate quiz';
            generateNote.style.color = 'var(--success-color)';
        } else {
            generateNote.textContent = 'Upload a document to begin';
            generateNote.style.color = 'var(--gray-500)';
        }
    },

    /**
     * Render MCQ quiz
     * @param {Array} questions - Array of MCQ questions
     */
    renderMCQ(questions) {
        const quizContent = document.getElementById('quizContent');
        quizContent.innerHTML = '';

        questions.forEach(q => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'quiz-question';

            questionDiv.innerHTML = `
                <div class="question-header">
                    <div class="question-number">${q.question_number}</div>
                    <div class="question-text">${q.question}</div>
                </div>
                <div class="quiz-options">
                    ${Object.entries(q.options).map(([letter, text]) => `
                        <div class="quiz-option ${letter === q.correct_answer ? 'correct answer-hidden' : ''}">
                            <div class="option-letter">${letter}</div>
                            <div class="option-text">${text}</div>
                        </div>
                    `).join('')}
                </div>
                <div class="correct-answer answer-hidden">
                    <span class="correct-answer-icon">✓</span>
                    <span>Correct Answer: ${q.correct_answer}</span>
                </div>
                ${q.explanation ? `
                    <div class="answer-explanation answer-hidden">
                        <span class="explanation-label">Explanation:</span>
                        <span class="explanation-text">${q.explanation}</span>
                    </div>
                ` : ''}
            `;

            quizContent.appendChild(questionDiv);
        });
    },

    /**
     * Render Q&A quiz
     * @param {Array} questions - Array of Q&A questions
     */
    renderQA(questions) {
        const quizContent = document.getElementById('quizContent');
        quizContent.innerHTML = '';

        questions.forEach(q => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'quiz-question';

            questionDiv.innerHTML = `
                <div class="question-header">
                    <div class="question-number">${q.question_number}</div>
                    <div class="question-text">${q.question}</div>
                </div>
                <div class="quiz-answer answer-hidden">
                    <div class="answer-label">
                        <span>💡</span>
                        <span>Answer:</span>
                    </div>
                    <div class="answer-text">${q.answer}</div>
                </div>
            `;

            quizContent.appendChild(questionDiv);
        });
    },

    /**
     * Show quiz results
     */
    showResults() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.remove('hidden');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },

    /**
     * Hide quiz results
     */
    hideResults() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.add('hidden');
    },

    /**
     * Toggle answer visibility
     * @param {boolean} show - Whether to show answers
     */
    toggleAnswers(show) {
        const answerElements = document.querySelectorAll('.answer-hidden');
        const toggleBtn = document.getElementById('toggleAnswersBtn');

        answerElements.forEach(el => {
            if (show) {
                el.classList.remove('answer-hidden');
            } else {
                el.classList.add('answer-hidden');
            }
        });

        if (toggleBtn) {
            toggleBtn.innerHTML = show
                ? '<span>🙈</span> Hide Answers'
                : '<span>👁️</span> Show Answers';
        }
    },

    /**
     * Format file size
     * @param {number} bytes - File size in bytes
     * @returns {string} Formatted size
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';

        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }
};