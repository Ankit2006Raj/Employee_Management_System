/**
 * Employee Management System - Main JavaScript
 * Professional Interactive Features
 */

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {
    initAlerts();
    initFormValidation();
    initTooltips();
    initSearchFeatures();
    initTableFeatures();
    initAnimations();
    initThemeToggle();
    initLoadingStates();
}

// ============================================
// ALERT MANAGEMENT
// ============================================
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        // Auto-dismiss after 5 seconds
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
}

// ============================================
// FORM VALIDATION & ENHANCEMENT
// ============================================
function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        // Add loading state on submit
        form.addEventListener('submit', function (e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('no-loading')) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });

        // Bootstrap validation
        if (form.classList.contains('needs-validation')) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        }
    });

    // Real-time validation feedback
    const inputs = document.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.addEventListener('blur', function () {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
}

// ============================================
// TOOLTIPS & POPOVERS
// ============================================
function initTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ============================================
// SEARCH FEATURES
// ============================================
function initSearchFeatures() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');

    searchInputs.forEach(input => {
        // Add search icon
        if (!input.parentElement.classList.contains('search-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'search-wrapper position-relative';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            const icon = document.createElement('i');
            icon.className = 'bi bi-search position-absolute';
            icon.style.cssText = 'left: 1rem; top: 50%; transform: translateY(-50%); color: var(--gray-400);';
            wrapper.appendChild(icon);

            input.style.paddingLeft = '2.5rem';
        }

        // Add clear button
        input.addEventListener('input', function () {
            if (this.value.length > 0 && !this.nextElementSibling?.classList.contains('clear-search')) {
                const clearBtn = document.createElement('button');
                clearBtn.type = 'button';
                clearBtn.className = 'clear-search btn btn-sm position-absolute';
                clearBtn.innerHTML = '<i class="bi bi-x-circle-fill"></i>';
                clearBtn.style.cssText = 'right: 0.5rem; top: 50%; transform: translateY(-50%); border: none; background: transparent; color: var(--gray-400);';
                clearBtn.onclick = function () {
                    input.value = '';
                    this.remove();
                    input.focus();
                };
                this.parentElement.appendChild(clearBtn);
            } else if (this.value.length === 0 && this.nextElementSibling?.classList.contains('clear-search')) {
                this.nextElementSibling.remove();
            }
        });
    });
}

// ============================================
// TABLE FEATURES
// ============================================
function initTableFeatures() {
    const tables = document.querySelectorAll('.table');

    tables.forEach(table => {
        // Add row hover effect
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function (e) {
                // Don't trigger if clicking on a button or link
                if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A' && !e.target.closest('button') && !e.target.closest('a')) {
                    const link = this.querySelector('a');
                    if (link) {
                        window.location.href = link.href;
                    }
                }
            });
        });

        // Add sorting capability (if not already implemented)
        const headers = table.querySelectorAll('thead th');
        headers.forEach((header, index) => {
            if (!header.querySelector('.sort-icon') && header.textContent.trim()) {
                header.style.cursor = 'pointer';
                header.classList.add('sortable');

                const sortIcon = document.createElement('i');
                sortIcon.className = 'bi bi-arrow-down-up ms-2 sort-icon text-muted';
                sortIcon.style.fontSize = '0.75rem';
                header.appendChild(sortIcon);
            }
        });
    });

    // Add table search/filter
    addTableSearch();
}

function addTableSearch() {
    const tables = document.querySelectorAll('.table');

    tables.forEach(table => {
        const searchInput = table.closest('.card')?.querySelector('input[type="search"]');
        if (searchInput) {
            searchInput.addEventListener('input', function () {
                const searchTerm = this.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');

                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                        row.classList.add('animate__animated', 'animate__fadeIn', 'animate__faster');
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        }
    });
}

// ============================================
// ANIMATIONS
// ============================================
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards
    const cards = document.querySelectorAll('.card:not(.stat-card)');
    cards.forEach(card => {
        observer.observe(card);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ============================================
// THEME TOGGLE (Optional Dark Mode)
// ============================================
function initThemeToggle() {
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Create theme toggle button (optional)
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const theme = document.documentElement.getAttribute('data-theme');
            const newTheme = theme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);

            // Update icon
            const icon = this.querySelector('i');
            if (icon) {
                icon.className = newTheme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
            }
        });
    }
}

// ============================================
// LOADING STATES
// ============================================
function initLoadingStates() {
    // Show loading spinner for page navigation
    const links = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"]):not(.no-loading)');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            if (this.href && !this.href.includes('javascript:')) {
                showPageLoader();
            }
        });
    });
}

function showPageLoader() {
    const loader = document.createElement('div');
    loader.id = 'page-loader';
    loader.innerHTML = `
        <div class="d-flex justify-content-center align-items-center" style="height: 100vh; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255, 255, 255, 0.9); z-index: 9999;">
            <div class="text-center">
                <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">Loading...</p>
            </div>
        </div>
    `;
    document.body.appendChild(loader);

    // Remove after 5 seconds as fallback
    setTimeout(() => {
        const loaderEl = document.getElementById('page-loader');
        if (loaderEl) loaderEl.remove();
    }, 5000);
}

// ============================================
// CONFIRMATION DIALOGS
// ============================================
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item? This action cannot be undone.');
}

// Add to delete buttons
document.querySelectorAll('a[href*="delete"], button[class*="delete"]').forEach(element => {
    element.addEventListener('click', function (e) {
        if (!confirmDelete()) {
            e.preventDefault();
        }
    });
});

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        showToast('Copied to clipboard!', 'success');
    }, function (err) {
        showToast('Failed to copy', 'error');
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3 animate__animated animate__slideInRight`;
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}-fill me-2"></i>
        ${message}
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('animate__slideOutRight');
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// ============================================
// EXPORT FUNCTIONS
// ============================================
window.EMS = {
    copyToClipboard,
    showToast,
    formatCurrency,
    formatDate,
    confirmDelete,
    showPageLoader
};

// ============================================
// PERFORMANCE MONITORING
// ============================================
if (window.performance) {
    window.addEventListener('load', function () {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`Page loaded in ${pageLoadTime}ms`);
    });
}
