// CVTailor - Main JavaScript

let currentSessionId = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cvForm');
    form.addEventListener('submit', handleFormSubmit);
    
    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.addEventListener('click', handleDownload);
    
    // Handle job input method toggle
    const jobUrlMethod = document.getElementById('jobUrlMethod');
    const jobTextMethod = document.getElementById('jobTextMethod');
    
    jobUrlMethod.addEventListener('change', toggleJobInputMethod);
    jobTextMethod.addEventListener('change', toggleJobInputMethod);
    
    // Initialize with URL method
    toggleJobInputMethod();
});

// Toggle between URL and text input
function toggleJobInputMethod() {
    const jobUrlMethod = document.getElementById('jobUrlMethod');
    const jobUrlSection = document.getElementById('jobUrlSection');
    const jobTextSection = document.getElementById('jobTextSection');
    const jobUrlInput = document.getElementById('jobUrl');
    const jobTextInput = document.getElementById('jobText');
    
    if (jobUrlMethod.checked) {
        // Show URL input, hide text input
        jobUrlSection.style.display = 'block';
        jobTextSection.style.display = 'none';
        jobUrlInput.required = true;
        jobTextInput.required = false;
        jobTextInput.value = ''; // Clear text input
    } else {
        // Show text input, hide URL input
        jobUrlSection.style.display = 'none';
        jobTextSection.style.display = 'block';
        jobUrlInput.required = false;
        jobTextInput.required = true;
        jobUrlInput.value = ''; // Clear URL input
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(e.target);
    
    // Validate job input
    const jobUrl = formData.get('job_url');
    const jobText = formData.get('job_text');
    
    if (!jobUrl && !jobText) {
        showError('Please provide either a job URL or paste the job description.');
        return;
    }
    
    // Show loading, hide other sections
    showSection('loadingSection');
    hideSection('uploadSection');
    hideSection('errorSection');
    hideSection('previewSection');
    
    try {
        // Submit to backend
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }
        
        // Store session ID
        currentSessionId = data.session_id;
        
        // Show preview
        displayPreview(data);
        
    } catch (error) {
        showError(error.message);
    }
}

// Display preview with comparison
function displayPreview(data) {
    // Hide loading
    hideSection('loadingSection');
    
    // Set match score
    document.getElementById('matchScore').textContent = data.match_score || 'N/A';
    
    // Set changes summary
    const summaryDiv = document.getElementById('changesSummary');
    summaryDiv.innerHTML = formatChangesSummary(data.changes_summary);
    
    // Set CV texts
    document.getElementById('originalCv').textContent = data.original_cv;
    document.getElementById('modifiedCv').textContent = data.modified_cv;
    
    // Show preview section with animation
    const previewSection = document.getElementById('previewSection');
    previewSection.style.display = 'block';
    previewSection.classList.add('fade-in');
    
    // Scroll to preview
    previewSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Format changes summary
function formatChangesSummary(summary) {
    if (!summary || summary === 'N/A') {
        return '<p class="text-muted">No specific changes summary available.</p>';
    }
    
    // Split by line breaks and format as list
    const lines = summary.split('\n').filter(line => line.trim());
    
    if (lines.length === 0) {
        return '<p class="text-muted">No specific changes summary available.</p>';
    }
    
    let html = '<ul>';
    lines.forEach(line => {
        // Remove leading bullets or dashes
        line = line.replace(/^[-•*]\s*/, '').trim();
        if (line) {
            html += `<li>${escapeHtml(line)}</li>`;
        }
    });
    html += '</ul>';
    
    return html;
}

// Handle download
function handleDownload() {
    if (!currentSessionId) {
        showError('No session found. Please process a CV first.');
        return;
    }
    
    // Trigger download
    window.location.href = `/download/${currentSessionId}`;
}

// Reset form and start over
function resetForm() {
    currentSessionId = null;
    
    // Reset form
    document.getElementById('cvForm').reset();
    
    // Show upload section
    showSection('uploadSection');
    hideSection('loadingSection');
    hideSection('errorSection');
    hideSection('previewSection');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show error
function showError(message) {
    hideSection('loadingSection');
    hideSection('previewSection');
    
    document.getElementById('errorMessage').textContent = message;
    showSection('errorSection');
    showSection('uploadSection');
    
    // Scroll to error
    document.getElementById('errorSection').scrollIntoView({ behavior: 'smooth' });
}

// Utility functions
function showSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    }
}

function hideSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'none';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Optional: Implement basic diff highlighting
// This is a simple version - could be enhanced with a proper diff library
function highlightDifferences(original, modified) {
    const originalLines = original.split('\n');
    const modifiedLines = modified.split('\n');
    
    // Simple line-by-line comparison
    // In a production app, use a proper diff algorithm
    
    return {
        original: original,
        modified: modified
    };
}
