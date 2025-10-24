// ============================================
// API Communication Module
// Handles all backend API requests
// ============================================

const API_BASE_URL = 'http://localhost:5000';

// API utility object
const API = {
    /**
     * Upload file to backend
     * @param {File} file - The file to upload
     * @returns {Promise<Object>} Response data
     */
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }

            return data;
        } catch (error) {
            console.error('Upload error:', error);
            throw error;
        }
    },

    /**
     * Generate quiz from uploaded document
     * @param {Object} params - Quiz generation parameters
     * @returns {Promise<Object>} Quiz data
     */
    async generateQuiz(params) {
        try {
            const response = await fetch(`${API_BASE_URL}/generate-quiz`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(params)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Quiz generation failed');
            }

            return data;
        } catch (error) {
            console.error('Generate quiz error:', error);
            throw error;
        }
    },

    /**
     * Download quiz as PDF
     * @param {Object} quizData - The quiz data to convert to PDF
     * @returns {Promise<Object>} Response data
     */
    async downloadPDF(quizData) {
        try {
            const response = await fetch(`${API_BASE_URL}/download-pdf`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quiz_data: quizData })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'PDF download failed');
            }

            return data;
        } catch (error) {
            console.error('Download PDF error:', error);
            throw error;
        }
    },

    /**
     * Check API health
     * @returns {Promise<Object>} Health status
     */
    async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Health check error:', error);
            throw error;
        }
    }
};