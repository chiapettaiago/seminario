// Presentation Manager for Multi-page slides
class PresentationManager {
    constructor() {
        this.setupTouchEvents();
        this.setupKeyboardNavigation();
        this.setupAnimations();
        // Save progress immediately on load to avoid race conditions with the 5s interval
        this.saveProgress();
        // Intercept Home/Início link clicks to show the resume modal before navigating
        this.setupHomeInterception();
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
                    // If there is progress beyond slide 1, show modal instead of hard navigating
                    const saved = localStorage.getItem('presentationProgress');
                    if (saved && saved !== '1' && window.location.pathname !== '/slide/1') {
                        this.showResumeModal(saved);
                    } else {
                        window.location.href = '/slide/1';
                    }
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
        if (!savedSlide || savedSlide === '1') return;
        this.showResumeModal(savedSlide);
    }

    showResumeModal(savedSlide) {
        const overlay = document.getElementById('resume-modal-overlay');
        const numberEl = document.getElementById('resume-slide-number');
        const btnContinue = document.getElementById('resume-continue');
        const btnReset = document.getElementById('resume-reset');

        if (overlay && numberEl && btnContinue && btnReset) {
            numberEl.textContent = savedSlide;

            const openModal = () => {
                overlay.classList.add('show');
                overlay.setAttribute('aria-hidden', 'false');
            };
            const closeModal = () => {
                overlay.classList.remove('show');
                overlay.setAttribute('aria-hidden', 'true');
            };

            btnContinue.onclick = () => {
                closeModal();
                window.location.href = `/slide/${savedSlide}`;
            };
            btnReset.onclick = () => {
                localStorage.removeItem('presentationProgress');
                closeModal();
                window.location.href = '/slide/1';
            };

            openModal();
        } else {
            const useConfirm = confirm(`Continuar do slide ${savedSlide}?`);
            if (useConfirm) {
                window.location.href = `/slide/${savedSlide}`;
            }
        }
    }

    setupHomeInterception() {
        try {
            const homeLinks = document.querySelectorAll('a[href="/slide/1"]');
            homeLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    const saved = localStorage.getItem('presentationProgress');
                    if (saved && saved !== '1' && window.location.pathname !== '/slide/1') {
                        e.preventDefault();
                        this.showResumeModal(saved);
                    }
                });
            });
        } catch (_) {}
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
    // Expose globally for template helpers to trigger modal
    window.presentationManager = presentationManager;
    window.showResumeModal = (saved) => {
        const target = saved || localStorage.getItem('presentationProgress') || '1';
        if (target && target !== '1') {
            presentationManager.showResumeModal(target);
        } else {
            window.location.href = '/slide/1';
        }
    };
    
    // Auto-save progress every 5 seconds
    setInterval(() => {
        presentationManager.saveProgress();
    }, 5000);
    
    // Load progress on first visit
    if (window.location.pathname === '/' || window.location.pathname === '/slide/1') {
        presentationManager.loadProgress();
    }
});