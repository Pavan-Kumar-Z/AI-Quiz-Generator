// Test backend connection
async function testBackend() {
    const statusDiv = document.getElementById('status');
    
    try {
        const response = await fetch('http://localhost:5000/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusDiv.innerHTML = `
                <p style="color: #28a745;">✅ Backend is running!</p>
                <p>API Status: ${data.status}</p>
            `;
        }
    } catch (error) {
        statusDiv.innerHTML = `
            <p style="color: #dc3545;">❌ Backend is not running</p>
            <p>Please start the backend server: <code>python backend/app.py</code></p>
        `;
    }
}

// Run test on page load
window.addEventListener('DOMContentLoaded', testBackend);