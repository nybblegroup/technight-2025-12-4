# Python Backend - FastAPI + SQLAlchemy

A minimal FastAPI backend with SQLAlchemy ORM, Swagger/OpenAPI documentation, and PostgreSQL support.

## Quick Start

### Using the run.sh Script (Recommended)

The easiest way to get started is using the automated setup script:

```bash
cd backend/python
./run.sh
```

This script will:
1. Check Python installation
2. Create and activate a virtual environment
3. Install system dependencies (PostgreSQL libraries)
4. Install Python dependencies
5. Install frontend dependencies
6. Configure environment files
7. Start both the Python backend and frontend

### Manual Setup

If you prefer manual setup:

#### 1. Create Virtual Environment

```bash
cd backend/python
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note on macOS**: If `psycopg2-binary` installation fails, install libpq first:
```bash
brew install libpq openssl@3
export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/libpq/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libpq/include"
pip install -r requirements.txt
```

#### 3. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your database configuration:

```env
PORT=6174
DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/technightdb-python"
```

#### 4. Run Database Migrations

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head
```

Esto creará las tablas necesarias en tu base de datos PostgreSQL. Si es la primera vez, creará la tabla `example`.

**Nota**: El script `run.sh` ejecuta esto automáticamente.

#### 5. Start the Server

```bash
python3 main.py
```

## API Endpoints

Once the server is running on http://localhost:6174:

### Documentation
- **Swagger UI**: http://localhost:6174/api/swagger
- **OpenAPI JSON**: http://localhost:6174/api/openapi.json
- **OpenAPI YAML**: http://localhost:6174/api/openapi.yaml

### Health Checks
- **API Health**: http://localhost:6174/api/health
- **Database Health**: http://localhost:6174/api/health/db

### Example CRUD Operations

The backend includes a complete Example entity implementation with full database support (matching the Node.js, Spring Boot, and .NET versions).

**Database Setup**: Before using the CRUD endpoints, make sure to:
1. Configure `DATABASE_URL` in `.env`
2. Run migrations: `python3 migrations.py`
3. Verify database connection: http://localhost:6174/api/health/db

#### Get all examples
```bash
curl http://localhost:6174/api/examples
```

#### Get example by ID
```bash
curl http://localhost:6174/api/examples/1
```

#### Search examples
```bash
curl http://localhost:6174/api/examples/search?name=First
```

#### Create new example
```bash
curl -X POST http://localhost:6174/api/examples \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","title":"Test Title","description":"A test example","isActive":true}'
```

#### Update example
```bash
curl -X PUT http://localhost:6174/api/examples/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'
```

#### Delete example
```bash
curl -X DELETE http://localhost:6174/api/examples/1
```

## Project Structure

```
backend/python/
├── main.py           # FastAPI application entry point
├── database.py       # SQLAlchemy database configuration
├── models.py         # SQLAlchemy models (Example entity)
├── schemas.py        # Pydantic schemas (DTOs for request/response)
├── migrations.py     # Helper script for Alembic migrations
├── alembic/          # Alembic migration files
│   ├── versions/     # Migration scripts
│   └── env.py        # Alembic configuration
├── alembic.ini        # Alembic configuration file
├── requirements.txt  # Python dependencies
├── run.sh           # Automated setup and run script
├── MIGRATIONS.md    # Migration guide (see this for details)
├── .env             # Environment variables (create from .env.example)
└── venv/            # Virtual environment (created by run.sh)
```

## Dependencies

- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool (similar to Prisma migrations)
- **psycopg2-binary**: PostgreSQL adapter
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation

## Environment Variables

- `PORT`: Server port (default: 6174)
- `DATABASE_URL`: PostgreSQL connection string (format: `postgresql://user:password@host:port/database`)

## Database Migrations

Este backend usa **Alembic** para manejar migraciones de base de datos de forma automática, similar a cómo Prisma lo hace en Node.js o Entity Framework en .NET.

### Migraciones Automáticas

Cuando modificas un modelo en `models.py` (por ejemplo, agregas un campo), Alembic puede detectar los cambios y generar migraciones automáticamente.

### Comandos Básicos

**Aplicar todas las migraciones pendientes:**
```bash
alembic upgrade head
```

**Crear una nueva migración después de modificar modelos:**
```bash
# Alembic detecta los cambios automáticamente
alembic revision --autogenerate -m "Add new field to Example"
alembic upgrade head
```

**Ver estado actual:**
```bash
alembic current
```

**Revertir última migración:**
```bash
alembic downgrade -1
```

### Ejemplo: Agregar un Campo

1. Modifica `models.py` agregando el nuevo campo
2. Genera la migración: `alembic revision --autogenerate -m "Add email field"`
3. Revisa el archivo generado en `alembic/versions/`
4. Aplica: `alembic upgrade head`

**📖 Para más detalles, consulta [MIGRATIONS.md](./MIGRATIONS.md)**

### Migración Inicial

La primera vez que configures la base de datos, ejecuta:

```bash
alembic upgrade head
```

Esto creará la tabla `example` con el siguiente esquema:
- `id` (integer, primary key, auto-increment)
- `name` (varchar 200, required)
- `title` (varchar 200, required)
- `entry_date` (timestamp, auto-set on creation)
- `description` (varchar 1000, optional)
- `is_active` (boolean, default: true)

El script `run.sh` ejecuta automáticamente las migraciones al iniciar.

## Development

### Running Tests
```bash
# Tests not yet implemented
pytest
```

### Type Checking
```bash
# Install mypy first
pip install mypy
mypy main.py
```

### Linting
```bash
# Install flake8 first
pip install flake8
flake8 main.py database.py
```

## Troubleshooting

### Python command not found
On macOS/Linux, use `python3` instead of `python`:
```bash
python3 main.py
```

### psycopg2-binary installation fails
Install PostgreSQL development libraries:

**macOS**:
```bash
brew install libpq openssl@3
```

**Ubuntu/Debian**:
```bash
sudo apt-get install libpq-dev
```

**RHEL/CentOS**:
```bash
sudo yum install postgresql-devel
```

### Port already in use
Change the port in `.env`:
```env
PORT=8081
```

### Database connection fails
1. Ensure PostgreSQL is running
2. Check the `DATABASE_URL` in `.env`
3. Verify database credentials
4. Test connection: http://localhost:6174/api/health/db
5. Run migrations: `alembic upgrade head`

### Migration errors
- **"Target database is not up to date"**: Run `alembic upgrade head`
- **"Can't locate revision"**: Check migration history with `alembic history`
- **"Multiple heads detected"**: Merge with `alembic merge heads -m "Merge branches"`
- See [MIGRATIONS.md](./MIGRATIONS.md) for detailed troubleshooting

## Example Entity

The `Example` entity matches the structure used in Node.js, .NET, and Spring Boot backends:

- `id` (int) - Primary key, auto-generated
- `name` (string) - Name of the example (required, max 200 chars)
- `title` (string) - Title of the example (required, max 200 chars)
- `entryDate` (datetime) - Date when the entry was created (auto-set)
- `description` (string?) - Optional description (max 1000 chars)
- `isActive` (bool) - Active status (default: true)

## Notes

- The backend runs on port 6174 by default (configurable via `PORT` env var)
- All backends share the same API contract for interoperability
- Swagger documentation is auto-generated from the code
- CORS is enabled for frontend development
- Database migrations are automatically run by `run.sh` if `DATABASE_URL` is configured

