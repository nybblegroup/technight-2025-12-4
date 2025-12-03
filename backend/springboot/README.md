# TechnightApi - Spring Boot

A Spring Boot 4.0 REST API with PostgreSQL, JPA, Flyway migrations, and Swagger/OpenAPI documentation.

## 🚀 Tech Stack

- **Java**: 25
- **Spring Boot**: 4.0.0
- **Database**: PostgreSQL 17
- **ORM**: Spring Data JPA
- **Migrations**: Flyway
- **Documentation**: SpringDoc OpenAPI (Swagger)
- **Lombok**: 1.18.40 (reduces boilerplate code)
- **Build Tool**: Maven

## 📋 Prerequisites

- Java 25 (JDK)
- Maven 3.9+
- PostgreSQL 17 (running locally or in Docker)

## 🗄️ Database Setup

### Option 1: Using Docker

```bash
docker run --name postgres-technight-springboot \
  -e POSTGRES_DB=technightdb-springboot \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres:17
```

### Option 2: Existing PostgreSQL

Create a new database:

```sql
CREATE DATABASE "technightdb-springboot";
```

Update the connection string in `src/main/resources/application.properties` if needed:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/technightdb-springboot
spring.datasource.username=postgres
spring.datasource.password=mysecretpassword
```

## 🏃 Running the Application

### Using Maven

```bash
# Build the project
mvn clean install

# Run the application
mvn spring-boot:run
```

### Using the run script

```bash
chmod +x run.sh
./run.sh
```

### Using Java directly

```bash
mvn clean package
java -jar target/technight-api-1.0.0.jar
```

The API will be available at: `http://localhost:8080`

## 📚 API Documentation

Once the application is running, access:

- **Swagger UI**: http://localhost:8080/api/swagger
- **OpenAPI JSON**: http://localhost:8080/api/openapi
- **Health Check**: http://localhost:8080/api/health

## 🔌 API Endpoints

### Health Check

- `GET /api/health` - Health check endpoint

### Examples

- `GET /api/examples` - Get all examples (ordered by entry date desc)
- `GET /api/examples/{id}` - Get example by ID
- `POST /api/examples` - Create a new example
- `PUT /api/examples/{id}` - Update an existing example
- `DELETE /api/examples/{id}` - Delete an example
- `GET /api/examples/search?name={name}` - Search examples by name (case-insensitive)

### Example Request Body (POST/PUT)

**Create Example (POST):**

```json
{
  "name": "My Example",
  "title": "Example Title",
  "description": "Optional description",
  "isActive": true
}
```

**Update Example (PUT):**

```json
{
  "name": "Updated Name",
  "title": "Updated Title",
  "description": "Updated description",
  "isActive": false
}
```

Note: All fields in the update request are optional.

## 🗂️ Project Structure

```
springboot/
├── src/
│   ├── main/
│   │   ├── java/com/technight/api/
│   │   │   ├── config/
│   │   │   │   └── OpenApiConfig.java       # Swagger configuration
│   │   │   ├── controller/
│   │   │   │   ├── ExampleController.java   # REST endpoints
│   │   │   │   └── HealthController.java    # Health check
│   │   │   ├── dto/
│   │   │   │   ├── CreateExampleDto.java    # Create DTO
│   │   │   │   └── UpdateExampleDto.java    # Update DTO
│   │   │   ├── model/
│   │   │   │   └── Example.java             # JPA entity
│   │   │   ├── repository/
│   │   │   │   └── ExampleRepository.java   # JPA repository
│   │   │   └── TechnightApiApplication.java # Main class
│   │   └── resources/
│   │       ├── db/migration/
│   │       │   └── V1__Initial_Create.sql   # Flyway migration
│   │       ├── application.properties        # Main config
│   │       └── application-dev.properties    # Dev config
│   └── test/
│       └── java/com/technight/api/
│           └── TechnightApiApplicationTests.java
├── pom.xml                                   # Maven configuration
├── README.md                                 # This file
└── run.sh                                    # Run script
```

## 🔧 Configuration

### Database Configuration

Edit `src/main/resources/application.properties`:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/technightdb-springboot
spring.datasource.username=postgres
spring.datasource.password=mysecretpassword
```

### Server Port

Change the server port in `application.properties`:

```properties
server.port=8080
```

### Flyway Migrations

Migrations are automatically applied on startup. Migration files are located in:

```
src/main/resources/db/migration/
```

To disable automatic migrations:

```properties
spring.flyway.enabled=false
```

## 🧪 Testing

```bash
# Run all tests
mvn test

# Run with coverage
mvn clean test jacoco:report
```

## 🏗️ Building for Production

```bash
# Build JAR file
mvn clean package

# Run the JAR
java -jar target/technight-api-1.0.0.jar
```

The JAR file will be created in the `target/` directory.

## 🔍 Database Schema

### Example Table

| Column      | Type         | Constraints       |
|-------------|--------------|-------------------|
| id          | INTEGER      | PRIMARY KEY, AUTO |
| name        | VARCHAR(200) | NOT NULL          |
| title       | VARCHAR(200) | NOT NULL          |
| entry_date  | TIMESTAMP    | NOT NULL          |
| description | VARCHAR(1000)| NULLABLE          |
| is_active   | BOOLEAN      | NOT NULL, DEFAULT true |

**Indexes:**
- `ix_example_entry_date` on `entry_date` column

## 📝 Development Notes

### Using Lombok

This project uses Lombok to reduce boilerplate code. Make sure your IDE has the Lombok plugin installed:

- **IntelliJ IDEA**: Install Lombok plugin from marketplace
- **Eclipse**: Install from https://projectlombok.org/setup/eclipse
- **VS Code**: Install "Lombok Annotations Support for VS Code"

### Hot Reload

Spring Boot DevTools is included for automatic restart during development. Any changes to:
- Java code
- Resources
- Configuration files

Will trigger an automatic application restart.

### CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (React/Next.js default)

Update `@CrossOrigin` annotations in controllers to modify this.

## 🐛 Troubleshooting

### Database Connection Issues

1. Verify PostgreSQL is running:
   ```bash
   docker ps | grep postgres
   # or
   pg_isready -h localhost -p 5432
   ```

2. Check connection string in `application.properties`

3. Verify database exists:
   ```bash
   psql -U postgres -l | grep technightdb-springboot
   ```

### Port Already in Use

If port 8080 is in use, change it in `application.properties`:

```properties
server.port=8081
```

### Flyway Migration Errors

If migrations fail, you can clean and retry:

```bash
# Connect to database
psql -U postgres -d technightdb-springboot

# Drop all tables
DROP TABLE IF EXISTS example CASCADE;
DROP TABLE IF EXISTS flyway_schema_history CASCADE;

# Restart application to re-run migrations
```

### Maven Build Issues

Clear Maven cache and rebuild:

```bash
mvn clean install -U
```

## 📦 Dependencies

Key dependencies and their versions:

- Spring Boot: 4.0.0
- PostgreSQL Driver: (managed by Spring Boot)
- Flyway: (managed by Spring Boot)
- SpringDoc OpenAPI: 2.7.0
- Lombok: (managed by Spring Boot)

## 🔗 Related Documentation

- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Flyway Documentation](https://flywaydb.org/documentation/)
- [SpringDoc OpenAPI](https://springdoc.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📄 License

MIT License

