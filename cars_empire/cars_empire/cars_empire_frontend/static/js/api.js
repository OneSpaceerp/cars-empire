// API Configuration
const API_BASE_URL = (typeof window !== 'undefined' && window.location && window.location.origin && window.location.origin.startsWith('http'))
    ? window.location.origin + '/api'
    : 'https://carsempire.net/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
    console.log('API Response:', response.status, response.url);  // Debug log
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        console.error('API Error Response:', response.status, error);  // Debug log
        
        // Handle 401 Unauthorized errors
        if (response.status === 401) {
            // Try to refresh the token first
            const refreshSuccess = await api.auth.refreshToken();
            if (!refreshSuccess) {
                // If refresh failed, clear the session and redirect to login
                logout();
                throw new Error('Session expired. Please login again.');
            }
            // If refresh succeeded, retry the original request
            const retryResponse = await fetch(response.url, {
                method: response.method || 'GET',
                headers: getAuthHeaders(),
                body: response.body
            });
            return handleResponse(retryResponse);
        }
        
        if (response.status === 404) {
            throw new Error(`API endpoint not found: ${response.url}`);
        }
        throw new Error(error.detail || error.message || `Server error: ${response.status}`);
    }
    if (response.status === 204) return Promise.resolve(null);
    return response.text().then(text => text ? JSON.parse(text) : null);
};

// Helper function to ensure array response
const ensureArray = (data) => {
    if (!data) return [];
    if (Array.isArray(data)) return data;
    if (data.results && Array.isArray(data.results)) return data.results;
    return [];
};

// Helper function to handle API errors
const handleApiError = (error) => {
    console.error('API Error:', error);
    if (typeof window.showError === 'function') {
        window.showError(error.message || 'An error occurred while fetching data');
    }
    return [];
};

// Show loading indicator
const showLoading = (element) => {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading-spinner';
    element.appendChild(loadingDiv);
    return loadingDiv;
};

// Get auth token from localStorage
const getAuthToken = () => {
    return localStorage.getItem('auth_token');
};

// Add auth token to headers if available
const getAuthHeaders = () => {
    const headers = {
        'Content-Type': 'application/json',
    };
    const token = getAuthToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
};

// Check if user is authenticated
const isAuthenticated = () => {
    return !!getAuthToken();
};

// Get current user
const getCurrentUser = () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
};

// Logout user
const logout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login/';
};

// API Functions
const api = {
    // Merchant endpoints
    merchants: {
        getAll: async (filters = {}) => {
            try {
                let url;
                const params = [];
                if (filters.category) params.push(`category=${encodeURIComponent(filters.category)}`);
                if (filters.lat && filters.lng) {
                    // Use the nearby endpoint for location-based filtering
                    url = `${API_BASE_URL}/merchants/nearby/?lat=${encodeURIComponent(filters.lat)}&lng=${encodeURIComponent(filters.lng)}`;
                    if (filters.radius) params.push(`radius=${encodeURIComponent(filters.radius)}`);
                } else {
                    url = `${API_BASE_URL}/merchants/`;
                    if (filters.radius) params.push(`radius=${encodeURIComponent(filters.radius)}`);
                }
                if (params.length > 0) {
                    if (url.includes('?')) {
                        url += `&${params.join('&')}`;
                    } else {
                        url += `?${params.join('&')}`;
                    }
                }
                const response = await fetch(url);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getById: async (id) => {
            try {
                const response = await fetch(`${API_BASE_URL}/merchants/${id}/`);
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getFeatured: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/merchants/featured/`);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getNearby: async (lat, lng, radius = 50) => {
            try {
                console.log(`Fetching nearby merchants: lat=${lat}, lng=${lng}, radius=${radius}`);  // Debug log
                const url = `${API_BASE_URL}/merchants/nearby/?lat=${lat}&lng=${lng}&radius=${radius}`;
                console.log('Request URL:', url);  // Debug log
                const response = await fetch(url);
                const data = await handleResponse(response);
                if (!data || data.length === 0) {
                    console.log('No merchants found within the specified radius');  // Debug log
                }
                return ensureArray(data);
            } catch (error) {
                console.error('Failed to get nearby merchants:', error);  // Debug log
                return handleApiError(error);
            }
        },
        addImage: async (merchantId, imageData) => {
            try {
                const response = await fetch(
                    `${API_BASE_URL}/merchants/${merchantId}/add_image/`,
                    {
                        method: 'POST',
                        body: imageData,
                    }
                );
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        removeImage: async (merchantId, imageId) => {
            try {
                const response = await fetch(
                    `${API_BASE_URL}/merchants/${merchantId}/remove_image/`,
                    {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ image_id: imageId }),
                    }
                );
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        }
    },

    // Category endpoints
    categories: {
        getAll: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/categories/`);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getAllForCarousel: async () => {
            try {
                console.log('Trying carousel-specific endpoint...');
                const response = await fetch(`${API_BASE_URL}/categories/all_for_carousel/`);
                const data = await handleResponse(response);
                console.log('Carousel endpoint successful:', data);
                return ensureArray(data);
            } catch (error) {
                console.warn('Carousel endpoint failed, falling back to regular endpoint:', error);
                // Fallback to regular getAll method
                try {
                    const response = await fetch(`${API_BASE_URL}/categories/`);
                    const data = await handleResponse(response);
                    console.log('Fallback endpoint successful:', data);
                    return ensureArray(data);
                } catch (fallbackError) {
                    console.error('Both endpoints failed:', fallbackError);
                    return handleApiError(fallbackError);
                }
            }
        },
        getById: async (id) => {
            try {
                const response = await fetch(`${API_BASE_URL}/categories/${id}/`);
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        }
    },

    // Deal endpoints
    deals: {
        getAll: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/deals/`);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getById: async (id) => {
            try {
                const response = await fetch(`${API_BASE_URL}/deals/${id}/`);
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getByCategory: async (categoryId) => {
            try {
                const response = await fetch(`${API_BASE_URL}/deals/?category=${categoryId}`);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getByMerchant: async (merchantId) => {
            try {
                const response = await fetch(`${API_BASE_URL}/deals/?merchant=${merchantId}`);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getFeatured: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/deals/featured/`);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getExpiringSoon: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/deals/expiring_soon/`);
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        }
    },

    // Authentication API calls
    auth: {
        login: async (credentials) => {
            try {
                // Validate credentials
                if (!credentials || !credentials.username || !credentials.password) {
                    throw new Error('Username and password are required');
                }
                
                // Determine if the input is an email or username
                const isEmail = credentials.username.includes('@');
                const payload = {
                    password: credentials.password,
                    [isEmail ? 'email' : 'username']: credentials.username
                };

                const response = await fetch(`${API_BASE_URL}/users/token/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload)
                });
                return await handleResponse(response);
            } catch (error) {
                handleApiError(error);
                return null;
            }
        },
        register: async (userData) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/register/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: userData.username,
                        email: userData.email,
                        phone: userData.phone,
                        password: userData.password,
                        re_password: userData.re_password,
                        first_name: userData.first_name,
                        last_name: userData.last_name
                    })
                });
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    let errorMessage = 'Registration failed';
                    if (typeof errorData === 'object' && errorData !== null) {
                        const messages = [];
                        for (const key in errorData) {
                            if (Array.isArray(errorData[key])) {
                                messages.push(`${key}: ${errorData[key].join(', ')}`);
                            } else if (typeof errorData[key] === 'string') {
                                messages.push(`${key}: ${errorData[key]}`);
                            }
                        }
                        if (messages.length > 0) {
                            errorMessage = messages.join('\n');
                        }
                    }
                    throw new Error(errorMessage);
                }
                
                return await response.json();
            } catch (error) {
                console.error('Registration error:', error);
                throw error;
            }
        },
        getProfile: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/profile/`, {
                    headers: getAuthHeaders()
                });
                const data = await handleResponse(response);
                return data.user;
            } catch (error) {
                handleApiError(error);
                return null;
            }
        },
        updateProfile: async (userData) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/profile/update/`, {
                    method: 'PATCH',
                    headers: getAuthHeaders(),
                    body: JSON.stringify(userData)
                });
                const data = await handleResponse(response);
                if (data.user) {
                    localStorage.setItem('user', JSON.stringify(data.user));
                }
                return data;
            } catch (error) {
                handleApiError(error);
                return null;
            }
        },
        refreshToken: async () => {
            try {
                const refresh = localStorage.getItem('refresh_token');
                if (!refresh) {
                    throw new Error('No refresh token available');
                }

                const response = await fetch(`${API_BASE_URL}/users/token/refresh/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ refresh })
                });
                const data = await handleResponse(response);
                if (data.access) {
                    localStorage.setItem('auth_token', data.access);
                    return true;
                }
                return false;
            } catch (error) {
                console.error('Token refresh failed:', error);
                logout();
                return false;
            }
        },
        changePassword: async (passwordData) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/set_password/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        ...getAuthHeaders()
                    },
                    body: JSON.stringify(passwordData)
                });
                return await handleResponse(response);
            } catch (error) {
                handleApiError(error);
                return null;
            }
        },
        logout: async () => {
            try {
                // Call logout endpoint if it exists
                const response = await fetch(`${API_BASE_URL}/users/logout/`, {
                    method: 'POST',
                    headers: getAuthHeaders()
                }).catch(() => null); // Ignore errors if endpoint doesn't exist
                
                // Clear local storage regardless of endpoint success
                localStorage.removeItem('auth_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                
                // Redirect to login page
                window.location.href = '/login/';
            } catch (error) {
                console.error('Logout error:', error);
                // Still clear storage and redirect even if there's an error
                localStorage.removeItem('auth_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                window.location.href = '/login/';
            }
        }
    },

    // User registration (Djoser)
    register: async function({ username, email, phone, password, re_password }) {
        const payload = { username, email, phone, password, re_password };
        const response = await fetch(`${API_BASE_URL}/auth/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            // Show all error messages if available
            if (typeof error === 'object' && error !== null) {
                let msg = '';
                for (const key in error) {
                    if (Array.isArray(error[key])) {
                        msg += `${key}: ${error[key].join(', ')}\n`;
                    } else {
                        msg += `${key}: ${error[key]}\n`;
                    }
                }
                throw new Error(msg || 'Registration failed');
            }
            throw new Error(error.detail || JSON.stringify(error) || 'Registration failed');
        }
        return response.json();
    },

    // User login (Djoser JWT)
    login: async function({ email, phone, password }) {
        // Djoser JWT login expects 'email' or 'username' by default. If you want to support phone, backend must support it.
        const payload = { password };
        if (email) payload.email = email;
        if (phone) payload.phone = phone;
        // Try email first, fallback to phone if provided
        const response = await fetch(`${API_BASE_URL}/auth/jwt/create/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || JSON.stringify(error) || 'Login failed');
        }
        const data = await response.json();
        if (data.access) {
            localStorage.setItem('auth_token', data.access);
        }
        return data;
    },

    // User vehicles endpoints
    vehicles: {
        getAll: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/vehicles/`, {
                    headers: getAuthHeaders()
                });
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        add: async (vehicleData) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/vehicles/`, {
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: JSON.stringify(vehicleData)
                });
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        update: async (vehicleId, vehicleData) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/vehicles/${vehicleId}/`, {
                    method: 'PUT',
                    headers: getAuthHeaders(),
                    body: JSON.stringify(vehicleData)
                });
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        delete: async (vehicleId) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/vehicles/${vehicleId}/`, {
                    method: 'DELETE',
                    headers: getAuthHeaders()
                });
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        }
    },

    // User orders endpoints
    orders: {
        getAll: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/orders/`, {
                    headers: getAuthHeaders()
                });
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getById: async (orderId) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/orders/${orderId}/`, {
                    headers: getAuthHeaders()
                });
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        cancel: async (orderId) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/orders/${orderId}/cancel/`, {
                    method: 'POST',
                    headers: getAuthHeaders()
                });
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        }
    },

    // User coupons endpoints
    coupons: {
        getAll: async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/coupons/`, {
                    headers: getAuthHeaders()
                });
                const data = await handleResponse(response);
                return ensureArray(data);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getById: async (couponId) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/coupons/${couponId}/`, {
                    headers: getAuthHeaders()
                });
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        redeem: async (couponCode) => {
            try {
                const response = await fetch(`${API_BASE_URL}/users/coupons/redeem/`, {
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: JSON.stringify({ code: couponCode })
                });
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        }
    },

    // Car makes and models endpoints
    cars: {
        getMakes: async () => {
            try {
                const response = await fetch(`${API_BASE_URL.replace('/api', '')}/api/cars/makes/`);
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        },
        getModels: async (makeId) => {
            try {
                // Assuming the backend supports filtering by make id
                const response = await fetch(`${API_BASE_URL.replace('/api', '')}/api/cars/models/?make_id=${makeId}`);
                return await handleResponse(response);
            } catch (error) {
                return handleApiError(error);
            }
        }
    }
};

// Export the API object
window.api = api;
window.handleApiError = handleApiError; 