class CarsEmpireApp {
    constructor() {
        this.apiBaseUrl = 'https://carsempire.net/api/';
        this.frontendBaseUrl = 'https://carsempire.net/';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadNotifications();
        this.setupPWA();
        this.loadUserPreferences();
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', this.handleSearch.bind(this));
        }

        // Save deal buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('save-deal-btn')) {
                const dealId = e.target.dataset.dealId;
                this.saveDeal(dealId);
            }
        });

        // Share deal buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('share-deal-btn')) {
                const dealId = e.target.dataset.dealId;
                this.shareDeal(dealId);
            }
        });
    }

    async handleSearch(e) {
        const query = e.target.value;
        if (query.length < 2) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}deals/?search=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.displaySearchResults(data.results || []);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    displaySearchResults(results) {
        // Implementation for displaying search results
        console.log('Search results:', results);
    }

    async saveDeal(dealId) {
        if (!this.isUserLoggedIn()) {
            this.showLoginModal();
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}deals/${dealId}/save_deal/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                this.showNotification('Deal saved successfully!', 'success');
            } else {
                this.showNotification('Failed to save deal', 'error');
            }
        } catch (error) {
            console.error('Save deal error:', error);
            this.showNotification('Failed to save deal', 'error');
        }
    }

    async shareDeal(dealId) {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'Check out this deal!',
                    url: this.frontendBaseUrl + `deals/${dealId}/`
                });
            } catch (error) {
                console.log('Share cancelled');
            }
        } else {
            // Fallback to copying URL
            const url = this.frontendBaseUrl + `deals/${dealId}/`;
            navigator.clipboard.writeText(url).then(() => {
                this.showNotification('Deal URL copied to clipboard!', 'success');
            });
        }
    }

    isUserLoggedIn() {
        // Check if user is logged in
        return localStorage.getItem('authToken') !== null;
    }

    showLoginModal() {
        // Show login modal
        console.log('Show login modal');
    }

    showNotification(message, type) {
        // Show notification
        console.log(`${type}: ${message}`);
    }

    getCSRFToken() {
        // Get CSRF token
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    async loadNotifications() {
        // Load notifications
        console.log('Loading notifications...');
    }

    setupPWA() {
        // Setup PWA
        console.log('Setting up PWA...');
    }

    loadUserPreferences() {
        // Load user preferences
        console.log('Loading user preferences...');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CarsEmpireApp();
});
