// Authentication utilities
class Auth {
    static async login(email, password) {
        try {
            // ✅ FIXED: Backend uses OAuth2PasswordRequestForm with 'username' field
            const formData = new URLSearchParams();
            formData.append('username', email);  // OAuth2 standard uses 'username'
            formData.append('password', password);
            
            const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.LOGIN}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',  // OAuth2 format
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw {
                    status: response.status,
                    message: data.detail || 'Login failed'
                };
            }
            
            // Store token
            api.setToken(data.access_token);
            
            // Get user details
            const user = await this.getCurrentUser();
            this.setUser(user);
            return user;
        } catch (error) {
            throw error;
        }
    }

    static async register(email, password, role = USER_ROLES.CUSTOMER, name = null) {
        try {
            // ✅ FIXED: Backend requires 'name' field (not optional)
            const userName = name || email.split('@')[0];
            
            const data = await api.post(API_ENDPOINTS.REGISTER, {
                email,
                name: userName,  // ✅ Required by backend
                password
                // ✅ NOTE: Backend doesn't accept 'role' in registration - defaults to 'customer'
            }, false);
            return data;
        } catch (error) {
            throw error;
        }
    }

    static async getCurrentUser() {
        try {
            const user = await api.get(API_ENDPOINTS.ME);
            return user;
        } catch (error) {
            throw error;
        }
    }

    static logout() {
        api.removeToken();
        window.location.href = '/pages/login.html';
    }

    static isAuthenticated() {
        return !!api.getToken();
    }

    static getUser() {
        const userStr = localStorage.getItem(STORAGE_KEYS.USER);
        return userStr ? JSON.parse(userStr) : null;
    }

    static setUser(user) {
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    }

    static hasRole(role) {
        const user = this.getUser();
        return user && user.role === role;
    }

    static redirectToDashboard(role) {
        const dashboardMap = {
            [USER_ROLES.ADMIN]: '/pages/admin/dashboard.html',
            [USER_ROLES.PROVIDER]: '/pages/provider/dashboard.html',
            [USER_ROLES.CUSTOMER]: '/pages/customer/dashboard.html'
        };
        window.location.href = dashboardMap[role] || '/pages/customer/dashboard.html';
    }

    static checkAuth(requiredRole = null) {
        if (!this.isAuthenticated()) {
            window.location.href = '/pages/login.html';
            return false;
        }

        if (requiredRole) {
            const user = this.getUser();
            if (!user || user.role !== requiredRole) {
                alert('Access denied. Insufficient permissions.');
                this.redirectToDashboard(user?.role);
                return false;
            }
        }

        return true;
    }
}
