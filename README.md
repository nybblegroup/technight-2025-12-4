# Technight 2025-12 Monorepo

A minimal monorepo setup with frontend (React + Vite), dual backend options (Node/Express + TypeScript + Prisma OR Python/FastAPI), and automatic SDK generation from either backend.

## Project Structure

```
technight-2025-12/
├── backend/
│   ├── node/            # Express + TypeScript backend with Swagger
│   │   ├── prisma/      # Prisma schema and migrations
│   │   ├── scripts/     # SDK generation script
│   │   └── server.ts    # Main entry point
│   └── python/          # FastAPI + Python backend with Swagger
│       ├── scripts/     # SDK generation script
│       └── main.py      # Main entry point
├── frontend/            # React + Vite + TypeScript
│   └── src/
│       ├── App.tsx      # Main app component
│       └── main.tsx     # Entry point
├── sdk/ts/              # Auto-generated TypeScript SDK
└── package.json         # Root monorepo configuration
```

## Technologies

### Backend (Node)
- **Framework**: Express.js
- **Language**: TypeScript 5.6
- **Database ORM**: Prisma
- **API Documentation**: Swagger/OpenAPI
- **Port**: 6173

### Backend (Python)
- **Framework**: FastAPI
- **Language**: Python 3.12
- **API Documentation**: Swagger/OpenAPI (auto-generated)
- **Server**: Uvicorn
- **Port**: 6174

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 6
- **Language**: TypeScript 5.6
- **Port**: 5173

### SDK
- **Generator**: OpenAPI Generator (typescript-fetch)
- **Package**: @technight/api
- **Auto-generated**: From either Node or Python backend OpenAPI spec

## Requirements

- **Node.js**: >= 20.19.4
- **npm**: >= 10.0.0
- **Python**: >= 3.12

Use [nvm](https://github.com/nvm-sh/nvm) to manage Node versions:

```bash
nvm use
```

The project includes a `.nvmrc` file that automatically sets the correct Node version.

## Getting Started with Python Backend

Once Python is installed, follow these steps to run the Python backend:

### 1. Install Python Dependencies

```bash
# Navigate to the Python backend directory
cd backend/python

# Install dependencies
pip install -r requirements.txt

# Or use pip3 if python3 is your command
pip3 install -r requirements.txt
```

**Optional: Using Virtual Environment (Recommended)**

Using a virtual environment keeps your project dependencies isolated:

```bash
# Navigate to Python backend directory
cd backend/python

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# When done, deactivate the virtual environment
deactivate
```

### 2. Configure Environment Variables

The Python backend uses environment variables from `.env` file:

```bash
# Edit backend/python/.env if needed
# Default configuration:
PORT=6174
```

### 3. Run the Python Backend

```bash
# From the project root directory
npm run dev:python

# Or directly from the Python backend directory
cd backend/python
python3 main.py
```

### 4. Verify the Backend is Running

Open your browser and visit:
- **Health Check**: http://localhost:6174/api/health
- **Swagger UI**: http://localhost:6174/api/swagger (interactive API documentation)
- **OpenAPI Spec**: http://localhost:6174/api/openapi.json

You should see a JSON response like:
```json
{
  "status": "ok",
  "timestamp": "2025-12-02T10:30:00.000Z"
}
```

### 5. Development Workflow

```bash
# Start Python backend (auto-reload enabled)
npm run dev:python

# The server will automatically reload when you make changes to main.py
```

### Common Python Issues and Solutions

**Issue: `python3: command not found` or `python: command not found`**
- Solution: Python is not installed or not in PATH. Follow the installation instructions above.

**Issue: `pip: command not found`**
- Solution: Install pip or use `python3 -m pip` instead of `pip`

**Issue: `Permission denied` when installing packages**
- Solution: Use a virtual environment (recommended) or use `--user` flag:
  ```bash
  pip install --user -r requirements.txt
  ```

**Issue: Port 6174 already in use**
- Solution: Change the port in `backend/python/.env`:
  ```
  PORT=6175
  ```

**Issue: Module not found errors**
- Solution: Make sure you're in the correct directory and dependencies are installed:
  ```bash
  cd backend/python
  pip install -r requirements.txt
  ```

## GitHub Codespaces

This project is fully configured for GitHub Codespaces. Simply:

1. Click "Code" → "Create codespace on master"
2. Wait for the environment to build (dependencies install automatically)
3. Run `npm run dev` to start both frontend and backend

The devcontainer includes:
- Node.js 20
- Python 3.12
- VS Code extensions (ESLint, Prettier, Prisma, Python, Pylance)
- Auto-forwarding for ports 5173 (frontend), 6173 (Node backend), and 6174 (Python backend)

## Getting Started

### Install Dependencies

```bash
# Install all dependencies (root, backend, frontend)
npm install

# Node backend
cd backend/node && npm install

# Python backend
cd ../python && pip install -r requirements.txt

# Frontend
cd ../../frontend && npm install
```

### Configure API Connection (Optional)

The frontend uses a centralized API configuration in `frontend/src/utils/api.ts`. By default, it connects to port 6173.

To change the backend URL, create a `.env` file in the `frontend/` directory:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:6173
```

To use the Python backend instead:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:6174
```

**Note:** Restart the frontend dev server after changing environment variables.

### Development

**Default Setup (Node Backend):**

By default, `npm run dev` runs the **Node backend** + frontend:

```bash
# Start Node backend + Frontend (default)
npm run dev
```

This will start:
- Node backend on http://localhost:6173
- Frontend on http://localhost:5173

**Using Python Backend:**

To use the Python backend instead, run it separately:

```bash
# Terminal 1: Python backend
npm run dev:python

# Terminal 2: Frontend
npm run dev:frontend
```

**Running Both Backends Simultaneously:**

To test both backends at the same time:

```bash
# Terminal 1: Node backend + Frontend (default)
npm run dev

# Terminal 2: Python backend
npm run dev:python
```

Or run all three individually:

```bash
# Terminal 1: Node backend
npm run dev:backend

# Terminal 2: Python backend
npm run dev:python

# Terminal 3: Frontend
npm run dev:frontend
```

**Available Commands:**
- `npm run dev` - Node backend + Frontend (default)
- `npm run dev:backend` - Node backend only (port 6173)
- `npm run dev:python` - Python backend only (port 6174)
- `npm run dev:frontend` - Frontend only (port 5173)

### Backend Endpoints

#### Node Backend (Port 6173)
- **Health Check**: http://localhost:6173/api/health
- **Swagger UI**: http://localhost:6173/api/swagger
- **OpenAPI JSON**: http://localhost:6173/api/openapi.json
- **OpenAPI YAML**: http://localhost:6173/api/openapi.yaml

#### Python Backend (Port 6174)
- **Health Check**: http://localhost:6174/api/health
- **Swagger UI**: http://localhost:6174/api/swagger
- **OpenAPI JSON**: http://localhost:6174/api/openapi.json
- **OpenAPI YAML**: http://localhost:6174/api/openapi.yaml

### Generate SDK

The SDK can be generated from either backend's OpenAPI specification:

```bash
# Generate from Node backend (default)
npm run sdk:generate

# Generate from Node backend (explicit)
npm run sdk:generate:node

# Generate from Python backend
npm run sdk:generate:python
```

Each script will:
1. Start the respective backend server on a temporary port (7173 for Node, 7174 for Python)
2. Wait for the health check endpoint
3. Generate the SDK to `sdk/ts/`
4. Stop the server

### Build for Production

```bash
# Build both frontend and backend
npm run build

# Or build individually:
npm run build:backend
npm run build:frontend
```

## Adding API Endpoints

### Node Backend

1. Add your endpoint in `backend/node/server.ts` with JSDoc comments:

```typescript
/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: Get all users
 *     responses:
 *       200:
 *         description: List of users
 */
app.get('/api/users', (req, res) => {
  res.json({ users: [] });
});
```

2. Regenerate the SDK:

```bash
npm run sdk:generate:node
```

### Python Backend

1. Add your endpoint in `backend/python/main.py`:

```python
@app.get("/api/users", tags=["Users"])
async def get_users():
    """
    Get all users

    Returns a list of all users
    """
    return {"users": []}
```

2. Regenerate the SDK:

```bash
npm run sdk:generate:python
```

### Using the SDK in Frontend

```typescript
import { Configuration, HealthApi } from '@technight/api';

const config = new Configuration({
  basePath: 'http://localhost:6173'  // or 6174 for Python
});

const healthApi = new HealthApi(config);
const response = await healthApi.apiHealthGet();
```

## Database Setup

### Node Backend (Prisma ORM)

The Node backend includes Prisma ORM. To set up your database:

1. Update `backend/node/.env` with your database URL:
```
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"
```

2. Define your schema in `backend/node/prisma/schema.prisma`

3. Run migrations:
```bash
cd backend/node
npm run prisma:migrate
```

### Python Backend (No ORM included)

The Python backend does not include an ORM by default. You can add SQLAlchemy or another ORM as needed.

## Notes

- No deployment configurations included (local development only)
- No authentication setup (minimal setup)
- No extra UI libraries (just React + basic styling)
- Both backends can run simultaneously on different ports
- Node backend includes Prisma ORM with empty schema
- Python backend has no ORM included (add as needed)
- SDK can be generated from either backend
