// ==========================================
// Navigation Scroll Effect
// ==========================================

const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ==========================================
// Mobile Menu Toggle
// ==========================================

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// ==========================================
// Smooth Scroll to Sections
// ==========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');

        // Skip if it's just "#" or doesn't exist
        if (href === '#' || !href) return;

        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ==========================================
// Hero Chat Animation
// ==========================================

function animateChatMockup() {
    const typingIndicator = document.getElementById('typingIndicator');
    const answer = document.getElementById('answer');

    // Reset animation
    typingIndicator.style.display = 'flex';
    answer.style.display = 'none';

    // Show typing indicator for 1 second
    setTimeout(() => {
        typingIndicator.style.display = 'none';
        answer.style.display = 'block';
        answer.style.animation = 'fadeInUp 0.5s ease forwards';
    }, 1000);

    // Loop animation every 5 seconds
    setTimeout(animateChatMockup, 5000);
}

// Start animation when page loads
window.addEventListener('load', () => {
    setTimeout(animateChatMockup, 500);
});

// ==========================================
// Scroll Fade-In Animation
// ==========================================

const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe all elements with scroll-fade class
document.querySelectorAll('.scroll-fade').forEach(el => {
    observer.observe(el);
});

// ==========================================
// FAQ Accordion
// ==========================================

const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');

    question.addEventListener('click', () => {
        // Close other items
        faqItems.forEach(otherItem => {
            if (otherItem !== item && otherItem.classList.contains('active')) {
                otherItem.classList.remove('active');
            }
        });

        // Toggle current item
        item.classList.toggle('active');
    });
});

// ==========================================
// Cost Calculator
// ==========================================

const documentsSlider = document.getElementById('documents');
const questionsSlider = document.getElementById('questions');
const docCountSpan = document.getElementById('docCount');
const questionCountSpan = document.getElementById('questionCount');
const indexingCostSpan = document.getElementById('indexingCost');
const queryCostSpan = document.getElementById('queryCost');
const costResultSpan = document.getElementById('costResult');

function calculateCost() {
    const documents = parseInt(documentsSlider.value);
    const questions = parseInt(questionsSlider.value);

    // Formula: (documents × $0.11) for indexing + (questions × $0.02) for queries
    const indexingCost = documents * 0.11;
    const queryCost = questions * 0.02;
    const totalCost = indexingCost + queryCost;

    // Update display
    docCountSpan.textContent = documents;
    questionCountSpan.textContent = questions;
    indexingCostSpan.textContent = '$' + indexingCost.toFixed(2);
    queryCostSpan.textContent = '$' + queryCost.toFixed(2);
    costResultSpan.textContent = '$' + totalCost.toFixed(2);
}

// Initialize calculator
if (documentsSlider && questionsSlider) {
    documentsSlider.addEventListener('input', calculateCost);
    questionsSlider.addEventListener('input', calculateCost);
    calculateCost(); // Initial calculation
}

// ==========================================
// Code Copy Button
// ==========================================

const copyButton = document.getElementById('copyButton');
const codeBlock = document.getElementById('codeBlock');
const toast = document.getElementById('toast');

if (copyButton && codeBlock) {
    copyButton.addEventListener('click', () => {
        // Copy code to clipboard
        const code = codeBlock.textContent;

        navigator.clipboard.writeText(code).then(() => {
            // Show toast notification
            showToast('Copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy:', err);
            showToast('Failed to copy');
        });
    });
}

function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

// ==========================================
// Animate Step Connectors on Scroll
// ==========================================

const stepConnectors = document.querySelectorAll('.step-connector');

const connectorObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'growLine 0.8s ease forwards';
        }
    });
}, { threshold: 0.5 });

stepConnectors.forEach(connector => {
    connectorObserver.observe(connector);
});

// Add CSS animation for connectors
const style = document.createElement('style');
style.textContent = `
    @keyframes growLine {
        from {
            transform: scaleX(0);
        }
        to {
            transform: scaleX(1);
        }
    }

    .step-connector {
        transform-origin: left;
    }

    @media (max-width: 1024px) {
        .step-connector {
            transform-origin: top;
        }

        @keyframes growLine {
            from {
                transform: scaleY(0);
            }
            to {
                transform: scaleY(1);
            }
        }
    }
`;
document.head.appendChild(style);

// ==========================================
// Lazy Load Images (if needed in future)
// ==========================================

function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Call when needed
// lazyLoadImages();

// ==========================================
// Parallax Effect for Hero Background (Optional)
// ==========================================

const heroBackground = document.querySelector('.hero-background');

window.addEventListener('scroll', () => {
    if (window.scrollY < window.innerHeight) {
        const scrolled = window.scrollY;
        if (heroBackground) {
            heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    }
});

// ==========================================
// Performance: Throttle Scroll Events
// ==========================================

function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = new Date().getTime();
        if (now - lastCall < delay) {
            return;
        }
        lastCall = now;
        return func(...args);
    };
}

// Apply throttling to scroll events
window.addEventListener('scroll', throttle(() => {
    // Throttled scroll handler
}, 100));

// ==========================================
// Analytics (Google Analytics placeholder)
// ==========================================

// Track button clicks
const ctaButtons = document.querySelectorAll('.btn-primary, .btn-secondary');

ctaButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        const buttonText = e.target.textContent;
        const buttonHref = e.target.getAttribute('href');

        // Send to analytics (placeholder)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'click', {
                'event_category': 'CTA',
                'event_label': buttonText,
                'value': buttonHref
            });
        }

        console.log('Button clicked:', buttonText, buttonHref);
    });
});

// ==========================================
// Add Loading Animation
// ==========================================

window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// ==========================================
// Feature Card Hover Effect Enhancement
// ==========================================

const featureCards = document.querySelectorAll('.feature-card');

featureCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// ==========================================
// Tech Item Hover Animation
// ==========================================

const techItems = document.querySelectorAll('.tech-item');

techItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px) scale(1.1)';
    });

    item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// ==========================================
// Keyboard Accessibility
// ==========================================

// Add focus visible for keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-nav');
    }
});

document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-nav');
});

// Add CSS for keyboard focus
const focusStyle = document.createElement('style');
focusStyle.textContent = `
    .keyboard-nav *:focus {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
    }
`;
document.head.appendChild(focusStyle);

// ==========================================
// Console Easter Egg
// ==========================================

console.log('%c🤖 FAQ Bot', 'font-size: 24px; font-weight: bold; color: #4F46E5;');
console.log('%cInterested in contributing? Check out our GitHub: https://github.com/funkydonkey/faq_bot', 'font-size: 14px; color: #6B7280;');
console.log('%cBuilt with ❤️ for the open-source community', 'font-size: 12px; color: #6B7280;');

// ==========================================
// End of Script
// ==========================================
