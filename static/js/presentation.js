// Additional JavaScript functionality for future enhancements
class PresentationManager {
    constructor() {
        this.touchStartX = 0;
        this.touchEndX = 0;
        this.setupTouchEvents();
        this.setupFullscreenToggle();
    }

    // Touch/swipe support for mobile devices
    setupTouchEvents() {
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.changedTouches[0].screenX;
        });

        document.addEventListener('touchend', (e) => {
            this.touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe();
        });
    }

    handleSwipe() {
        const swipeThreshold = 50;
        const swipeDistance = this.touchEndX - this.touchStartX;

        if (Math.abs(swipeDistance) > swipeThreshold) {
            if (swipeDistance > 0) {
                previousSlide();
            } else {
                nextSlide();
            }
        }
    }

    // Fullscreen toggle
    setupFullscreenToggle() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'F11') {
                e.preventDefault();
                this.toggleFullscreen();
            }
        });
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log(`Error attempting to enable fullscreen: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    }

    // Save presentation progress
    saveProgress() {
        localStorage.setItem('presentationProgress', currentSlide);
    }

    // Load presentation progress
    loadProgress() {
        const savedSlide = localStorage.getItem('presentationProgress');
        if (savedSlide !== null) {
            goToSlide(parseInt(savedSlide));
        }
    }
}

// Initialize presentation manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const presentationManager = new PresentationManager();
    
    // Auto-save progress
    setInterval(() => {
        presentationManager.saveProgress();
    }, 5000);
});

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

// Quiz tracking system
class QuizTracker {
    constructor() {
        this.scores = {
            correct: 0,
            total: 0
        };
    }

    recordAnswer(isCorrect) {
        this.scores.total++;
        if (isCorrect) {
            this.scores.correct++;
        }
        this.updateScore();
    }

    updateScore() {
        const percentage = (this.scores.correct / this.scores.total * 100).toFixed(1);
        console.log(`Quiz Score: ${this.scores.correct}/${this.scores.total} (${percentage}%)`);
    }

    getScore() {
        return this.scores;
    }
}

// Initialize quiz tracker
const quizTracker = new QuizTracker();