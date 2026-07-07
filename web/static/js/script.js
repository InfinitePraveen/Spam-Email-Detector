// web/static/js/script.js

// Auto-resize textarea
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('.form-control');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
    
    // Add loading state to form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('.btn-primary');
            if (btn) {
                btn.textContent = '⏳ Classifying...';
                btn.disabled = true;
                btn.style.opacity = '0.7';
            }
        });
    });
    
    // Add smooth scroll to results
    const resultContainer = document.querySelector('.result-container');
    if (resultContainer) {
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Confetti animation for ham predictions
    const prediction = document.querySelector('.prediction.ham');
    if (prediction) {
        // Add a small celebration effect
        createConfetti();
    }
});

// Confetti effect for ham predictions
function createConfetti() {
    const colors = ['#00b894', '#00a86b', '#6c5ce7', '#fd79a8', '#fdcb6e'];
    const container = document.body;
    
    for (let i = 0; i < 30; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 8px;
            height: 8px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${Math.random() * 100}vw;
            top: -10px;
            border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
            animation: fall ${2 + Math.random() * 3}s linear forwards;
            animation-delay: ${Math.random() * 2}s;
            pointer-events: none;
            z-index: 999;
        `;
        container.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 5000);
    }
}

// Add keyframe animation for confetti
const style = document.createElement('style');
style.textContent = `
    @keyframes fall {
        0% {
            transform: translateY(-10px) rotate(0deg) scale(1);
            opacity: 1;
        }
        100% {
            transform: translateY(110vh) rotate(720deg) scale(0.5);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Dark mode toggle (optional)
// Add toggle functionality if needed
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Check saved preference
// if (localStorage.getItem('darkMode') === 'true') {
//     document.body.classList.add('dark-mode');
// }

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.querySelector('form');
        if (form) {
            const btn = form.querySelector('.btn-primary');
            if (btn && !btn.disabled) {
                form.submit();
            }
        }
    }
});

// Copy result to clipboard (optional)
function copyResult() {
    const resultText = document.querySelector('.prediction-text h4');
    if (resultText) {
        navigator.clipboard.writeText(resultText.textContent).then(() => {
            // Show feedback
            const btn = document.querySelector('#copyBtn');
            if (btn) {
                btn.textContent = '✅ Copied!';
                setTimeout(() => {
                    btn.textContent = '📋 Copy';
                }, 2000);
            }
        });
    }
}

// Add loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<div class="spinner"></div>';
    document.querySelector('main').prepend(spinner);
}

// Add this to CSS if you want a loading spinner
// .loading-spinner {
//     text-align: center;
//     padding: 2rem;
// }
// .spinner {
//     width: 40px;
//     height: 40px;
//     border: 4px solid #f3f3f3;
//     border-top: 4px solid #6c5ce7;
//     border-radius: 50%;
//     animation: spin 1s linear infinite;
//     margin: 0 auto;
// }
// @keyframes spin {
//     0% { transform: rotate(0deg); }
//     100% { transform: rotate(360deg); }
// }