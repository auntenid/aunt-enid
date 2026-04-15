// Clean, working version of script.js for Read Story functionality

// Article reading functions for static articles - optimized for speed
function readMuseveniArticle() {
    console.log('Opening Museveni nomination article...');
    // Direct navigation without redirects for faster loading
    window.location.href = '/president-museveni-historic-nomination/';
}

function readBuharaArticle() {
    console.log('Opening Buhara article...');
    // Direct navigation without redirects for faster loading
    window.location.href = '/clarification-on-false-reports-circulating-online/';
}

function readCampaignArticle() {
    console.log('Opening Campaign article...');
    // Direct navigation without redirects for faster loading
    window.location.href = '/successful-campaign-rally-in-kabale-town/';
}

function readWomenArticle() {
    console.log('Opening Women article...');
    // Direct navigation without redirects for faster loading
    window.location.href = '/women-empowerment-workshop-launched/';
}

function readYouthArticle() {
    console.log('Opening Youth article...');
    // Direct navigation without redirects for faster loading
    window.location.href = '/youth-engagement-forum/';
}

function readAuntEnidStoryArticle() {
    console.log('Opening Aunt Enid Story article...');
    // Direct navigation without redirects for faster loading
    window.location.href = '/the-lasting-case-for-aunt-enid/';
}

// Share article with preview - optimized for social media crawlers
function shareArticleWithPreview(title, excerpt, imageUrl, articleId = '') {
    try {
        console.log('Sharing article:', title);
        
        // Validate inputs
        if (!title || !excerpt) {
            throw new Error('Missing title or excerpt');
        }
        
        // Create article-specific URL (direct link to article page)
        const articleUrl = createArticleUrl(title, articleId);
        
        // Create share data with proper URL
        const shareData = {
            title: title,
            text: excerpt,
            url: articleUrl
        };
        
        // Check if Web Share API is supported
        if (navigator.share) {
            navigator.share(shareData)
                .then(() => {
                    showNotification('Article shared successfully!', 'success');
                })
                .catch((error) => {
                    console.log('Error sharing:', error);
                    fallbackShare(shareData);
                });
        } else {
            fallbackShare(shareData);
        }
    } catch (error) {
        console.error('Error in shareArticleWithPreview:', error);
        alert('Error sharing article. Please try again.');
    }
}

// Share using a provided absolute URL
function shareDirect(url, title, text) {
    const shareData = { title: title || document.title, text: text || '', url };
    if (navigator.share) {
        navigator.share(shareData).catch(() => fallbackShare(shareData));
    } else {
        fallbackShare(shareData);
    }
}

// Create a proper article URL for sharing - optimized for social media crawlers
function createArticleUrl(title, articleId = '') {
    try {
        // Extract the base URL
        const baseUrl = window.location.origin;
        
        // Use predefined article slugs for consistency and SEO
        const articleSlugs = {
            'museveni': 'president-museveni-historic-nomination',
            'buhara': 'clarification-on-false-reports-circulating-online',
            'campaign': 'successful-campaign-rally-in-kabale-town',
            'women': 'women-empowerment-workshop-launched',
            'youth': 'youth-engagement-forum'
        };
        
        if (articleId && articleSlugs[articleId]) {
            // Use predefined slug for better SEO and consistency
            return `${baseUrl}/${articleSlugs[articleId]}/`;
        } else {
            // Fallback: create slug from title
            const slug = title.toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '') // Remove special characters
                .replace(/\s+/g, '-') // Replace spaces with hyphens
                .replace(/-+/g, '-') // Replace multiple hyphens with single
                .trim();
            return `${baseUrl}/${slug}/`;
        }
    } catch (error) {
        console.error('Error creating article URL:', error);
        return window.location.href;
    }
}

// Note: Meta tags are now handled statically in each article page for better social media crawler support
// This ensures consistent previews without relying on JavaScript execution

// Meta tag helper function removed - now using static meta tags in article pages for better SEO

// Fallback share function
function fallbackShare(shareData) {
    try {
        // Copy URL to clipboard
        navigator.clipboard.writeText(shareData.url).then(() => {
            showNotification('Article URL copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = shareData.url;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Article URL copied to clipboard!', 'success');
        });
    } catch (error) {
        console.error('Error in fallback share:', error);
        alert('Unable to share. Please copy the URL manually: ' + shareData.url);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Simple notification - you can enhance this
    console.log(`Notification (${type}): ${message}`);
}

// Get article excerpt based on title
function getArticleExcerpt(title) {
    switch(title) {
        case 'President Museveni\'s Historic Nomination':
            return 'Hon. Enid Origumisiriza Atuheire joined thousands of NRM supporters at Kololo to celebrate the official nomination of H.E. President Yoweri Kaguta Museveni as the NRM presidential candidate for the 2026 elections — a historic moment of unity, strength, and renewed commitment to Uganda\'s future.';
        case 'CLARIFICATION ON FALSE REPORTS CIRCULATING ONLINE':
            return 'We wish to clarify that the information circulating on social media regarding the alleged storming of Buhara Police Post by residents of Kiringa village is false and misleading.';
        case 'Successful Campaign Rally in Kabale Town':
            return 'Aunt Enid addressed thousands of supporters at the main square, sharing her vision for Kabale District\'s future and listening to community concerns.';
        case 'Women Empowerment Workshop Launched':
            return 'Aunt Enid launched a series of workshops aimed at empowering women entrepreneurs in Kabale District with business skills and financial literacy.';
        case 'Youth Engagement Forum':
            return 'Aunt Enid met with youth leaders to discuss employment opportunities, education access, and youth participation in community development.';
        default:
            return 'Read the full article for more details.';
    }
}

// Get article ID based on title
function getArticleId(title) {
    switch(title) {
        case 'President Museveni\'s Historic Nomination':
            return 'museveni';
        case 'CLARIFICATION ON FALSE REPORTS CIRCULATING ONLINE':
            return 'buhara';
        case 'Successful Campaign Rally in Kabale Town':
            return 'campaign';
        case 'Women Empowerment Workshop Launched':
            return 'women';
        case 'Youth Engagement Forum':
            return 'youth';
        default:
            return 'article';
    }
}

// Direct article access handling removed - articles now load directly without redirects

// Article dates are now static and story-specific - no dynamic updates
// This ensures dates remain consistent with the actual story dates
function updateArticleDates() {
    // Dates are now static in HTML - no dynamic updates needed
    console.log('Article dates are static and story-specific');
}

// Static stories are now handled directly in HTML - no dynamic loading needed

// Dynamic story functions removed - using static HTML instead

// All dynamic story functions removed - using static HTML stories instead

// Escape text for JavaScript usage
function escapeForJS(text) {
    if (!text) return '';
    return text.replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, '\\n').replace(/\r/g, '\\r');
}




// Read story function for dynamic stories
function readStory(slug) {
    window.location.href = `/${slug}/`;
}

// Cache clearing function
function clearBrowserCache() {
    // Clear localStorage cache
    if (localStorage.getItem('cache_version') !== getCurrentVersion()) {
        localStorage.clear();
        localStorage.setItem('cache_version', getCurrentVersion());
        console.log('Local storage cache cleared');
    }
    
    // Clear sessionStorage
    sessionStorage.clear();
    
    // Force reload of images with cache busting
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (!img.src.includes('?')) {
            img.src = img.src + '?v=' + Date.now();
        }
    });
    
    // Add cache control headers via meta tags
    const metaCache = document.createElement('meta');
    metaCache.setAttribute('http-equiv', 'Cache-Control');
    metaCache.setAttribute('content', 'no-cache, no-store, must-revalidate');
    document.head.appendChild(metaCache);
    
    const metaPragma = document.createElement('meta');
    metaPragma.setAttribute('http-equiv', 'Pragma');
    metaPragma.setAttribute('content', 'no-cache');
    document.head.appendChild(metaPragma);
    
    const metaExpires = document.createElement('meta');
    metaExpires.setAttribute('http-equiv', 'Expires');
    metaExpires.setAttribute('content', '0');
    document.head.appendChild(metaExpires);
}

// Get current version for cache management
function getCurrentVersion() {
    return '1.0.0'; // Update this when you make changes
}

// Debounce function to prevent rapid API calls
// Debounce function removed - no longer needed for static stories

// Initialize everything when page loads - simplified for better performance
document.addEventListener('DOMContentLoaded', () => {
    // Clear cache first
    clearBrowserCache();
    
    updateArticleDates();
    setupMobileNavigation();
    
    // Test function availability
    console.log('=== Read Story Functions Test ===');
    const functions = ['readMuseveniArticle', 'readBuharaArticle', 'readCampaignArticle', 'readWomenArticle', 'readYouthArticle', 'readAuntEnidStoryArticle'];
    functions.forEach(funcName => {
        if (typeof window[funcName] === 'function') {
            console.log(`✅ ${funcName} is available`);
        } else {
            console.log(`❌ ${funcName} is missing`);
        }
    });
    console.log('=== End Test ===');
});

// Setup mobile navigation functionality
function setupMobileNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

// Export functions for testing
window.readMuseveniArticle = readMuseveniArticle;
window.readBuharaArticle = readBuharaArticle;
window.readCampaignArticle = readCampaignArticle;
window.readWomenArticle = readWomenArticle;
window.readYouthArticle = readYouthArticle;
window.readAuntEnidStoryArticle = readAuntEnidStoryArticle;
window.shareArticleWithPreview = shareArticleWithPreview;
window.shareDirect = shareDirect;
window.getArticleExcerpt = getArticleExcerpt;
window.getArticleId = getArticleId;
