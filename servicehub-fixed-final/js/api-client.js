// API Client - Handles all HTTP requests
class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    getToken() {
        return localStorage.getItem(STORAGE_KEYS.TOKEN);
    }

    setToken(token) {
        localStorage.setItem(STORAGE_KEYS.TOKEN, token);
    }

    removeToken() {
        localStorage.removeItem(STORAGE_KEYS.TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER);
    }

    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (includeAuth) {
            const token = this.getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }

        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: this.getHeaders(options.includeAuth !== false)
        };

        try {
            const response = await fetch(url, config);

            // Handle 204 No Content (e.g., DELETE responses)
            if (response.status === 204) {
                return { success: true };
            }

            // Try to parse JSON, but handle empty responses
            let data;
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                const text = await response.text();
                try {
                    data = JSON.parse(text);
                } catch {
                    data = { message: text || 'Success' };
                }
            }

            if (!response.ok) {
                throw {
                    status: response.status,
                    message: data.detail || data.message || 'An error occurred',
                    data: data
                };
            }

            return data;
        } catch (error) {
            if (error.status === 401) {
                this.removeToken();
                window.location.href = '/pages/login.html';
            }
            throw error;
        }
    }

    async get(endpoint, params = {}, includeAuth = true) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        return this.request(url, { method: 'GET', includeAuth });
    }

    async post(endpoint, data = {}, includeAuth = true) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
            includeAuth
        });
    }

    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }

    async patch(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }
}

// Global API instance
const api = new APIClient();