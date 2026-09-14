// PWA API for Cars Empire

class PWAAPI {
    constructor() {
        this.baseURL = (typeof window !== 'undefined' && window.location && window.location.origin && window.location.origin.startsWith('http'))
            ? window.location.origin + '/api'
            : 'https://carsempire.net/api';
        this.cache = new Map();
        this.offlineQueue = [];
        this.init();
    }

    init() {
        this.setupOfflineQueue();
        this.setupCache();
    }

    // Cache management
    setupCache() {
        // Clear old cache entries
        const now = Date.now();
        const maxAge = 5 * 60 * 1000; // 5 minutes
        
        for (const [key, value] of this.cache.entries()) {
            if (now - value.timestamp > maxAge) {
                this.cache.delete(key);
            }
        }
    }

    // Offline queue management
    setupOfflineQueue() {
        window.addEventListener('online', () => {
            this.processOfflineQueue();
        });
    }

    async processOfflineQueue() {
        if (this.offlineQueue.length === 0) return;

        console.log('Processing offline queue...');
        
        for (const request of this.offlineQueue) {
            try {
                await this.makeRequest(request);
                console.log('Offline request processed:', request);
            } catch (error) {
                console.error('Failed to process offline request:', error);
            }
        }
        
        this.offlineQueue = [];
        localStorage.removeItem('offline-queue');
    }

    // Main request method
    async makeRequest(options) {
        const { url, method = 'GET', data = null, useCache = true } = options;
        const cacheKey = `${method}:${url}`;
        
        // Check cache for GET requests
        if (method === 'GET' && useCache && this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < 5 * 60 * 1000) { // 5 minutes
                return cached.data;
            }
        }

        try {
            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    ...this.getAuthHeaders()
                },
                body: data ? JSON.stringify(data) : null
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            
            // Cache successful GET requests
            if (method === 'GET' && useCache) {
                this.cache.set(cacheKey, {
                    data: result,
                    timestamp: Date.now()
                });
            }

            return result;
        } catch (error) {
            // If offline, queue the request
            if (!navigator.onLine && method !== 'GET') {
                this.queueOfflineRequest(options);
            }
            throw error;
        }
    }

    queueOfflineRequest(request) {
        this.offlineQueue.push(request);
        localStorage.setItem('offline-queue', JSON.stringify(this.offlineQueue));
        console.log('Request queued for offline processing:', request);
    }

    getAuthHeaders() {
        const token = localStorage.getItem('auth_token');
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }

    // Categories API
    async getCategories() {
        return this.makeRequest({
            url: `${this.baseURL}/categories/all_for_carousel/`,
            useCache: true
        });
    }

    async getCategory(id) {
        return this.makeRequest({
            url: `${this.baseURL}/categories/${id}/`,
            useCache: true
        });
    }

    // Deals API
    async getDeals(page = 1, filters = {}) {
        const params = new URLSearchParams({ page, ...filters });
        return this.makeRequest({
            url: `${this.baseURL}/deals/?${params}`,
            useCache: true
        });
    }

    async getDeal(id) {
        return this.makeRequest({
            url: `${this.baseURL}/deals/${id}/`,
            useCache: true
        });
    }

    async getFeaturedDeals() {
        return this.makeRequest({
            url: `${this.baseURL}/deals/featured/`,
            useCache: true
        });
    }

    async getDealsByCategory(categoryId, page = 1) {
        return this.makeRequest({
            url: `${this.baseURL}/deals/?category=${categoryId}&page=${page}`,
            useCache: true
        });
    }

    // Merchants API
    async getMerchants(page = 1, filters = {}) {
        const params = new URLSearchParams({ page, ...filters });
        return this.makeRequest({
            url: `${this.baseURL}/merchants/?${params}`,
            useCache: true
        });
    }

    async getMerchant(id) {
        return this.makeRequest({
            url: `${this.baseURL}/merchants/${id}/`,
            useCache: true
        });
    }

    async getNearbyMerchants(lat, lng, radius = 50) {
        return this.makeRequest({
            url: `${this.baseURL}/merchants/nearby/?lat=${lat}&lng=${lng}&radius=${radius}`,
            useCache: false
        });
    }

    async getMerchantDeals(merchantId) {
        return this.makeRequest({
            url: `${this.baseURL}/deals/?merchant=${merchantId}`,
            useCache: true
        });
    }

    // Cart API
    async getCart() {
        return this.makeRequest({
            url: `${this.baseURL}/cart/`,
            useCache: false
        });
    }

    async addToCart(dealId, quantity = 1) {
        return this.makeRequest({
            url: `${this.baseURL}/cart/add/`,
            method: 'POST',
            data: { deal_id: dealId, quantity }
        });
    }

    async updateCartItem(itemId, quantity) {
        return this.makeRequest({
            url: `${this.baseURL}/cart/update/${itemId}/`,
            method: 'PUT',
            data: { quantity }
        });
    }

    async removeFromCart(itemId) {
        return this.makeRequest({
            url: `${this.baseURL}/cart/remove/${itemId}/`,
            method: 'DELETE'
        });
    }

    // User API
    async login(credentials) {
        const response = await this.makeRequest({
            url: `${this.baseURL}/users/token/`,
            method: 'POST',
            data: credentials
        });

        if (response.access) {
            localStorage.setItem('auth_token', response.access);
            localStorage.setItem('refresh_token', response.refresh);
        }

        return response;
    }

    async register(userData) {
        return this.makeRequest({
            url: `${this.baseURL}/users/register/`,
            method: 'POST',
            data: userData
        });
    }

    async getProfile() {
        return this.makeRequest({
            url: `${this.baseURL}/users/profile/`,
            useCache: false
        });
    }

    async updateProfile(profileData) {
        return this.makeRequest({
            url: `${this.baseURL}/users/profile/`,
            method: 'PUT',
            data: profileData
        });
    }

    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) return false;

        try {
            const response = await this.makeRequest({
                url: `${this.baseURL}/users/token/refresh/`,
                method: 'POST',
                data: { refresh: refreshToken }
            });

            if (response.access) {
                localStorage.setItem('auth_token', response.access);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
        }

        return false;
    }

    // Orders API
    async getOrders() {
        return this.makeRequest({
            url: `${this.baseURL}/users/orders/`,
            useCache: false
        });
    }

    async getOrder(id) {
        return this.makeRequest({
            url: `${this.baseURL}/users/orders/${id}/`,
            useCache: false
        });
    }

    async createOrder(orderData) {
        return this.makeRequest({
            url: `${this.baseURL}/orders/create/`,
            method: 'POST',
            data: orderData
        });
    }

    // Search API
    async search(query, type = 'all') {
        return this.makeRequest({
            url: `${this.baseURL}/search/?q=${encodeURIComponent(query)}&type=${type}`,
            useCache: true
        });
    }

    // Helper function to convert deal API data to frontend URL
    getDealUrl(deal) {
        if (!deal) return '#';
        // Convert API deal data to frontend URL format
        const slug = deal.slug || deal.title?.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || deal.id;
        return `/deals/${slug}/`;
    }

    // Utility methods
    clearCache() {
        this.cache.clear();
        console.log('Cache cleared');
    }

    getCacheSize() {
        return this.cache.size;
    }

    getOfflineQueueSize() {
        return this.offlineQueue.length;
    }

    isOnline() {
        return navigator.onLine;
    }

    // Error handling
    handleError(error) {
        console.error('API Error:', error);
        
        if (error.message.includes('401')) {
            // Token expired, try to refresh
            return this.refreshToken().then(success => {
                if (success) {
                    // Retry the original request
                    return this.makeRequest(this.lastRequest);
                } else {
                    // Redirect to login
                    window.location.href = '/pwa/login/';
                }
            });
        }
        
        throw error;
    }
}

// Initialize PWA API
window.pwaAPI = new PWAAPI();

// Expose getDealUrl globally
window.getDealUrl = (deal) => window.pwaAPI.getDealUrl(deal);

// Global API functions for backward compatibility
window.api = {
    categories: {
        getAll: () => window.pwaAPI.getCategories(),
        getById: (id) => window.pwaAPI.getCategory(id)
    },
    deals: {
        getAll: (page, filters) => window.pwaAPI.getDeals(page, filters),
        getById: (id) => window.pwaAPI.getDeal(id),
        getFeatured: () => window.pwaAPI.getFeaturedDeals(),
        getByCategory: (categoryId, page) => window.pwaAPI.getDealsByCategory(categoryId, page),
        getByMerchant: (merchantId) => window.pwaAPI.getMerchantDeals(merchantId)
    },
    merchants: {
        getAll: (page, filters) => window.pwaAPI.getMerchants(page, filters),
        getById: (id) => window.pwaAPI.getMerchant(id),
        getNearby: (lat, lng, radius) => window.pwaAPI.getNearbyMerchants(lat, lng, radius)
    },
    cart: {
        get: () => window.pwaAPI.getCart(),
        add: (dealId, quantity) => window.pwaAPI.addToCart(dealId, quantity),
        update: (itemId, quantity) => window.pwaAPI.updateCartItem(itemId, quantity),
        remove: (itemId) => window.pwaAPI.removeFromCart(itemId)
    },
    auth: {
        login: (credentials) => window.pwaAPI.login(credentials),
        register: (userData) => window.pwaAPI.register(userData),
        getProfile: () => window.pwaAPI.getProfile(),
        updateProfile: (profileData) => window.pwaAPI.updateProfile(profileData),
        refreshToken: () => window.pwaAPI.refreshToken()
    },
    orders: {
        getAll: () => window.pwaAPI.getOrders(),
        getById: (id) => window.pwaAPI.getOrder(id),
        create: (orderData) => window.pwaAPI.createOrder(orderData)
    },
    search: {
        query: (query, type) => window.pwaAPI.search(query, type)
    }
};