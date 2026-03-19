// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';

const API_ENDPOINTS = {
    // Auth
    REGISTER: '/api/auth/register',
    LOGIN: '/api/auth/token',
    ME: '/api/auth/me',
    
    // Categories
    CATEGORIES: '/categories/',
    CATEGORY_BY_ID: (id) => `/categories/${id}`,
    
    // Services (public)
    SERVICES: '/services',
    SERVICE_BY_ID: (id) => `/services/${id}`,
    SEARCH_SERVICES: '/search/services',
    SERVICES_BY_CATEGORY: (categoryId) => `/services/category/${categoryId}`,
    
    // Services (provider)
    PROVIDER_SERVICES: '/services/provider/services',
    PROVIDER_SERVICE_BY_ID: (id) => `/services/provider/services/${id}`,
    
    // Bookings (customer)
    CREATE_BOOKING: '/bookings/customer',
    CUSTOMER_BOOKINGS: '/bookings/customer/me',
    CANCEL_BOOKING: (id) => `/bookings/${id}/cancel`,
    
    // Bookings (provider)
    PROVIDER_BOOKINGS: '/bookings/provider/me',
    ACCEPT_BOOKING: (id) => `/bookings/${id}/accept`,
    REJECT_BOOKING: (id) => `/bookings/${id}/reject`,
    COMPLETE_BOOKING: (id) => `/bookings/${id}/complete`,
    
    // Bookings (admin)
    ADMIN_BOOKINGS: '/bookings/admin/all',
    ADMIN_BOOKING_STATUS: (id) => `/admin/bookings/${id}/status`,
    
    // Availability
    PROVIDER_AVAILABILITY: '/availability/provider/weekly',
    PROVIDER_TIMEOFF: '/availability/provider/timeoff',
    PROVIDER_SLOTS: (providerId) => `/availability/provider/${providerId}/slots`,
    
    // Reviews
    REVIEWS: '/reviews/',
    PROVIDER_REVIEWS: (providerId) => `/reviews/provider/${providerId}`,
    
    // Provider management
    PROVIDERS_LIST: '/providers/',
    PROVIDER_BY_ID: (id) => `/providers/${id}`,
    PROVIDER_ME: '/providers/me',
    
    // Dashboards
    ADMIN_SUMMARY: '/admin/summary',
    ADMIN_DASHBOARD: '/admin/dashboard',
    ADMIN_DASHBOARD_ADVANCED: '/admin/dashboard/advanced',
    PROVIDER_DASHBOARD: '/provider/dashboard/summary',
    PROVIDER_EARNINGS: '/provider/dashboard/earnings',
    PROVIDER_BOOKING_STATS: '/provider/dashboard/bookings/stats',
    PROVIDER_REVIEWS_SUMMARY: '/provider/dashboard/reviews',
    PROVIDER_ACTIVITY: '/provider/dashboard/activity',
    CUSTOMER_DASHBOARD: '/customer/dashboard',
    CUSTOMER_DASHBOARD_ADVANCED: '/customer/dashboard/advanced',
    
    // Admin Operations
    ADMIN_USERS: '/admin/users',
    ADMIN_USER_ACTIVATE: (id) => `/admin/users/${id}/activate`,
    ADMIN_APPROVE_PROVIDER: (id) => `/admin/providers/${id}/approve`,
    ADMIN_SERVICES: '/admin/services',
    ADMIN_SERVICE_TOGGLE: (id) => `/admin/services/${id}/toggle`,
    ADMIN_DELETE_REVIEW: (id) => `/admin/reviews/${id}`,
    ADMIN_BOOKINGS_LIST: '/admin/bookings'
};

// User roles
const USER_ROLES = {
    CUSTOMER: 'customer',
    PROVIDER: 'provider',
    ADMIN: 'admin'
};

// Booking statuses
const BOOKING_STATUS = {
    PENDING: 'pending',
    ACCEPTED: 'accepted',
    REJECTED: 'rejected',
    COMPLETED: 'completed',
    CANCELLED: 'cancelled'
};

// Storage keys
const STORAGE_KEYS = {
    TOKEN: 'servicehub_token',
    USER: 'servicehub_user'
};
