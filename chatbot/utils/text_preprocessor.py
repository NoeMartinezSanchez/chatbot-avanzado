import re
import unicodedata
from typing import List

class TextPreprocessor:
    """Clase para preprocesamiento y normalización de texto"""
    
    # Palabras vacías en español (stop words básicas)
    SPANISH_STOP_WORDS = {
        'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 
        'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 
        'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 
        'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 
        'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 
        'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 
        'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 
        'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 
        'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 
        'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 
        'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 
        'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 
        'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 
        'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 
        'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 
        'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 
        'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 'estén', 
        'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 
        'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 
        'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 
        'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 
        'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 
        'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 
        'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 
        'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 
        'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 
        'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán', 
        'habría', 'habrías', 'habríamos', 'habríais', 'habrían', 'había', 
        'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 
        'hubo', 'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 
        'hubiéramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses', 
        'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 
        'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 
        'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 
        'serás', 'será', 'seremos', 'seréis', 'serán', 'sería', 'serías', 
        'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 'erais', 
        'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 
        'fuera', 'fueras', 'fuéramos', 'fuerais', 'fueran', 'fuese', 
        'fueses', 'fuésemos', 'fueseis', 'fuesen', 'sintiendo', 'sentido', 
        'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 'tengo', 
        'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 
        'tengas', 'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 
        'tendrá', 'tendremos', 'tendréis', 'tendrán', 'tendría', 
        'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía', 
        'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 
        'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 
        'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses', 
        'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 
        'tenida', 'tenidos', 'tenidas', 'tened'
    }
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normaliza el texto: lowercase, elimina acentos y caracteres especiales"""
        if not text:
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar acentos
        text = unicodedata.normalize('NFKD', text)
        text = ''.join([c for c in text if not unicodedata.combining(c)])
        
        # Eliminar caracteres especiales, mantener letras, números y espacios
        text = re.sub(r'[^a-z0-9áéíóúñü\s]', '', text)
        
        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def remove_stop_words(text: str) -> str:
        """Elimina palabras vacías del texto"""
        words = text.split()
        filtered_words = [word for word in words if word not in TextPreprocessor.SPANISH_STOP_WORDS]
        return ' '.join(filtered_words)
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Divide el texto en tokens (palabras)"""
        return text.split()
    
    @classmethod
    def full_preprocess(cls, text: str, remove_stopwords: bool = True) -> str:
        """Pipeline completo de preprocesamiento"""
        processed = cls.normalize_text(text)
        if remove_stopwords:
            processed = cls.remove_stop_words(processed)
        return processed