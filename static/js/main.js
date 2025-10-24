// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});

// Format currency inputs
function formatCurrency(input) {
    let value = input.value.replace(/[^0-9.]/g, '');
    const parts = value.split('.');
    if (parts.length > 2) {
        value = parts[0] + '.' + parts.slice(1).join('');
    }
    if (parts[1] && parts[1].length > 2) {
        value = parts[0] + '.' + parts[1].substring(0, 2);
    }
    input.value = value;
}

// Validate amount input
function validateAmount(input, min = 1, max = 1000000) {
    const value = parseFloat(input.value);
    if (isNaN(value)) {
        return false;
    }
    return value >= min && value <= max;
}

// Confirm actions
function confirmAction(message) {
    return confirm(message);
}

// Phone number formatting for Haiti
function formatHaitiPhone(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.startsWith('509')) {
        value = value.substring(3);
    }
    if (value.length > 8) {
        value = value.substring(0, 8);
    }
    if (value.length > 4) {
        value = value.substring(0, 4) + ' ' + value.substring(4);
    }
    if (value) {
        input.value = '+509 ' + value;
    }
}

// Add event listeners for phone inputs
document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener('blur', function() {
        formatHaitiPhone(this);
    });
});

// Add event listeners for currency inputs
document.querySelectorAll('input[type="number"][step="0.01"]').forEach(input => {
    input.addEventListener('input', function() {
        formatCurrency(this);
    });
});

// Utility: Copy to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            alert('Copied to clipboard!');
        });
    } else {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('Copied to clipboard!');
    }
}

// Add copy functionality to account numbers
document.querySelectorAll('.account-number').forEach(element => {
    element.style.cursor = 'pointer';
    element.title = 'Click to copy';
    element.addEventListener('click', function() {
        copyToClipboard(this.textContent.trim());
    });
});
