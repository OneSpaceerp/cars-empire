// Utility functions for Cars Empire frontend

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    const container = document.querySelector('.container');
    const refNode = container ? container.querySelector('.row') : null;
    if (container && refNode && refNode.parentNode === container) {
        container.insertBefore(errorDiv, refNode);
    } else if (container) {
        container.appendChild(errorDiv);
    } else {
        document.body.appendChild(errorDiv);
    }
    setTimeout(() => errorDiv.remove(), 5000);
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success alert-dismissible fade show';
    successDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    const container = document.querySelector('.container');
    const refNode = container ? container.querySelector('.row') : null;
    if (container && refNode && refNode.parentNode === container) {
        container.insertBefore(successDiv, refNode);
    } else if (container) {
        container.appendChild(successDiv);
    } else {
        document.body.appendChild(successDiv);
    }
    setTimeout(() => successDiv.remove(), 5000);
}

// Export utility functions
window.showError = showError;
window.showSuccess = showSuccess; 