# Technight Challenge

## Objetivo

Desarrollar una experiencia via web app visualmente atractiva con **gamificación** y **mucho IA** 😂 para la recepción de encuestas/feedback de eventos/reuniones/webinars, medir participación y/o asistencia para utilizar durante la misma en todas las presentaciones de NYBBLE GROUP integrable a nuestro hub como un espacio social.

### Características Principales

- La idea es cubrir con el app todo el ciclo de vida de un evento/reunion desde el PRE/DURANTE/POST por medio del app generando engagement en los participantes
- Piensa opciones **dinámicas** con feedback recurrente y poder reiterar el mismo que sean **divertidas** y a su vez traigan **información de valor**
- Asociar el web app con la reunion de calendario de algun modo para crear nuevas experiencias.
- Puede ser algo genérico pero sería bueno que el app realice algunas que otras **preguntas incisivas** (o las invente) en base a lo que pasó !?
- Puedes simular comunicación con **Slack** para ciertas interacciones pero debe tener una **interfase gráfica ÚNICA**
- No sólo puedes preguntar sino **inferir datos** desde otros sistemas:
  - Información básica de people force / fotos / skills
  - Información del calendario
  - Informacion previa de eventos similares
  - Videos/fotos de los eventos (virtuales o presenciales)
  - Grabadores de meet
  - Extracción o uso de resúmenes
  - Assistance de meet
  - Fellow summary, etc.

> **Nota**: Simulando información con mocks o similares a la realidad o usando información previa (no necesitas conectar los sistemas hoy pero si puedes en 2 horas adelante! 😀)

Ej: Puedes simular partes del sistema como enviar un mensaje por Slack a X persona o traer X información del calendario que luego integraremos con el equipo de Nybble Labs y los ganadores.

#### Dashboard

Debe tener al menos una pantalla de **dashboard/resumen amigable** para ver las estadísticas y lo que resulto interesante del feedback del evento/reunión aumentado con AI para sacar conceptos claves y métricas para los equipos.

### Premio

**El mejor trabajo (votado entre todos) será integrado en el nuevo Nybble Hub como iniciativa de innovación durante 2026 y estará disponible el acceso para todos**

<img width="1421" height="752" alt="image" src="https://github.com/user-attachments/assets/0c0cecfb-2470-48cb-aba1-e7a1674c9a75" />

---

## Cronograma y Entrega

La misma debe ser desarrollada **íntegramente con AI** por medio de modo agéntico al **100%**.

### Reglas de Oro

- ❌ **No hace falta escribir código**. ¡Deja que la AI lo haga por vos!
- ✅ Nos enfocamos en las necesidades, contexto técnico, experiencia y controlar al monstruo! 👾🤖
- 👑 **Somos los gobernadores de los agentes!** 😣

### Timeline (3 horas totales)

| Fase | Duración | Descripción |
|------|----------|-------------|
| **KickOff** | 15 min | Definición del Tech Challenge |
| **Ideación + Discovery** | 45 min | Definir alcance y planeamiento |
| **Ejecución con IA** | ~1 hora | Creación por medio de IA |
| **Break** | 15-20 min | Pausa para preparar presentaciones |
| **Presentaciones** | ~40 min | Demos y votación |

### Modos de Trabajo

#### 1. Modo PLANEAMIENTO 📋

- Determinar las tareas a realizar cuando tengan claro el alcance de tu proyecto
- Debajo dejamos un **PROMPT de base** que puedes utilizar: [SPEC_PROMPT.md](./SPEC_PROMPT.md)
- Documentar alcance y planeamiento
- Evalua si realizaras todo en un solo prompt o ejecutaras cada historia por separado

#### 2. Modo EJECUCIÓN 🚀

- Basado en las tareas y el discovery inicial del planeamiento
- Todo el contexto que crean conveniente
- Implementación con agentes de IA

#### 3. Modo PRESENTACIÓN 🎤

- Pedimos a un **representante de NEGOCIO** que la rompa con la presentación
- **¡Es parte de la evaluación!**
- Presentación del producto funcionando

### Premio

🎁 **Hay premio de navidad para el ganador…** (no será el gordo…) pero algo habrá! 😂

---

## Restricciones Técnicas

### 1. Repositorio Base

- ✅ Crear un **fork** del repositorio modelo:

  ```bash
  https://github.com/nybblegroup/technight-2025-12
  ```

- 📖 Leer el `README.MD` con el proyecto de startup disponible

### 2. Stack Tecnológico

#### Frontend (Común para todos)

- **React** + **Vite**
- Encontrarán un frontend común para todos donde crearan su magia! 🪄

#### Backend (Elegir UNO)

Elegir la tecnología de API/BACKEND que más puedan trabajar según el equipo y líder técnico:

- ☕ **Java** (Spring Boot)
- 🟢 **Node.js** (Express + TypeScript) - *ya configurado en el repo*
- 🐍 **Python** (FastAPI) - *ya configurado en el repo*
- 🔷 **.NET Core** (C#)

### 3. Herramientas de IA Permitidas

Debes únicamente utilizar una de estas tecnologías para trabajar en modo agéntico:

| Herramienta | Descripción |
|-------------|-------------|
| **Cursor Agent mode** 👍 | Modo agente de Cursor |

<img width="1057" height="461" alt="image" src="https://github.com/user-attachments/assets/227743e3-5ca7-422d-9fd4-17a4559cc426" />

| **Gemini CLI** 👏 | Google Gemini en línea de comandos |

<img width="1324" height="476" alt="image" src="https://github.com/user-attachments/assets/a74c88c1-897e-4a89-a3f5-8e19b35cbcac" />

You can use the Gemini Key provided or with your Nybble Group account (https://geminicli.com/docs/get-started/authentication/#gemini-api)
To enable Gemini 3 Pro, use the /settings command in Gemini CLI and set Preview Features to true.
You can switch model if needed it with /model command.

<img width="639" height="458" alt="image" src="https://github.com/user-attachments/assets/aeee77a6-6437-4169-a95b-e7d4c9a2a5af" />

| **Claude Code or OpenAI Codex** ➕ | Si lo tienes en tu stack y lo prefieres para esta technight! |

<img width="1336" height="194" alt="image" src="https://github.com/user-attachments/assets/5409584b-7810-4206-b718-66e263b595c9" />

### 4. Base de Datos

- 🐘 **PostgreSQL** (disponibilizado por el equipo)
- Una base de datos **por equipo**
- Credenciales provistas el día del evento

### 5. API Keys

- 🔑 **Gemini API Key** para uso de AI
- Provisto por el equipo el día del evento

## Consejos para el Éxito

1. 💡 **Enfócate en la experiencia**: Que sea divertido y útil
2. 🎯 **Define bien el alcance**: No intentes hacer todo, prioriza
3. 🤖 **Confía en la IA**: Deja que los agentes hagan el trabajo pesado
4. 📊 **Datos visuales**: Un buen dashboard vale más que mil palabras
5. 🎮 **Gamifica todo**: Hazlo adictivo y entretenido
6. 🎤 **Prepara la demo**: La presentación cuenta mucho
7. 👥 **Trabaja en equipo**: Dividan las responsabilidades
8. ⏰ **Maneja el tiempo**: 3 horas pasan rápido

## Soporte Durante el Evento

- 💬 Canal de Slack: `#topgun-technight`
- 🆘 Mentores disponibles para consultas técnicas
- 🔑 Credenciales de base de datos: Se compartirán al inicio
- 🎯 API Keys: Se compartirán al inicio

---

## ¡Mucha suerte y que gane el mejor! 🚀🎉

**Remember**: No escribas código, gobierna los agentes! 👾🤖
