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

## Manual Setup Guide (Python Backend + SDK + Frontend)

This guide explains how to manually set up the Python backend, generate the SDK, and run the frontend without using the automated script. Follow these steps for **macOS**, **Windows**, or **Linux**.

### Prerequisites

- **Python**: >= 3.12
- **Node.js**: >= 20.19.4
- **npm**: >= 10.0.0
- **Java**: >= 17 (for SDK generation) OR Docker (alternative)

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
   - `sqlalchemy` - ORM for database
   - `psycopg2-binary` - PostgreSQL adapter (requires system dependencies from Step 1)
   - Another packages listed on requirements.txt file.

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
   PORT=6174
   DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
   EOF
   ```

   ```powershell
   # Windows (PowerShell):
   @"
   PORT=6174
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
   echo "VITE_API_BASE_URL=http://localhost:6174" > .env
   ```

   ```powershell
   # Windows (PowerShell):
   "VITE_API_BASE_URL=http://localhost:6174" | Out-File -FilePath .env -Encoding utf8
   ```

   This tells the frontend to connect to the Python backend on port 6174.

### Step 7: Generate SDK from Python Backend

The SDK is required for the frontend to communicate with the backend. It's generated from the OpenAPI specification.

#### Option A: Using Java (Recommended)

1. **Install Java 17 or higher**:
   - **macOS**: `brew install openjdk@17`
   - **Linux (Debian/Ubuntu)**: `sudo apt-get install openjdk-17-jdk`
   - **Linux (RHEL/CentOS)**: `sudo yum install java-17-openjdk-devel`
   - **Windows**: Download from [Adoptium](https://adoptium.net/) or use Chocolatey: `choco install openjdk17`

2. **Verify Java installation**:
   ```bash
   java -version
   ```

3. **Generate SDK**:
   ```bash
   # From project root
   npm run sdk:generate:python
   ```

   This will:
   - Start the Python backend on a temporary port (7174)
   - Wait for it to be ready
   - Generate the SDK to `sdk/ts/`
   - Compile the SDK
   - Stop the temporary server

#### Option B: Using Docker

1. **Install Docker**:
   - **macOS**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - **Linux**: Follow [Docker installation guide](https://docs.docker.com/engine/install/)
   - **Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Configure Docker in `openapitools.json`**:
   ```json
   {
     "generator-cli": {
       "version": "7.0.0",
       "useDocker": true
     }
   }
   ```

3. **Generate SDK**:
   ```bash
   npm run sdk:generate:python
   ```

### Step 8: Run the Python Backend

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
   Server is running on http://localhost:6174
   Swagger UI available at http://localhost:6174/api/swagger
   OpenAPI JSON available at http://localhost:6174/api/openapi.json
   ```

4. **Verify it's working**:
   - Open http://localhost:6174/api/health in your browser
   - You should see: `{"status":"ok","timestamp":"..."}`

### Step 9: Run the Frontend

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

#### Issue: SDK generation fails

- **Java not found**: Install Java 17+ and verify with `java -version`
- **Docker not running**: Start Docker Desktop or use Java instead
- **Backend not starting**: Check if port 7174 is available, or manually start the backend first

#### Issue: Frontend can't connect to backend

- Verify backend is running on http://localhost:6174
- Check `frontend/.env` has `VITE_API_BASE_URL=http://localhost:6174`
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
