# ✨ Feature: Botón de Reiniciar

## Nueva Funcionalidad

Se agregó un **botón "🔄 Reiniciar"** en el header del Event Hub que permite resetear tus respuestas y empezar de nuevo sin recargar la página.

---

## 🎯 Ubicación

El botón está ubicado en el **header del chat**, junto al contador de puntos:

```
┌─────────────────────────────────────────────────────┐
│ Tech Night: AI en Producción                       │
│ 📅 Hoy | 👥 87 participantes | ⏱️ En vivo          │
│                                                     │
│                    [🔄 Reiniciar]  [850 Puntos]   │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Cómo Funciona

### Frontend

1. **Click en "🔄 Reiniciar"**
   - Muestra confirmación: "¿Estás seguro?"
   
2. **Confirmación**
   - Llama a `/api/participants/{id}/reset`
   
3. **Recarga Automática**
   - Recarga todos los datos del evento
   - Resetea el estado local
   - Vuelve a la primera pregunta

### Backend

**Endpoint:** `POST /api/participants/{participant_id}/reset`

**Acciones:**
1. ✅ Elimina todas las respuestas del participante
2. ✅ Elimina mensajes del usuario en el chat
3. ✅ Resetea puntos a 0
4. ✅ Resetea estadísticas (quality_score, sentiment_score)
5. ✅ Resetea conteo de respuestas
6. ✅ Resetea posición en ranking

**NO elimina:**
- ❌ El participante (se mantiene en la BD)
- ❌ El evento
- ❌ Las preguntas
- ❌ Los badges del sistema
- ❌ Otros participantes

---

## 💻 Implementación

### Backend: `routes/participants.py`

```python
@router.post("/{participant_id}/reset")
async def reset_participant_responses(
    participant_id: int,
    db: Session = Depends(get_db)
):
    """Reset participant's responses, points, and stats (for testing)"""
    participant = db.query(Participant).filter(
        Participant.id == participant_id
    ).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    from models import Response, Message
    
    # Delete all responses
    db.query(Response).filter(Response.participant_id == participant_id).delete()
    
    # Delete user messages
    db.query(Message).filter(
        Message.participant_id == participant_id,
        Message.message_type == 'user'
    ).delete()
    
    # Reset participant stats
    participant.points = 0
    participant.responses_count = 0
    participant.quality_score = 0.0
    participant.sentiment_score = 0.0
    participant.rank_position = None
    
    db.commit()
    db.refresh(participant)
    
    return {
        "message": "Participant responses reset successfully",
        "participant_id": participant_id,
        "points": participant.points
    }
```

### Frontend API Client: `utils/api.ts`

```typescript
participants: {
  // ... otros métodos
  reset: (id: number) => apiFetch<{
    message: string; 
    participant_id: number; 
    points: number
  }>(`/api/participants/${id}/reset`, {
    method: 'POST',
  }),
}
```

### Frontend EventHub: `pages/EventHub.tsx`

```typescript
const handleReset = async () => {
  if (!participant) return;

  const confirmed = window.confirm(
    '¿Estás seguro que quieres reiniciar? Se borrarán todas tus respuestas y puntos.'
  );

  if (!confirmed) return;

  try {
    setLoading(true);

    // Call reset endpoint
    await api.participants.reset(participant.id);

    // Reload event data
    await loadEventData();

    alert('✅ Reiniciado con éxito! Puedes responder todas las preguntas de nuevo.');
  } catch (error) {
    console.error('Error resetting:', error);
    alert('❌ Error al reiniciar. Por favor recarga la página.');
  } finally {
    setLoading(false);
  }
};
```

### Frontend ChatContainer: `components/eventhub/ChatContainer.tsx`

```typescript
<button
  onClick={onReset}
  style={{
    background: 'rgba(255, 255, 255, 0.2)',
    border: '2px solid rgba(255, 255, 255, 0.5)',
    color: 'white',
    padding: '8px 16px',
    borderRadius: '12px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    transition: 'all 0.3s ease',
  }}
  onMouseEnter={(e) => {
    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)';
    e.currentTarget.style.transform = 'translateY(-2px)';
  }}
  onMouseLeave={(e) => {
    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
    e.currentTarget.style.transform = 'translateY(0)';
  }}
>
  🔄 Reiniciar
</button>
```

---

## 🎨 UI/UX

### Diseño del Botón

- **Color**: Semi-transparente sobre el gradient del header
- **Efecto Hover**: 
  - Fondo más opaco
  - Elevación (translateY -2px)
- **Icono**: 🔄 (emoji de refresh)
- **Texto**: "Reiniciar"

### Confirmación

```
┌───────────────────────────────────────────┐
│  ⚠️  Confirmar                            │
├───────────────────────────────────────────┤
│                                           │
│  ¿Estás seguro que quieres reiniciar?    │
│  Se borrarán todas tus respuestas y       │
│  puntos.                                  │
│                                           │
│        [Cancelar]      [Aceptar]         │
│                                           │
└───────────────────────────────────────────┘
```

### Mensajes

**Éxito:**
```
✅ Reiniciado con éxito! 
   Puedes responder todas las preguntas de nuevo.
```

**Error:**
```
❌ Error al reiniciar. 
   Por favor recarga la página.
```

---

## 🧪 Testing

### Flujo Normal

```bash
# 1. Abrir evento
http://localhost:5173/events/1

# 2. Responder algunas preguntas
Pregunta 1: ✅ Respondida (15 pts)
Pregunta 2: ✅ Respondida (25 pts)
Total: 40 pts

# 3. Click en "🔄 Reiniciar"
[Confirmar] → Sí

# 4. Verificar reset
Puntos: 0 pts
Pregunta actual: Pregunta 1
Mensajes del chat: Solo mensajes del bot
Ranking: Posición actualizada
```

### Casos de Prueba

| Caso | Esperado |
|------|----------|
| Click en Reiniciar → Cancelar | No hace nada |
| Click en Reiniciar → Aceptar | Resetea todo |
| Reiniciar en pregunta #3 | Vuelve a pregunta #1 |
| Reiniciar con 500 pts | Puntos = 0 |
| Reiniciar y responder de nuevo | Funciona correctamente |

---

## 📊 Comparación de Métodos de Reset

| Método | Ventajas | Cuándo Usar |
|--------|----------|-------------|
| **🔄 Botón Reiniciar** | • Sin recargar página<br>• UX fluida<br>• Mantiene participante | Testing rápido durante desarrollo |
| **F5 Recarga** | • Nuevo participante<br>• Simula usuario real | Testing de múltiples usuarios |
| **Script reset_responses.py** | • Resetea todos<br>• Limpieza completa | Antes de demos o presentaciones |

---

## 🎯 Casos de Uso

### Durante Desarrollo

```
1. Probar cambios en preguntas
   → Reiniciar → Responder con nuevos textos

2. Probar análisis de IA
   → Responder → Ver sentimiento → Reiniciar → Probar otro sentimiento

3. Probar sistema de puntos
   → Responder → Ver puntos → Reiniciar → Probar con respuestas diferentes
```

### Testing de Features

```
1. Probar Quick Options
   → Elegir opción → Reiniciar → Elegir otra opción

2. Probar Rating
   → Dar 5 estrellas → Reiniciar → Dar 1 estrella → Comparar sentimiento

3. Probar Badges
   → Responder todas → Ver badges → Reiniciar → Intentar desbloquear otros
```

### Demos

```
1. Mostrar flujo completo
   → Responder todas las preguntas → Mostrar resultado final

2. Reiniciar para otra demo
   → Click "🔄 Reiniciar" → Repetir con audiencia diferente
```

---

## 🔒 Seguridad

### Validaciones

✅ Verifica que el participante exista
✅ Solo resetea datos del participante específico
✅ No afecta a otros participantes
✅ No elimina el evento ni las preguntas

### Limitaciones

⚠️ Cualquier usuario puede resetear cualquier participante (conociendo el ID)
⚠️ Para producción, agregar autenticación:

```typescript
// Futuro: Validar que el usuario autenticado es el dueño del participante
if (participant.user_id !== current_user.id):
    raise HTTPException(status_code=403, detail="Forbidden")
```

---

## 📁 Archivos Modificados

### Backend
- ✅ `backend/python/routes/participants.py` - Nuevo endpoint `/reset`

### Frontend
- ✅ `frontend/src/utils/api.ts` - Método `participants.reset()`
- ✅ `frontend/src/pages/EventHub.tsx` - Handler `handleReset()`
- ✅ `frontend/src/components/eventhub/ChatContainer.tsx` - Botón UI

---

## 🚀 Próximas Mejoras (Opcional)

1. **Animación de Reset**
   - Fade out/in del chat
   - Loading spinner más elegante

2. **Confirmación Moderna**
   - Modal personalizado en lugar de `window.confirm`
   - Mejor UX con animaciones

3. **Estadísticas de Reset**
   - Contador: "Has reiniciado 3 veces"
   - Análisis de comparación de intentos

4. **Undo Reset**
   - Guardar snapshot antes de resetear
   - Permitir deshacer en 5 segundos

---

## ✅ Conclusión

El botón de **🔄 Reiniciar** mejora significativamente la experiencia de testing:

✅ No necesitas recargar la página
✅ No necesitas ejecutar scripts
✅ UX simple y directa
✅ Perfecto para desarrollo y demos

¡Ahora puedes probar el Event Hub infinitamente sin fricción! 🎉





