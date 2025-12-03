# Swagger/OpenAPI Configuration for Spring Boot

## Overview

This Spring Boot application uses **SpringDoc OpenAPI 3** (version 2.7.0) to provide automatic API documentation via Swagger UI.

## Configuration

### Dependencies (pom.xml)

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.7.0</version>
</dependency>
```

### Application Properties

Located in `src/main/resources/application.properties`:

```properties
# SpringDoc OpenAPI Configuration
springdoc.api-docs.path=/api/openapi
springdoc.swagger-ui.path=/api/swagger
springdoc.swagger-ui.operationsSorter=method
springdoc.swagger-ui.tagsSorter=alpha
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.enabled=true
springdoc.api-docs.enabled=true
```

### OpenAPI Config Bean

Located in `src/main/java/com/technight/api/config/OpenApiConfig.java`:

```java
@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI technightOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("TechnightApi")
                        .description("A Spring Boot API with PostgreSQL and JPA")
                        .version("v1")
                        .contact(new Contact()
                                .name("Technight Team")
                                .email("info@technight.com"))
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")));
    }
}
```

## Accessing Swagger UI

Once the application is running on port 8080:

### Swagger UI (Interactive Documentation)
```
http://localhost:8080/api/swagger
```

### OpenAPI JSON Specification
```
http://localhost:8080/api/openapi
```

### Alternative Formats
SpringDoc automatically provides:
- JSON format: `http://localhost:8080/api/openapi`
- YAML format: Add `Accept: application/yaml` header

## Controller Annotations

Example from `ExampleController.java`:

```java
@RestController
@RequestMapping("/api/examples")
@Tag(name = "Examples", description = "Example management endpoints")
public class ExampleController {

    @GetMapping
    @Operation(summary = "Get all examples", 
               description = "Retrieves all example records from the database")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", 
                     description = "Successfully retrieved list",
                     content = @Content(schema = @Schema(implementation = Example.class)))
    })
    public ResponseEntity<List<Example>> getAllExamples() {
        // Implementation
    }
}
```

## Key Annotations

### Class Level
- `@Tag(name, description)` - Groups endpoints in Swagger UI
- `@RestController` - Marks class as REST controller
- `@RequestMapping("/path")` - Base path for all endpoints

### Method Level
- `@Operation(summary, description)` - Describes the endpoint
- `@ApiResponses` - Documents possible responses
- `@ApiResponse(responseCode, description)` - Individual response documentation
- `@Parameter(description)` - Documents request parameters

### DTOs and Models
- `@Schema(description)` - Documents model fields
- Spring Boot validation annotations (`@NotNull`, `@Size`, etc.) are automatically documented

## Troubleshooting

### Swagger UI Not Loading

1. **Check the URL**: Make sure you're accessing `/api/swagger`
   ```
   ✅ Correct: http://localhost:8080/api/swagger
   ```

2. **Verify Configuration**: Check `application.properties`:
   ```properties
   springdoc.swagger-ui.enabled=true
   springdoc.api-docs.enabled=true
   ```

3. **Check Logs**: Look for SpringDoc initialization messages:
   ```
   Swagger UI available at: /api/swagger
   OpenAPI docs available at: /api/openapi
   ```

4. **Verify Dependencies**: Ensure `springdoc-openapi-starter-webmvc-ui` is in `pom.xml`

5. **Rebuild**: Clean and rebuild the project:
   ```bash
   mvn clean install
   ```

### 404 Not Found

If you get 404 errors:
- Ensure the application started successfully
- Check that port 8080 is not blocked
- Verify no other application is using port 8080
- Check application logs for errors

### No Endpoints Visible

If Swagger UI loads but shows no endpoints:
- Verify controllers have `@RestController` annotation
- Check controllers are in the component scan path (`com.technight.api` package)
- Ensure methods have proper HTTP method annotations (`@GetMapping`, etc.)
- Check for compilation errors

### API Documentation Not Updating

If changes don't appear:
1. Rebuild the project: `mvn clean install`
2. Restart the application
3. Clear browser cache
4. Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

## Testing Swagger Endpoints

### Using curl

```bash
# Get OpenAPI specification
curl http://localhost:8080/api/openapi

# Get YAML format
curl -H "Accept: application/yaml" http://localhost:8080/api/openapi

# Test an API endpoint
curl http://localhost:8080/api/health
curl http://localhost:8080/api/examples
```

### Using Browser
Simply navigate to:
```
http://localhost:8080/api/swagger
```

The interactive UI allows you to:
- Browse all endpoints
- See request/response schemas
- Try out endpoints directly
- View example responses

## Additional Resources

- [SpringDoc OpenAPI Documentation](https://springdoc.org/)
- [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.0)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)

## Notes

- SpringDoc automatically generates documentation from your code
- No need for separate Swagger configuration files
- Swagger UI is enabled by default in development
- Consider disabling in production with: `springdoc.swagger-ui.enabled=false`

