# 🎨 Gemini Sentiment & Color Themes - Guía Completa

## ✅ Arreglos Aplicados

### 1. Modelo de Gemini Actualizado

**Problema:**
```
Error analyzing sentiment: 404 models/gemini-pro is not found for API version v1beta
```

**Solución:**
El modelo `gemini-pro` fue deprecado. Ahora usamos `gemini-1.5-flash`.

**Cambio en `backend/python/services/gemini_service.py`:**
```python
# ANTES (deprecated)
self.model = genai.GenerativeModel('gemini-pro')

# AHORA (actualizado)
self.model = genai.GenerativeModel('gemini-2.5-flash')
```

**Alternativas:**
- `gemini-2.5-flash` ← **Usamos este** (rápido, gratis, última versión)
- `gemini-2.5-pro` - Mejor calidad, más lento
- `gemini-flash-latest` - Apunta siempre al último modelo flash disponible

---

### 2. Colores de Fondo Según Sentimiento

**Requisito:**
- 🔴 **Rojo** cuando el puntaje es bajo y palabras negativas
- 🟢 **Verde** cuando el puntaje es alto y palabras positivas
- 🔵 **Azul/Morado** cuando es neutral

**Implementación en `frontend/src/styles/eventhub.css`:**

```css
/* Temas emocionales - COLORES MÁS VISIBLES */
.event-hub.positive {
    /* Verde brillante cuando el sentimiento es positivo */
    --bg-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
}

.event-hub.negative {
    /* Rojo cuando el sentimiento es negativo */
    --bg-gradient: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
}

.event-hub.neutral {
    /* Azul/Morado neutro por defecto */
    --bg-gradient: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
}
```

**Cómo funciona:**
1. El usuario envía una respuesta
2. Gemini analiza el sentimiento → devuelve `positive`, `negative`, o `neutral`
3. El frontend aplica la clase CSS correspondiente al contenedor `event-hub`
4. El fondo cambia dinámicamente con transición suave

---

## 🧪 Cómo Probar

### Paso 1: Verificar que Gemini Está Funcionando

```bash
cd backend/python

# Verificar que la API key está configurada
cat .env | grep GEMINI_API_KEY

# Debería mostrar:
# GEMINI_API_KEY=tu_api_key_aqui
```

Si no está configurada:
```bash
echo "GEMINI_API_KEY=your_gemini_api_key" >> .env
```

**Obtener API Key:**
1. Ve a https://makersuite.google.com/app/apikey
2. Crea una nueva API key
3. Cópiala y agrégala al `.env`

### Paso 2: Reiniciar el Backend

```bash
cd backend/python

# Detener el servidor (Ctrl+C)
# Reiniciar
python3 main.py
```

### Paso 3: Probar Diferentes Sentimientos

Envía respuestas con diferentes tonos:

**Respuesta POSITIVA (fondo verde):**
```
"¡Excelente evento! Me encantó todo, muy claro e interesante. 
Definitivamente voy a aplicar esto en mi trabajo. Fantástico!"
```

**Respuesta NEGATIVA (fondo rojo):**
```
"No entendí nada, muy confuso y aburrido. 
La presentación fue terrible y muy complicada. 
No me sirvió para nada."
```

**Respuesta NEUTRAL (fondo azul/morado):**
```
"El evento estuvo bien. Algunos puntos fueron interesantes, 
otros no tanto. Nada especial."
```

### Paso 4: Verificar en la Consola del Backend

Cuando envíes una respuesta, deberías ver en el backend:

```bash
🤖 Gemini - Analyzing sentiment for: ¡Excelente evento! Me encantó todo...
✅ Gemini - Raw response: {"sentiment":"positive","score":0.85,"confidence":0.9}
📊 Sentiment: positive (score: 0.85, confidence: 0.90)
```

O si hay un error:

```bash
❌ Error analyzing sentiment: [detalles del error]
⚠️ Using fallback sentiment analysis based on keywords
📊 Sentiment: positive (score: 0.50, confidence: 0.60)
```

---

## 🔍 Debugging

### Verificar que el Sentiment se Está Enviando al Frontend

```bash
# Hacer una request de prueba
curl -X POST http://localhost:8080/api/responses \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1,
    "participant_id": 1,
    "text": "¡Excelente evento! Me encantó todo.",
    "is_quick_option": false
  }' | python3 -m json.tool
```

Debería devolver:

```json
{
  "id": 123,
  "sentiment": "positive",    ← IMPORTANTE
  "sentiment_score": 0.85,    ← IMPORTANTE
  "quality_score": 0.75,
  "points_awarded": 50,
  ...
}
```

### Verificar en el Navegador

Abre la consola del navegador (F12) y busca:

```javascript
// Network tab → busca la request a /api/responses
// Debería mostrar:
Response {
  sentiment: "positive",
  sentiment_score: 0.85,
  ...
}
```

Luego verifica que el estado se actualiza:

```javascript
// En EventHub.tsx línea 119:
if (response.sentiment) {
  setSentiment(response.sentiment as 'positive' | 'negative' | 'neutral');
}
```

### Verificar que la Clase CSS se Aplica

Inspecciona el elemento HTML del contenedor principal:

```html
<!-- ANTES de responder (neutral) -->
<div class="event-hub neutral">

<!-- DESPUÉS de responder con sentimiento positivo -->
<div class="event-hub positive">

<!-- DESPUÉS de responder con sentimiento negativo -->
<div class="event-hub negative">
```

El fondo debería cambiar instantáneamente.

---

## 🐛 Problemas Comunes

### 1. "Error analyzing sentiment: 404 models/gemini-pro is not found"

**Causa:** Modelo deprecado

**Solución:** ✅ Ya arreglado en `gemini_service.py` (usa `gemini-1.5-flash`)

**Verificar:**
```bash
grep "GenerativeModel" backend/python/services/gemini_service.py

# Debería mostrar:
# self.model = genai.GenerativeModel('gemini-1.5-flash')
```

---

### 2. "Error analyzing sentiment: API key not valid"

**Causa:** API key incorrecta o no configurada

**Solución:**
```bash
cd backend/python

# Verificar API key
cat .env | grep GEMINI_API_KEY

# Si no existe o es incorrecta:
# 1. Ve a https://makersuite.google.com/app/apikey
# 2. Crea una nueva API key
# 3. Actualiza el .env:
echo "GEMINI_API_KEY=tu_nueva_api_key" >> .env

# Reinicia el backend
python3 main.py
```

---

### 3. El fondo NO cambia de color

**Diagnóstico:**

#### A. Verificar que el sentiment se está devolviendo

```bash
# En la consola del backend, busca:
📊 Sentiment: positive (score: 0.85, confidence: 0.90)
```

Si NO aparece:
- Verifica que Gemini está funcionando
- Revisa los logs del backend para ver el error completo

#### B. Verificar que el frontend recibe el sentiment

```javascript
// En la consola del navegador (F12):
// Network tab → POST /api/responses → Response

// Debería incluir:
{
  "sentiment": "positive",
  "sentiment_score": 0.85,
  ...
}
```

Si NO aparece:
- El backend no está devolviendo el sentiment
- Verifica `routes/responses.py` línea 166-169

#### C. Verificar que el estado se actualiza

```javascript
// En EventHub.tsx, agrega un console.log temporal:

if (response.sentiment) {
  console.log('🎨 Updating sentiment to:', response.sentiment); // ← ADD THIS
  setSentiment(response.sentiment as 'positive' | 'negative' | 'neutral');
}
```

Recompila el frontend y verifica que aparece en la consola.

#### D. Verificar que la clase CSS se aplica

```javascript
// En la consola del navegador, ejecuta:
document.querySelector('.event-hub').className

// Debería devolver:
// "event-hub positive"  (o "negative" / "neutral")
```

Si la clase NO cambia:
- El `setSentiment` no se está ejecutando
- Verifica el flujo en `EventHub.tsx` líneas 117-120

#### E. Verificar que el CSS está cargado

```javascript
// En la consola del navegador:
getComputedStyle(document.querySelector('.event-hub.positive')).background

// Debería devolver algo como:
// "linear-gradient(135deg, rgb(16, 185, 129) 0%, rgb(5, 150, 105) 100%)"
```

Si NO devuelve el gradiente:
- El CSS no está cargado correctamente
- Verifica que `eventhub.css` está importado en `EventHub.tsx`
- Limpia el caché del navegador (Ctrl+Shift+R)

---

### 4. El color cambia pero no es visible

**Causa:** El gradiente es demasiado sutil o similar

**Solución:** Los colores ya fueron actualizados para ser MÁS VISIBLES:

```css
/* VERDE BRILLANTE - muy visible */
.event-hub.positive {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
}

/* ROJO INTENSO - muy visible */
.event-hub.negative {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
}
```

El `!important` fuerza que este estilo se aplique sobre otros.

---

## 📊 Lógica de Sentimiento

### Gemini AI Analysis

```python
# En gemini_service.py:

# Prompt a Gemini:
"""
- "positive" if score > 0.3 (palabras positivas, elogio, satisfacción)
- "negative" if score < -0.3 (palabras negativas, queja, insatisfacción)  
- "neutral" if score between -0.3 and 0.3
"""

# Ejemplos de palabras que detecta:

POSITIVAS:
- excelente, genial, bueno, útil, claro, interesante
- me encanta, definitivamente, sí, perfecto, increíble
- fantástico, maravilloso, great, excellent, amazing

NEGATIVAS:
- confuso, difícil, no entendí, malo, aburrido, no
- complicado, terrible, horrible, bad, difficult, boring
```

### Fallback Analysis (si Gemini falla)

```python
# Si Gemini no está disponible, usa análisis básico de palabras clave:

positive_words = ['excelente', 'genial', 'bueno', 'útil', ...]
negative_words = ['confuso', 'difícil', 'malo', 'aburrido', ...]

if positive_count > negative_count:
    sentiment = "positive"
elif negative_count > positive_count:
    sentiment = "negative"
else:
    sentiment = "neutral"
```

---

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Backend corriendo (`python3 main.py`)
- [ ] Frontend corriendo (`npm run dev` en `frontend/`)
- [ ] `GEMINI_API_KEY` configurada en `backend/python/.env`
- [ ] Modelo actualizado a `gemini-1.5-flash` (no `gemini-pro`)
- [ ] CSS de colores actualizado en `eventhub.css`
- [ ] Logs del backend muestran `🤖 Gemini - Analyzing sentiment...`
- [ ] Response de API incluye `sentiment` y `sentiment_score`
- [ ] Clase CSS del contenedor cambia a `.event-hub.positive/negative/neutral`
- [ ] Fondo visible cambia de color

---

## 🎯 Resultado Esperado

Cuando TODO funciona correctamente:

1. **Envías una respuesta positiva:**
   ```
   "¡Excelente evento! Me encantó todo."
   ```

2. **Backend logs:**
   ```
   🤖 Gemini - Analyzing sentiment for: ¡Excelente evento! Me encantó todo.
   ✅ Gemini - Raw response: {"sentiment":"positive","score":0.85,"confidence":0.9}
   📊 Sentiment: positive (score: 0.85, confidence: 0.90)
   ```

3. **Frontend:**
   - El contenedor cambia a `<div class="event-hub positive">`
   - El fondo se vuelve VERDE BRILLANTE
   - Transición suave de 0.6 segundos

4. **Envías una respuesta negativa:**
   ```
   "No entendí nada, muy confuso."
   ```

5. **Backend logs:**
   ```
   🤖 Gemini - Analyzing sentiment for: No entendí nada, muy confuso.
   ✅ Gemini - Raw response: {"sentiment":"negative","score":-0.65,"confidence":0.85}
   📊 Sentiment: negative (score: -0.65, confidence: 0.85)
   ```

6. **Frontend:**
   - El contenedor cambia a `<div class="event-hub negative">`
   - El fondo se vuelve ROJO INTENSO
   - Transición suave de 0.6 segundos

---

## 🔧 Si Nada Funciona

Reset completo:

```bash
# 1. Backend
cd backend/python
# Ctrl+C para detener
python3 main.py  # Reiniciar

# 2. Frontend  
cd ../../frontend
# Ctrl+C para detener
npm run dev  # Reiniciar

# 3. Limpiar caché del navegador
# En el navegador: Ctrl+Shift+R (hard reload)

# 4. Verificar logs
# Backend: Busca "🤖 Gemini" en la terminal
# Frontend: F12 → Console tab
```

Si aún así NO funciona, envíame:
1. Logs completos del backend (desde que inicia hasta que envías una respuesta)
2. Screenshot de la consola del navegador (F12)
3. Screenshot de la Network tab mostrando la response de `/api/responses`

