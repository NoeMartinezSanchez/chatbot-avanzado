// Utilidades generales para el chatbot
class ChatBotUtils {
    constructor() {
        this.debugMode = true;
        this.messageHistory = [];
        this.maxHistoryLength = 50;
    }

    // Logger para debugging
    log(message, type = 'info') {
        if (!this.debugMode) return;

        const timestamp = new Date().toLocaleTimeString();
        const styles = {
            info: 'color: #3498db;',
            success: 'color: #27ae60;',
            warning: 'color: #f39c12;',
            error: 'color: #e74c3c;'
        };

        console.log(`%c[${timestamp}] ${message}`, styles[type] || styles.info);
    }

    // Formatear mensajes para mostrar
    formatMessage(text) {
        if (!text) return '';

        // Procesar formato básico Markdown
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/\•/g, '•')
            .replace(/(\d+)\./g, '$1.');
    }

    // Sanitizar entrada del usuario
    sanitizeInput(input) {
        if (typeof input !== 'string') return '';
        
        return input
            .trim()
            .substring(0, 500) // Limitar longitud
            .replace(/[<>]/g, ''); // Prevenir XSS básico
    }

    // Validar entrada del usuario
    validateInput(input) {
        if (!input || input.trim().length === 0) {
            return { isValid: false, message: 'Por favor, escribe un mensaje.' };
        }

        if (input.length > 500) {
            return { isValid: false, message: 'El mensaje es demasiado largo (máximo 500 caracteres).' };
        }

        // Verificar si es solo espacios en blanco
        if (!input.replace(/\s/g, '').length) {
            return { isValid: false, message: 'El mensaje no puede contener solo espacios.' };
        }

        return { isValid: true, message: '' };
    }

    // Guardar en historial
    addToHistory(message, isUser = true) {
        const historyItem = {
            id: Date.now() + Math.random(),
            timestamp: new Date().toISOString(),
            content: message,
            isUser: isUser,
            type: isUser ? 'user' : 'bot'
        };

        this.messageHistory.unshift(historyItem);
        
        // Mantener tamaño máximo del historial
        if (this.messageHistory.length > this.maxHistoryLength) {
            this.messageHistory = this.messageHistory.slice(0, this.maxHistoryLength);
        }

        // Guardar en localStorage
        this.saveHistoryToStorage();
    }

    // Cargar historial desde localStorage
    loadHistoryFromStorage() {
        try {
            const saved = localStorage.getItem('chatbotHistory');
            if (saved) {
                this.messageHistory = JSON.parse(saved);
            }
        } catch (error) {
            this.log('Error cargando historial: ' + error, 'error');
        }
    }

    // Guardar historial en localStorage
    saveHistoryToStorage() {
        try {
            localStorage.setItem('chatbotHistory', JSON.stringify(this.messageHistory));
        } catch (error) {
            this.log('Error guardando historial: ' + error, 'error');
        }
    }

    // Limpiar historial
    clearHistory() {
        this.messageHistory = [];
        localStorage.removeItem('chatbotHistory');
        this.log('Historial limpiado', 'success');
    }

    // Obtener estadísticas del historial
    getHistoryStats() {
        const userMessages = this.messageHistory.filter(msg => msg.isUser).length;
        const botMessages = this.messageHistory.filter(msg => !msg.isUser).length;
        const totalMessages = this.messageHistory.length;

        return {
            totalMessages,
            userMessages,
            botMessages,
            interactionRatio: totalMessages > 0 ? (userMessages / totalMessages * 100).toFixed(1) : 0
        };
    }

    // Animación de escritura
    async typeWriter(element, text, speed = 20) {
        return new Promise((resolve) => {
            let i = 0;
            element.innerHTML = '';

            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                } else {
                    resolve();
                }
            }

            type();
        });
    }

    // Copiar texto al portapapeles
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.log('Texto copiado al portapapeles', 'success');
            return true;
        } catch (error) {
            // Fallback para navegadores antiguos
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.log('Texto copiado (fallback)', 'success');
            return true;
        }
    }

    // Formatear timestamp
    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('es-MX', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    // Detectar dispositivo
    getDeviceInfo() {
        return {
            isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
            isTablet: /iPad|Android/i.test(navigator.userAgent) && !/Mobile/i.test(navigator.userAgent),
            userAgent: navigator.userAgent,
            language: navigator.language
        };
    }

    // Debounce para eventos
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Instancia global de utilidades
const chatUtils = new ChatBotUtils();