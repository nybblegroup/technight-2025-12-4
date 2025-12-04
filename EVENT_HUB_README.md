# 🎉 Nybble Event Engagement Hub

> Plataforma AI-powered de engagement para eventos con gamificación, chat conversacional y analytics en tiempo real.

![Status](https://img.shields.io/badge/status-production--ready-success)
![Python](https://img.shields.io/badge/python-3.12-blue)
![React](https://img.shields.io/badge/react-19.0-61dafb)
![AI](https://img.shields.io/badge/AI-Gemini-orange)

---

## 🚀 Quick Start

### 1️⃣ Configurar Backend

```bash
cd backend/python

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env con:
# DATABASE_URL="postgresql://user:password@localhost:5432/nybble_event_hub"
# GEMINI_API_KEY="tu-api-key-aqui"

# Ejecutar migraciones
alembic upgrade head

# Seed de datos
python seed_data.py

# Ejecutar servidor
python main.py
```

### 2️⃣ Configurar Frontend

```bash
# Desde la raíz
npm install

# Ejecutar frontend
npm run dev:frontend
```

### 3️⃣ Acceder

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **Swagger**: http://localhost:8080/api/swagger
- **Evento Demo**: http://localhost:5173/events/1

---

## 🎯 Características Principales

### 🤖 IA Integrada (Gemini)
- ✅ Análisis de sentimiento automático
- ✅ Cálculo de calidad de respuestas
- ✅ Generación de preguntas contextuales
- ✅ Insights en tiempo real

### 🎮 Gamificación Completa
- ✅ Sistema de puntos dinámico
- ✅ 8 badges desbloqueables
- ✅ Rankings en tiempo real
- ✅ Rachas y logros

### 💬 Chat Conversacional
- ✅ Interfaz tipo chatbot
- ✅ Opciones rápidas
- ✅ Rating con estrellas
- ✅ Respuestas abiertas
- ✅ @mentions de Nybblers

### 📊 Analytics & Reporting
- ✅ Dashboard de participantes
- ✅ Estadísticas de eventos
- ✅ Top respuestas de calidad
- ✅ Métricas de engagement

### 🎨 UI/UX Avanzado
- ✅ Temas dinámicos (sentimiento)
- ✅ Animaciones fluidas
- ✅ Responsive design
- ✅ Confetti y celebraciones

---

## 📚 Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM
- **Alembic** - Migraciones
- **Gemini AI** - Análisis con IA
- **PostgreSQL** - Base de datos

### Frontend
- **React 19** - UI library
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **React Router** - Routing
- **CSS Custom** - Estilos personalizados

---

## 🗂️ Estructura del Proyecto

```
technight-2025-12-4/
├── backend/python/          # Backend FastAPI
│   ├── models.py            # Modelos DB
│   ├── schemas.py           # DTOs
│   ├── routes/              # API endpoints
│   ├── services/            # Servicios (IA, gamificación)
│   ├── alembic/             # Migraciones
│   └── seed_data.py         # Seed script
│
├── frontend/                # Frontend React
│   ├── src/
│   │   ├── pages/           # Páginas
│   │   ├── components/      # Componentes
│   │   ├── utils/           # API client
│   │   └── styles/          # CSS
│   └── package.json
│
├── SETUP_INSTRUCTIONS.md    # Setup completo
├── IMPLEMENTATION_SUMMARY.md # Resumen técnico
└── EVENT_HUB_README.md      # Este archivo
```

---

## 🎮 Sistema de Puntos

| Acción | Puntos |
|--------|--------|
| Opción rápida | 10 pts |
| Respuesta corta (<50 chars) | 15 pts |
| Respuesta mediana (50-100) | 25 pts |
| Respuesta larga (100+) | 40 pts |
| **Bonus calidad alta** | +20 pts |
| **Bonus sentimiento positivo** | +10 pts |
| **Primera respuesta** | +50 pts |

---

## 🏅 Badges Disponibles

| Badge | Criterio | Rareza |
|-------|----------|--------|
| 🎤 First Voice | Primera respuesta | Common |
| 🔥 On Fire | Racha de 5 eventos | Rare |
| 💎 Insight Master | 10 respuestas de calidad | Epic |
| 👑 Community Leader | 1000 puntos | Legendary |
| 🎯 Perfectionist | Completa todas las preguntas | Rare |
| ⚡ Speed Demon | Responde en <10s | Rare |
| ✍️ Wordsmith | Respuesta >200 chars | Common |
| 😊 Positive Vibes | 10 respuestas positivas | Common |

---

## 🔑 Configuración Requerida

### Gemini API Key

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crea una API key
3. Agrégala a `backend/python/.env`:
   ```env
   GEMINI_API_KEY="tu-api-key-aqui"
   ```

### Database URL

```env
DATABASE_URL="postgresql://user:password@localhost:5432/nybble_event_hub"
```

---

## 📖 Documentación Completa

- **Setup detallado**: [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md)
- **Resumen técnico**: [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
- **Swagger API**: http://localhost:8080/api/swagger

---

## 🐛 Troubleshooting

### Backend no inicia
```bash
# Verifica que tienes PostgreSQL corriendo
# Verifica GEMINI_API_KEY en .env
# Verifica DATABASE_URL en .env
```

### Frontend no conecta
```bash
# Verifica que backend está en http://localhost:8080
# Verifica en consola del navegador los errores
```

### Error de migraciones
```bash
cd backend/python
alembic upgrade head
```

---

## 👥 Mock Data Incluido

El seed script crea:
- ✅ 1 evento: "Tech Night: AI en Producción"
- ✅ 4 participantes con puntos y avatares
- ✅ 5 preguntas variadas
- ✅ 8 badges del sistema
- ✅ 10 Nybblers de People Force

---

## 🎯 Próximos Pasos (Opcional)

- [ ] WebSockets para real-time
- [ ] Autenticación real
- [ ] Integración real con Slack
- [ ] Integración real con Google Calendar
- [ ] Dashboard administrativo
- [ ] Testing automatizado
- [ ] CI/CD pipeline
- [ ] Docker deployment

---

## 📧 Contacto

**Proyecto:** Nybble Event Engagement Hub  
**Versión:** 2.0.0  
**Status:** Production Ready ✨

---

## 📄 Licencia

Este proyecto es propiedad de **Nybble**.

---

<div align="center">

**🚀 ¡Listo para revolucionar tus eventos con IA! 🎉**

[Ver Documentación](./SETUP_INSTRUCTIONS.md) • [Resumen Técnico](./IMPLEMENTATION_SUMMARY.md) • [Swagger API](http://localhost:8080/api/swagger)

</div>





