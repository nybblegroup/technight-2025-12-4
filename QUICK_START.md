# ⚡ Quick Start - Nybble Event Hub

## 🎯 TL;DR - Pasos Mínimos para Ejecutar

### 1. Configurar Gemini API Key (OBLIGATORIO)

Edita `backend/python/.env` y agrega tu API key:

```env
GEMINI_API_KEY="tu-api-key-de-gemini-aqui"
```

**¿Cómo obtener la API key?**
1. Ve a: https://aistudio.google.com/app/apikey
2. Click en "Create API Key"
3. Copia la key y pégala en el .env

### 2. Instalar Dependencias

```bash
# Backend
cd backend/python
pip install -r requirements.txt

# Frontend
cd ../..
npm install
```

### 3. Configurar Base de Datos

```bash
cd backend/python

# Ejecutar migraciones
alembic upgrade head

# Crear datos de ejemplo
python seed_data.py
```

### 4. Ejecutar la App

```bash
# Terminal 1 - Backend
cd backend/python
python main.py

# Terminal 2 - Frontend  
npm run dev:frontend
```

### 5. Abrir en el Navegador

🎉 **http://localhost:5173**

Click en "Tech Night: AI en Producción" para ver el Event Hub en acción!

---

## 🆘 Si algo falla...

### Error: "GEMINI_API_KEY not set"
- ✅ Verifica que editaste `backend/python/.env`
- ✅ Verifica que guardaste el archivo
- ✅ Reinicia el backend

### Error: "Database connection failed"
- ✅ Verifica que PostgreSQL está corriendo
- ✅ Verifica el `DATABASE_URL` en `backend/python/.env`
- ✅ La base de datos debe existir

### Error: "Module not found"
- ✅ Ejecuta `pip install -r requirements.txt` en `backend/python/`
- ✅ Ejecuta `npm install` en la raíz del proyecto

### Frontend no se conecta al backend
- ✅ Verifica que el backend está corriendo en http://localhost:8080
- ✅ Abre http://localhost:8080/api/health - debería decir "ok"

---

## 📚 Más Info

- **Setup completo**: [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md)
- **Resumen técnico**: [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
- **README del Hub**: [EVENT_HUB_README.md](./EVENT_HUB_README.md)

---

## ✅ Checklist de Verificación

Antes de ejecutar, verifica:

- [ ] PostgreSQL está corriendo
- [ ] `backend/python/.env` tiene `GEMINI_API_KEY` configurado
- [ ] `backend/python/.env` tiene `DATABASE_URL` configurado
- [ ] Ejecutaste `pip install -r requirements.txt`
- [ ] Ejecutaste `npm install`
- [ ] Ejecutaste `alembic upgrade head`
- [ ] Ejecutaste `python seed_data.py`

Si todos los checks están ✅, ejecuta:

```bash
# Terminal 1
cd backend/python && python main.py

# Terminal 2
npm run dev:frontend
```

🎉 **¡Listo! Abre http://localhost:5173**





