// Map initialization and management
class MerchantMap {
    constructor(elementId) {
        this.mapElement = document.getElementById(elementId);
        this.map = null;
        this.markers = [];
        this.loading = false;
        this.error = null;
        this.currentLocation = null;
        this.defaultRadius = 50; // Increased default radius to 50km
        this.init();
    }

    init() {
        try {
            // Initialize the map with a default view
            this.map = L.map(this.mapElement).setView([30.0444, 31.2357], 10); // Zoomed out to show more area
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(this.map);

            // Add error handling for map events
            this.map.on('error', (e) => {
                console.error('Map error:', e);
                this.showError('Failed to load map. Please try refreshing the page.');
            });

            // Add loading indicator
            this.showLoading();

            // Load initial merchants
            this.loadMerchants();

            // Initialize location button
            this.initLocationButton();
        } catch (error) {
            console.error('Failed to initialize map:', error);
            this.showError('Failed to initialize map. Please try refreshing the page.');
        }
    }

    initLocationButton() {
        const useLocationButton = document.getElementById('use-location');
        if (useLocationButton) {
            useLocationButton.addEventListener('click', async () => {
                if (navigator.geolocation) {
                    try {
                        useLocationButton.disabled = true;
                        useLocationButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting Location...';
                        
                        const position = await new Promise((resolve, reject) => {
                            navigator.geolocation.getCurrentPosition(resolve, reject);
                        });

                        this.currentLocation = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        };
                        // Center map on user's location
                        this.map.setView([this.currentLocation.lat, this.currentLocation.lng], 12);
                        // Update merchants
                        await this.updateNearbyMerchants();
                    } catch (error) {
                        console.error('Geolocation error:', error);
                        this.showError('Error getting your location: ' + error.message);
                        // If geolocation fails, show all merchants
                        await this.loadMerchants();
                    } finally {
                        useLocationButton.disabled = false;
                        useLocationButton.innerHTML = '<i class="fas fa-location-dot"></i> Use My Location';
                    }
                } else {
                    this.showError('Geolocation is not supported by your browser');
                    // If geolocation is not supported, show all merchants
                    await this.loadMerchants();
                }
            });
        }
    }

    showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'map-loading';
        loadingDiv.innerHTML = '<div class="spinner"></div>';
        this.mapElement.appendChild(loadingDiv);
    }

    hideLoading() {
        const loadingDiv = this.mapElement.querySelector('.map-loading');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'map-error';
        errorDiv.textContent = message;
        this.mapElement.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }

    async loadMerchants(filters = {}) {
        try {
            this.loading = true;
            const merchants = await api.merchants.getAll(filters);
            
            if (!merchants || merchants.length === 0) {
                console.warn('No merchants found');
                this.showError('No merchants found in your area. Try increasing the search radius or check back later.');
                return;
            }

            this.addMerchantMarkers(merchants, filters);
        } catch (error) {
            console.error('Failed to load merchants:', error);
            this.showError('Failed to load merchants. Please try again later.');
        } finally {
            this.loading = false;
            this.hideLoading();
        }
    }

    // Haversine formula to calculate distance between two lat/lng points in km
    haversineDistance(lat1, lng1, lat2, lng2) {
        function toRad(x) { return x * Math.PI / 180; }
        const R = 6371; // km
        const dLat = toRad(lat2 - lat1);
        const dLng = toRad(lng2 - lng1);
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
                  Math.sin(dLng/2) * Math.sin(dLng/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    addMerchantMarkers(merchants, filters = {}) {
        if (!Array.isArray(merchants)) {
            console.warn('Invalid merchants data:', merchants);
            return;
        }

        this.clearMarkers();
        const bounds = L.latLngBounds();
        let validLocations = 0;
        const filterByLocation = filters && filters.lat && filters.lng && filters.radius;
        const userLat = filterByLocation ? parseFloat(filters.lat) : null;
        const userLng = filterByLocation ? parseFloat(filters.lng) : null;
        const radius = filterByLocation ? parseFloat(filters.radius) : null;

        merchants.forEach(merchant => {
            // Plot merchant main location (if within radius or not filtering by location)
            let plotMerchant = true;
            if (filterByLocation && merchant.latitude && merchant.longitude) {
                const dist = this.haversineDistance(userLat, userLng, parseFloat(merchant.latitude), parseFloat(merchant.longitude));
                plotMerchant = dist <= radius;
            }
            if (!filterByLocation || plotMerchant) {
                if (merchant.latitude && merchant.longitude) {
                    const marker = this.addMerchantMarker(merchant);
                    if (marker) {
                        bounds.extend(marker.getLatLng());
                        validLocations++;
                    }
                }
            }
            // Plot all branch locations (only those within radius if filtering)
            if (merchant.branches && Array.isArray(merchant.branches)) {
                merchant.branches.forEach(branch => {
                    if (branch.latitude && branch.longitude) {
                        let plotBranch = true;
                        if (filterByLocation) {
                            const dist = this.haversineDistance(userLat, userLng, parseFloat(branch.latitude), parseFloat(branch.longitude));
                            plotBranch = dist <= radius;
                        }
                        if (plotBranch) {
                            const marker = this.addBranchMarker(branch, merchant);
                            if (marker) {
                                bounds.extend(marker.getLatLng());
                                validLocations++;
                            }
                        }
                    }
                });
            }
        });

        if (validLocations > 0) {
            if (bounds.isValid()) {
                this.map.fitBounds(bounds, { padding: [50, 50] });
            }
        } else {
            console.warn('No valid merchant or branch locations to display');
            this.showError('No merchants or branches with valid locations found. Please try again later.');
        }
    }

    addMerchantMarker(merchant) {
        try {
            const marker = L.marker([merchant.latitude, merchant.longitude])
                .bindPopup(this.createMerchantPopup(merchant));
            marker.addTo(this.map);
            this.markers.push(marker);
            return marker;
        } catch (error) {
            console.error('Failed to add merchant marker:', error);
            return null;
        }
    }

    createMerchantPopup(merchant) {
        const popupContent = document.createElement('div');
        popupContent.className = 'merchant-popup';

        // Add logo if available
        if (merchant.logo_url) {
            const logo = document.createElement('img');
            logo.src = merchant.logo_url;
            logo.alt = merchant.name;
            logo.className = 'merchant-logo';
            popupContent.appendChild(logo);
        }

        // Add merchant name
        const name = document.createElement('h3');
        name.textContent = merchant.name;
        popupContent.appendChild(name);

        // Add rating if available
        if (merchant.rating) {
            const rating = document.createElement('div');
            rating.className = 'merchant-rating';
            rating.innerHTML = this.createRatingStars(merchant.rating);
            popupContent.appendChild(rating);
        }

        // Add address
        if (merchant.address_text) {
            const address = document.createElement('p');
            address.textContent = merchant.address_text;
            popupContent.appendChild(address);
        }

        // Add distance if available
        if (merchant.distance) {
            const distance = document.createElement('p');
            distance.className = 'merchant-distance';
            distance.textContent = `Distance: ${merchant.distance.toFixed(1)} km`;
            popupContent.appendChild(distance);
        }

        // Add social media links
        if (merchant.social_media) {
            const socialLinks = document.createElement('div');
            socialLinks.className = 'merchant-social';
            Object.entries(merchant.social_media).forEach(([platform, url]) => {
                if (url) {
                    const link = document.createElement('a');
                    link.href = url;
                    link.target = '_blank';
                    link.className = `social-link ${platform}`;
                    link.innerHTML = `<i class="fab fa-${platform}"></i>`;
                    socialLinks.appendChild(link);
                }
            });
            if (socialLinks.children.length > 0) {
                popupContent.appendChild(socialLinks);
            }
        }

        return popupContent;
    }

    createRatingStars(rating) {
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

        let stars = '';
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star"></i>';
        }
        if (halfStar) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        }
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="far fa-star"></i>';
        }
        return stars;
    }

    addBranchMarker(branch, merchant) {
        try {
            // Convert to numbers if they are strings
            const lat = typeof branch.latitude === 'string' ? parseFloat(branch.latitude) : branch.latitude;
            const lng = typeof branch.longitude === 'string' ? parseFloat(branch.longitude) : branch.longitude;
            if (!lat || !lng) return null; // skip if invalid

            const marker = L.marker([lat, lng])
                .bindPopup(this.createBranchPopup(branch, merchant));
            marker.addTo(this.map);
            this.markers.push(marker);
            return marker;
        } catch (error) {
            console.error('Failed to add branch marker:', error);
            return null;
        }
    }

    createBranchPopup(branch, merchant) {
        const popupContent = document.createElement('div');
        popupContent.className = 'merchant-popup';

        // Add merchant logo if available
        if (merchant.logo_url) {
            const logo = document.createElement('img');
            logo.src = merchant.logo_url;
            logo.alt = merchant.name;
            logo.className = 'merchant-logo';
            popupContent.appendChild(logo);
        }

        // Add merchant name
        const name = document.createElement('h3');
        name.textContent = merchant.name;
        popupContent.appendChild(name);

        // Add branch name
        const branchName = document.createElement('div');
        branchName.className = 'branch-name';
        branchName.innerHTML = `<strong>Branch:</strong> ${branch.name}`;
        popupContent.appendChild(branchName);

        // Add rating if available
        if (merchant.rating) {
            const rating = document.createElement('div');
            rating.className = 'merchant-rating';
            rating.innerHTML = this.createRatingStars(merchant.rating);
            popupContent.appendChild(rating);
        }

        // Add branch address
        if (branch.address_text) {
            const address = document.createElement('p');
            address.textContent = branch.address_text;
            popupContent.appendChild(address);
        }

        // Add branch phone
        if (branch.contact_phone) {
            const phone = document.createElement('p');
            phone.innerHTML = `<i class="fas fa-phone-alt"></i> <a href="tel:${branch.contact_phone}">${branch.contact_phone}</a>`;
            popupContent.appendChild(phone);
        }

        // Add social media links (from merchant)
        if (merchant.social_media) {
            const socialLinks = document.createElement('div');
            socialLinks.className = 'merchant-social';
            Object.entries(merchant.social_media).forEach(([platform, url]) => {
                if (url) {
                    const link = document.createElement('a');
                    link.href = url;
                    link.target = '_blank';
                    link.className = `social-link ${platform}`;
                    link.innerHTML = `<i class="fab fa-${platform}"></i>`;
                    socialLinks.appendChild(link);
                }
            });
            if (socialLinks.children.length > 0) {
                popupContent.appendChild(socialLinks);
            }
        }

        return popupContent;
    }

    clearMarkers() {
        this.markers.forEach(marker => marker.remove());
        this.markers = [];
    }

    async getNearbyMerchants(lat, lng, radius = this.defaultRadius) {
        try {
            return await api.merchants.getNearby(lat, lng, radius);
        } catch (error) {
            console.error('Failed to get nearby merchants:', error);
            this.showError('Failed to find nearby merchants. Showing all merchants instead.');
            return await api.merchants.getAll();
        }
    }

    async updateNearbyMerchants() {
        if (!this.currentLocation) {
            await this.loadMerchants();
            return;
        }

        try {
            this.loading = true;
            const merchants = await this.getNearbyMerchants(
                this.currentLocation.lat,
                this.currentLocation.lng
            );
            
            if (!merchants || merchants.length === 0) {
                console.warn('No nearby merchants found');
                this.showError('No merchants found nearby. Try increasing the search radius or check back later.');
                return;
            }

            this.addMerchantMarkers(merchants);
        } catch (error) {
            console.error('Failed to update nearby merchants:', error);
            this.showError('Failed to find nearby merchants. Showing all merchants instead.');
            await this.loadMerchants();
        } finally {
            this.loading = false;
            this.hideLoading();
        }
    }
}

// Helper for logging
async function loadMerchantsWithLog(filters) {
    console.log('Calling loadMerchants with filters:', filters);
    await window.merchantMap.loadMerchants(filters);
}

// Initialize map when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('merchant-map');
    if (mapElement) {
        window.merchantMap = new MerchantMap('merchant-map');

        // Filter controls
        const categoryFilter = document.getElementById('category-filter');
        const radiusFilter = document.getElementById('radius-filter');
        const updateBtn = document.getElementById('update-merchants');
        const useLocationBtn = document.getElementById('use-location');
        const radiusValue = document.getElementById('radius-value');

        // Prevent multiple updates during geolocation
        let isUpdatingLocation = false;
        let hasUsedLocation = false;

        // Update radius value display
        if (radiusFilter && radiusValue) {
            radiusFilter.addEventListener('input', () => {
                radiusValue.textContent = `${radiusFilter.value} km`;
            });
        }

        // Helper to get current filter values
        function getFilters() {
            const filters = {};
            if (categoryFilter && categoryFilter.value) filters.category = categoryFilter.value;
            if (radiusFilter && radiusFilter.value) filters.radius = radiusFilter.value;
            if (window.merchantMap.currentLocation) {
                filters.lat = window.merchantMap.currentLocation.lat;
                filters.lng = window.merchantMap.currentLocation.lng;
            }
            return filters;
        }

        // Only load merchants on page load if user hasn't used location
        if (!hasUsedLocation) {
            loadMerchantsWithLog(getFilters());
        }

        // Update map on filter change
        if (updateBtn) {
            updateBtn.addEventListener('click', async () => {
                if (!isUpdatingLocation) await loadMerchantsWithLog(getFilters());
            });
        }
        if (categoryFilter) {
            categoryFilter.addEventListener('change', async () => {
                if (!isUpdatingLocation) await loadMerchantsWithLog(getFilters());
            });
        }
        if (radiusFilter) {
            radiusFilter.addEventListener('change', async () => {
                if (!isUpdatingLocation) await loadMerchantsWithLog(getFilters());
            });
        }
        if (useLocationBtn) {
            useLocationBtn.addEventListener('click', async () => {
                if (navigator.geolocation) {
                    isUpdatingLocation = true;
                    hasUsedLocation = true;
                    useLocationBtn.disabled = true;
                    useLocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting Location...';
                    try {
                        const position = await new Promise((resolve, reject) => {
                            navigator.geolocation.getCurrentPosition(resolve, reject);
                        });
                        window.merchantMap.currentLocation = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        };
                        window.merchantMap.map.setView([position.coords.latitude, position.coords.longitude], 12);
                        await loadMerchantsWithLog(getFilters());
                    } catch (error) {
                        window.merchantMap.showError('Error getting your location: ' + error.message);
                        await loadMerchantsWithLog(getFilters());
                    } finally {
                        useLocationBtn.disabled = false;
                        useLocationBtn.innerHTML = '<i class="fas fa-location-dot"></i> Use My Location';
                        setTimeout(() => { isUpdatingLocation = false; }, 500); // allow updates after a short delay
                    }
                }
            });
        }
    }
}); 