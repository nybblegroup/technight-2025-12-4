# 🚀 Nybble Event Engagement Hub - Setup Instructions

Este documento explica cómo configurar y ejecutar el **Nybble Event Engagement Hub** completo.

## 📋 Requisitos Previos

- **Node.js** >= 20.19.4
- **Python** >= 3.12
- **PostgreSQL** (base de datos configurada)
- **Gemini API Key** (de Google AI Studio)

## 🔧 Configuración del Backend (Python + FastAPI)

### 1. Instalar dependencias de Python

```bash
cd backend/python
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en `backend/python/` con el siguiente contenido:

```env
# Server Configuration
PORT=8080

# Database Configuration (reemplaza con tu connection string real)
DATABASE_URL="postgresql://user:password@localhost:5432/nybble_event_hub"

# Gemini AI Configuration (⚠️ IMPORTANTE: Agrega tu API key aquí)
GEMINI_API_KEY="tu-api-key-de-gemini-aqui"

# Mock API URLs (para integraciones futuras)
GOOGLE_CALENDAR_API_URL="http://localhost:8080/mock/calendar"
SLACK_API_URL="http://localhost:8080/mock/slack"
PEOPLE_FORCE_API_URL="http://localhost:8080/mock/people-force"
EMAIL_API_URL="http://localhost:8080/mock/email"

# Application Settings
ENVIRONMENT="development"
DEBUG=True
```

### 3. Obtener Gemini API Key

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crea una API key nueva
3. Cópiala y pégala en el archivo `.env` como valor de `GEMINI_API_KEY`

### 4. Ejecutar migraciones de base de datos

```bash
cd backend/python

# Ejecutar migración para crear las tablas
alembic upgrade head
```

### 5. Seed de datos de prueba

```bash
# Desde backend/python
python seed_data.py
```

Este script creará:
- Badges del sistema
- Un evento de ejemplo: "Tech Night: AI en Producción"
- 4 participantes con puntos y rankings
- 5 preguntas para el evento

### 6. Ejecutar el backend

```bash
# Desde backend/python
python main.py
```

O desde la raíz del proyecto:

```bash
npm run dev:python
```

El backend estará disponible en:
- **API**: http://localhost:8080
- **Swagger UI**: http://localhost:8080/api/swagger
- **Health Check**: http://localhost:8080/api/health

## 🎨 Configuración del Frontend (React + Vite)

### 1. Instalar dependencias de Node.js

```bash
# Desde la raíz del proyecto
npm install

# O desde frontend/
cd frontend
npm install
```

### 2. Configurar variables de entorno (opcional)

Si quieres cambiar la URL del backend, crea un archivo `.env` en `frontend/`:

```env
VITE_API_BASE_URL=http://localhost:8080
```

Por defecto, el frontend ya está configurado para conectarse a `http://localhost:8080`.

### 3. Ejecutar el frontend

```bash
# Desde la raíz del proyecto
npm run dev:frontend

# O desde frontend/
cd frontend
npm run dev
```

El frontend estará disponible en:
- **App**: http://localhost:5173

## 🎯 Uso de la Aplicación

### Acceder al Event Hub

1. Abre http://localhost:5173
2. Verás la lista de eventos disponibles
3. Haz clic en "Tech Night: AI en Producción" (el evento creado por el seed)
4. Serás redirigido a: http://localhost:5173/events/1

### Funcionalidades Disponibles

#### 📊 Rankings (Sidebar Izquierdo)
- Top 10 participantes ordenados por puntos
- Badges y rachas de cada usuario
- Top respuestas de calidad

#### 💬 Chat Conversacional (Centro)
- Responde preguntas del evento
- Sistema de puntos automático con IA
- Análisis de sentimiento en tiempo real
- Opciones rápidas o respuestas abiertas
- Sistema de rating con estrellas

#### 📈 Estadísticas (Sidebar Derecho)
- Tu progreso personal
- Badges desbloqueados
- Racha actual
- Calidad promedio de respuestas

### Sistema de Puntos

El sistema otorga puntos automáticamente basado en:
- **Opciones rápidas**: 10 puntos
- **Respuestas cortas** (<50 chars): 15 puntos
- **Respuestas medianas** (50-100 chars): 25 puntos
- **Respuestas largas** (100+ chars): 40 puntos
- **Bonus de calidad** (IA): +20 puntos
- **Bonus sentimiento positivo**: +10 puntos
- **Primera respuesta**: +50 puntos

### Sistema de Badges

Los badges se desbloquean automáticamente al cumplir criterios:
- 🎤 **First Voice**: Primera respuesta en un evento
- 🔥 **On Fire**: Racha de 5 eventos consecutivos
- 💎 **Insight Master**: 10 respuestas de alta calidad
- 👑 **Community Leader**: 1000 puntos acumulados
- 🎯 **Perfectionist**: Completa todas las preguntas
- ⚡ **Speed Demon**: Responde en menos de 10 segundos
- ✍️ **Wordsmith**: Respuesta de más de 200 caracteres
- 😊 **Positive Vibes**: 10 respuestas con sentimiento positivo

## 🧪 Endpoints de API Disponibles

### Events
- `GET /api/events` - Listar eventos
- `GET /api/events/{id}` - Obtener evento
- `POST /api/events` - Crear evento
- `GET /api/events/{id}/rankings` - Rankings del evento
- `GET /api/events/{id}/stats` - Estadísticas del evento
- `POST /api/events/{id}/start` - Iniciar evento
- `POST /api/events/{id}/complete` - Completar evento

### Participants
- `POST /api/participants` - Unirse a un evento
- `GET /api/participants/{id}` - Obtener participante
- `GET /api/participants/{id}/stats` - Estadísticas del participante
- `GET /api/participants/{id}/badges` - Badges del participante

### Questions
- `GET /api/questions?event_id={id}` - Listar preguntas del evento
- `POST /api/questions` - Crear pregunta
- `POST /api/questions/generate` - Generar pregunta con IA

### Responses
- `POST /api/responses` - Enviar respuesta (con análisis de IA automático)
- `GET /api/responses/top/quality?event_id={id}` - Top respuestas de calidad

### Messages
- `GET /api/messages?event_id={id}` - Obtener mensajes del chat
- `POST /api/messages` - Enviar mensaje

### Nybblers (People Force Mock)
- `GET /api/nybblers` - Listar todos los Nybblers
- `GET /api/nybblers/search?query={name}` - Buscar Nybblers
- `GET /api/nybblers/{id}` - Obtener Nybbler por ID

## 📚 Documentación de API

Una vez que el backend esté corriendo, puedes explorar la API completa en:

- **Swagger UI**: http://localhost:8080/api/swagger
- **OpenAPI JSON**: http://localhost:8080/api/openapi.json
- **OpenAPI YAML**: http://localhost:8080/api/openapi.yaml

## 🛠️ Comandos Útiles

### Backend

```bash
# Ejecutar backend
npm run dev:python

# Ejecutar migraciones
cd backend/python
alembic upgrade head

# Crear nueva migración
alembic revision -m "descripcion"

# Seed de datos
python seed_data.py
```

### Frontend

```bash
# Ejecutar frontend
npm run dev:frontend

# Build para producción
npm run build:frontend
```

### Ambos (Backend + Frontend)

```bash
# Ejecutar todo junto (desde la raíz)
npm run dev
```

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not set"
- Asegúrate de haber creado el archivo `.env` en `backend/python/`
- Verifica que la variable `GEMINI_API_KEY` tenga tu API key válida

### Error: "Database connection failed"
- Verifica que PostgreSQL esté corriendo
- Verifica que el `DATABASE_URL` en `.env` sea correcto
- Asegúrate de que la base de datos exista

### Error: "Module not found"
- Ejecuta `pip install -r requirements.txt` en `backend/python/`
- Ejecuta `npm install` en `frontend/`

### Error: "Port already in use"
- Backend: Cambia el `PORT` en `backend/python/.env`
- Frontend: El puerto se asigna automáticamente si 5173 está ocupado

## 🎉 ¡Listo!

Si todo está configurado correctamente:

1. Backend corriendo en http://localhost:8080
2. Frontend corriendo en http://localhost:5173
3. Evento de ejemplo disponible en http://localhost:5173/events/1

¡Disfruta de tu Event Engagement Hub con IA! 🚀

