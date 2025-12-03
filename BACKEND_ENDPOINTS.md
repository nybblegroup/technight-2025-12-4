# Backend API Endpoints Reference

All backends run on **port 8080** and share the same API structure for consistency.

## Common Endpoints (All Backends)

### Swagger UI (Interactive API Documentation)
```
http://localhost:8080/api/swagger
```
- Interactive interface to explore and test all API endpoints
- View request/response schemas
- Execute API calls directly from the browser

### Health Check
```
http://localhost:8080/api/health
```
- Returns server health status
- Useful for monitoring and load balancers

### Examples API
Base path: `http://localhost:8080/api/examples`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/examples` | Get all examples |
| GET | `/api/examples/{id}` | Get example by ID |
| GET | `/api/examples/search?name={name}` | Search examples by name |
| POST | `/api/examples` | Create new example |
| PUT | `/api/examples/{id}` | Update example |
| DELETE | `/api/examples/{id}` | Delete example |

## Backend-Specific Details

### Node.js Backend (Express + TypeScript + Prisma)

**Start:**
```bash
cd backend/node
npm run dev
```

**Endpoints:**
- Swagger UI: http://localhost:8080/api/swagger
- OpenAPI JSON: http://localhost:8080/api/openapi.json
- OpenAPI YAML: http://localhost:8080/api/openapi.yaml
- Health: http://localhost:8080/api/health

**Features:**
- TypeScript with full type safety
- Prisma ORM for database operations
- Modular route organization
- Auto-generated Swagger docs from JSDoc comments

---

### Spring Boot Backend (Java + JPA + Flyway)

**Start:**
```bash
cd backend/springboot
./run.sh
# or
mvn spring-boot:run
```

**Endpoints:**
- Swagger UI: http://localhost:8080/api/swagger
- OpenAPI JSON: http://localhost:8080/api/openapi
- Health: http://localhost:8080/api/health

**Features:**
- Spring Boot 4.0
- JPA with Hibernate
- Flyway database migrations
- SpringDoc OpenAPI 3 integration
- Auto-generated Swagger docs from annotations

---

### .NET Backend (ASP.NET Core 10 + Entity Framework)

**Start:**
```bash
cd backend/dotnet/TechnightApi
dotnet run
```

**Endpoints:**
- Swagger UI: http://localhost:8080/api/swagger
- OpenAPI JSON: http://localhost:8080/api/swagger/v1/swagger.json
- Health: http://localhost:8080/api/health

**Features:**
- .NET 10 with minimal APIs
- Entity Framework Core for database operations
- Migration support
- Built-in Swagger generation

---

### Python Backend (FastAPI + SQLAlchemy)

**Start:**
```bash
cd backend/python
./run.sh
# or
python3 main.py
```

**Endpoints:**
- Swagger UI: http://localhost:8080/api/swagger
- OpenAPI JSON: http://localhost:8080/api/openapi.json
- OpenAPI YAML: http://localhost:8080/api/openapi.yaml
- Health: http://localhost:8080/api/health
- Database Health: http://localhost:8080/api/health/db

**Features:**
- FastAPI with automatic OpenAPI generation
- SQLAlchemy ORM
- Async support
- Pydantic models for validation
- Built-in Swagger UI

---

## Testing Endpoints

### Using curl

```bash
# Health check
curl http://localhost:8080/api/health

# Get all examples
curl http://localhost:8080/api/examples

# Get example by ID
curl http://localhost:8080/api/examples/1

# Search examples
curl http://localhost:8080/api/examples/search?name=First

# Create example
curl -X POST http://localhost:8080/api/examples \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","title":"Test Title","description":"Test description","isActive":true}'

# Update example
curl -X PUT http://localhost:8080/api/examples/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Delete example
curl -X DELETE http://localhost:8080/api/examples/1
```

### Using Swagger UI

1. Start any backend
2. Open http://localhost:8080/api/swagger in your browser
3. Browse available endpoints
4. Click "Try it out" on any endpoint
5. Fill in parameters and click "Execute"

## Database Configuration

Each backend uses its own PostgreSQL database:

- **Node.js**: `technightdb-node`
- **Spring Boot**: `technightdb-springboot`
- **.NET**: `technightdb-dotnet`
- **Python**: `technightdb-python`

Connection string format:
```
postgresql://postgres:mysecretpassword@localhost:5432/[database-name]
```

## CORS Configuration

All backends allow requests from:
- http://localhost:5173 (Vite dev server)
- http://localhost:3000 (React/Next.js dev server)

## Notes

- Only **one backend can run at a time** since they all use port 8080
- All backends implement the **same API contract** for interoperability
- Frontend can connect to any backend by changing `VITE_API_BASE_URL`
- Each backend has its own seed data and migrations

