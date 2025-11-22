from flask import Flask, render_template, request, jsonify, session
import os
from datetime import datetime
from config import Config
from chatbot.intents_manager import IntentsManager
from chatbot.response_generator import ResponseGenerator

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar componentes del chatbot
try:
    intents_manager = IntentsManager(Config.INTENTS_FILE, min_confidence=Config.MIN_CONFIDENCE)
    response_generator = ResponseGenerator(intents_manager)
    print("✅ Chatbot inicializado correctamente")
except Exception as e:
    print(f"❌ Error inicializando chatbot: {e}")
    raise e

@app.route('/')
def home():
    """Página principal del chatbot"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para procesar mensajes del chat"""
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': 'Por favor, escribe tu mensaje.',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            })
        
        # Obtener respuesta del chatbot
        bot_response = response_generator.get_response(user_message)
        
        return jsonify(bot_response)
        
    except Exception as e:
        app.logger.error(f"Error en endpoint /chat: {e}")
        return jsonify({
            'response': '❌ Lo siento, ha ocurrido un error en el sistema. Por favor, intenta nuevamente.',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Endpoint para obtener estadísticas del chatbot"""
    try:
        stats = intents_manager.get_statistics()
        return jsonify({
            'statistics': stats,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs(Config.CONVERSATIONS_DIR, exist_ok=True)
    
    print("🚀 Iniciando ChatBot Avanzado...")
    print(f"📊 Configuración: {Config.get_settings()}")
    
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=Config.DEBUG,
        threaded=True
    )