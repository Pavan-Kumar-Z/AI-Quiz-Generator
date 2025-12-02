// ============================================
// UI Utilities Module - FIXED VERSION
// Fixes: (1) Answers no longer auto-show on MCQ click (toggle button works now)
//        (2) Removed A/B/C/D letters from MCQ options (cleaner look)
// Handles UI updates, rendering, and feedback
// ui.js
// ============================================

// Global state for quiz interactivity (shared across functions)
let userAnswers = {};  // e.g., {1: 'A', 2: 'B'} for MCQ
let currentQuestionIndex = 0;  // For navigation (future: add prev/next buttons)
let quizMode = 'mcq';  // Set dynamically

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

        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        icon.textContent = icons[type] || icons.info;
        messageEl.textContent = message;

        banner.classList.remove('success', 'error', 'warning', 'info');
        banner.classList.add(type);
        banner.classList.remove('hidden');

        if (type === 'success') {
            setTimeout(() => this.hideStatus(), 5000);
        }
    },

    hideStatus() {
        const banner = document.getElementById('statusBanner');
        banner.classList.add('hidden');
    },

    showFileInfo(fileData) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');

        fileName.textContent = fileData.name;
        fileSize.textContent = fileData.sizeText;

        fileInfo.classList.remove('hidden');
    },

    hideFileInfo() {
        const fileInfo = document.getElementById('fileInfo');
        fileInfo.classList.add('hidden');
    },

    updateProgress(percent, message) {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');

        progressFill.style.width = `${percent}%`;
        progressText.textContent = message;
    },

    showProgress() {
        const progressSection = document.getElementById('progressSection');
        progressSection.classList.remove('hidden');
        this.updateProgress(0, 'Initializing...');
    },

    hideProgress() {
        const progressSection = document.getElementById('progressSection');
        progressSection.classList.add('hidden');
    },

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
     * Render MCQ quiz - FIXED: No A/B/C/D letters, cleaner look
     * @param {Array} questions - Array of MCQ questions
     */
    renderMCQ(questions) {
        quizMode = 'mcq';
        userAnswers = {};  // Reset answers
        currentQuestionIndex = 0;
        this.updateQuizProgress(1, questions.length);

        const quizContent = document.getElementById('quizContent');
        quizContent.innerHTML = '';

        questions.forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = `quiz-question ${index === 0 ? 'active' : 'inactive'}`;  // Show first question
            questionDiv.dataset.questionIndex = index;

            questionDiv.innerHTML = `
                <div class="question-header">
                    <div class="question-number">Q${q.question_number}</div>
                    <div class="question-text">${q.question}</div>
                </div>
                <div class="quiz-options" data-question="${q.question_number}">
                    ${Object.entries(q.options).map(([letter, text]) => `
                        <label class="quiz-option" data-option="${letter}" data-correct="${letter === q.correct_answer}">
                            <input type="radio" name="option-${q.question_number}" value="${letter}" class="option-radio">
                            <div class="option-content">
                                <div class="option-text">${text}</div>  <!-- Removed option-letter div -->
                            </div>
                        </label>
                    `).join('')}
                </div>
                <div class="feedback hidden" data-question="${q.question_number}">
                    <div class="feedback-icon"></div>
                    <div class="feedback-message"></div>
                </div>
                <div class="correct-answer answer-hidden">
                    <span class="correct-answer-icon">✓</span>
                    <span>Correct Answer: ${q.correct_answer}) ${q.options[q.correct_answer]}</span>  <!-- Show full correct option text -->
                </div>
                ${q.explanation ? `
                    <div class="answer-explanation answer-hidden">
                        <span class="explanation-label">Explanation:</span>
                        <span class="explanation-text">${q.explanation}</span>
                    </div>
                ` : ''}
                <button class="btn btn-primary submit-btn hidden" data-question="${q.question_number}">Submit Answer</button>
            `;

            quizContent.appendChild(questionDiv);

            // Add event listener for this question's options
            const options = questionDiv.querySelectorAll('.quiz-option');
            options.forEach(option => {
                option.addEventListener('click', (e) => this.handleMCQClick(e, q));
            });

            // Submit button listener
            const submitBtn = questionDiv.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.addEventListener('click', (e) => this.handleMCQSubmit(e, q));
            }
        });

        // Show score display for MCQ
        document.getElementById('scoreDisplay').classList.remove('hidden');
    },

    /**
     * Handle MCQ option click - FIXED: No auto-reveal of answers (toggle controls it)
     * @param {Event} e - Click event
     * @param {Object} question - Question data
     */
    handleMCQClick(e, question) {
        const option = e.currentTarget;
        const selectedLetter = option.dataset.option;
        const isCorrect = option.dataset.correct === 'true';
        const questionNum = question.question_number;

        // Store user answer
        userAnswers[questionNum] = selectedLetter;

        // Visual feedback (highlight selected + correct/wrong, but DON'T auto-reveal explanations/answers)
        const optionsContainer = option.closest('.quiz-options');
        optionsContainer.querySelectorAll('.quiz-option').forEach(opt => opt.classList.remove('selected', 'correct', 'wrong'));

        option.classList.add('selected');
        if (isCorrect) {
            option.classList.add('correct');
            this.showFeedback(questionNum, 'Correct! Well done.', 'success');
        } else {
            option.classList.add('wrong');
            // Reveal correct option visually (but not full answer block)
            optionsContainer.querySelector(`[data-option="${question.correct_answer}"]`).classList.add('correct');
            this.showFeedback(questionNum, 'Incorrect. Try again!', 'error');
        }

        // REMOVED: this.toggleAnswerVisibility(true);  // Let toggle button control global answers

        // Update score and progress
        this.calculateAndUpdateScore();
        this.updateQuizProgress(Object.keys(userAnswers).length + 1, Object.keys(userAnswers).length);  // +1 for current
    },

    /**
     * Handle MCQ submit (if using per-question submit)
     * @param {Event} e - Click event
     * @param {Object} question - Question data
     */
    handleMCQSubmit(e, question) {
        // Trigger feedback on submit (similar to click)
        const selectedRadio = e.currentTarget.closest('.quiz-question').querySelector('input[type="radio"]:checked');
        if (selectedRadio) {
            selectedRadio.click();  // Simulate click for feedback
        }
    },

    /**
     * Show feedback for a question
     * @param {number} questionNum - Question number
     * @param {string} message - Feedback message
     * @param {string} type - success/error
     */
    showFeedback(questionNum, message, type) {
        const feedback = document.querySelector(`[data-question="${questionNum}"] .feedback`);
        if (feedback) {
            feedback.classList.remove('hidden');
            feedback.querySelector('.feedback-message').textContent = message;
            feedback.querySelector('.feedback-icon').textContent = type === 'success' ? '✅' : '❌';
        }
    },

    /**
     * Render Q&A quiz - INTERACTIVE VERSION
     * @param {Array} questions - Array of Q&A questions
     */
    renderQA(questions) {
        quizMode = 'qa';
        userAnswers = {};  // Reset (for future: store user text)
        currentQuestionIndex = 0;
        this.updateQuizProgress(1, questions.length);

        const quizContent = document.getElementById('quizContent');
        quizContent.innerHTML = '';

        questions.forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = `quiz-question ${index === 0 ? 'active' : 'inactive'}`;
            questionDiv.dataset.questionIndex = index;

            questionDiv.innerHTML = `
                <div class="question-header">
                    <div class="question-number">Q${q.question_number}</div>
                    <div class="question-text">${q.question}</div>
                </div>
                <div class="user-input-section">
                    <textarea placeholder="Type your answer here..." class="answer-textarea" data-question="${q.question_number}"></textarea>
                    <button class="btn btn-primary check-btn" data-question="${q.question_number}">Check Answer</button>
                </div>
                <div class="feedback hidden" data-question="${q.question_number}">
                    <div class="feedback-icon"></div>
                    <div class="feedback-message"></div>
                </div>
                <div class="quiz-answer answer-hidden">
                    <div class="answer-label">
                        <span>💡</span>
                        <span>Correct Answer:</span>
                    </div>
                    <div class="answer-text">${q.answer}</div>
                </div>
            `;

            quizContent.appendChild(questionDiv);

            // Check button listener
            const checkBtn = questionDiv.querySelector('.check-btn');
            checkBtn.addEventListener('click', (e) => this.handleQACheck(e, q));
        });

        // Hide score for Q&A (or customize for similarity score later)
        document.getElementById('scoreDisplay').classList.add('hidden');
    },

    /**
     * Handle Q&A check button
     * @param {Event} e - Click event
     * @param {Object} question - Question data
     */
    handleQACheck(e, question) {
        const textarea = e.currentTarget.previousElementSibling;
        const userAnswer = textarea.value.trim();
        const questionNum = question.question_number;

        // Store user answer
        userAnswers[questionNum] = userAnswer;

        // Simple feedback (reveal answer + basic match)
        const feedback = e.currentTarget.parentElement.nextElementSibling;
        feedback.classList.remove('hidden');
        let message = 'Answer revealed below!';
        let type = 'info';

        if (userAnswer.toLowerCase().includes(question.answer.toLowerCase().substring(0, 20))) {  // Simple keyword match
            message = 'Good attempt! Your answer matches key concepts.';
            type = 'success';
        } else {
            message = 'Check the correct answer below for details.';
            type = 'info';
        }

        feedback.querySelector('.feedback-message').textContent = message;
        feedback.querySelector('.feedback-icon').textContent = type === 'success' ? '✅' : 'ℹ️';

        // Reveal correct answer
        this.toggleAnswerVisibility(true);

        // Update progress
        this.updateQuizProgress(Object.keys(userAnswers).length + 1, Object.keys(userAnswers).length);
    },

    /**
     * Update quiz progress (questions completed)
     * @param {number} current - Current question
     * @param {number} total - Total questions
     */
    updateQuizProgress(current, total) {
        document.getElementById('currentQuestion').textContent = current;
        document.getElementById('totalQuestions').textContent = total;
        document.getElementById('totalQuestionsScore').textContent = total;  // For score too

        const progressFill = document.getElementById('questionProgressFill');
        if (progressFill) {
            progressFill.style.width = `${(current / total) * 100}%`;
        }
    },

    /**
     * Calculate and update score (MCQ only)
     */
    calculateAndUpdateScore() {
        if (quizMode !== 'mcq') return;

        const quizContent = document.getElementById('quizContent');
        const questions = Array.from(quizContent.querySelectorAll('.quiz-question'));
        let score = 0;

        questions.forEach(qDiv => {
            const questionNum = parseInt(qDiv.dataset.questionIndex) + 1;
            const selected = userAnswers[questionNum];
            if (selected && qDiv.querySelector(`[data-option="${selected}"][data-correct="true"]`)) {
                score++;
            }
        });

        document.getElementById('currentScore').textContent = score;
        this.updateQuizProgress(score + 1, questions.length);  // Visual update
    },

    /**
     * Show quiz results
     */
    showResults() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },

    hideResults() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.add('hidden');
    },

    /**
     * Toggle answer visibility (global) - FIXED: Works independently now
     * @param {boolean} show - Whether to show answers
     */
    toggleAnswers(show) {
        const answerElements = document.querySelectorAll('.answer-hidden');
        answerElements.forEach(el => {
            if (show) {
                el.classList.remove('answer-hidden');
            } else {
                el.classList.add('answer-hidden');
            }
        });

        const toggleBtn = document.getElementById('toggleAnswersBtn');
        if (toggleBtn) {
            toggleBtn.innerHTML = show
                ? '<span>🙈</span> Hide Answers'
                : '<span>👁️</span> Show Answers';
        }
    },

    /**
     * Reset quiz state and UI
     */
    resetQuiz() {
        userAnswers = {};
        currentQuestionIndex = 0;
        document.getElementById('quizContent').innerHTML = '';
        this.hideResults();
        document.getElementById('restartSection').classList.add('hidden');
        document.getElementById('scoreDisplay').classList.add('hidden');  // Reset for next mode
        UI.showStatus('Quiz reset. Generate a new one!', 'info');
    },

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }
};

// Add global event listener for restart button (after rendering)
document.addEventListener('click', (e) => {
    if (e.target.id === 'restartBtn') {
        UI.resetQuiz();
    }
});