# 🔧 Troubleshooting - No Veo la Pregunta 1

## Problema

No se ve la pregunta 1 cuando cargas el Event Hub.

---

## ✅ Solución Rápida (3 Pasos)

### 1️⃣ Verificar que el Backend Esté Corriendo

```bash
# Abre una terminal y verifica:
curl http://localhost:8080/api/health

# Debería devolver:
# {"status":"ok","timestamp":"..."}
```

Si no funciona:
```bash
cd backend/python
python3 main.py
```

### 2️⃣ Verificar Mensajes en la Base de Datos

```bash
cd backend/python

# Script rápido de verificación
python3 -c "
from database import SessionLocal
from models import Message

db = SessionLocal()
messages = db.query(Message).filter(Message.event_id == 1).all()
print(f'Mensajes en DB: {len(messages)}')
for msg in messages:
    print(f'  - [{msg.message_type}] {msg.text[:50]}...')
db.close()
"
```

**Si muestra 0 mensajes**, ejecuta:
```bash
# Crear mensajes iniciales
python3 -c "
from database import SessionLocal
from models import Message, Question

db = SessionLocal()

# Delete old messages
db.query(Message).filter(Message.event_id == 1).delete()

# Get first question
first_q = db.query(Question).filter(Question.event_id == 1).order_by(Question.order).first()
total_q = db.query(Question).filter(Question.event_id == 1).count()

# Welcome message
db.add(Message(
    event_id=1,
    text='¡Hola! 👋 Bienvenido al Tech Night de hoy. Soy tu asistente IA y voy a guiarte en esta experiencia.<br><br>Tus respuestas nos ayudan a mejorar y vos ganás puntos para el ranking. ¡Empecemos! 🚀',
    message_type='bot'
))

# First question
db.add(Message(
    event_id=1,
    text=f'Pregunta 1 de {total_q}:<br><strong>{first_q.text}</strong>',
    message_type='bot'
))

db.commit()
db.close()
print('✅ Mensajes creados')
"
```

### 3️⃣ Recargar el Frontend

```bash
# En el navegador:
http://localhost:5173/events/1

# Presiona: F5 (recargar página)
```

---

## 🧪 Verificación Completa

### Verifica el API

```bash
# Ver mensajes del evento
curl http://localhost:8080/api/messages?event_id=1 | jq

# Debería mostrar 2 mensajes:
# [
#   {
#     "id": 1,
#     "text": "¡Hola! 👋 Bienvenido...",
#     "message_type": "bot",
#     ...
#   },
#   {
#     "id": 2,
#     "text": "Pregunta 1 de 5...",
#     "message_type": "bot",
#     ...
#   }
# ]
```

### Verifica el Frontend

Abre la consola del navegador (F12) y busca:

```javascript
// Debería ver:
GET http://localhost:8080/api/messages?event_id=1&limit=100
Status: 200 OK

// Y la respuesta con 2 mensajes
```

---

## 🐛 Problemas Comunes

### 1. "No aparece nada en el chat"

**Causa:** Los mensajes no están en la BD

**Solución:**
```bash
cd backend/python
python3 seed_data.py
```

### 2. "Solo veo un mensaje vacío"

**Causa:** El HTML no se está renderizando

**Solución:** Verifica que ChatContainer.tsx usa `dangerouslySetInnerHTML`

### 3. "Veo el mensaje pero sin opciones"

**Causa:** La pregunta no es de tipo `quick_options` o el `currentQuestion` es null

**Solución:** Verifica en consola del navegador:
```javascript
console.log(currentQuestion);
// Debería mostrar el objeto de la pregunta 1
```

### 4. "Error 500 en la API"

**Causa:** La tabla `messages` no existe o hay error de migraciones

**Solución:**
```bash
cd backend/python
python3 reset_db.py
alembic upgrade head
python3 seed_data.py
```

---

## 🎯 Estado Esperado Después del Fix

Cuando cargas http://localhost:5173/events/1 deberías ver:

```
┌────────────────────────────────────────────────┐
│ 🤖 ¡Hola! 👋 Bienvenido al Tech Night de hoy. │
│    Soy tu asistente IA...                      │
│                                          18:05 │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│ 🤖 Pregunta 1 de 5:                            │
│    ¿Qué te motivó a unirte a este evento hoy? │
│                                                │
│    [💡 Aprender sobre IA] [🤝 Networking]      │
│    [🎤 El speaker] [✍️ Escribir mi respuesta]  │
│                                          18:05 │
└────────────────────────────────────────────────┘
```

---

## 🔄 Reset Completo (Si Nada Funciona)

Si nada de lo anterior funciona, reset completo:

```bash
cd backend/python

# 1. Reset completo de BD
echo "yes" | python3 reset_db.py

# 2. Ejecutar migraciones
alembic upgrade head

# 3. Seed de datos
python3 seed_data.py

# 4. Reiniciar backend
# Ctrl+C en el terminal del backend
python3 main.py

# 5. Recargar frontend
# F5 en el navegador
```

---

## 📞 Si Sigue Sin Funcionar

Envíame:

1. **Output de:**
   ```bash
   curl http://localhost:8080/api/messages?event_id=1
   ```

2. **Console del navegador** (F12 → Console tab)

3. **Logs del backend** (en el terminal donde corre `python3 main.py`)

---

## ✅ Checklist

- [ ] Backend corriendo en http://localhost:8080
- [ ] Frontend corriendo en http://localhost:5173
- [ ] Mensajes en BD: `curl http://localhost:8080/api/messages?event_id=1` devuelve 2 mensajes
- [ ] Preguntas en BD: `curl http://localhost:8080/api/questions?event_id=1` devuelve 5 preguntas
- [ ] Página recargada con F5

Si todos los checks están ✅, debería funcionar!





