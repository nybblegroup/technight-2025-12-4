# 🧪 Testing Guide - Nybble Event Hub

## Cómo dar Feedback Múltiples Veces

Cuando estás testeando la aplicación, el backend **previene que respondas la misma pregunta dos veces** (esto es correcto en producción). Sin embargo, durante el desarrollo necesitas poder probar múltiples veces.

---

## ✅ Solución 1: Auto-Reset (RECOMENDADO)

**El frontend ahora crea automáticamente un nuevo participante cada vez que recargas la página.**

### Cómo Funciona

Cada vez que entras a http://localhost:5173/events/1:
- Se genera un `user_id` único basado en el timestamp
- Se crea un nuevo participante en la base de datos
- Puedes responder todas las preguntas de nuevo

### Código

```typescript
// Genera un ID único cada vez
const sessionUserId = `test_${Date.now()}`;

const participantData = await api.participants.join({
  event_id: Number(eventId),
  user_id: sessionUserId,
  name: "Tú",
  email: `test_${Date.now()}@nybble.com.ar`,
  avatar_url: "https://i.pravatar.cc/150?img=5"
});
```

### Uso

```bash
# 1. Recarga la página
http://localhost:5173/events/1

# 2. Se crea un nuevo participante automáticamente
# 3. Puedes responder todas las preguntas de nuevo
# 4. Tus respuestas anteriores se mantienen en la BD (útil para analytics)
```

### Ventajas

✅ No necesitas resetear nada manualmente
✅ Mantiene histórico de todas las pruebas
✅ Simula múltiples usuarios reales
✅ Puedes ver cómo cambia el ranking

---

## ✅ Solución 2: Script de Reset

Si quieres **limpiar completamente** las respuestas y volver a empezar:

### Script: `reset_responses.py`

```bash
cd backend/python
python3 reset_responses.py
```

Este script:
- ✅ Borra todas las respuestas de todos los participantes
- ✅ Resetea puntos a 0
- ✅ Resetea estadísticas (quality_score, sentiment_score)
- ✅ Borra mensajes de usuarios del chat
- ✅ Mantiene las preguntas y el evento

### Cuándo Usar

- Quieres empezar completamente de cero
- Quieres limpiar datos de prueba antes de una demo
- Necesitas resetear el ranking

### Ejemplo de Uso

```bash
cd backend/python

# Resetear todas las respuestas
echo "yes" | python3 reset_responses.py

# Recarga el frontend
# http://localhost:5173/events/1
```

---

## 🔄 Workflow de Testing Recomendado

### Durante Desarrollo (Testing Rápido)

```bash
# 1. Simplemente recarga la página
# Cada recarga = nuevo participante

http://localhost:5173/events/1
```

### Antes de una Demo (Limpieza)

```bash
# 1. Resetear respuestas
cd backend/python
python3 reset_responses.py

# 2. (Opcional) Re-seed con datos limpios
python3 seed_data.py

# 3. Iniciar demo
http://localhost:5173/events/1
```

---

## 📊 Ver Todos los Participantes (Debug)

Si quieres ver cuántos participantes de prueba se crearon:

```bash
# Conectarse a la base de datos
psql -d nybble_event_hub

# Ver participantes
SELECT id, user_id, name, email, points, responses_count 
FROM participants 
WHERE event_id = 1
ORDER BY points DESC;

# Contar participantes de prueba
SELECT COUNT(*) FROM participants 
WHERE user_id LIKE 'test_%';
```

---

## 🧹 Limpiar Participantes de Prueba

Si acumulaste muchos participantes de prueba:

```bash
cd backend/python
python3 reset_responses.py
```

O manualmente en psql:

```sql
-- Borrar solo participantes de prueba
DELETE FROM responses 
WHERE participant_id IN (
  SELECT id FROM participants WHERE user_id LIKE 'test_%'
);

DELETE FROM participants 
WHERE user_id LIKE 'test_%';
```

---

## 🎯 Scripts Disponibles

### En `backend/python/`

| Script | Propósito |
|--------|-----------|
| `seed_data.py` | Crear evento y datos iniciales |
| `reset_responses.py` | Resetear respuestas y puntos |
| `reset_db.py` | Resetear toda la base de datos |

### Uso Común

```bash
cd backend/python

# Resetear solo respuestas (mantiene evento y preguntas)
python3 reset_responses.py

# Resetear toda la BD (elimina todo)
python3 reset_db.py
alembic upgrade head
python3 seed_data.py
```

---

## 💡 Tips

### 1. Ver Ranking en Tiempo Real

Abre múltiples pestañas del navegador:
```
Tab 1: http://localhost:5173/events/1 (Participante 1)
Tab 2: http://localhost:5173/events/1 (Participante 2)
Tab 3: http://localhost:5173/events/1 (Participante 3)
```

Cada tab será un participante diferente. Verás cómo cambia el ranking en tiempo real.

### 2. Probar con Diferentes User IDs

Puedes modificar el código para usar nombres específicos:

```typescript
// EventHub.tsx - para testing con nombres reales
const testUsers = [
  { id: "maria", name: "María González", avatar: 1 },
  { id: "carlos", name: "Carlos Ruiz", avatar: 2 },
  { id: "ana", name: "Ana Martínez", avatar: 3 },
];

const randomUser = testUsers[Math.floor(Math.random() * testUsers.length)];

const participantData = await api.participants.join({
  event_id: Number(eventId),
  user_id: `${randomUser.id}_${Date.now()}`,
  name: randomUser.name,
  email: `${randomUser.id}@nybble.com.ar`,
  avatar_url: `https://i.pravatar.cc/150?img=${randomUser.avatar}`
});
```

### 3. Testing de Gemini AI

Si quieres probar el análisis de sentimiento:

**Respuestas Positivas:**
- "Me encantó la presentación, muy clara y útil"
- "Excelente explicación sobre embeddings"
- "Definitivamente implementaré estas técnicas"

**Respuestas Negativas:**
- "No entendí nada, muy confuso"
- "Demasiado complicado para mi nivel"
- "No me gustó el enfoque"

**Respuestas Neutras:**
- "Fue informativo"
- "Creo que necesito más tiempo para procesarlo"
- "Interesante concepto"

---

## 🎉 Resumen

### Testing Rápido
✅ **Simplemente recarga la página** - cada recarga crea un nuevo participante

### Limpieza Completa
✅ **`python3 reset_responses.py`** - elimina todas las respuestas

### Reset Total
✅ **`python3 reset_db.py`** + seed - empieza desde cero

---

¡Ahora puedes testear infinitamente sin problemas! 🚀





