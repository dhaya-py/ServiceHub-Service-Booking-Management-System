// Dashboard Component - Reusable for all roles
class DashboardComponent {
    constructor(role) {
        this.role = role;
        this.user = Auth.getUser();
        this.setupMobileMenu();
        this.highlightActiveNav();
        this.setupUserDropdown();
    }

    // Generate sidebar HTML
    static getSidebarHTML(role) {
        const commonNav = `
            <div class="sidebar-header">
                <a href="/index.html" class="sidebar-brand">
                    <div class="sidebar-logo">S</div>
                    <span class="sidebar-title">ServiceHub</span>
                </a>
            </div>
        `;

        const customerNav = `
            <ul class="sidebar-nav">
                <li class="nav-section-title">Main</li>
                <li class="nav-item">
                    <a href="dashboard.html" class="nav-link" data-page="dashboard">
                        <i class="bi bi-grid"></i>
                        <span>Dashboard</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="services.html" class="nav-link" data-page="services">
                        <i class="bi bi-grid-3x3"></i>
                        <span>Browse Services</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="bookings.html" class="nav-link" data-page="bookings">
                        <i class="bi bi-calendar-check"></i>
                        <span>My Bookings</span>
                    </a>
                </li>
                <li class="nav-section-title">Account</li>
                <li class="nav-item">
                    <a href="profile.html" class="nav-link" data-page="profile">
                        <i class="bi bi-person"></i>
                        <span>Profile</span>
                    </a>
                </li>
            </ul>
        `;

        const providerNav = `
            <ul class="sidebar-nav">
                <li class="nav-section-title">Main</li>
                <li class="nav-item">
                    <a href="dashboard.html" class="nav-link" data-page="dashboard">
                        <i class="bi bi-grid"></i>
                        <span>Dashboard</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="bookings.html" class="nav-link" data-page="bookings">
                        <i class="bi bi-calendar-check"></i>
                        <span>Bookings</span>
                    </a>
                </li>
                <li class="nav-section-title">Manage</li>
                <li class="nav-item">
                    <a href="services.html" class="nav-link" data-page="services">
                        <i class="bi bi-briefcase"></i>
                        <span>My Services</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="availability.html" class="nav-link" data-page="availability">
                        <i class="bi bi-clock"></i>
                        <span>Availability</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="reviews.html" class="nav-link" data-page="reviews">
                        <i class="bi bi-star"></i>
                        <span>Reviews</span>
                    </a>
                </li>
                <li class="nav-section-title">Account</li>
                <li class="nav-item">
                    <a href="profile.html" class="nav-link" data-page="profile">
                        <i class="bi bi-person"></i>
                        <span>Profile</span>
                    </a>
                </li>
            </ul>
        `;

        const adminNav = `
            <ul class="sidebar-nav">
                <li class="nav-section-title">Main</li>
                <li class="nav-item">
                    <a href="dashboard.html" class="nav-link" data-page="dashboard">
                        <i class="bi bi-grid"></i>
                        <span>Dashboard</span>
                    </a>
                </li>
                <li class="nav-section-title">Manage</li>
                <li class="nav-item">
                    <a href="users.html" class="nav-link" data-page="users">
                        <i class="bi bi-people"></i>
                        <span>Users</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="providers.html" class="nav-link" data-page="providers">
                        <i class="bi bi-briefcase"></i>
                        <span>Providers</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="services.html" class="nav-link" data-page="services">
                        <i class="bi bi-grid-3x3"></i>
                        <span>Services</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="categories.html" class="nav-link" data-page="categories">
                        <i class="bi bi-tag"></i>
                        <span>Categories</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a href="bookings.html" class="nav-link" data-page="bookings">
                        <i class="bi bi-calendar-check"></i>
                        <span>Bookings</span>
                    </a>
                </li>
            </ul>
        `;

        const footer = `
            <div class="sidebar-footer">
                <a href="#" class="nav-link" id="logoutBtn">
                    <i class="bi bi-box-arrow-right"></i>
                    <span>Logout</span>
                </a>
            </div>
        `;

        const navMap = {
            customer: customerNav,
            provider: providerNav,
            admin: adminNav
        };

        return commonNav + navMap[role] + footer;
    }

    // Generate navbar HTML
    static getNavbarHTML(user, pageTitle = 'Dashboard') {
        const initials = user.email.substring(0, 2).toUpperCase();

        return `
            <button class="mobile-menu-toggle" id="mobileMenuToggle">
                <i class="bi bi-list"></i>
            </button>
            
            <h1 class="navbar-title">${pageTitle}</h1>
            
            <div class="navbar-actions">
                <div class="navbar-notifications">
                    <button class="btn btn-link text-dark">
                        <i class="bi bi-bell fs-5"></i>
                        <span class="notification-badge">3</span>
                    </button>
                </div>
                
                <div class="navbar-user dropdown">
                    <div class="d-flex align-items-center" id="userDropdownToggle" data-bs-toggle="dropdown" aria-expanded="false" style="cursor: pointer;">
                        <div class="user-avatar">${initials}</div>
                        <div class="user-info">
                            <div class="user-name">${user.email}</div>
                            <div class="user-role">${user.role}</div>
                        </div>
                        <i class="bi bi-chevron-down ms-2"></i>
                    </div>
                    <ul class="dropdown-menu dropdown-menu-end shadow border-0" aria-labelledby="userDropdownToggle">
                        <li><a class="dropdown-item py-2" href="${role === 'customer' ? '/pages/customer/profile.html' : role === 'provider' ? '/pages/provider/profile.html' : '#'}"><i class="bi bi-person me-2"></i>My Profile</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item text-danger py-2" href="#" id="navbarLogoutBtn"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
                    </ul>
                </div>
            </div>
        `;
    }

    // Setup mobile menu
    setupMobileMenu() {
        const mobileToggle = document.getElementById('mobileMenuToggle');
        const sidebar = document.querySelector('.sidebar');

        if (mobileToggle && sidebar) {
            // Create overlay
            const overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            document.body.appendChild(overlay);

            mobileToggle.addEventListener('click', () => {
                sidebar.classList.toggle('show');
                overlay.classList.toggle('show');
            });

            overlay.addEventListener('click', () => {
                sidebar.classList.remove('show');
                overlay.classList.remove('show');
            });

            // Close on navigation
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', () => {
                    sidebar.classList.remove('show');
                    overlay.classList.remove('show');
                });
            });
        }
    }

    // Highlight active navigation
    highlightActiveNav() {
        const currentPage = window.location.pathname.split('/').pop();
        document.querySelectorAll('.nav-link').forEach(link => {
            const linkPage = link.getAttribute('href');
            if (linkPage === currentPage) {
                link.classList.add('active');
            }
        });
    }

    // Setup user dropdown
    setupUserDropdown() {
        const logoutBtn = document.getElementById('navbarLogoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                Auth.logout();
            });
        }
    }

    // Setup logout
    static setupLogout() {
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                Auth.logout();
            });
        }
    }

    // Initialize dashboard
    static init(role, pageTitle = 'Dashboard') {
        // Check authentication
        if (!Auth.checkAuth(role)) {
            return;
        }

        const user = Auth.getUser();

        // Inject sidebar
        const sidebarElement = document.querySelector('.sidebar');
        if (sidebarElement) {
            sidebarElement.innerHTML = this.getSidebarHTML(role);
        }

        // Inject navbar
        const navbarElement = document.querySelector('.top-navbar');
        if (navbarElement) {
            navbarElement.innerHTML = this.getNavbarHTML(user, pageTitle);
        }

        // Setup logout
        this.setupLogout();

        // Initialize component
        new DashboardComponent(role);
    }
}
