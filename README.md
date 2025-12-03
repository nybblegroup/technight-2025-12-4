# Technight 2025-12 Monorepo

A minimal monorepo setup with frontend (React + Vite) and dual backend options (Node/Express + TypeScript + Prisma OR Python/FastAPI). The frontend connects directly to the backend APIs.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend :5173"
        FE[React + Vite + TypeScript]
    end

    subgraph "Backend Options"
        subgraph "Node Backend :8080"
            NODE[Express + TypeScript]
            PRISMA[Prisma ORM]
            SWAGGER_NODE[Swagger/OpenAPI]
        end

        subgraph "Python Backend :8080"
            PYTHON[FastAPI + Python]
            SQLALCHEMY[SQLAlchemy ORM]
            SWAGGER_PY[Swagger/OpenAPI]
        end
    end

    subgraph "Database"
        DB[(PostgreSQL)]
    end

    FE -->|Direct HTTP Requests<br/>fetch API| NODE
    FE -.->|Direct HTTP Requests<br/>fetch API| PYTHON

    NODE --> PRISMA
    PYTHON --> SQLALCHEMY
    PRISMA --> DB
    SQLALCHEMY --> DB

    style FE fill:#61dafb,stroke:#333,stroke-width:2px
    style NODE fill:#68a063,stroke:#333,stroke-width:2px
    style PYTHON fill:#3776ab,stroke:#333,stroke-width:2px
    style DB fill:#336791,stroke:#333,stroke-width:2px
```

**Key Points:**
- **Frontend** connects directly to backends using fetch API
- **Node Backend** uses Prisma ORM for database operations
- **Python Backend** uses SQLAlchemy ORM for database operations
- Both backends connect to **PostgreSQL** database
- Both backends expose **Swagger UI** for interactive API documentation
- Backends can run **simultaneously** on different ports
- API base URL is **configurable** via environment variables

## Project Structure

```
technight-2025-12/
├── backend/
│   ├── node/            # Express + TypeScript backend with Swagger
│   │   ├── prisma/      # Prisma schema and migrations
│   │   └── server.ts    # Main entry point
│   └── python/          # FastAPI + Python backend with Swagger
│       ├── database.py  # SQLAlchemy database configuration
│       └── main.py      # Main entry point
├── frontend/            # React + Vite + TypeScript
│   └── src/
│       ├── utils/
│       │   └── api.ts   # API client with direct fetch calls
│       ├── App.tsx      # Main app component
│       └── main.tsx     # Entry point
└── package.json         # Root monorepo configuration
```

## Technologies

### Backend (Node)
- **Framework**: Express.js
- **Language**: TypeScript 5.6
- **Database ORM**: Prisma
- **API Documentation**: Swagger/OpenAPI
- **Port**: 8080

### Backend (Python)
- **Framework**: FastAPI
- **Language**: Python 3.12
- **Database ORM**: SQLAlchemy
- **API Documentation**: Swagger/OpenAPI (auto-generated)
- **Server**: Uvicorn
- **Port**: 8080

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite 6
- **Language**: TypeScript 5.6
- **API Client**: Native fetch API
- **Port**: 5173

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
PORT=8080
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
- **Health Check**: http://localhost:8080/api/health
- **Database Health**: http://localhost:8080/api/health/db (checks PostgreSQL connection)
- **Swagger UI**: http://localhost:8080/api/swagger (interactive API documentation)
- **OpenAPI Spec**: http://localhost:8080/api/openapi.json

You should see a JSON response like:
```json
{
  "status": "ok",
  "timestamp": "2025-12-02T10:30:00.000Z"
}
```

**Database Health Check Response Examples:**
```json
// If database is connected:
{
  "connected": true,
  "message": "Database connection successful",
  "timestamp": "2025-12-02T10:30:00.000Z"
}

// If DATABASE_URL is not set:
{
  "connected": false,
  "error": "Database not configured. DATABASE_URL environment variable not set.",
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

**Issue: Port 8080 already in use**
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

## Manual Setup Guide (Python Backend + Frontend)

This guide explains how to manually set up the Python backend and run the frontend. Follow these steps for **macOS**, **Windows**, or **Linux**.

### Prerequisites

- **Python**: >= 3.12
- **Node.js**: >= 20.19.4
- **npm**: >= 10.0.0

### Step 1: Install System Dependencies for PostgreSQL

The Python backend uses `psycopg2-binary` which requires system-level PostgreSQL libraries and OpenSSL.

#### macOS

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install libpq** (PostgreSQL client library):
   ```bash
   brew install libpq
   ```

3. **Install OpenSSL**:
   ```bash
   brew install openssl@3
   # Or if openssl@3 is not available:
   brew install openssl@1.1
   ```

4. **Configure environment variables** (add to `~/.zshrc` or `~/.bash_profile`):
   ```bash
   # Find libpq path
   export PATH="$(brew --prefix libpq)/bin:$PATH"
   export LDFLAGS="-L$(brew --prefix libpq)/lib"
   export CPPFLAGS="-I$(brew --prefix libpq)/include"
   export PKG_CONFIG_PATH="$(brew --prefix libpq)/lib/pkgconfig:$PKG_CONFIG_PATH"
   
   # Find OpenSSL path (try openssl@3 first)
   export PATH="$(brew --prefix openssl@3)/bin:$PATH" 2>/dev/null || export PATH="$(brew --prefix openssl@1.1)/bin:$PATH"
   export LDFLAGS="-L$(brew --prefix openssl@3)/lib $LDFLAGS" 2>/dev/null || export LDFLAGS="-L$(brew --prefix openssl@1.1)/lib $LDFLAGS"
   export CPPFLAGS="-I$(brew --prefix openssl@3)/include $CPPFLAGS" 2>/dev/null || export CPPFLAGS="-I$(brew --prefix openssl@1.1)/include $CPPFLAGS"
   export PKG_CONFIG_PATH="$(brew --prefix openssl@3)/lib/pkgconfig:$PKG_CONFIG_PATH" 2>/dev/null || export PKG_CONFIG_PATH="$(brew --prefix openssl@1.1)/lib/pkgconfig:$PKG_CONFIG_PATH"
   ```

5. **Reload your shell configuration**:
   ```bash
   source ~/.zshrc  # or source ~/.bash_profile
   ```

#### Linux (Debian/Ubuntu)

1. **Update package list**:
   ```bash
   sudo apt-get update
   ```

2. **Install PostgreSQL development libraries**:
   ```bash
   sudo apt-get install -y libpq-dev
   ```

3. **OpenSSL is usually pre-installed**, but if needed:
   ```bash
   sudo apt-get install -y libssl-dev
   ```

#### Linux (RHEL/CentOS/Fedora)

1. **Install PostgreSQL development libraries**:
   ```bash
   # For RHEL/CentOS:
   sudo yum install -y postgresql-devel
   
   # For Fedora:
   sudo dnf install -y postgresql-devel
   ```

2. **Install OpenSSL development libraries** (if needed):
   ```bash
   # For RHEL/CentOS:
   sudo yum install -y openssl-devel
   
   # For Fedora:
   sudo dnf install -y openssl-devel
   ```

#### Windows

1. **Install PostgreSQL** from [postgresql.org](https://www.postgresql.org/download/windows/)
   - During installation, make sure to include "Command Line Tools"
   - Note the installation path (usually `C:\Program Files\PostgreSQL\<version>`)

2. **Install OpenSSL**:
   - Option 1: Use [vcpkg](https://vcpkg.io/en/getting-started.html):
     ```powershell
     vcpkg install openssl
     ```
   - Option 2: Download pre-built binaries from [slproweb.com](https://slproweb.com/products/Win32OpenSSL.html)
   - Option 3: Use [Chocolatey](https://chocolatey.org/):
     ```powershell
     choco install openssl
     ```

3. **Add PostgreSQL to PATH** (in PowerShell as Administrator):
   ```powershell
   # Add to system PATH (replace <version> with your PostgreSQL version)
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\<version>\bin", [EnvironmentVariableTarget]::Machine)
   ```

4. **Set environment variables** (in PowerShell):
   ```powershell
   # Set PostgreSQL paths (replace <version> with your PostgreSQL version)
   $env:PATH = "C:\Program Files\PostgreSQL\<version>\bin;$env:PATH"
   $env:LDFLAGS = "-LC:\Program Files\PostgreSQL\<version>\lib"
   $env:CPPFLAGS = "-IC:\Program Files\PostgreSQL\<version>\include"
   ```

### Step 2: Set Up Python Virtual Environment

1. **Navigate to Python backend directory**:
   ```bash
   cd backend/python
   ```

2. **Create virtual environment**:
   ```bash
   # macOS/Linux:
   python3 -m venv venv
   
   # Windows (Command Prompt):
   python -m venv venv
   
   # Windows (PowerShell):
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # macOS/Linux:
   source venv/bin/activate
   
   # Windows (Command Prompt):
   venv\Scripts\activate.bat
   
   # Windows (PowerShell):
   venv\Scripts\Activate.ps1
   ```

   You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

1. **Upgrade pip** (recommended):
   ```bash
   pip install --upgrade pip
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `fastapi` - Web framework
   - `uvicorn` - ASGI server
   - `python-dotenv` - Environment variable management
   - `PyYAML` - YAML parsing
   - `sqlalchemy` - SQLAlchemy ORM for database operations
   - `psycopg2-binary` - PostgreSQL adapter (requires system dependencies from Step 1)
   - Other packages listed in requirements.txt file

3. **Verify installation**:
   ```bash
   pip list
   ```

   You should see all packages from `requirements.txt` listed.

### Step 4: Configure Environment Variables

1. **Create `.env` file** in `backend/python/`:
   ```bash
   cd backend/python
   ```

2. **Create `.env` file** with the following content:
   ```bash
   # macOS/Linux:
   cat > .env << EOF
   PORT=8080
   DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
   EOF
   ```

   ```powershell
   # Windows (PowerShell):
   @"
   PORT=8080
   DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
   "@ | Out-File -FilePath .env -Encoding utf8
   ```

3. **Edit `.env`** with your actual database credentials:
   - Replace `user` with your PostgreSQL username
   - Replace `password` with your PostgreSQL password
   - Replace `localhost:5432` with your PostgreSQL host and port
   - Replace `mydb` with your database name

   **Note**: If you don't have PostgreSQL running, you can leave `DATABASE_URL` as is. The backend will still work, but database endpoints will return errors.

### Step 5: Install Node.js Dependencies

1. **Navigate to project root**:
   ```bash
   cd ../..  # from backend/python
   # or
   cd /path/to/technight-2025-12  # from anywhere
   ```

2. **Install root dependencies**:
   ```bash
   npm install
   ```

3. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Step 6: Configure Frontend Environment

1. **Create `.env` file** in `frontend/` directory:
   ```bash
   cd frontend
   ```

2. **Create `.env` file**:
   ```bash
   # macOS/Linux:
   echo "VITE_API_BASE_URL=http://localhost:8080" > .env
   ```

   ```powershell
   # Windows (PowerShell):
   "VITE_API_BASE_URL=http://localhost:8080" | Out-File -FilePath .env -Encoding utf8
   ```

   This tells the frontend to connect to the Python backend on port 8080.

### Step 7: Run the Python Backend

1. **Navigate to Python backend directory**:
   ```bash
   cd backend/python
   ```

2. **Activate virtual environment** (if not already active):
   ```bash
   # macOS/Linux:
   source venv/bin/activate
   
   # Windows (Command Prompt):
   venv\Scripts\activate.bat
   
   # Windows (PowerShell):
   venv\Scripts\Activate.ps1
   ```

3. **Start the backend**:
   ```bash
   python3 main.py  # macOS/Linux
   # or
   python main.py   # Windows
   ```

   You should see:
   ```
   Server is running on http://localhost:8080
   Swagger UI available at http://localhost:8080/api/swagger
   OpenAPI JSON available at http://localhost:8080/api/openapi.json
   ```

4. **Verify it's working**:
   - Open http://localhost:8080/api/health in your browser
   - You should see: `{"status":"ok","timestamp":"..."}`

### Step 8: Run the Frontend

1. **Open a new terminal** (keep the backend running in the first terminal)

2. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

3. **Start the frontend**:
   ```bash
   npm run dev
   ```

   You should see:
   ```
   VITE v6.x.x  ready in xxx ms

   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

4. **Open your browser**:
   - Navigate to http://localhost:5173
   - You should see the frontend connecting to the Python backend

### Troubleshooting

#### Issue: `psycopg2-binary` fails to install

**macOS**:
- Make sure `libpq` and `openssl@3` are installed via Homebrew
- Verify environment variables are set correctly
- Try: `export PATH="$(brew --prefix libpq)/bin:$PATH"` before installing

**Linux**:
- Make sure `libpq-dev` (Debian/Ubuntu) or `postgresql-devel` (RHEL/CentOS) is installed
- Verify with: `dpkg -l | grep libpq-dev` (Debian/Ubuntu) or `rpm -qa | grep postgresql-devel` (RHEL/CentOS)

**Windows**:
- Make sure PostgreSQL is installed and in PATH
- Verify with: `pg_config --version`
- If using vcpkg, make sure OpenSSL is properly linked

#### Issue: Frontend can't connect to backend

- Verify backend is running on http://localhost:8080
- Check `frontend/.env` has `VITE_API_BASE_URL=http://localhost:8080`
- Restart frontend after changing `.env` file

#### Issue: Database connection errors

- Verify PostgreSQL is running: `pg_isready` (macOS/Linux) or check Windows services
- Check `DATABASE_URL` in `backend/python/.env` is correct
- Test connection: `psql -U user -d mydb -h localhost` (replace with your credentials)

## GitHub Codespaces

This project is fully configured for GitHub Codespaces. Simply:

1. Click "Code" → "Create codespace on master"
2. Wait for the environment to build (dependencies install automatically)
3. Run `npm run dev` to start both frontend and backend

The devcontainer includes:
- Node.js 20
- Python 3.12
- VS Code extensions (ESLint, Prettier, Prisma, Python, Pylance)
- Auto-forwarding for ports 5173 (frontend), 8080 (Node backend), and 8080 (Python backend)

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

The frontend uses a centralized API configuration in `frontend/src/utils/api.ts`. By default, it connects to port 8080.

To change the backend URL, create a `.env` file in the `frontend/` directory:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8080
```

To use the Python backend instead:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8080
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
- Node backend on http://localhost:8080
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
- `npm run dev:backend` - Node backend only (port 8080)
- `npm run dev:python` - Python backend only (port 8080)
- `npm run dev:frontend` - Frontend only (port 5173)

### Backend Endpoints

#### Node Backend (Port 8080)
- **Health Check**: http://localhost:8080/api/health
- **Swagger UI**: http://localhost:8080/api/swagger
- **OpenAPI JSON**: http://localhost:8080/api/openapi.json
- **OpenAPI YAML**: http://localhost:8080/api/openapi.yaml

#### Spring Boot Backend (Port 8080)
- **Health Check**: http://localhost:8080/api/health
- **Swagger UI**: http://localhost:8080/api/swagger
- **OpenAPI JSON**: http://localhost:8080/api/openapi

#### Python Backend (Port 8080)
- **Health Check**: http://localhost:8080/api/health
- **Database Health**: http://localhost:8080/api/health/db
- **Swagger UI**: http://localhost:8080/api/swagger
- **OpenAPI JSON**: http://localhost:8080/api/openapi.json
- **OpenAPI YAML**: http://localhost:8080/api/openapi.yaml

#### .NET Backend (Port 8080)
- **Health Check**: http://localhost:8080/api/health
- **Swagger UI**: http://localhost:8080/api/swagger
- **OpenAPI JSON**: http://localhost:8080/api/swagger/v1/swagger.json

### API Documentation

Both backends provide Swagger UI for interactive API documentation:

- **Node Backend**: http://localhost:8080/api/swagger
- **Python Backend**: http://localhost:8080/api/swagger

You can also view the OpenAPI specifications:
- **Node Backend JSON**: http://localhost:8080/api/openapi.json
- **Node Backend YAML**: http://localhost:8080/api/openapi.yaml
- **Python Backend JSON**: http://localhost:8080/api/openapi.json
- **Python Backend YAML**: http://localhost:8080/api/openapi.yaml

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

Add your endpoint in `backend/node/server.ts` with JSDoc comments for Swagger documentation:

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

### Python Backend

Add your endpoint in `backend/python/main.py`:

```python
@app.get("/api/users", tags=["Users"])
async def get_users():
    """
    Get all users

    Returns a list of all users
    """
    return {"users": []}
```

### Using the API in Frontend

1. **Add type definition** in `frontend/src/utils/api.ts`:

```typescript
export interface User {
  id: string;
  name: string;
  email: string;
}
```

2. **Add API method** in `frontend/src/utils/api.ts`:

```typescript
export const api = {
  health: {
    get: () => apiFetch<HealthResponse>('/api/health'),
  },
  users: {
    getAll: () => apiFetch<User[]>('/api/users'),
    getById: (id: string) => apiFetch<User>(`/api/users/${id}`),
    create: (data: Omit<User, 'id'>) => apiFetch<User>('/api/users', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },
};
```

3. **Use in components**:

```typescript
import { api } from './utils/api';

// In your component
const users = await api.users.getAll();
```

## Database Setup

Both backends include full PostgreSQL support with their respective ORMs.

### Node Backend (Prisma ORM)

The Node backend uses Prisma ORM for database operations.

1. **Update `backend/node/.env`** with your database URL:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"
```

2. **Define your schema** in `backend/node/prisma/schema.prisma`

3. **Run migrations**:
```bash
cd backend/node
npm run prisma:migrate
```

4. **Verify database connection**: Visit http://localhost:8080/api/health

### Python Backend (SQLAlchemy ORM)

The Python backend uses SQLAlchemy ORM for database operations.

1. **Update `backend/python/.env`** with your database URL:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

2. **Database module** is located at `backend/python/database.py` and includes:
   - SQLAlchemy engine with connection pooling
   - Session management with dependency injection
   - Base declarative class for models
   - Database health check function

3. **Check database connection**:
   - **Basic health**: http://localhost:8080/api/health
   - **Database health**: http://localhost:8080/api/health/db

4. **Create models** by extending `Base` from `database.py`:
```python
from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
```

5. **Use database sessions** in endpoints:
```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

@app.get("/api/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}
```

**Note**: The Python backend gracefully handles missing database configuration. If `DATABASE_URL` is not set, the server will still run but database endpoints will return appropriate error messages.

## Notes

- No deployment configurations included (local development only)
- No authentication setup (minimal setup)
- No extra UI libraries (just React + basic styling)
- Both backends can run simultaneously on different ports
- Node backend includes Prisma ORM with empty schema
- Python backend includes SQLAlchemy ORM with database module
- Both backends support PostgreSQL with their respective ORMs
- Frontend uses native fetch API for direct backend communication
- API base URL is configurable via `VITE_API_BASE_URL` environment variable
- Python backend includes database health check endpoint (`/api/health/db`)
- Both backends provide Swagger UI for API documentation
