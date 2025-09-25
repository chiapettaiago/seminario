// Presentation Manager for Multi-page slides
class PresentationManager {
    constructor() {
        this.setupTouchEvents();
        this.setupKeyboardNavigation();
        this.setupAnimations();
    }

    // Touch/swipe support for mobile devices
    setupTouchEvents() {
        let touchStartX = 0;
        let touchStartY = 0;
        let touchEndX = 0;
        let touchEndY = 0;
        
        document.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            this.handleSwipe(touchStartX, touchEndX, touchStartY, touchEndY);
        }, { passive: true });
    }

    handleSwipe(startX, endX, startY, endY) {
        const swipeThreshold = 50;
        const swipeDistanceX = endX - startX;
        const swipeDistanceY = Math.abs(endY - startY);
        
        // Only trigger if horizontal swipe is longer than vertical
        if (Math.abs(swipeDistanceX) > swipeThreshold && swipeDistanceY < 100) {
            if (swipeDistanceX > 0) {
                // Swipe right - go to previous slide
                this.navigateToPreviousSlide();
            } else {
                // Swipe left - go to next slide
                this.navigateToNextSlide();
            }
        }
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowRight':
                case ' ':
                    e.preventDefault();
                    this.navigateToNextSlide();
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    this.navigateToPreviousSlide();
                    break;
                case 'Home':
                    e.preventDefault();
                    window.location.href = '/slide/1';
                    break;
                case 'End':
                    e.preventDefault();
                    window.location.href = '/slide/10';
                    break;
            }
        });
    }

    navigateToNextSlide() {
        const nextBtn = document.getElementById('next-btn');
        if (nextBtn && nextBtn.href) {
            window.location.href = nextBtn.href;
        }
    }

    navigateToPreviousSlide() {
        const prevBtn = document.getElementById('prev-btn');
        if (prevBtn && prevBtn.href) {
            window.location.href = prevBtn.href;
        }
    }

    setupAnimations() {
        // Add entrance animations to elements
        const animatedElements = document.querySelectorAll('.slide-content > *');
        animatedElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    // Save and load progress
    saveProgress() {
        const currentSlide = document.getElementById('current-slide').textContent;
        localStorage.setItem('presentationProgress', currentSlide);
    }

    loadProgress() {
        const savedSlide = localStorage.getItem('presentationProgress');
        if (savedSlide && savedSlide !== '1') {
            const confirmResume = confirm(`Continuar do slide ${savedSlide}?`);
            if (confirmResume) {
                window.location.href = `/slide/${savedSlide}`;
            }
        }
    }
}

// Enhanced audio pronunciation with different voices
function speakTextWithVoice(text, voiceIndex = 0) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        
        speechSynthesis.getVoices().then(voices => {
            const englishVoices = voices.filter(voice => voice.lang.startsWith('en-'));
            if (englishVoices.length > voiceIndex) {
                utterance.voice = englishVoices[voiceIndex];
            }
        });
        
        utterance.lang = 'en-US';
        utterance.rate = 0.7;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        speechSynthesis.speak(utterance);
    }
}

// Initialize presentation manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const presentationManager = new PresentationManager();
    
    // Auto-save progress every 5 seconds
    setInterval(() => {
        presentationManager.saveProgress();
    }, 5000);
    
    // Load progress on first visit
    if (window.location.pathname === '/' || window.location.pathname === '/slide/1') {
        presentationManager.loadProgress();
    }
});