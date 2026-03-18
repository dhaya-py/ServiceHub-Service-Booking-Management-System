// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';  // ✅ FIXED: No /api prefix

const API_ENDPOINTS = {
    // Auth - Only routes with /api/auth prefix
    REGISTER: '/api/auth/register',
    LOGIN: '/api/auth/token',
    ME: '/api/auth/me',  // ✅ FIXED: Was /me, now /api/auth/me
    
    // Categories
    CATEGORIES: '/categories',
    CATEGORY_BY_ID: (id) => `/categories/${id}`,
    
    // Services
    SERVICES: '/services',
    SERVICE_BY_ID: (id) => `/services/${id}`,
    PROVIDER_SERVICES: '/services',  // ✅ FIXED: Same as SERVICES
    SEARCH_SERVICES: '/search/services',
    
    // Bookings
    BOOKINGS: '/bookings',
    CREATE_BOOKING: '/bookings/customer',  // ✅ FIXED: Specific endpoint
    BOOKING_BY_ID: (id) => `/bookings/${id}`,
    CANCEL_BOOKING: (id) => `/bookings/${id}/cancel`,
    CUSTOMER_BOOKINGS: '/bookings/customer/me',  // ✅ FIXED: Matches backend
    PROVIDER_BOOKINGS: '/bookings/provider/me',  // ✅ FIXED: Matches backend
    ACCEPT_BOOKING: (id) => `/bookings/provider/${id}/accept`,  // ✅ FIXED
    REJECT_BOOKING: (id) => `/bookings/provider/${id}/reject`,  // ✅ FIXED
    COMPLETE_BOOKING: (id) => `/bookings/provider/${id}/complete`,  // ✅ FIXED
    
    // Availability
    PROVIDER_AVAILABILITY: '/availability/provider',
    PROVIDER_TIMEOFF: '/availability/provider/timeoff',
    PROVIDER_SLOTS: (providerId) => `/availability/provider/${providerId}/slots`,
    
    // Reviews
    REVIEWS: '/reviews',
    PROVIDER_REVIEWS: (providerId) => `/reviews/provider/${providerId}`,
    SERVICE_REVIEWS: (serviceId) => `/reviews/service/${serviceId}`,
    
    // Dashboards
    ADMIN_SUMMARY: '/admin/summary',
    ADMIN_DASHBOARD: '/admin/dashboard',  // ✅ FIXED: Was /admin/dashboard/advanced
    ADMIN_DASHBOARD_ADVANCED: '/admin/dashboard/advanced',
    PROVIDER_DASHBOARD: '/provider/dashboard/summary',
    PROVIDER_EARNINGS: '/provider/dashboard/earnings',
    PROVIDER_BOOKING_STATS: '/provider/dashboard/bookings/stats',
    PROVIDER_REVIEWS_SUMMARY: '/provider/dashboard/reviews',
    CUSTOMER_DASHBOARD: '/customer/dashboard',
    CUSTOMER_DASHBOARD_ADVANCED: '/customer/dashboard/advanced',
    
    // Admin Operations
    ADMIN_USERS: '/admin/users',
    ADMIN_USER_BY_ID: (id) => `/admin/users/${id}`,
    ADMIN_USER_STATUS: (id) => `/admin/users/${id}/status`,
    ADMIN_APPROVE_PROVIDER: (id) => `/providers/${id}/approve`  // ✅ FIXED: /providers not /admin/providers
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
