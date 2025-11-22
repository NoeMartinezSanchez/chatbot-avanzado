import random
import logging
from typing import Dict, Any, List
from datetime import datetime

class ResponseGenerator:
    def __init__(self, intents_manager):
        self.intents_manager = intents_manager
        self.logger = self.setup_logger()
        
        # Respuestas por defecto organizadas por contexto
        self.default_responses = {
            "general": [
                "🤔 No estoy seguro de entender. ¿Podrías reformular tu pregunta?",
                "💭 Interesante pregunta. Puedo ayudarte con información del módulo propedéutico, técnicas de estudio, uso de plataforma y más.",
                "🎓 Como asistente del módulo propedéutico, puedo orientarte sobre: técnicas de estudio, plataforma virtual, organización del tiempo y evaluación."
            ],
            "welcome": [
                "¡Bienvenido de nuevo! ¿En qué más puedo ayudarte?",
                "¡Hola otra vez! ¿Qué te gustaría saber ahora?",
                "Encantado de verte de nuevo. ¿Tienes alguna otra pregunta?"
            ],
            "fallback_suggestions": [
                "¿Te interesa saber sobre las **técnicas de estudio** como Pomodoro o mapas mentales?",
                "¿Necesitas ayuda con el **acceso a la plataforma** o **participación en foros**?",
                "¿Quieres información sobre la **evaluación** o **duración del módulo**?"
            ]
        }
    
    def setup_logger(self):
        """Configura el sistema de logging"""
        logger = logging.getLogger('ResponseGenerator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def get_response(self, user_input: str) -> Dict[str, Any]:
        """Genera una respuesta contextual para la entrada del usuario"""
        try:
            intent_result = self.intents_manager.find_best_intent(user_input)
            
            if intent_result["status"] == "success":
                response_data = self._get_intent_response(intent_result)
            else:
                response_data = self._get_unknown_response(intent_result)
            
            # Agregar metadata
            response_data.update({
                "timestamp": datetime.now().isoformat(),
                "input_length": len(user_input),
                "response_length": len(response_data["response"])
            })
            
            self.logger.info(f"Respuesta generada - Tag: {response_data['tag']}, Confianza: {intent_result['confidence']:.3f}")
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"Error generando respuesta: {e}")
            return self._get_error_response()
    
    def _get_intent_response(self, intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Genera respuesta para un intent reconocido"""
        intent = intent_result["intent"]
        
        # Seleccionar respuesta aleatoria
        response = random.choice(intent["responses"])
        
        # Agregar sugerencias si el contexto lo permite
        if intent_result["confidence"] < 0.6:  # Confianza media
            response += "\n\n¿Es esto lo que necesitabas? Si no, por favor reformula tu pregunta."
        
        return {
            "response": response,
            "tag": intent_result["tag"],
            "confidence": intent_result["confidence"],
            "status": "success",
            "has_suggestions": intent_result["confidence"] < 0.6,
            "context": intent.get("context", "general")
        }
    
    def _get_unknown_response(self, intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Genera respuesta para intent desconocido"""
        base_response = random.choice(self.default_responses["general"])
        suggestion = random.choice(self.default_responses["fallback_suggestions"])
        
        response = f"{base_response}\n\n💡 **Sugerencia:** {suggestion}"
        
        return {
            "response": response,
            "tag": "unknown",
            "confidence": intent_result["confidence"],
            "status": "unknown",
            "has_suggestions": True,
            "context": "general"
        }
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Genera respuesta de error"""
        return {
            "response": "❌ Lo siento, ha ocurrido un error interno. Por favor, intenta nuevamente.",
            "tag": "error",
            "confidence": 0.0,
            "status": "error",
            "has_suggestions": False,
            "context": "error"
        }
    
    def get_available_topics(self) -> List[str]:
        """Retorna lista de temas disponibles para sugerencias"""
        topics = set()
        for intent in self.intents_manager.intents["intents"]:
            if "context" in intent:
                topics.add(intent["context"])
            topics.add(intent["tag"])
        return sorted(list(topics))