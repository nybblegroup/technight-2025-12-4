# 🛠️ Nybble Event Hub - Comandos Útiles

## 📦 Instalación Inicial

```bash
# Instalar dependencias del backend
cd backend/python
pip install -r requirements.txt

# Instalar dependencias del frontend
cd ../..
npm install
```

---

## 🗄️ Base de Datos

```bash
cd backend/python

# Ejecutar todas las migraciones
alembic upgrade head

# Ver estado actual de migraciones
alembic current

# Crear una nueva migración (después de cambiar models.py)
alembic revision -m "descripcion del cambio"

# Revertir última migración
alembic downgrade -1

# Ver historial de migraciones
alembic history

# Seed de datos de ejemplo
python seed_data.py
```

---

## 🚀 Ejecutar la Aplicación

```bash
# OPCIÓN 1: Ejecutar todo junto (desde la raíz)
npm run dev

# OPCIÓN 2: Ejecutar por separado

# Backend (Terminal 1)
cd backend/python
python main.py

# Frontend (Terminal 2)
npm run dev:frontend
```

---

## 🔍 Testing & Debugging

```bash
# Ver logs del backend
cd backend/python
python main.py
# Los logs aparecerán en la consola

# Verificar health del backend
curl http://localhost:8080/api/health

# Verificar health de la base de datos
curl http://localhost:8080/api/health/db

# Ver documentación Swagger
open http://localhost:8080/api/swagger

# Ver OpenAPI spec
curl http://localhost:8080/api/openapi.json | jq
```

---

## 🧪 API Testing con cURL

### Events

```bash
# Listar todos los eventos
curl http://localhost:8080/api/events

# Obtener evento específico
curl http://localhost:8080/api/events/1

# Crear nuevo evento
curl -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Evento",
    "description": "Descripción del evento",
    "event_date": "2025-12-10T18:00:00Z",
    "event_type": "tech_night"
  }'

# Ver rankings del evento
curl http://localhost:8080/api/events/1/rankings

# Ver estadísticas del evento
curl http://localhost:8080/api/events/1/stats
```

### Participants

```bash
# Unirse a un evento
curl -X POST http://localhost:8080/api/participants \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "user_id": "test123",
    "name": "Test User",
    "email": "test@nybble.com.ar"
  }'

# Ver participante
curl http://localhost:8080/api/participants/1

# Ver badges del participante
curl http://localhost:8080/api/participants/1/badges
```

### Questions

```bash
# Listar preguntas de un evento
curl http://localhost:8080/api/questions?event_id=1

# Crear pregunta
curl -X POST http://localhost:8080/api/questions \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "text": "¿Qué te pareció?",
    "question_type": "open",
    "order": 1
  }'

# Generar pregunta con IA
curl -X POST http://localhost:8080/api/questions/generate \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "context": "Tech Night sobre IA en Producción"
  }'
```

### Responses

```bash
# Enviar respuesta (con análisis de IA automático)
curl -X POST http://localhost:8080/api/responses \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1,
    "participant_id": 1,
    "text": "Me pareció excelente la presentación sobre embeddings!",
    "is_quick_option": false
  }'

# Ver top respuestas de calidad
curl http://localhost:8080/api/responses/top/quality?event_id=1&limit=5
```

### Messages

```bash
# Ver mensajes del chat
curl http://localhost:8080/api/messages?event_id=1

# Enviar mensaje
curl -X POST http://localhost:8080/api/messages \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "participant_id": 1,
    "text": "Hola!",
    "message_type": "user"
  }'
```

### Nybblers (People Force Mock)

```bash
# Listar todos los Nybblers
curl http://localhost:8080/api/nybblers

# Buscar Nybblers
curl http://localhost:8080/api/nybblers/search?query=maria

# Obtener Nybbler específico
curl http://localhost:8080/api/nybblers/1
```

---

## 🧹 Limpieza

```bash
# Limpiar cache de Python
cd backend/python
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Limpiar node_modules (si necesitas reinstalar)
cd ../..
rm -rf node_modules frontend/node_modules
npm install
```

---

## 📊 Monitoreo

```bash
# Ver procesos corriendo
ps aux | grep python  # Backend
ps aux | grep node    # Frontend

# Ver puertos en uso
lsof -i :8080  # Backend
lsof -i :5173  # Frontend

# Kill proceso si está bloqueado
kill -9 $(lsof -t -i:8080)  # Backend
kill -9 $(lsof -t -i:5173)  # Frontend
```

---

## 🔧 Configuración

```bash
# Editar configuración del backend
nano backend/python/.env

# Editar configuración del frontend
nano frontend/.env

# Ver variables de entorno cargadas (Python)
cd backend/python
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

---

## 📦 Build para Producción

```bash
# Build del frontend
cd frontend
npm run build
# Output en: frontend/dist/

# Build del backend (no necesario, Python se ejecuta directamente)
# Solo asegúrate de que .env esté configurado correctamente
```

---

## 🐳 Docker (Futuro)

```bash
# TODO: Agregar Dockerfile y docker-compose.yml
# docker-compose up -d
```

---

## 📝 Logs & Debugging

```bash
# Ver logs del backend en tiempo real
cd backend/python
python main.py 2>&1 | tee backend.log

# Ver logs del frontend
npm run dev:frontend 2>&1 | tee frontend.log

# Buscar errores en logs
grep -i "error" backend.log
grep -i "failed" frontend.log
```

---

## 🔐 Seguridad

```bash
# NUNCA commitees el .env
git check-ignore backend/python/.env
# Debería mostrar: backend/python/.env

# Ver qué archivos están ignorados
git status --ignored

# Verificar que .env NO está en git
git ls-files | grep .env
# No debería mostrar nada
```

---

## 🚨 Troubleshooting Rápido

```bash
# Resetear base de datos (CUIDADO: borra todo)
cd backend/python
alembic downgrade base
alembic upgrade head
python seed_data.py

# Reinstalar dependencias Python
pip install --force-reinstall -r requirements.txt

# Reinstalar dependencias Node
npm ci

# Verificar versiones
python --version  # Debería ser >= 3.12
node --version    # Debería ser >= 20.19
npm --version     # Debería ser >= 10.0
```

---

## 📚 URLs Importantes

```bash
# Frontend
http://localhost:5173              # Home
http://localhost:5173/events/1     # Event Hub
http://localhost:5173/examples     # Ejemplos (legacy)

# Backend
http://localhost:8080/api/health   # Health check
http://localhost:8080/api/swagger  # API docs (Swagger)
http://localhost:8080/api/openapi.json  # OpenAPI spec

# Database (local)
psql -h localhost -p 5432 -U user -d nybble_event_hub
```

---

## 💡 Tips

```bash
# Ejecutar en modo debug (backend)
cd backend/python
PYTHONUNBUFFERED=1 python main.py

# Watch mode para frontend (ya incluido en dev)
npm run dev:frontend  # Ya tiene hot reload

# Prettier para formatear código frontend
cd frontend
npm run format  # Si lo agregas a package.json

# Linting
cd backend/python
pylint models.py schemas.py  # Si instalas pylint
```

---

## 🎯 Workflow Típico de Desarrollo

```bash
# 1. Pull últimos cambios
git pull

# 2. Instalar nuevas dependencias (si las hay)
cd backend/python && pip install -r requirements.txt
cd ../.. && npm install

# 3. Ejecutar migraciones nuevas
cd backend/python && alembic upgrade head

# 4. Ejecutar backend y frontend
# Terminal 1:
cd backend/python && python main.py

# Terminal 2:
npm run dev:frontend

# 5. Hacer cambios, testear, commitear
git add .
git commit -m "feat: descripción del cambio"
git push
```

---

¿Necesitas ayuda? Consulta:
- [QUICK_START.md](./QUICK_START.md) - Inicio rápido
- [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) - Setup completo
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Resumen técnico





