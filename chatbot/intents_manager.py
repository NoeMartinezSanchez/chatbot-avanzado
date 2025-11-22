import json
import re
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime
from .utils.text_preprocessor import TextPreprocessor

class IntentsManager:
    def __init__(self, intents_file: str, min_confidence: float = 0.3):
        self.intents_file = intents_file
        self.min_confidence = min_confidence
        self.intents = self.load_intents()
        self.conversation_log = []
        self.text_preprocessor = TextPreprocessor()
        
        # Estadísticas
        self.stats = {
            "total_queries": 0,
            "recognized_intents": 0,
            "unknown_intents": 0,
            "average_confidence": 0.0
        }
    
    def load_intents(self) -> Dict[str, Any]:
        """Carga y valida los intents desde el archivo JSON"""
        try:
            if not os.path.exists(self.intents_file):
                raise FileNotFoundError(f"Archivo de intents no encontrado: {self.intents_file}")
            
            with open(self.intents_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Validar estructura básica
            if "intents" not in data:
                raise ValueError("El archivo JSON debe contener una clave 'intents'")
            
            print(f"✅ Cargados {len(data['intents'])} intents correctamente")
            return data
            
        except Exception as e:
            print(f"❌ Error cargando intents: {e}")
            return {"intents": []}
    
    def calculate_similarity(self, user_input: str, pattern: str) -> float:
        """Calcula similitud usando múltiples estrategias"""
        user_processed = self.text_preprocessor.full_preprocess(user_input)
        pattern_processed = self.text_preprocessor.full_preprocess(pattern)
        
        if not user_processed or not pattern_processed:
            return 0.0
        
        user_words = set(self.text_preprocessor.tokenize(user_processed))
        pattern_words = set(self.text_preprocessor.tokenize(pattern_processed))
        
        # Estrategia 1: Coincidencia exacta de palabras
        exact_matches = user_words.intersection(pattern_words)
        
        # Estrategia 2: Coincidencia parcial (para futuras mejoras)
        partial_matches = 0
        
        # Calcular score combinado
        if not pattern_words:
            return 0.0
        
        exact_score = len(exact_matches) / len(pattern_words)
        total_score = exact_score + (partial_matches * 0.1)  # Peso menor para coincidencias parciales
        
        return min(total_score, 1.0)  # Asegurar que no exceda 1.0
    
    def find_best_intent(self, user_input: str) -> Dict[str, Any]:
        """Encuentra el intent que mejor coincide con la entrada del usuario"""
        best_intent = None
        best_score = 0.0
        best_pattern = ""
        
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                score = self.calculate_similarity(user_input, pattern)
                if score > best_score:
                    best_score = score
                    best_intent = intent
                    best_pattern = pattern
        
        # Actualizar estadísticas
        self.stats["total_queries"] += 1
        if best_score > self.min_confidence:
            self.stats["recognized_intents"] += 1
        else:
            self.stats["unknown_intents"] += 1
        
        # Actualizar confianza promedio
        total_confidence = self.stats["average_confidence"] * (self.stats["total_queries"] - 1)
        self.stats["average_confidence"] = (total_confidence + best_score) / self.stats["total_queries"]
        
        # Log de la conversación
        self.log_conversation(user_input, best_intent, best_score, best_pattern)
        
        if best_score > self.min_confidence:
            return {
                "intent": best_intent,
                "confidence": best_score,
                "tag": best_intent["tag"],
                "matched_pattern": best_pattern,
                "status": "success"
            }
        else:
            return {
                "intent": None,
                "confidence": best_score,
                "tag": "unknown",
                "matched_pattern": "",
                "status": "unknown"
            }
    
    def log_conversation(self, user_input: str, intent: Dict, confidence: float, pattern: str):
        """Registra la conversación para análisis posterior"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "intent_tag": intent["tag"] if intent else "unknown",
            "confidence": confidence,
            "matched_pattern": pattern,
            "recognized": confidence > self.min_confidence
        }
        self.conversation_log.append(log_entry)
        
        # Mantener solo los últimos 100 logs en memoria
        if len(self.conversation_log) > 100:
            self.conversation_log.pop(0)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estadísticas de uso del chatbot"""
        recognition_rate = (self.stats["recognized_intents"] / self.stats["total_queries"] * 100) if self.stats["total_queries"] > 0 else 0
        
        return {
            "total_queries": self.stats["total_queries"],
            "recognized_intents": self.stats["recognized_intents"],
            "unknown_intents": self.stats["unknown_intents"],
            "recognition_rate": round(recognition_rate, 2),
            "average_confidence": round(self.stats["average_confidence"], 3),
            "conversation_log_size": len(self.conversation_log)
        }
    
    def save_conversation_log(self, file_path: str = None):
        """Guarda el log de conversaciones en un archivo JSON"""
        if not file_path:
            file_path = os.path.join(os.path.dirname(self.intents_file), "conversations", f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.conversation_log, file, indent=2, ensure_ascii=False)
            print(f"✅ Log de conversaciones guardado en: {file_path}")
        except Exception as e:
            print(f"❌ Error guardando log: {e}")