// Security Configuration and Utilities
class SecurityManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupCSP();
        this.setupXSSProtection();
        this.setupCSRFProtection();
        this.setupInputValidation();
        this.setupRateLimiting();
        this.setupSecureHeaders();
    }

    // Content Security Policy
    setupCSP() {
        const csp = `
            default-src 'self';
            script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
            style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com;
            font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com;
            img-src 'self' data: blob: https:;
            connect-src 'self';
            frame-ancestors 'none';
            base-uri 'self';
            form-action 'self';
        `.replace(/\s+/g, ' ').trim();

        const meta = document.createElement('meta');
        meta.setAttribute('http-equiv', 'Content-Security-Policy');
        meta.setAttribute('content', csp);
        document.head.appendChild(meta);
    }

    // XSS Protection
    setupXSSProtection() {
        // Sanitize all user inputs
        this.sanitizeInputs();
        
        // Add XSS protection header
        const meta = document.createElement('meta');
        meta.setAttribute('http-equiv', 'X-XSS-Protection');
        meta.setAttribute('content', '1; mode=block');
        document.head.appendChild(meta);
    }

    sanitizeInputs() {
        // Override innerHTML to sanitize content
        const originalInnerHTML = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');
        
        Object.defineProperty(Element.prototype, 'innerHTML', {
            set: function(value) {
                const sanitized = SecurityManager.sanitizeHTML(value);
                originalInnerHTML.set.call(this, sanitized);
            },
            get: originalInnerHTML.get
        });
    }

    static sanitizeHTML(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    }

    // CSRF Protection
    setupCSRFProtection() {
        // Generate CSRF token
        const token = this.generateCSRFToken();
        localStorage.setItem('csrf_token', token);
        
        // Add token to all forms
        this.addCSRFTokenToForms();
    }

    generateCSRFToken() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    addCSRFTokenToForms() {
        document.addEventListener('DOMContentLoaded', () => {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                const token = localStorage.getItem('csrf_token');
                if (token && !form.querySelector('input[name="csrf_token"]')) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'csrf_token';
                    input.value = token;
                    form.appendChild(input);
                }
            });
        });
    }

    // Input Validation
    setupInputValidation() {
        this.setupEmailValidation();
        this.setupPasswordValidation();
        this.setupFileValidation();
    }

    setupEmailValidation() {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        
        document.addEventListener('input', (e) => {
            if (e.target.type === 'email') {
                const isValid = emailRegex.test(e.target.value);
                e.target.setCustomValidity(isValid ? '' : 'Please enter a valid email address');
            }
        });
    }

    setupPasswordValidation() {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        
        document.addEventListener('input', (e) => {
            if (e.target.type === 'password' && e.target.id === 'new-password') {
                const isValid = passwordRegex.test(e.target.value);
                e.target.setCustomValidity(isValid ? '' : 
                    'Password must contain at least 8 characters, including uppercase, lowercase, number, and special character');
            }
        });
    }

    setupFileValidation() {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        const maxSize = 5 * 1024 * 1024; // 5MB
        
        document.addEventListener('change', (e) => {
            if (e.target.type === 'file') {
                const file = e.target.files[0];
                if (file) {
                    if (!allowedTypes.includes(file.type)) {
                        e.target.setCustomValidity('Please select a valid image file (JPEG, PNG, GIF, or WebP)');
                        return;
                    }
                    
                    if (file.size > maxSize) {
                        e.target.setCustomValidity('File size must be less than 5MB');
                        return;
                    }
                    
                    e.target.setCustomValidity('');
                }
            }
        });
    }

    // Rate Limiting
    setupRateLimiting() {
        this.rateLimitMap = new Map();
        
        // Rate limit form submissions
        document.addEventListener('submit', (e) => {
            const formId = e.target.id || 'anonymous';
            if (!this.checkRateLimit(formId, 5, 60000)) { // 5 submissions per minute
                e.preventDefault();
                this.showSecurityNotification('Too many requests. Please wait before trying again.', 'warning');
                return false;
            }
        });
    }

    checkRateLimit(key, maxRequests, windowMs) {
        const now = Date.now();
        const requests = this.rateLimitMap.get(key) || [];
        
        // Remove old requests outside the window
        const validRequests = requests.filter(time => now - time < windowMs);
        
        if (validRequests.length >= maxRequests) {
            return false;
        }
        
        validRequests.push(now);
        this.rateLimitMap.set(key, validRequests);
        return true;
    }

    // Secure Headers
    setupSecureHeaders() {
        const headers = [
            { name: 'X-Content-Type-Options', value: 'nosniff' },
            { name: 'X-Frame-Options', value: 'DENY' },
            { name: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
            { name: 'Permissions-Policy', value: 'geolocation=(), microphone=(), camera=()' }
        ];

        headers.forEach(header => {
            const meta = document.createElement('meta');
            meta.setAttribute('http-equiv', header.name);
            meta.setAttribute('content', header.value);
            document.head.appendChild(meta);
        });
    }

    // Security Notifications
    showSecurityNotification(message, type = 'warning') {
        const notification = document.createElement('div');
        notification.className = `security-notification ${type}`;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-shield-alt"></i>
                <span>${message}</span>
            </div>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'error' ? '#dc2626' : type === 'warning' ? '#f59e0b' : '#10b981'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            max-width: 500px;
            animation: slideInDown 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // Data Encryption
    static encrypt(data, key) {
        // Simple encryption for sensitive data (in production, use proper encryption)
        const encoded = btoa(JSON.stringify(data));
        return encoded;
    }

    static decrypt(encryptedData, key) {
        try {
            const decoded = atob(encryptedData);
            return JSON.parse(decoded);
        } catch (e) {
            return null;
        }
    }

    // Session Security
    setupSessionSecurity() {
        // Auto-logout after inactivity
        let inactivityTimer;
        const resetTimer = () => {
            clearTimeout(inactivityTimer);
            inactivityTimer = setTimeout(() => {
                this.logout('Session expired due to inactivity');
            }, 30 * 60 * 1000); // 30 minutes
        };

        ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
            document.addEventListener(event, resetTimer, true);
        });

        resetTimer();
    }

    logout(reason) {
        // Clear sensitive data
        localStorage.removeItem('admin_token');
        localStorage.removeItem('admin_user');
        localStorage.removeItem('csrf_token');
        
        // Redirect to login
        if (window.location.pathname.includes('admin')) {
            window.location.href = 'admin.html';
        }
        
        this.showSecurityNotification(`Logged out: ${reason}`, 'info');
    }

    // Audit Logging
    logSecurityEvent(event, details = {}) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            event,
            details,
            userAgent: navigator.userAgent,
            url: window.location.href,
            ip: 'client-side' // In production, this would be server-side
        };

        const logs = JSON.parse(localStorage.getItem('security_logs') || '[]');
        logs.push(logEntry);
        
        // Keep only last 100 logs
        if (logs.length > 100) {
            logs.splice(0, logs.length - 100);
        }
        
        localStorage.setItem('security_logs', JSON.stringify(logs));
    }
}

// Initialize security manager
const securityManager = new SecurityManager();

// Add CSS for security notifications
const securityStyles = document.createElement('style');
securityStyles.textContent = `
    @keyframes slideInDown {
        from {
            transform: translateX(-50%) translateY(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }
    }
    
    .security-notification {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
`;
document.head.appendChild(securityStyles);
