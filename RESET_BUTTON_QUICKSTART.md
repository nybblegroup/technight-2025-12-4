# 🔄 Botón de Reiniciar - Quick Start

## ¡Nueva Funcionalidad Agregada!

Ahora tienes un **botón "🔄 Reiniciar"** en el Event Hub para resetear tus respuestas sin recargar la página.

---

## 🚀 Cómo Usarlo

### 1. Reiniciar el Backend (IMPORTANTE)

El backend necesita reiniciarse para tomar el nuevo endpoint:

```bash
# Presiona Ctrl+C en el terminal del backend

# Luego ejecuta de nuevo:
cd backend/python
python3 main.py
```

### 2. Refrescar el Frontend

El frontend se recargará automáticamente si tienes `npm run dev:frontend` corriendo.

Si no, recarga la página del navegador: **F5**

### 3. Usar el Botón

```
1. Ve a: http://localhost:5173/events/1
2. Responde algunas preguntas
3. Click en "🔄 Reiniciar" (arriba a la derecha)
4. Confirma: "Sí"
5. ¡Listo! Puedes responder de nuevo
```

---

## 🎯 Qué Hace el Botón

**Al hacer click:**

1. ⚠️ Te pide confirmación
2. 🗑️ Elimina tus respuestas
3. 🔄 Resetea tus puntos a 0
4. 💬 Borra tus mensajes del chat
5. 📊 Actualiza el ranking
6. 🔙 Vuelve a la primera pregunta
7. ✅ Muestra confirmación de éxito

---

## 📊 Comparación

| Método | Ventajas | Cuándo Usar |
|--------|----------|-------------|
| **🔄 Botón Reiniciar** | • Sin recargar<br>• Rápido<br>• Simple | Testing rápido |
| **F5 Recarga Página** | • Nuevo participante<br>• Simula usuario real | Testing de múltiples usuarios |
| **Script reset_responses.py** | • Resetea todos<br>• Limpieza total | Antes de demos |

---

## 🎨 Vista Previa

```
╔══════════════════════════════════════════════════════╗
║ Tech Night: AI en Producción        [🔄 Reiniciar] ║
║ 📅 Hoy | 👥 5 participantes                 850 pts ║
╠══════════════════════════════════════════════════════╣
║ ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░ 50%                           ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🤖 Pregunta 3 de 5:                                ║
║     Del 1 al 5, ¿qué tan clara fue la explicación? ║
║                                                      ║
║     ⭐ ⭐ ⭐ ⭐ ⭐                                    ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

**Click en "🔄 Reiniciar" →**

```
╔══════════════════════════════════════════════════════╗
║  ⚠️  Confirmar                                       ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  ¿Estás seguro que quieres reiniciar?               ║
║  Se borrarán todas tus respuestas y puntos.         ║
║                                                      ║
║           [Cancelar]      [Aceptar]                 ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

**Después de confirmar:**

```
╔══════════════════════════════════════════════════════╗
║ Tech Night: AI en Producción        [🔄 Reiniciar] ║
║ 📅 Hoy | 👥 5 participantes                   0 pts ║
╠══════════════════════════════════════════════════════╣
║ ░░░░░░░░░░░░░░░░░░░░ 0%                            ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🤖 Pregunta 1 de 5:                                ║
║     ¿Qué te motivó a unirte a este evento hoy?     ║
║                                                      ║
║     [💡 Aprender sobre IA] [🤝 Networking]          ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

## ✅ Checklist de Uso

Para que funcione, asegúrate de:

- [ ] Reiniciar el backend (Ctrl+C → `python3 main.py`)
- [ ] Frontend recargado automáticamente (o presiona F5)
- [ ] Navega a http://localhost:5173/events/1
- [ ] Verás el botón "🔄 Reiniciar" en el header

---

## 🐛 Troubleshooting

### El botón no aparece
✅ Recarga la página (F5)
✅ Verifica que el frontend se haya actualizado

### Error al hacer click
✅ Reinicia el backend con `python3 main.py`
✅ Verifica que el backend esté en http://localhost:8080

### No se resetea
✅ Revisa la consola del navegador (F12)
✅ Revisa los logs del backend
✅ Verifica la conexión a la base de datos

---

## 🎉 ¡Listo!

**REINICIA EL BACKEND** y recarga el frontend.

Verás el botón "🔄 Reiniciar" en la esquina superior derecha del chat.

¡Ahora puedes testear infinitamente! 🚀





