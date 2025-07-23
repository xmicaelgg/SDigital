// Efectos de partículas avanzados
class ParticleSystem {
    constructor() {
        this.particles = [];
        this.container = document.querySelector('.particles');
        this.init();
    }

    init() {
        for (let i = 0; i < 20; i++) {
            this.createParticle();
        }
    }

    createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle-advanced';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
        
        this.container.appendChild(particle);
        this.particles.push(particle);
    }
}

// Efectos de parallax
class ParallaxEffect {
    constructor() {
        this.init();
    }

    init() {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.parallax');
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }
}

// Efectos de hover 3D
class Hover3DEffect {
    constructor() {
        this.init();
    }

    init() {
        const cards = document.querySelectorAll('.card-3d');
        
        cards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            });
        });
    }
}

// Efectos de notificación
class NotificationSystem {
    static show(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${this.getIcon(type)} me-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, duration);
    }
    
    static getIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
}

// Efectos de carga de página
class PageLoader {
    constructor() {
        this.createLoader();
    }
    
    createLoader() {
        const loader = document.createElement('div');
        loader.className = 'page-loader';
        loader.innerHTML = `
            <div class="text-center text-white">
                <div class="loader-spinner mb-3"></div>
                <h5>Cargando RMA Recepción</h5>
                <p class="text-white-50">Inicializando sistema...</p>
            </div>
        `;
        
        document.body.appendChild(loader);
        
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(loader);
                }, 500);
            }, 1000);
        });
    }
}

// Efectos de contador animado
class AnimatedCounter {
    static animate(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }
}

// Efectos de typing
class TypewriterEffect {
    constructor(element, text, speed = 100) {
        this.element = element;
        this.text = text;
        this.speed = speed;
        this.currentIndex = 0;
        this.init();
    }
    
    init() {
        this.element.textContent = '';
        this.type();
    }
    
    type() {
        if (this.currentIndex < this.text.length) {
            this.element.textContent += this.text.charAt(this.currentIndex);
            this.currentIndex++;
            setTimeout(() => this.type(), this.speed);
        }
    }
}

// Efectos de scroll suave
class SmoothScroll {
    static init() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// Efectos de ripple
class RippleEffect {
    static init() {
        document.addEventListener('click', (e) => {
            const button = e.target.closest('.ripple');
            if (button) {
                const ripple = document.createElement('span');
                const rect = button.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple-effect');
                
                button.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            }
        });
    }
}

// Efectos de validación de formularios
class FormValidation {
    static init() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const requiredFields = form.querySelectorAll('[required]');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        this.showFieldError(field, 'Este campo es requerido');
                    } else {
                        this.clearFieldError(field);
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    NotificationSystem.show('Por favor, completa todos los campos requeridos', 'warning');
                }
            });
        });
    }
    
    static showFieldError(field, message) {
        field.classList.add('is-invalid');
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }
    
    static clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
}

// Efectos de búsqueda en tiempo real
class LiveSearch {
    constructor(inputSelector, resultsSelector) {
        this.input = document.querySelector(inputSelector);
        this.results = document.querySelector(resultsSelector);
        this.init();
    }
    
    init() {
        if (this.input) {
            this.input.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase();
                this.performSearch(query);
            });
        }
    }
    
    performSearch(query) {
        // Implementar lógica de búsqueda según necesidades
        console.log('Buscando:', query);
    }
}

// Inicialización de todos los efectos
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar sistemas (sin partículas para mejor rendimiento)
    new ParallaxEffect();
    new Hover3DEffect();
    // new PageLoader(); // Deshabilitado para usar la nueva pantalla de carga
    
    // Inicializar efectos
    SmoothScroll.init();
    RippleEffect.init();
    FormValidation.init();
    
    // Efectos adicionales
    const statsNumbers = document.querySelectorAll('.stats-number');
    statsNumbers.forEach(number => {
        const target = parseInt(number.textContent);
        if (target > 0) {
            AnimatedCounter.animate(number, target);
        }
    });
    
    // Efecto de typing en títulos
    const titles = document.querySelectorAll('.typewriter');
    titles.forEach(title => {
        const text = title.textContent;
        new TypewriterEffect(title, text, 100);
    });
    
    // Efectos de hover en botones
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.classList.add('hover-glow');
    });
    
    // Efectos de entrada para cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('slide-up');
    });
    
    console.log('🎨 Efectos visuales cargados exitosamente');
});

// Exportar clases para uso global
window.ParticleSystem = ParticleSystem;
window.ParallaxEffect = ParallaxEffect;
window.Hover3DEffect = Hover3DEffect;
window.NotificationSystem = NotificationSystem;
window.PageLoader = PageLoader;
window.AnimatedCounter = AnimatedCounter;
window.TypewriterEffect = TypewriterEffect;
window.SmoothScroll = SmoothScroll;
window.RippleEffect = RippleEffect;
window.FormValidation = FormValidation;
window.LiveSearch = LiveSearch; 