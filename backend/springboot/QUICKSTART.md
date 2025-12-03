# TechnightApi Spring Boot - Quick Start Guide

This guide will help you get the Spring Boot API up and running in 5 minutes.

## ⚡ Quick Start (5 minutes)

### 1. Prerequisites

Make sure you have:
- ☕ Java 25 installed
- 📦 Maven 3.9+ installed
- 🐘 PostgreSQL running (or use Docker)

Check versions:
```bash
java -version    # Should show Java 25
mvn -version     # Should show Maven 3.9+
```

### 2. Start PostgreSQL Database

**Option A: Using Docker (Recommended)**
```bash
docker run --name postgres-technight-springboot \
  -e POSTGRES_DB=technightdb-springboot \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres:17
```

**Option B: Use Existing PostgreSQL**
```sql
CREATE DATABASE "technightdb-springboot";
```

### 3. Run the Application

```bash
# Make the run script executable
chmod +x run.sh

# Run the application
./run.sh
```

Or using Maven directly:
```bash
mvn spring-boot:run
```

### 4. Verify It's Working

Open your browser and visit:
- 🏥 Health Check: http://localhost:8080/api/health
- 📚 Swagger UI: http://localhost:8080/api/swagger

You should see:
- Health check returning `{"status":"healthy",...}`
- Swagger UI with all API endpoints documented

### 5. Test the API

Using Swagger UI:
1. Go to http://localhost:8080/api/swagger
2. Click on `GET /api/examples`
3. Click "Try it out"
4. Click "Execute"
5. You should see 2 example records in the response

Using curl:
```bash
# Get all examples
curl http://localhost:8080/api/examples

# Get example by ID
curl http://localhost:8080/api/examples/1

# Create a new example
curl -X POST http://localhost:8080/api/examples \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Example",
    "title": "Test Title",
    "description": "This is a test",
    "isActive": true
  }'
```

## 🎯 What You Get

The application includes:
- ✅ REST API with CRUD operations
- ✅ PostgreSQL database with Flyway migrations
- ✅ Swagger/OpenAPI documentation
- ✅ JPA/Hibernate for database operations
- ✅ Input validation
- ✅ CORS enabled for frontend
- ✅ Sample data already loaded

## 📍 Important URLs

| Service | URL |
|---------|-----|
| API Base | http://localhost:8080 |
| Swagger UI | http://localhost:8080/api/swagger |
| OpenAPI JSON | http://localhost:8080/api/openapi |
| Health Check | http://localhost:8080/api/health |
| Database | postgresql://localhost:5432/technightdb-springboot |

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/examples` | Get all examples |
| GET | `/api/examples/{id}` | Get example by ID |
| POST | `/api/examples` | Create new example |
| PUT | `/api/examples/{id}` | Update example |
| DELETE | `/api/examples/{id}` | Delete example |
| GET | `/api/examples/search?name=xxx` | Search examples |

## 🛠️ Common Commands

```bash
# Build the project
mvn clean install

# Run the application
mvn spring-boot:run

# Run with dev profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# Run tests
mvn test

# Package as JAR
mvn clean package

# Run the JAR
java -jar target/technight-api-1.0.0.jar

# Stop the application
Ctrl+C
```

## 🐛 Troubleshooting

### Port 8080 already in use

Change the port in `src/main/resources/application.properties`:
```properties
server.port=8081
```

### Database connection error

1. Check if PostgreSQL is running:
   ```bash
   docker ps | grep postgres
   ```

2. Verify connection settings in `application.properties`:
   ```properties
   spring.datasource.url=jdbc:postgresql://localhost:5432/technightdb-springboot
   spring.datasource.username=postgres
   spring.datasource.password=mysecretpassword
   ```

3. Test database connection:
   ```bash
   psql -h localhost -U postgres -d technightdb-springboot
   ```

### Flyway migration errors

Clean and recreate database:
```bash
# Drop and recreate database
docker exec -it postgres-technight-springboot psql -U postgres -c "DROP DATABASE IF EXISTS \"technightdb-springboot\";"
docker exec -it postgres-technight-springboot psql -U postgres -c "CREATE DATABASE \"technightdb-springboot\";"

# Restart application
mvn spring-boot:run
```

### Maven build fails

Clear Maven cache:
```bash
mvn clean install -U
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [SWAGGER.md](SWAGGER.md) for Swagger/OpenAPI customization
- Explore the code in `src/main/java/com/technight/api/`
- Add your own entities, controllers, and endpoints
- Configure additional features like authentication, caching, etc.

## 💡 Development Tips

1. **Hot Reload**: DevTools is included, so code changes trigger automatic restart
2. **Database Viewer**: Use tools like DBeaver or pgAdmin to view database
3. **Testing**: Use Swagger UI for quick API testing during development
4. **Logs**: Check console output for SQL queries and application logs
5. **Profiles**: Use `-Dspring-boot.run.profiles=dev` for development settings

## 🎓 Learning Resources

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Data JPA Guide](https://spring.io/guides/gs/accessing-data-jpa/)
- [Flyway Migrations](https://flywaydb.org/documentation/)
- [SpringDoc OpenAPI](https://springdoc.org/)

---

**Need help?** Check the detailed README.md or open an issue.

