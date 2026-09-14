// PWA App for Cars Empire

class CarsEmpirePWA {
    constructor() {
        this.isOnline = navigator.onLine;
        this.deferredPrompt = null;
        this.currentLanguage = localStorage.getItem('language') || 'en';
        this.init();
    }

    async init() {
        console.log('Initializing Cars Empire PWA...');
        
        // Register service worker
        await this.registerServiceWorker();
        
        // Initialize PWA features
        this.setupInstallPrompt();
        this.setupOfflineDetection();
        this.setupBottomNavigation();
        this.setupPullToRefresh();
        this.setupInfiniteScroll();
        this.setupLanguageSupport();
        
        // Hide loading screen
        this.hideLoadingScreen();
        
        console.log('PWA initialized successfully');
    }

    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/pwa/sw.js');
                console.log('Service Worker registered:', registration);
                
                // Handle updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            this.showUpdateNotification();
                        }
                    });
                });
            } catch (error) {
                console.error('Service Worker registration failed:', error);
            }
        }
    }

    setupInstallPrompt() {
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallPrompt();
        });

        window.addEventListener('appinstalled', () => {
            console.log('PWA installed successfully');
            this.hideInstallPrompt();
            this.deferredPrompt = null;
        });
    }

    setupOfflineDetection() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.hideOfflineBanner();
            this.showToast('You are back online', 'success');
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showOfflineBanner();
            this.showToast('You are offline', 'warning');
        });
    }

    setupBottomNavigation() {
        const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
        
        bottomNavItems.forEach(item => {
            item.addEventListener('click', () => {
                const page = item.dataset.page;
                this.navigateToPage(page);
                
                // Update active state
                bottomNavItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');
            });
        });
    }

    setupPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        const threshold = 80;
        let isPulling = false;

        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                isPulling = true;
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (!isPulling) return;
            
            currentY = e.touches[0].clientY;
            pullDistance = currentY - startY;
            
            if (pullDistance > 0) {
                e.preventDefault();
                this.updatePullToRefresh(pullDistance);
            }
        });

        document.addEventListener('touchend', () => {
            if (isPulling && pullDistance > threshold) {
                this.refreshPage();
            }
            this.resetPullToRefresh();
            isPulling = false;
        });
    }

    setupInfiniteScroll() {
        let isLoading = false;
        let page = 1;
        
        window.addEventListener('scroll', () => {
            if (isLoading) return;
            
            const scrollTop = window.pageYOffset;
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            
            if (scrollTop + windowHeight >= documentHeight - 100) {
                this.loadMoreContent(page++);
                isLoading = true;
            }
        });
    }

    setupLanguageSupport() {
        // Set initial language
        this.setLanguage(this.currentLanguage);
        
        // Language switcher
        window.switchLanguage = (lang) => {
            this.setLanguage(lang);
        };
    }

    setLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('language', lang);
        
        // Update document attributes
        document.documentElement.lang = lang;
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
        
        // Update current language display
        const currentLangElement = document.getElementById('current-language');
        if (currentLangElement) {
            currentLangElement.textContent = lang.toUpperCase();
        }
        
        // Load translations
        this.loadTranslations(lang);
        
        // Update all translatable elements
        this.updateTranslations();
    }

    async loadTranslations(lang) {
        try {
            const response = await fetch(`/static/pwa/translations/${lang}.json`);
            this.translations = await response.json();
        } catch (error) {
            console.error('Failed to load translations:', error);
            this.translations = {};
        }
    }

    updateTranslations() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.translations[key];
            if (translation) {
                element.textContent = translation;
            }
        });
    }

    navigateToPage(page) {
        const routes = {
            home: '/pwa/',
            deals: '/pwa/deals/',
            merchants: '/pwa/merchants/',
            profile: '/pwa/profile/'
        };
        
        const route = routes[page];
        if (route) {
            window.location.href = route;
        }
    }

    async loadMoreContent(page) {
        const currentPage = window.location.pathname;
        
        try {
            let data = [];
            
            if (currentPage.includes('/deals/')) {
                data = await this.loadMoreDeals(page);
            } else if (currentPage.includes('/merchants/')) {
                data = await this.loadMoreMerchants(page);
            }
            
            if (data.length > 0) {
                this.appendContent(data);
            }
        } catch (error) {
            console.error('Failed to load more content:', error);
        } finally {
            this.isLoading = false;
        }
    }

    async loadMoreDeals(page) {
        // Implementation for loading more deals
        return [];
    }

    async loadMoreMerchants(page) {
        // Implementation for loading more merchants
        return [];
    }

    appendContent(data) {
        // Implementation for appending content to the page
        console.log('Appending content:', data);
    }

    updatePullToRefresh(distance) {
        const pullElement = document.querySelector('.pull-to-refresh');
        if (pullElement) {
            pullElement.style.transform = `translateY(${Math.min(distance, 80)}px)`;
            pullElement.classList.toggle('active', distance > 40);
        }
    }

    resetPullToRefresh() {
        const pullElement = document.querySelector('.pull-to-refresh');
        if (pullElement) {
            pullElement.style.transform = 'translateY(0)';
            pullElement.classList.remove('active');
        }
    }

    async refreshPage() {
        this.showToast('Refreshing...', 'info');
        window.location.reload();
    }

    showInstallPrompt() {
        const prompt = document.getElementById('install-prompt');
        if (prompt) {
            prompt.classList.remove('d-none');
        }
    }

    hideInstallPrompt() {
        const prompt = document.getElementById('install-prompt');
        if (prompt) {
            prompt.classList.add('d-none');
        }
    }

    async installPWA() {
        if (this.deferredPrompt) {
            this.deferredPrompt.prompt();
            const { outcome } = await this.deferredPrompt.userChoice;
            console.log('Install prompt outcome:', outcome);
            this.deferredPrompt = null;
        }
    }

    dismissInstallPrompt() {
        this.hideInstallPrompt();
        localStorage.setItem('install-prompt-dismissed', Date.now());
    }

    showOfflineBanner() {
        const banner = document.getElementById('offline-indicator');
        if (banner) {
            banner.classList.remove('d-none');
        }
    }

    hideOfflineBanner() {
        const banner = document.getElementById('offline-indicator');
        if (banner) {
            banner.classList.add('d-none');
        }
    }

    hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 300);
        }
    }

    showUpdateNotification() {
        this.showToast('New version available. Refresh to update.', 'info', {
            action: 'Refresh',
            onClick: () => window.location.reload()
        });
    }

    showToast(message, type = 'info', options = {}) {
        const toastContainer = document.querySelector('.toast-container') || this.createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} fade-in`;
        toast.innerHTML = `
            <div class="toast-header">
                <strong class="me-auto">Cars Empire</strong>
                <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
            <div class="toast-body">
                ${message}
                ${options.action ? `<button class="btn btn-sm btn-primary ms-2" onclick="this.parentElement.parentElement.remove(); ${options.onClick}">${options.action}</button>` : ''}
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    // Utility methods
    getCurrentPage() {
        return window.location.pathname.split('/')[2] || 'home';
    }

    isAuthenticated() {
        return !!localStorage.getItem('auth_token');
    }

    logout() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/pwa/login/';
    }
}

// Initialize PWA
function initializePWA() {
    window.pwaApp = new CarsEmpirePWA();
}

// Global functions for HTML onclick handlers
window.installPWA = function() {
    if (window.pwaApp) {
        window.pwaApp.installPWA();
    }
};

window.dismissInstallPrompt = function() {
    if (window.pwaApp) {
        window.pwaApp.dismissInstallPrompt();
    }
};

window.switchLanguage = function(lang) {
    if (window.pwaApp) {
        window.pwaApp.setLanguage(lang);
    }
};

window.logout = function() {
    if (window.pwaApp) {
        window.pwaApp.logout();
    }
}; 