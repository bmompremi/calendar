// Haiti National Bank - Main JavaScript

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Format currency inputs
function formatCurrency(input) {
    let value = input.value.replace(/[^0-9.]/g, '');
    if (value) {
        input.value = parseFloat(value).toFixed(2);
    }
}

// Validate account number format
function validateAccountNumber(accountNumber) {
    return /^509\d{13}$/.test(accountNumber);
}

// Confirm dangerous actions
function confirmAction(message) {
    return confirm(message);
}
