Copyright (c) 2025 Software Tree

# ORMCP Server Examples

Working example repositories demonstrating ORMCP Server with various Gilhari microservice configurations.

All examples include:
- Complete source code
- Pre-configured Gilhari microservice
- SQLite database with sample data (or instructions for other databases)
- Dockerfile and build scripts
- README with step-by-step instructions
- curl test scripts for API validation
- Ready to run with Docker

---

## Getting Started with Examples

### Quick Start

**IMPORTANT:** Docker is required for building and running a Gilhari microservice — **[Get Docker](https://docs.docker.com/get-docker/)** if not already installed on your machine

```bash
# 1. Clone an example repository
git clone https://github.com/SoftwareTree/gilhari_example1.git
cd gilhari_example1

# 2. Pull Gilhari Docker image
docker pull softwaretree/gilhari:latest

# 3. Build the example microservice
./build.sh   # Linux/Mac
# or
build.cmd    # Windows

# 4. Run the microservice
docker run -d -p 80:8081 --name gilhari_example1 gilhari_example1:1.0

# 5. Verify it's running
curl http://localhost:80/gilhari/v1/health/check

# 6. Configure ORMCP Server (if using ORMCP)
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
export MCP_SERVER_NAME="MyORMCPServer"

# 7. Start ORMCP Server
ormcp-server
```

---

## Available Examples

### 1. gilhari_example1 - Basic User Management ⭐ **Start Here**

**Repository:** [github.com/SoftwareTree/gilhari_example1](https://github.com/SoftwareTree/gilhari_example1)

**What it demonstrates:**
- Simple single-entity object model (User)
- Basic CRUD operations (Create, Read, Update, Delete)
- Query filtering (`age > 40`, `state='CA'`)
- Aggregate queries (COUNT, AVG)
- SQLite database integration
- ORM mapping fundamentals
- Advanced projections with `operationDetails` parameter

**Object Model:**
```json
{
  "id": 55,
  "name": "Mary55",
  "age": 55,
  "city": "Campbell",
  "state": "CA"
}
```

**Use this when:**
- Learning ORMCP/Gilhari basics
- Testing simple queries
- Understanding ORM concepts
- First time with Gilhari microservices

---

### 2. gilhari_simple_example - Employee Management

**Repository:** [github.com/SoftwareTree/gilhari_simple_example](https://github.com/SoftwareTree/gilhari_simple_example)

**What it demonstrates:**
- Simple Employee object management
- Basic domain model patterns
- Fundamental CRUD operations
- Filtering and queries

**Object Model:**
- Employee (basic employee information)

**Use this when:**
- Building HR or employee systems
- Learning simple business object patterns
- Testing basic business data models

---

### 3. gilhari_onetomany_example - One-to-Many Relationships

**Repository:** [github.com/SoftwareTree/gilhari_onetomany_example](https://github.com/SoftwareTree/gilhari_onetomany_example)

**What it demonstrates:**
- One-to-many relationships (parent has multiple children)
- BYVALUE containment semantics
- Deep vs shallow queries
- Relationship traversal
- Referenced object retrieval
- Cascading operations

**Object Model:**
- Parent → Children (one parent has many child objects)

**Use this when:**
- Modeling parent-child relationships
- Understanding deep queries
- Learning relationship navigation
- Implementing containment patterns

---

### 4. gilhari_relationships_example - Complex Relationships

**Repository:** [github.com/SoftwareTree/gilhari_relationships_example](https://github.com/SoftwareTree/gilhari_relationships_example)

**What it demonstrates:**
- One-to-one relationships (A → B)
- One-to-many relationships (A → C array)
- Multiple relationship types in single model
- BYVALUE containment semantics
- Path expressions for querying (`jdxObject.aB.bInt>100`)
- Advanced projections and selective following
- Nested object queries

**Object Model:**
```json
{
  "aId": 1,
  "aString": "aString_1",
  "aBoolean": true,
  "aFloat": 1.1,
  "aB": { "bId": 100, "bInt": 100 },
  "aCs": [
    { "cId": 1000, "cInt": 100 },
    { "cId": 2000, "cInt": 200 }
  ]
}
```

**Use this when:**
- Building complex data models
- Understanding multiple relationship types
- Learning nested queries
- Implementing both one-to-one and one-to-many patterns

---

### 5. gilhari_manytomany_example - Many-to-Many Relationships

**Repository:** [github.com/SoftwareTree/gilhari_manytomany_example](https://github.com/SoftwareTree/gilhari_manytomany_example)

**What it demonstrates:**
- Many-to-many relationships
- Junction table handling
- Bidirectional relationships
- Complex queries across relationships
- Association management

**Object Model:**
- Entity A ↔ Entity B (entities can have multiple associations in both directions)
- Junction/association table for relationship management

**Use this when:**
- Modeling many-to-many relationships
- Understanding junction tables
- Building enrollment, membership, or tagging systems
- Implementing bidirectional associations

---

### 6. gilhari_streaming_example - Large Result Sets

**Repository:** [github.com/SoftwareTree/gilhari_streaming_example](https://github.com/SoftwareTree/gilhari_streaming_example)

**What it demonstrates:**
- Efficient handling of large datasets
- Streaming query results
- Pagination techniques
- Memory optimization strategies
- Performance best practices for large tables

**Use this when:**
- Dealing with large tables (thousands+ rows)
- Optimizing query performance
- Understanding pagination and result limiting
- Managing memory efficiently

---

### 7. gilhari_autoincrement_example - Auto-Generated Keys

**Repository:** [github.com/SoftwareTree/gilhari_autoincrement_example](https://github.com/SoftwareTree/gilhari_autoincrement_example)

**What it demonstrates:**
- Database-generated primary keys
- Auto-increment columns (SQLite, MySQL)
- Identity columns (SQL Server)
- Sequence handling (PostgreSQL, Oracle)
- RDBMS_GENERATED configuration
- Different database-specific key generation strategies

**Use this when:**
- Using auto-increment IDs instead of manual IDs
- Working with identity columns
- Understanding key generation strategies
- Letting the database manage primary keys

---

## Example Structure

Each example repository follows this standard structure:

```
gilhari_example_name/
├── README.md                    # Complete setup instructions
├── Dockerfile                   # Docker image configuration
├── gilhari_service.config       # Gilhari microservice runtime configuration
├── build.sh / build.cmd         # Docker image build scripts
├── run_docker_app.sh / .cmd     # Container run scripts
├── compile.sh / compile.cmd     # Java compilation scripts
├── sources.txt                  # List of Java source files
├── src/                         # Java container domain model classes
│   └── com/softwaretree/.../model/
│       └── *.java               # Container classes (extend JDX_JSONObject)
├── bin/                         # Compiled .class files (generated)
│   └── com/softwaretree/.../model/
│       └── *.class
├── config/                      # Configuration files
│   ├── *.jdx                    # ORM specification file
│   ├── *.db                     # SQLite database (if using SQLite)
│   ├── classnames_map*.js       # Optional class name mappings
│   └── [jdbc-driver.jar]        # JDBC driver (if not using default)
├── curlCommands.sh / .cmd       # API testing scripts
└── curlCommandsPopulate.sh/.cmd # Data population scripts
```

---

## Using Examples with ORMCP

### Step-by-Step Workflow

**1. Choose an Example**

Pick an example that matches your learning goal or use case. Start with **gilhari_example1** if you're new to Gilhari/ORMCP.

**2. Clone and Build**

```bash
git clone https://github.com/SoftwareTree/<example-name>.git
cd <example-name>

# Pull base image
docker pull softwaretree/gilhari:latest

# Build the Docker image
./build.sh  # or build.cmd on Windows
```

**3. Run Gilhari Microservice**

```bash
# Run with default port mapping (80 → 8081)
docker run -d -p 80:8081 --name <example-name> <example-name>:1.0

# Or use a custom port
docker run -d -p 8888:8081 --name <example-name> <example-name>:1.0
```

**4. Verify Gilhari is Running**

```bash
# Health check
curl http://localhost:80/gilhari/v1/health/check

# Get object model summary
curl http://localhost:80/gilhari/v1/getObjectModelSummary/now
```

**5. Test with curl Scripts (Optional)**

```bash
# Run comprehensive API tests
./curlCommands.sh      # or curlCommands.cmd on Windows

# Populate sample data
./curlCommandsPopulate.sh

# View results
cat curl.log
```

**6. Configure ORMCP Server (If Using ORMCP)**

```bash
# Set Gilhari endpoint
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"

# Optional: Set server name
export MCP_SERVER_NAME="MyORMCPServer"
```

**7. Start ORMCP Server**

```bash
ormcp-server
```

**8. Connect Your MCP Client**

Configure Claude Desktop (or your MCP client) to use the ORMCP Server. See the [Quick Start Guide](../guides/quickstart.md) for details.

**9. Try Natural Language Queries**

Use natural language to interact with the example data:

```
"Show me all users"
"Get users from California"
"What's the average age of users?"
"Create a new user named John, age 30, in San Francisco, CA"
"Delete all users older than 50"
```

---

## Learning Path

### Beginner

**1. Start with gilhari_example1** ⭐
- Basic CRUD operations
- Simple queries and filters
- Understanding ORM fundamentals
- GET, POST, PUT, DELETE operations

**2. Try gilhari_simple_example**
- Business object patterns
- Domain model basics
- More complex filtering

### Intermediate

**3. Explore gilhari_onetomany_example**
- Parent-child relationships
- Deep vs shallow queries
- Relationship traversal
- BYVALUE containment

**4. Study gilhari_relationships_example**
- Multiple relationship types
- Complex nested objects
- Path expressions
- Advanced projections

### Advanced

**5. Master gilhari_manytomany_example**
- Junction tables
- Bidirectional relationships
- Complex association patterns
- Many-to-many queries

**6. Optimize with gilhari_streaming_example**
- Performance tuning
- Large dataset handling
- Pagination strategies
- Memory optimization

**7. Understand gilhari_autoincrement_example**
- Auto-generated keys
- Database-specific features
- RDBMS_GENERATED configuration
- Different ID generation strategies

---

## Customizing Examples

### Modify the Data Model

**1. Edit Container Domain Model Classes** (`src/com/.../model/*.java`)

Add or modify Java container classes:
```java
public class MyClass extends JDX_JSONObject {
    public MyClass() { super(); }
    public MyClass(JSONObject jsonObject) throws JSONException { 
        super(jsonObject); 
    }
    // For relationships, declare attributes
    public MyRelatedClass myRelation;
}
```

**2. Update ORM Specification** (`config/*.jdx`)

Map the new classes and attributes:
```
CLASS com.example.model.MyClass TABLE MY_TABLE
  VIRTUAL_ATTRIB id ATTRIB_TYPE int
  VIRTUAL_ATTRIB name ATTRIB_TYPE java.lang.String
  PRIMARY_KEY id
  RELATIONSHIP myRelation REFERENCES MyRelatedClass BYVALUE WITH id
;
```

**3. Recompile Container Classes**

```bash
# Ensure JX_HOME is set to Gilhari SDK location
./compile.sh  # or compile.cmd on Windows
```

**4. Rebuild Docker Image**

```bash
./build.sh
docker run -d -p 80:8081 --name custom-example custom-example:1.0
```

### Switch to a Different Database

#### Example: Using PostgreSQL Instead of SQLite

**1. Edit ORM Specification** (`config/model.jdx`)

```
JDX_DATABASE JDX:jdbc:postgresql://host.docker.internal:5432/mydb;USER=myuser;PASSWORD=mypass;JDX_DBTYPE=POSTGRES;DEBUG_LEVEL=5
JDBC_DRIVER org.postgresql.Driver
```

See `JDX_DATABASE_JDBC_DRIVER_Specification_Guide.md` for other database configurations.

**2. Download PostgreSQL JDBC Driver**

- Download from [https://jdbc.postgresql.org/](https://jdbc.postgresql.org/)
- Place `postgresql-42.7.1.jar` (or current version) in `config/` directory

**3. Edit Service Configuration** (`gilhari_service.config`)

```json
{
  "gilhari_microservice_name": "my_custom_example",
  "jdx_orm_spec_file": "./config/model.jdx",
  "jdbc_driver_path": "./config/postgresql-42.7.1.jar",
  "jdx_debug_level": 3,
  "jdx_force_create_schema": "true",
  "jdx_persistent_classes_location": "./bin",
  "classnames_map_file": "config/classnames_map.js",
  "gilhari_rest_server_port": 8081
}
```

**4. Create PostgreSQL Database**

```sql
CREATE DATABASE mydb;
-- Gilhari will create tables automatically if jdx_force_create_schema is true
```

**5. Rebuild and Run**

```bash
./build.sh
docker run -d -p 80:8081 --name custom-example custom-example:1.0
```

**Note for Docker:**
- Use `host.docker.internal` instead of `localhost` to access databases running on the host machine
- For cloud databases, use the actual IP address or hostname

---

## Troubleshooting Examples

### Example Won't Build

**Check Docker Installation:**
```bash
docker --version
docker images | grep gilhari
```

**Pull Base Image:**
```bash
docker pull softwaretree/gilhari:latest
```

**Check for Build Errors:**
```bash
# Review build output for errors
./build.sh 2>&1 | tee build.log
```

### Example Won't Compile

**Check JX_HOME:**
```bash
# Linux/Mac
echo $JX_HOME

# Windows
echo %JX_HOME%
```

**Verify JDK Installation:**
```bash
javac -version  # Should be 1.8 or higher
```

**Check Source Files:**
- Ensure all `.java` files are listed in `sources.txt`
- Verify package declarations match directory structure

### Example Won't Run

**Check Port Availability:**
```bash
# Ensure port 80 (or your chosen port) is free
# Linux/Mac
netstat -an | grep :80
lsof -i :80

# Windows
netstat -an | findstr :80
```

**Use Different Port if Needed:**
```bash
docker run -d -p 8888:8081 --name example example:1.0
# Access at http://localhost:8888
```

**Check Container Logs:**
```bash
# Get container ID
docker ps -a

# View logs
docker logs <container-id>

# Follow logs in real-time
docker logs -f <container-id>
```

**Common Log Issues:**
- Missing or incorrect `.jdx` file
- JDBC driver not found
- Database connection errors
- Invalid class paths

### Can't Connect from ORMCP

**Verify Gilhari is Running:**
```bash
curl http://localhost:80/gilhari/v1/health/check
# Should return: {"status": "Gilhari REST Server is up and running"}
```

**Check Object Model Summary:**
```bash
curl http://localhost:80/gilhari/v1/getObjectModelSummary/now
# Should return JSON with class definitions
```

**Verify Environment Variable:**
```bash
echo $GILHARI_BASE_URL
# Should be: http://localhost:80/gilhari/v1/
# Or match the port your Gilhari microservice is running on
```

**Check ORMCP Server Logs:**
- ORMCP server logs connection attempts
- Verify the URL matches the running Gilhari instance

### Database Connection Issues

**SQLite (Default):**
- Database file created automatically in `config/` directory
- No configuration needed beyond what's in the example

**External Databases (MySQL, PostgreSQL):**
- Verify database server is running
- Check username/password in `.jdx` file
- For Docker: Use `host.docker.internal` instead of `localhost`
- Ensure JDBC driver JAR is in `config/` directory
- Check firewall rules allow connections

---

## Creating Your Own Example

Want to create a custom Gilhari microservice from scratch? See the comprehensive [Gilhari Setup Guide](../guides/gilhari_setup.md).

**Basic Steps:**
1. Define your domain model (Java container classes)
2. Create ORM specification (.jdx file)
3. Set up database and JDBC driver
4. Configure service (gilhari_service.config)
5. Create Dockerfile
6. Build and test
7. Document and share

**What You Need:**
- Gilhari SDK (for compiling custom classes)
- JDK 1.8+ (for compilation)
- Docker (for building and running)
- Your target database and JDBC driver

---

## Additional Resources

- **[Gilhari Setup Guide](../guides/gilhari_setup.md)** - Complete guide to creating custom microservices
- **[Quick Start Guide](../guides/quickstart.md)** - Get started with ORMCP quickly
- **[MCP Tools Reference](../reference/ormcp_tools_reference.md)** - API documentation
- **[Troubleshooting Guide](../guides/troubleshooting.md)** - Common issues and solutions
- **[Database Configuration Guide](JDX_DATABASE_JDBC_DRIVER_Specification_Guide.md)** - Database-specific configurations
- **[operationDetails Documentation](operationDetails_doc.md)** - Advanced query capabilities

---

## Support

**Questions about examples?**
- GitHub Issues: [softwaretree/ormcp-docs/issues](https://github.com/softwaretree/ormcp-docs/issues)
- Email: ormcp_support@softwaretree.com

**Found a bug in an example?**
- Report in the specific example repository's issues
- Or in the main ORMCP docs repository

**Want to contribute an example?**

We welcome contributions! If you've built a useful example, please share:
- Use cases and requirements
- Domain model description
- Any special configurations
- Documentation

Contact us via GitHub Issues or email to discuss contribution.

---

## Related Documentation

- [Back to Main README](../README.md)
- [Installation Guide](../guides/installation.md)
- [Quick Start Guide](../guides/quickstart.md)
- [Gilhari Setup Guide](../guides/gilhari_setup.md)
- [Troubleshooting Guide](../guides/troubleshooting.md)