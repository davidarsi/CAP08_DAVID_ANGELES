# Chatbot con Búsqueda en Internet y Respuestas en Streaming

## Descripción del Sistema
Este chatbot es una aplicación de consola que combina búsquedas en internet con procesamiento de lenguaje natural para proporcionar respuestas informadas y contextuales. El sistema utiliza la API de Serper.dev para búsquedas en Google y OpenAI para generar respuestas coherentes.

## Características Principales
- Búsqueda en tiempo real usando Serper.dev
- Extracción de texto de páginas web
- Respuestas en streaming usando OpenAI
- Memoria de conversación
- Citación automática de fuentes

## Requisitos Previos
- Python 3.8 o superior
- Cuenta en OpenAI (para obtener API key)
- Cuenta en Serper.dev (para obtener API key)

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install python-dotenv requests openai beautifulsoup4 pytest pytest-mock
```

3. Configurar variables de entorno:
Editar archivo `.env` en la raíz del proyecto:
```
OPENAI_API_KEY=tu-api-key-de-openai
SERPER_API_KEY=tu-api-key-de-serper
```

## Estructura del Proyecto
```
chatbot/
├── chatbot.py        # Código principal del chatbot
├── test_chatbot.py   # Pruebas unitarias
├── .env             # Variables de entorno
└── README.md        # Documentación
```

## Ejecución del Chatbot

1. Activar el entorno virtual:
```bash
.\venv\Scripts\activate
```

2. Ejecutar el chatbot (ir a la carpeta del proyecto "solucion"):
```bash
python chatbot.py
```

3. Interactuar con el chatbot:
- Escribir preguntas naturalmente
- El chatbot buscará en internet y generará respuestas
- Escribir 'salir' para terminar

## Ejecución de Pruebas Unitarias

1. Ejecutar todas las pruebas:
```bash
pytest test_chatbot.py -v
```

2. Ejecutar una prueba específica:
```bash
pytest test_chatbot.py -v -k "test_nombre_prueba"
```

## Componentes del Sistema

### 1. Módulo de Búsqueda
- Utiliza Serper.dev API para búsquedas en Google
- Recupera los 5 resultados más relevantes
- Maneja errores de conexión y respuesta

### 2. Extractor de Texto
- Visita las URLs encontradas
- Extrae contenido relevante
- Elimina elementos no deseados (scripts, estilos)

### 3. Procesador de Lenguaje Natural
- Integra OpenAI GPT-3.5-turbo
- Genera respuestas en streaming
- Mantiene contexto de la conversación

### 4. Gestor de Fuentes
- Almacena referencias de las fuentes consultadas
- Proporciona enlaces para verificación
- Mantiene transparencia en la información

## Flujo de Operación
1. Usuario ingresa una pregunta
2. Sistema realiza búsqueda en internet
3. Extrae información relevante
4. Procesa y genera respuesta
5. Muestra respuesta en streaming
6. Lista fuentes consultadas

## Pruebas del Sistema
Las pruebas unitarias cubren:
- Inicialización del chatbot
- Funcionalidad de búsqueda
- Extracción de texto
- Generación de respuestas
- Manejo de conversación
- Gestión de fuentes
- Manejo de errores

## Mantenimiento y Soporte
- Verificar periódicamente las API keys
- Mantener actualizadas las dependencias
- Monitorear límites de uso de APIs

## Limitaciones Conocidas
- Requiere conexión a internet
- Depende de disponibilidad de APIs externas
- Límites de uso según plan de APIs
