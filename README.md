# 🤖 ChatBot Avanzado - Módulo Propedéutico

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?logo=flask)
![GitHub](https://img.shields.io/badge/GitHub-Repository-lightgrey?logo=github)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Asistente Virtual Inteligente con NLP para el Programa Propedéutico**

[Características](#-características) • [Demo](#-demo-rápida) • [Instalación](#-instalación-completa) • [Uso](#-uso) • [Estructura](#️-estructura-del-proyecto)

</div>

---

## 📋 Descripción

ChatBot especializado desarrollado con arquitectura escalable para proporcionar asistencia inteligente a estudiantes del módulo propedéutico de **Prepa en Línea SEP**. Incluye sistema de reconocimiento de intenciones, gestión de conversaciones y interfaz moderna.

---

## 🚀 Características

### 🤖 **Núcleo Inteligente**
- ✅ **Sistema de Intenciones** con matching avanzado
- ✅ **Preprocesamiento de texto** en español
- ✅ **Gestión de contexto** conversacional
- ✅ **Métricas de confianza** en respuestas
- ✅ **Logging de conversaciones** para mejora continua

### 🎨 **Experiencia de Usuario**
- ✅ **Interfaz responsive** y moderna
- ✅ **Preguntas rápidas** para acceso inmediato
- ✅ **Indicador de escritura** en tiempo real
- ✅ **Historial de conversaciones** persistente
- ✅ **Animaciones fluidas** y feedback visual

### 🛠️ **Arquitectura Profesional**
- ✅ **Separación de concerns** (MVC-like)
- ✅ **Configuración centralizada**
- ✅ **Sistema de logging** integrado
- ✅ **Manejo de errores** robusto
- ✅ **API RESTful** documentada

---

## 🎯 Demo Rápida

```bash
# Clonar y ejecutar
git clone https://github.com/TU_USUARIO/chatbot-avanzado.git
cd chatbot-avanzado
pip install -r requirements.txt
python app.py

# Acceder a: http://localhost:5000
```

---

## 📦 Instalación Completa

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes Python)

### 🛠️ Configuración

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/chatbot-avanzado.git
cd chatbot-avanzado

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

### 🌐 Acceso

Abre tu navegador y ve a: **http://localhost:5000**

---

## 💻 Uso

### Para Estudiantes

1. Escribe preguntas en lenguaje natural
2. Usa preguntas rápidas para acceso inmediato
3. Recibe respuestas contextuales con nivel de confianza
4. Mantén conversaciones fluidas sobre múltiples temas

### Ejemplos de Consultas

- "¿Qué es el módulo propedéutico?"
- "Explícame la técnica Pomodoro"
- "¿Cómo me evalúan en el módulo?"
- "Necesito ayuda con la plataforma virtual"

---

## 🏗️ Estructura del Proyecto

```
chatbot-avanzado/
├── 📁 chatbot/           # Núcleo de la aplicación
│   ├── intents_manager.py
│   ├── response_generator.py
│   └── utils/
├── 📁 data/              # Datos y configuración
│   ├── intents.json
│   └── conversations/
├── 📁 templates/         # Vistas HTML
│   └── index.html
├── 📁 static/           # Assets estáticos
│   ├── css/
│   └── js/
├── 📁 tests/            # Pruebas unitarias
├── app.py              # Aplicación principal
├── config.py           # Configuración
└── requirements.txt    # Dependencias
```

---

## 🔧 Configuración Avanzada

### Modificar Intenciones

Edita `data/intents.json` para agregar nuevas capacidades:

```json
{
  "tag": "nueva_intencion",
  "patterns": ["patrón 1", "patrón 2"],
  "responses": ["Respuesta 1", "Respuesta 2"],
  "context": "contexto"
}
```

### Variables de Entorno

Crea un archivo `.env`:

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta
MIN_CONFIDENCE=0.3
```

---

## 🧪 Pruebas

```bash
# Ejecutar pruebas unitarias
python -m pytest tests/

# Verificar cobertura
python -m pytest --cov=chatbot tests/
```

---

## 📊 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Interfaz web |
| `POST` | `/chat` | Procesar mensajes |
| `GET` | `/stats` | Estadísticas del chatbot |
| `GET` | `/health` | Estado del servicio |

---

## 🚀 Despliegue

### Desarrollo

```bash
python app.py
```

### Producción (Gunicorn)

```bash
pip install gunicorn
gunicorn app:app -b 0.0.0.0:5000 -w 4
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Distribuido bajo licencia MIT. Ver `LICENSE` para más información.

---

## 👨‍💻 Autor

**Noé Martínez Sánchez**

- 🐙 GitHub: [@NoeMartinezSanchez](https://github.com/NoeMartinezSanchez)
- 📁 Proyecto: ChatBot Avanzado

---

<div align="center">

### ⭐ ¿Te gusta este proyecto?

Dale una estrella en GitHub para apoyar el desarrollo continuo.

[⬆ Volver al inicio](#-chatbot-avanzado---módulo-propedéutico)

</div>
