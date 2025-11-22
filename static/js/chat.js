// Clase principal del ChatBot
class AdvancedChatBot {
    constructor() {
        this.utils = chatUtils;
        this.isTyping = false;
        this.currentSessionId = this.generateSessionId();
        this.initializeElements();
        this.setupEventListeners();
        this.loadMessageHistory();
        
        this.utils.log('ChatBot inicializado', 'success');
        this.utils.log(`Sesión: ${this.currentSessionId}`, 'info');
    }

    // Generar ID único para la sesión
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Inicializar elementos DOM
    initializeElements() {
        this.elements = {
            chatMessages: document.getElementById('chat-messages'),
            userInput: document.getElementById('user-input'),
            sendButton: document.getElementById('send-button'),
            typingIndicator: document.getElementById('typing-indicator'),
            charCounter: document.getElementById('char-counter')
        };

        // Verificar que todos los elementos existen
        Object.keys(this.elements).forEach(key => {
            if (!this.elements[key]) {
                this.utils.log(`Elemento no encontrado: ${key}`, 'error');
            }
        });
    }

    // Configurar event listeners
    setupEventListeners() {
        // Envío de mensaje
        this.elements.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter para enviar
        this.elements.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Contador de caracteres
        this.elements.userInput.addEventListener('input', this.updateCharCounter.bind(this));

        // Focus automático en el input
        this.elements.userInput.focus();

        // Eventos de teclado adicionales
        document.addEventListener('keydown', (e) => {
            // Ctrl + K para focus en input
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.elements.userInput.focus();
            }

            // Escape para limpiar input
            if (e.key === 'Escape') {
                this.elements.userInput.value = '';
                this.updateCharCounter();
            }
        });

        // Guardar historial antes de cerrar la página
        window.addEventListener('beforeunload', () => {
            this.utils.saveHistoryToStorage();
        });

        this.utils.log('Event listeners configurados', 'success');
    }

    // Actualizar contador de caracteres
    updateCharCounter() {
        const length = this.elements.userInput.value.length;
        const maxLength = 500;
        this.elements.charCounter.textContent = `${length}/${maxLength}`;

        // Cambiar color según la longitud
        if (length > 400) {
            this.elements.charCounter.className = 'char-counter warning';
        } else if (length > 480) {
            this.elements.charCounter.className = 'char-counter danger';
        } else {
            this.elements.charCounter.className = 'char-counter';
        }
    }

    // Enviar mensaje
    async sendMessage() {
        const userInput = this.elements.userInput.value.trim();
        
        // Validar entrada
        const validation = this.utils.validateInput(userInput);
        if (!validation.isValid) {
            this.showSystemMessage(validation.message, 'warning');
            return;
        }

        // Limpiar input
        this.elements.userInput.value = '';
        this.updateCharCounter();

        // Mostrar mensaje del usuario
        this.addMessageToChat(userInput, true);

        // Mostrar indicador de escritura
        this.showTypingIndicator();

        try {
            // Enviar al servidor
            const response = await this.sendToServer(userInput);
            
            // Ocultar indicador
            this.hideTypingIndicator();

            // Procesar respuesta
            if (response.status === 'success') {
                this.addMessageToChat(response.response, false, {
                    confidence: response.confidence,
                    tag: response.tag
                });
            } else {
                this.addMessageToChat(response.response, false, {
                    isError: true
                });
            }

        } catch (error) {
            this.hideTypingIndicator();
            this.utils.log('Error enviando mensaje: ' + error, 'error');
            this.showSystemMessage('❌ Error de conexión. Por favor, intenta nuevamente.', 'error');
        }
    }

    // Enviar mensaje al servidor
    async sendToServer(message) {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                session_id: this.currentSessionId,
                timestamp: new Date().toISOString()
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    // Agregar mensaje al chat
    addMessageToChat(content, isUser = false, metadata = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        // Contenido formateado
        const formattedContent = this.utils.formatMessage(content);
        
        // Construir HTML del mensaje
        let messageHTML = `
            <div class="message-content">
                ${formattedContent}
            </div>
        `;

        // Agregar metadata si existe
        if (metadata.confidence && !isUser) {
            messageHTML += `
                <div class="message-metadata">
                    <span class="confidence-badge">Confianza: ${(metadata.confidence * 100).toFixed(1)}%</span>
                    <span class="message-tag">#${metadata.tag}</span>
                </div>
            `;
        }

        if (metadata.isError) {
            messageDiv.classList.add('error-message');
        }

        messageDiv.innerHTML = messageHTML;

        // Agregar al chat
        this.elements.chatMessages.appendChild(messageDiv);

        // Guardar en historial
        this.utils.addToHistory(content, isUser);

        // Scroll al final
        this.scrollToBottom();

        // Animación para mensajes del bot
        if (!isUser && !metadata.isError) {
            this.animateMessageAppearance(messageDiv);
        }

        this.utils.log(`Mensaje ${isUser ? 'usuario' : 'bot'} agregado`, 'info');
    }

    // Animación para aparición de mensajes
    animateMessageAppearance(element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        requestAnimationFrame(() => {
            element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        });
    }

    // Mostrar indicador de escritura
    showTypingIndicator() {
        if (this.isTyping) return;

        this.isTyping = true;
        this.elements.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
        
        this.utils.log('Indicador de escritura activado', 'info');
    }

    // Ocultar indicador de escritura
    hideTypingIndicator() {
        this.isTyping = false;
        this.elements.typingIndicator.style.display = 'none';
        
        this.utils.log('Indicador de escritura desactivado', 'info');
    }

    // Scroll al final del chat
    scrollToBottom() {
        requestAnimationFrame(() => {
            this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        });
    }

    // Mostrar mensaje del sistema
    showSystemMessage(message, type = 'info') {
        const systemDiv = document.createElement('div');
        systemDiv.className = `system-message system-${type}`;
        systemDiv.textContent = message;

        this.elements.chatMessages.appendChild(systemDiv);
        this.scrollToBottom();

        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (systemDiv.parentNode) {
                systemDiv.remove();
            }
        }, 5000);

        this.utils.log(`Mensaje del sistema: ${message}`, type);
    }

    // Cargar historial de mensajes
    loadMessageHistory() {
        this.utils.loadHistoryFromStorage();
        const stats = this.utils.getHistoryStats();
        
        this.utils.log(`Historial cargado: ${stats.totalMessages} mensajes`, 'info');
        
        if (stats.totalMessages > 0) {
            this.showSystemMessage(
                `💾 Historial restaurado (${stats.totalMessages} mensajes anteriores)`, 
                'success'
            );
        }
    }

    // Pregunta rápida
    askQuickQuestion(question) {
        this.elements.userInput.value = question;
        this.updateCharCounter();
        this.sendMessage();
    }

    // Obtener estadísticas del servidor
    async getServerStats() {
        try {
            const response = await fetch('/stats');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.utils.log('Estadísticas del servidor obtenidas', 'success');
                return data.statistics;
            }
        } catch (error) {
            this.utils.log('Error obteniendo estadísticas: ' + error, 'error');
        }
        return null;
    }

    // Health check
    async healthCheck() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            return data.status === 'healthy';
        } catch (error) {
            return false;
        }
    }
}

// Funciones globales para HTML
function askQuickQuestion(question) {
    if (window.chatBot) {
        window.chatBot.askQuickQuestion(question);
    }
}

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    window.chatBot = new AdvancedChatBot();
    
    // Health check inicial
    setTimeout(async () => {
        const isHealthy = await window.chatBot.healthCheck();
        if (!isHealthy) {
            window.chatBot.showSystemMessage('⚠️ El servidor parece no estar disponible', 'warning');
        }
    }, 1000);
});