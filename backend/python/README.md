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
PORT=8080
DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/technightdb-python?schema=public"
```

#### 4. Start the Server

```bash
python3 main.py
```

## API Endpoints

Once the server is running on http://localhost:8080:

### Documentation
- **Swagger UI**: http://localhost:8080/api/swagger
- **OpenAPI JSON**: http://localhost:8080/api/openapi.json
- **OpenAPI YAML**: http://localhost:8080/api/openapi.yaml

### Health Checks
- **API Health**: http://localhost:8080/api/health
- **Database Health**: http://localhost:8080/api/health/db

### Example CRUD Operations

The backend includes a complete Example entity implementation (matching the Node.js, Spring Boot, and .NET versions).

**Note**: The Python backend currently uses an in-memory data structure. Database integration is planned.

#### Get all examples
```bash
curl http://localhost:8080/api/examples
```

#### Get example by ID
```bash
curl http://localhost:8080/api/examples/1
```

#### Search examples
```bash
curl http://localhost:8080/api/examples/search?name=First
```

#### Create new example
```bash
curl -X POST http://localhost:8080/api/examples \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","title":"Test Title","description":"A test example","isActive":true}'
```

#### Update example
```bash
curl -X PUT http://localhost:8080/api/examples/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'
```

#### Delete example
```bash
curl -X DELETE http://localhost:8080/api/examples/1
```

## Project Structure

```
backend/python/
├── main.py           # FastAPI application entry point
├── database.py       # SQLAlchemy database configuration
├── requirements.txt  # Python dependencies
├── run.sh           # Automated setup and run script
├── .env             # Environment variables (create from .env.example)
└── venv/            # Virtual environment (created by run.sh)
```

## Dependencies

- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: SQL toolkit and ORM
- **psycopg2-binary**: PostgreSQL adapter
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation

## Environment Variables

- `PORT`: Server port (default: 8080)
- `DATABASE_URL`: PostgreSQL connection string

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
4. Test connection: http://localhost:8080/api/health/db

## Notes

- The backend runs on port 8080 (same as other backend implementations)
- All backends share the same API contract for interoperability
- Swagger documentation is auto-generated from the code
- CORS is enabled for frontend development

