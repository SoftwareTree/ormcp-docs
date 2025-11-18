Copyright (c) 2025 Software Tree

# Gilhari Microservice Setup Guide

> **Complete guide to setting up Gilhari microservices for RESTful JSON object persistence**

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Components](#setup-components)
  - [1. Container Domain Model Classes (Java)](#1-container-domain-model-classes-java)
  - [2. ORM Specification File (.jdx)](#2-orm-specification-file-jdx)
  - [3. Service Configuration File](#3-service-configuration-file)
  - [4. Class Names Mapping File](#4-class-names-mapping-file)
  - [5. Dockerfile](#5-dockerfile)
- [Relationship Mapping](#relationship-mapping)
- [Compilation and Build](#compilation-and-build)
- [Additional Examples](#additional-examples)
- [Troubleshooting](#troubleshooting)

## Troubleshooting

### Common Setup Issues

#### Compilation Errors

**Problem**: `javac: command not found`
- **Solution**: Install JDK 1.8+ and ensure `javac` is in your PATH
- **Verify**: Run `javac -version`

**Problem**: `Cannot find symbol: class JDX_JSONObject`
- **Solution**: Ensure `JX_HOME` environment variable is set correctly
- **Check**: `echo %JX_HOME%` (Windows) or `echo $JX_HOME` (Linux/Mac)
- **Verify**: JDX libraries exist at `$JX_HOME/JDXAndroid/libs/`

**Problem**: `package com.softwaretree.jdx does not exist`
- **Solution**: Verify CLASSPATH includes JDX JAR files in compilation script
- **Check**: `jdxjson-2.0.jar` and `json-20090211.jar` are in CLASSPATH

#### Docker Build Issues

**Problem**: `ERROR [internal] load metadata for docker.io/softwaretree/gilhari:latest`
- **Solution**: Pull the base image: `docker pull softwaretree/gilhari`
- **Alternative**: Check Docker Hub connectivity

**Problem**: `COPY failed: no source files were specified`
- **Solution**: Ensure `bin/` and `config/` directories exist and contain required files
- **Check**: Run compilation before building Docker image

**Problem**: Port 80 already in use
- **Solution**: Change port mapping in `run_docker_app` script
- **Example**: `-p 8080:8081` instead of `-p 80:8081`

#### Runtime Issues

**Problem**: Container starts but immediately exits
- **Solution**: Check container logs: `docker logs <container-id>`
- **Common causes**: 
  - Missing or incorrect `gilhari_service.config`
  - Invalid `.jdx` file syntax
  - Missing JDBC driver

**Problem**: `Database connection failed`
- **Solution**: Verify database URL in `.jdx` file
- **For Docker**: Use `host.docker.internal` instead of `localhost` for host databases
- **Example**: `jdbc:mysql://host.docker.internal:3306/mydb`

**Problem**: `ClassNotFoundException` for container classes
- **Solution**: Verify `jdx_persistent_classes_location` points to correct directory
- **Check**: `.class` files exist in `bin/` directory with correct package structure

**Problem**: `JDBC Driver not found`
- **Solution**: 
  - Verify JDBC driver path in `gilhari_service.config`
  - Ensure driver JAR is in `config/` directory
  - Check that Dockerfile includes: `ADD config ./config`

#### ORM Specification Issues

**Problem**: `Syntax error in .jdx file`
- **Solution**: Check for:
  - Missing semicolons (`;`) at end of class definitions
  - Typos in keywords (CLASS, VIRTUAL_ATTRIB, PRIMARY_KEY, etc.)
  - Incorrect attribute types
  - Mismatched class names between `.jdx` and `.java` files

**Problem**: Schema not created or tables missing
- **Solution**: 
  - Set `"jdx_force_create_schema": "true"` in config (for development)
  - Check `jdx_debug_level` (set to 3 to see SQL statements)
  - Review container logs for SQL errors

**Problem**: Relationship attributes not saved
- **Solution**: 
  - Verify RELATIONSHIP specification in `.jdx` file
  - Check BYVALUE vs BYREFERENCE configuration
  - Ensure child classes have correct REFERENCE_KEY definitions
  - For arrays, verify COLLECTION_CLASS is defined

#### REST API Issues

**Problem**: 404 Not Found for API endpoints
- **Solution**: 
  - Verify service is running: `docker ps`
  - Check correct port mapping
  - Use correct class name in URL (check `classnames_map` file)
  - Ensure base path is `/gilhari/v1/`

**Problem**: Cannot create objects with relationships
- **Solution**: 
  - Include complete nested object structure in POST body
  - Verify child objects have required primary keys
  - Check that parent-child linking attributes match (e.g., `aId`)

**Problem**: Path expressions not working
- **Solution**: 
  - Use `jdxObject` prefix: `jdxObject.aB.bInt>100`
  - URL-encode the filter parameter
  - Use `-G` and `--data-urlencode` with curl

**Problem**: Projections or follow operations failing
- **Solution**: 
  - Properly URL-encode `operationDetails` parameter
  - Use correct JSON array syntax
  - Set `deep=false` when using selective follow
  - Verify class and attribute names are correct

### Database-Specific Issues

#### SQLite

**Problem**: Database file not created
- **Solution**: Ensure path is writable: `./config/mydb.db`
- **Note**: SQLite creates file automatically if it doesn't exist

**Problem**: Database locked errors
- **Solution**: 
  - Only one write operation at a time with SQLite
  - Consider using PostgreSQL or MySQL for high concurrency

#### MySQL

**Problem**: `Authentication failed`
- **Solution**: 
  - Verify username and password in `.jdx` file
  - Check MySQL user has correct permissions
  - Ensure MySQL allows remote connections if not on localhost

**Problem**: `Unknown database`
- **Solution**: Create database first:
  ```sql
  CREATE DATABASE mydb;
  ```

**Problem**: `Public Key Retrieval is not allowed`
- **Solution**: Add to connection URL: `?allowPublicKeyRetrieval=true&useSSL=false`

#### PostgreSQL

**Problem**: `Connection refused`
- **Solution**: 
  - Verify PostgreSQL is running
  - Check `postgresql.conf` allows connections
  - Verify `pg_hba.conf` authentication settings

**Problem**: `Password authentication failed`
- **Solution**: 
  - Verify username/password in `.jdx` file
  - Check PostgreSQL user exists: `\du` in psql

### Best Practices

#### Development Environment

1. **Use `jdx_force_create_schema: true`** during development
   - Automatically recreates schema with each restart
   - Great for rapid iteration on object model
   - **Remember**: Set to `false` for production

2. **Set appropriate `jdx_debug_level`**
   - Level 3: Shows all SQL statements (recommended for development)
   - Level 5: Minimal logging (production)
   - Level 0: Maximum verbosity (troubleshooting)

3. **Test with curl scripts**
   - Create comprehensive test scripts
   - Include CRUD operations and edge cases
   - Log responses for verification

4. **Version control**
   - Include `src/`, `config/`, compilation scripts
   - Exclude `bin/` directory (generated files)
   - Include `.gitignore` for generated files and sensitive data

#### Production Deployment

1. **Database considerations**
   - Use production-grade databases (PostgreSQL, MySQL)
   - Don't use SQLite for high-concurrency scenarios
   - Set `jdx_force_create_schema: false`
   - Configure appropriate connection pooling

2. **Security**
   - Don't commit database passwords to version control
   - Use environment variables or secrets management
   - Restrict database user permissions (principle of least privilege)
   - Consider using encrypted connections (SSL/TLS)

3. **Performance**
   - Configure caching in `.jdx` file for frequently accessed data
   - Use indexes on frequently queried attributes
   - Monitor database query performance
   - Consider using projections to limit data transfer

4. **Monitoring**
   - Set up health check endpoints: `/gilhari/v1/health/check`
   - Monitor Docker container logs
   - Track API response times
   - Monitor database connections

#### Schema Management

1. **Initial development**
   - Use `jdx_force_create_schema: true`
   - Iterate quickly on object model
   - Test with sample data

2. **Schema changes**
   - For production, consider migration strategies
   - Back up data before schema changes
   - Test migrations in staging environment

3. **Multi-environment**
   - Use different `.jdx` files or configurations per environment
   - Separate development, staging, and production databases
   - Document schema versions

### Getting Help

#### Documentation Resources

- **JDX User Manual**: Comprehensive ORM documentation (included in Gilhari SDK)
- **Gilhari SDK**: Full SDK with examples and libraries from [https://softwaretree.com](https://softwaretree.com)
- **[Database Configuration Guide](../examples/JDX_DATABASE_JDBC_DRIVER_Specification_Guide.md)** - Database-specific configurations
- **[operationDetails Documentation](../examples/operationDetails_doc.md)** - Advanced query capabilities
- **Example Repositories**: Working examples on GitHub

#### Support Channels

- **GitHub Issues**: Report issues in specific example repositories
- **ORMCP Documentation**: [https://github.com/softwaretree/ormcp-docs](https://github.com/softwaretree/ormcp-docs)
- **Email Support**: [gilhari_support@softwaretree.com](mailto:gilhari_support@softwaretree.com)
- **Website**: [https://www.softwaretree.com](https://www.softwaretree.com)

---

## Quick Reference

### Essential File Checklist

- [ ] Container domain model classes (.java) in `src/`
- [ ] Compiled classes (.class) in `bin/`
- [ ] ORM specification (.jdx) in `config/`
- [ ] JDBC driver JAR in `config/` (if not using default SQLite)
- [ ] Service configuration (gilhari_service.config) in root
- [ ] Dockerfile in root
- [ ] Compilation script (compile.cmd/.sh)
- [ ] Build script (build.cmd/.sh)
- [ ] Run script (run_docker_app.cmd/.sh)
- [ ] Optional: classnames_map file in `config/`
- [ ] Optional: curl test scripts

### Common Commands

**Compilation:**
```bash
# Windows
compile.cmd

# Linux/Mac
./compile.sh
```

**Build Docker Image:**
```bash
# Windows
build.cmd

# Linux/Mac
./build.sh
```

**Run Service:**
```bash
# Windows
run_docker_app.cmd

# Linux/Mac
./run_docker_app.sh
```

**Docker Management:**
```bash
# List running containers
docker ps

# View logs
docker logs <container-id>

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# Shell into container
docker exec -it <container-id> bash
```

**API Testing:**
```bash
# Health check
curl -X GET "http://localhost:80/gilhari/v1/health/check"

# Get object model summary
curl -X GET "http://localhost:80/gilhari/v1/getObjectModelSummary/now"

# Query all objects
curl -X GET "http://localhost:80/gilhari/v1/User"

# Create object
curl -X POST "http://localhost:80/gilhari/v1/User" \
  -H "Content-Type: application/json" \
  -d '{"entity": {...}}'

# Query with filter
curl -X GET "http://localhost:80/gilhari/v1/User?filter=age>30"

# Delete with filter
curl -X DELETE "http://localhost:80/gilhari/v1/User?filter=id=123"
```

### Key Concepts Summary

**Container Domain Model Classes**
- Extend `JDX_JSONObject`
- Require only two constructors
- Declare relationship attributes as instance variables
- No getters/setters needed

**ORM Specification (.jdx)**
- Maps JSON objects to database tables
- Uses VIRTUAL_ATTRIB for JSON properties
- Defines relationships with RELATIONSHIP keyword
- Configures database connection and JDBC driver

**Relationships**
- BYVALUE: Containment (cascading deletes)
- BYREFERENCE: Loose coupling
- One-to-one: Single object reference
- One-to-many: Array/collection reference

**Service Configuration**
- Points to .jdx file
- Specifies JDBC driver location
- Configures debug level
- Sets port and other runtime parameters

**Docker Setup**
- Extends base Gilhari image
- Adds compiled classes and config
- Exposes service port
- Runs Gilhari REST server

---

## Conclusion

You now have a complete understanding of setting up Gilhari microservices. The key components are:

1. **Container domain model classes** - Simple Java shell classes
2. **ORM specification (.jdx)** - Declarative mapping configuration
3. **Service configuration** - Runtime parameters
4. **Dockerfile** - Container image definition

With these components properly configured, Gilhari handles all the REST API generation, CRUD operations, and database management automatically.

**Next Steps:**
- Study the example repositories for working implementations
- Start with `gilhari_example1` for basic patterns
- Progress to `gilhari_relationships_example` for relationships
- Explore other examples for advanced patterns
- Refer to JDX User Manual for comprehensive ORM features

**Remember:** The examples include pre-compiled classes for immediate use, but you'll need the Gilhari SDK to modify or create your own microservices.

---

**Document Version:** 1.0  
**Last Updated:** 2025  
**Copyright:** Software Tree  

For the latest documentation and updates, visit [https://www.softwaretree.com](https://www.softwaretree.com)

## Overview

Gilhari is a Docker-compatible microservice framework that provides RESTful Object-Relational Mapping (ORM) functionality for JSON objects with any relational database. Setting up a Gilhari microservice involves creating several key components that work together to enable JSON object persistence.

**What Gilhari automates:**
- RESTful API endpoints (POST, GET, PUT, DELETE, etc.)
- JSON CRUD operations
- Database schema creation and management
- Object-relational mapping
- Transaction management

**What you need to provide:**
- Container domain model classes (simple Java shell classes)
- Declarative ORM specification (.jdx file)
- Service configuration
- Docker configuration

---

## Prerequisites

### Required Software

1. **Gilhari SDK** 
   - Download from [https://softwaretree.com](https://softwaretree.com)
   - Set `JX_HOME` environment variable to the SDK installation directory
   - Contains JDX libraries and base classes needed for compilation

2. **Java Development Kit (JDK 1.8+)**
   - Required for compiling container domain model classes
   - Verify installation: `java -version` and `javac -version`

3. **Docker**
   - Required for building and running the microservice
   - Verify installation: `docker --version`
   - Pull base image: `docker pull softwaretree/gilhari`

### Optional Software

- **Git** - For cloning example repositories
- **cURL** or **Postman** - For testing REST APIs
- **Your preferred IDE** - VS Code, IntelliJ IDEA, Eclipse, etc.

---

## Project Structure

A typical Gilhari microservice project has the following structure:

```
my_gilhari_service/
├── src/                              # Source files
│   └── com/mycompany/myapp/model/    # Container domain model classes
│       ├── MyClass1.java
│       ├── MyClass2.java
│       └── ...
├── bin/                              # Compiled .class files
│   └── com/mycompany/myapp/model/
│       ├── MyClass1.class
│       ├── MyClass2.class
│       └── ...
├── config/                           # Configuration files
│   ├── my_service.jdx               # ORM specification
│   ├── classnames_map.js            # Class name mappings (optional)
│   └── [jdbc-driver.jar]            # JDBC driver (recommended location)
├── Dockerfile                        # Docker image definition
├── gilhari_service.config           # Service configuration
├── compile.cmd / .sh                # Compilation script
├── build.cmd / .sh                  # Docker build script
├── run_docker_app.cmd / .sh         # Docker run script
├── sources.txt                      # List of source files to compile
└── curlCommands.cmd / .sh           # API testing scripts (optional)
```

**Key directories:**
- **src/** - Contains Java source files for container domain model classes
- **bin/** - Contains compiled .class files (generated from src/)
- **config/** - Contains ORM specification, JDBC driver, and optional mappings

---

## Setup Components

### 1. Container Domain Model Classes (Java)

Container domain model classes are simple Java "shell" classes that represent your JSON object types. They serve as containers for handling the persistence of domain-specific JSON objects.

#### Characteristics

- Extend `JDX_JSONObject` base class
- Require only two constructors (no-arg and JSONObject)
- No need for getter/setter methods
- Minimal code - most processing handled by the superclass
- For relationship attributes, declare them as instance variables (used only for ORM specification)

#### Example 1: Simple Class (User)

From `gilhari_example1`:

```java
package com.softwaretree.gilhariexample1.model;

import org.json.JSONException;
import org.json.JSONObject;
import com.softwaretree.jdx.JDX_JSONObject;

/**
 * Container class for User objects.
 * Only needs two constructors - all processing handled by JDX_JSONObject superclass.
 */
public class User extends JDX_JSONObject {

    public User() {
        super();
    }

    public User(JSONObject jsonObject) throws JSONException {
        super(jsonObject);
    }
}
```

**Corresponding JSON object:**
```json
{
  "id": 39,
  "name": "John39",
  "age": 39,
  "city": "San Francisco",
  "state": "CA"
}
```

#### Example 2: Class with Relationships (A, B, C)

From `gilhari_relationships_example`:

**Parent class A (contains B object and C array):**
```java
package com.softwaretree.jdxjson2example.model;

import org.json.JSONException;
import org.json.JSONObject;
import com.softwaretree.jdx.JDX_JSONObject;

/**
 * Container class for A objects with relationships.
 * Declares relationship attributes (aB and aCs) for ORM specification.
 * No setters/getters needed.
 */
public class A extends JDX_JSONObject {

    public A() {
        super();
    }

    public A(JSONObject jsonObject) throws JSONException {
        super(jsonObject);
    }
    
    // Relationship attributes declared for ORM specification only
    // No need to define setters/getters
    public B aB;        // One-to-one relationship
    public C[] aCs;     // One-to-many relationship (array)
}
```

**Child class B:**
```java
package com.softwaretree.jdxjson2example.model;

import org.json.JSONException;
import org.json.JSONObject;
import com.softwaretree.jdx.JDX_JSONObject;

public class B extends JDX_JSONObject {

    public B() {
        super();
    }

    public B(JSONObject jsonObject) throws JSONException {
        super(jsonObject);
    }
}
```

**Child class C:**
```java
package com.softwaretree.jdxjson2example.model;

import org.json.JSONException;
import org.json.JSONObject;
import com.softwaretree.jdx.JDX_JSONObject;

public class C extends JDX_JSONObject {

    public C() {
        super();
    }

    public C(JSONObject jsonObject) throws JSONException {
        super(jsonObject);
    }
}
```

**Corresponding JSON object with relationships:**
```json
{
  "aId": 1,
  "aString": "aString_1",
  "aBoolean": true,
  "aFloat": 1.1,
  "aDate": 347184000001,
  "aB": {
    "bId": 100,
    "aId": 1,
    "bInt": 100,
    "bString": "bString_1"
  },
  "aCs": [
    {
      "cId": 1000,
      "aId": 1,
      "cInt": 100,
      "cString": "cString_1"
    },
    {
      "cId": 2000,
      "aId": 1,
      "cInt": 200,
      "cString": "cString_2"
    }
  ]
}
```

#### Key Points

- **Location**: Place source files in `src/` with appropriate package structure
- **Compilation**: Compile to `bin/` directory (see [Compilation](#compilation-and-build))
- **Dependencies**: Requires JDX libraries from Gilhari SDK (set via JX_HOME)
- **Naming**: Use meaningful class names that represent your domain objects
- **Relationships**: For classes with relationships, declare relationship attributes as instance variables

---

### 2. ORM Specification File (.jdx)

The `.jdx` file is a declarative Object-Relational Mapping specification that defines how your JSON objects map to database tables. This file is the heart of the Gilhari configuration.

#### File Location

- **Required location**: `config/` directory
- **Naming convention**: `<service_name>.jdx`
- **Referenced in**: `gilhari_service.config` file

#### File Structure

Every `.jdx` file has the following structure:

```
1. Database connection specification (JDX_DATABASE)
2. JDBC driver specification (JDBC_DRIVER)
3. Optional object model overview
4. Class mappings with attributes and relationships
```

#### Example 1: Simple Mapping (User)

From `gilhari_example1/config/gilhari_example1.jdx`:

```
JDX_DATABASE JDX:jdbc:sqlite:./config/gilhari_example1.db;USER=sa;PASSWORD=sa;JDX_DBTYPE=SQLITE;DEBUG_LEVEL=5
JDBC_DRIVER org.sqlite.JDBC

// Optional: Describe your object model
OBJECT_MODEL_OVERVIEW This is a simple object model with only User type of objects
;

// Class mapping for User
CLASS com.softwaretree.gilhariexample1.model.User TABLE USER

  // First declare all persistent JSON properties using VIRTUAL_ATTRIB
  VIRTUAL_ATTRIB id ATTRIB_TYPE int
  VIRTUAL_ATTRIB name ATTRIB_TYPE java.lang.String
  VIRTUAL_ATTRIB age ATTRIB_TYPE int
  VIRTUAL_ATTRIB city ATTRIB_TYPE java.lang.String
  VIRTUAL_ATTRIB state ATTRIB_TYPE java.lang.String

  // Define primary key
  PRIMARY_KEY id

  // Optional: Enable auto-increment for SQLite
  // SQLMAP FOR id SQLTYPE 'INTEGER PRIMARY KEY AUTOINCREMENT'
  // RDBMS_GENERATED id

  // Optional: Enable auto-increment for MySQL
  // SQLMAP FOR id COLUMN_NAME userId SQLTYPE 'INTEGER AUTO_INCREMENT'
  // RDBMS_GENERATED id
;
```

#### Example 2: Mapping with Relationships (A, B, C)

From `gilhari_relationships_example/config/gilhari_relationships_example.jdx`:

```
JDX_DATABASE JDX:jdbc:sqlite:./config/json_relationships_example.db;USER=sa;PASSWORD=sa;JDX_DBTYPE=SQLITE;DEBUG_LEVEL=5;
JDBC_DRIVER org.sqlite.JDBC

OBJECT_MODEL_OVERVIEW This object model describes one-to-one (between A and B) and one-to-many (between A and C) relationships

// Optional: Set package for all classes in this file
JDX_OBJECT_MODEL_PACKAGE com.softwaretree.jdxjson2example.model
;

// Parent class A with relationships
CLASS .A TABLE A
 
   // Optional: Configure caching for performance
   // CACHE MODE READONLY PRE_POPULATE 'aId>0'

   // Declare all persistent JSON properties
   VIRTUAL_ATTRIB aId ATTRIB_TYPE int
   VIRTUAL_ATTRIB aString ATTRIB_TYPE java.lang.String
   VIRTUAL_ATTRIB aBoolean ATTRIB_TYPE boolean
   VIRTUAL_ATTRIB aFloat ATTRIB_TYPE double
   VIRTUAL_ATTRIB aDate ATTRIB_TYPE long

   PRIMARY_KEY aId 
   
   // One-to-one relationship: A contains one B object
   RELATIONSHIP aB REFERENCES .B BYVALUE REFERENCED_KEY parentId WITH aId
   
   // One-to-many relationship: A contains array of C objects
   RELATIONSHIP aCs REFERENCES ArrayC BYVALUE WITH aId
;

// Child class B
CLASS .B TABLE B

   // Optional: Configure caching
   // CACHE MODE READONLY

   VIRTUAL_ATTRIB bId ATTRIB_TYPE int
   VIRTUAL_ATTRIB aId ATTRIB_TYPE int
   VIRTUAL_ATTRIB bInt ATTRIB_TYPE int
   VIRTUAL_ATTRIB bString ATTRIB_TYPE java.lang.String
   
   PRIMARY_KEY bId 
   REFERENCE_KEY parentId aId
;

// Child class C
CLASS .C TABLE C

   VIRTUAL_ATTRIB cId ATTRIB_TYPE int
   VIRTUAL_ATTRIB aId ATTRIB_TYPE int
   VIRTUAL_ATTRIB cInt ATTRIB_TYPE int
   VIRTUAL_ATTRIB cString ATTRIB_TYPE java.lang.String
   
   PRIMARY_KEY cId 
;

// Collection class for array of C objects
COLLECTION_CLASS ArrayC COLLECTION_TYPE ARRAY ELEMENT_CLASS .C
    PRIMARY_KEY aId 
;
```

#### Key Specifications

**JDX_DATABASE Format:**
```
JDX:jdbc:<db_type>://<host>:<port>/<database>;USER=<username>;PASSWORD=<password>;JDX_DBTYPE=<type>;DEBUG_LEVEL=<level>
```

**Database Types:**
- SQLite: `jdbc:sqlite:./config/mydb.db`
- MySQL: `jdbc:mysql://localhost:3306/mydb`
- PostgreSQL: `jdbc:postgresql://localhost:5432/mydb`
- MS SQL Server: `jdbc:sqlserver://localhost:1433;database=mydb`

See the [Database Configuration Guide](../examples/JDX_DATABASE_JDBC_DRIVER_Specification_Guide.md) for comprehensive database configuration examples.

**VIRTUAL_ATTRIB Types:**
- Primitives: `int`, `long`, `float`, `double`, `boolean`
- Objects: `java.lang.String`, `java.util.Date`
- Note: JSON properties are declared as virtual attributes

**Primary Key:**
```
PRIMARY_KEY attribute1 [attribute2 ...]
```

**Relationships:**
```
RELATIONSHIP <attributeName> REFERENCES <className> BYVALUE [OPTIONS]
```

---

### 3. Service Configuration File

The `gilhari_service.config` file (located at project root) specifies runtime parameters for your Gilhari microservice.

#### Example 1: Basic Configuration

From `gilhari_example1/gilhari_service.config`:

```json
{
  "gilhari_microservice_name": "gilhari_example1",
  "jdx_orm_spec_file": "./config/gilhari_example1.jdx",
  "jdbc_driver_path": "/node/node_modules/jdxnode/external_libs/sqlite-jdbc-3.50.3.0.jar",
  "jdx_debug_level": 3,
  "jdx_force_create_schema": "true",
  "jdx_persistent_classes_location": "./bin",
  "classnames_map_file": "config/classnames_map_example.js",
  "gilhari_rest_server_port": 8081
}
```

#### Example 2: Relationships Configuration

From `gilhari_relationships_example/gilhari_service.config`:

```json
{
  "gilhari_microservice_name": "gilhari_relationships_example",
  "jdx_orm_spec_file": "./config/gilhari_relationships_example.jdx",
  "jdbc_driver_path": "/node/node_modules/jdxnode/external_libs/sqlite-jdbc-3.50.3.0.jar",
  "jdx_debug_level": 5,
  "jdx_force_create_schema": "true",
  "jdx_persistent_classes_location": "./bin",
  "classnames_map_file": "config/classnames_map_example.js",
  "gilhari_rest_server_port": 8081
}
```

#### Configuration Parameters

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `gilhari_microservice_name` | Identifies the microservice (logged at startup) | - | Optional but recommended |
| `jdx_orm_spec_file` | Path to ORM specification (.jdx) file | - | **Required** |
| `jdbc_driver_path` | Path to JDBC driver JAR file | - | **Required** (default SQLite included) |
| `jdx_debug_level` | Debug verbosity (0=most, 5=least) | 5 | Level 3 shows all SQL statements |
| `jdx_force_create_schema` | Recreate schema on each startup | false | Use `true` for development |
| `jdx_persistent_classes_location` | Root path to compiled .class files | - | **Required** (directory or JAR) |
| `classnames_map_file` | Optional simplified class name mappings | - | Optional |
| `gilhari_rest_server_port` | Service port inside container | 8081 | Map to different port with Docker |

#### JDBC Driver Location

**Recommended:** Place JDBC driver JARs in the `config/` directory alongside your `.jdx` file.

**Why?**
- Keeps configuration files together
- Easy to include in Docker image
- Simplifies path references

**For external databases (MySQL, PostgreSQL, etc.):**
1. Download the appropriate JDBC driver JAR
2. Place it in `config/` directory
3. Update `jdbc_driver_path` in `gilhari_service.config`:
   ```json
   "jdbc_driver_path": "./config/mysql-connector-java-8.0.33.jar"
   ```

---

### 4. Class Names Mapping File

An optional JSON file that maps fully-qualified container class names to simpler names for use in REST URLs.

#### Purpose

Simplifies REST API URLs by removing package names.

**Without mapping:**
```
POST /gilhari/v1/com.softwaretree.gilhariexample1.model.User
```

**With mapping:**
```
POST /gilhari/v1/User
```

#### Example

From `config/classnames_map_example.js`:

```javascript
{
    "User": "com.softwaretree.gilhariexample1.model.User",
    "A": "com.softwaretree.jdxjson2example.model.A",
    "B": "com.softwaretree.jdxjson2example.model.B",
    "C": "com.softwaretree.jdxjson2example.model.C"
}
```

#### Configuration

Reference in `gilhari_service.config`:
```json
"classnames_map_file": "config/classnames_map_example.js"
```

**Note:** This is optional. If not provided, use fully-qualified class names in REST URLs.

---

### 5. Dockerfile

The Dockerfile builds your application-specific Gilhari microservice image from the base Gilhari image.

#### Example 1: Basic Dockerfile

From `gilhari_example1/Dockerfile`:

```dockerfile
# Create docker image for RESTful server providing JSON object persistence
# Starting with base Gilhari image that includes jdxnode_rest_server 
# and required environment variables (JX_HOME, NODE_PATH)

FROM softwaretree/gilhari
WORKDIR /opt/gilhari_example1

# Add compiled classes, configuration files, and service config
ADD bin ./bin
ADD config ./config
ADD gilhari_service.config .

# Expose the service port
EXPOSE 8081 

# Start the Gilhari REST server with the service configuration
CMD ["node", "/node/node_modules/gilhari_rest_server/gilhari_rest_server.js", "gilhari_service.config"]
```

#### Example 2: Relationships Dockerfile

From `gilhari_relationships_example/Dockerfile`:

```dockerfile
FROM softwaretree/gilhari
WORKDIR /opt/gilhari_relationships_example

ADD bin ./bin
ADD config ./config
ADD gilhari_service.config .

EXPOSE 8081 
CMD ["node", "/node/node_modules/gilhari_rest_server/gilhari_rest_server.js", "gilhari_service.config"]
```

#### Dockerfile Components

**FROM softwaretree/gilhari**
- Base image with JDX, Node.js, and Gilhari REST server pre-installed
- Includes environment variables (JX_HOME, NODE_PATH)
- Contains default SQLite JDBC driver

**WORKDIR /opt/<your_service_name>**
- Sets working directory inside container
- All subsequent paths are relative to this directory

**ADD commands**
- `ADD bin ./bin` - Copies compiled .class files
- `ADD config ./config` - Copies ORM spec, JDBC driver, and mappings
- `ADD gilhari_service.config .` - Copies service configuration to root

**EXPOSE 8081**
- Documents the port used by the service inside container
- Actual external port mapping done in `docker run` command

**CMD**
- Starts the Gilhari REST server
- Passes `gilhari_service.config` as argument
- Server reads config and initializes the microservice

#### Important Notes

1. **Base Image**: Always pull the latest base image: `docker pull softwaretree/gilhari`
2. **Working Directory**: Use a unique name for your service
3. **Port Mapping**: The EXPOSE port (8081) is mapped to an external port when running:
   ```bash
   docker run -p 80:8081 my_service
   ```
4. **File Paths**: All paths in `gilhari_service.config` are relative to WORKDIR

---

## Relationship Mapping

Gilhari supports various relationship patterns using BYVALUE (containment) and BYREFERENCE semantics.

### BYVALUE Relationships (Containment)

With BYVALUE, child objects are "contained" within the parent object:
- Deleting parent deletes children (cascading delete)
- Children typically managed through parent
- Represents strong ownership

#### One-to-One Relationship

**Parent A contains one B object:**

**Container class A:**
```java
public class A extends JDX_JSONObject {
    public A() { super(); }
    public A(JSONObject jsonObject) throws JSONException { super(jsonObject); }
    
    public B aB;  // One-to-one relationship attribute
}
```

**ORM Specification:**
```
CLASS .A TABLE A
   VIRTUAL_ATTRIB aId ATTRIB_TYPE int
   PRIMARY_KEY aId
   
   // One-to-one: aB references B class
   RELATIONSHIP aB REFERENCES .B BYVALUE REFERENCED_KEY parentId WITH aId
;

CLASS .B TABLE B
   VIRTUAL_ATTRIB bId ATTRIB_TYPE int
   VIRTUAL_ATTRIB aId ATTRIB_TYPE int
   VIRTUAL_ATTRIB bInt ATTRIB_TYPE int
   
   PRIMARY_KEY bId
   REFERENCE_KEY parentId aId
;
```

**JSON Structure:**
```json
{
  "aId": 1,
  "aB": {
    "bId": 100,
    "aId": 1,
    "bInt": 100
  }
}
```

#### One-to-Many Relationship

**Parent A contains array of C objects:**

**Container class A:**
```java
public class A extends JDX_JSONObject {
    public A() { super(); }
    public A(JSONObject jsonObject) throws JSONException { super(jsonObject); }
    
    public C[] aCs;  // One-to-many relationship attribute (array)
}
```

**ORM Specification:**
```
CLASS .A TABLE A
   VIRTUAL_ATTRIB aId ATTRIB_TYPE int
   PRIMARY_KEY aId
   
   // One-to-many: aCs references ArrayC collection
   RELATIONSHIP aCs REFERENCES ArrayC BYVALUE WITH aId
;

CLASS .C TABLE C
   VIRTUAL_ATTRIB cId ATTRIB_TYPE int
   VIRTUAL_ATTRIB aId ATTRIB_TYPE int
   VIRTUAL_ATTRIB cInt ATTRIB_TYPE int
   
   PRIMARY_KEY cId
;

// Collection class for array of C objects
COLLECTION_CLASS ArrayC COLLECTION_TYPE ARRAY ELEMENT_CLASS .C
    PRIMARY_KEY aId
;
```

**JSON Structure:**
```json
{
  "aId": 1,
  "aCs": [
    {
      "cId": 1000,
      "aId": 1,
      "cInt": 100
    },
    {
      "cId": 2000,
      "aId": 1,
      "cInt": 200
    }
  ]
}
```

### Relationship Keywords

**BYVALUE**
- Child contained within parent
- Cascading delete behavior
- Strong ownership semantics

**REFERENCED_KEY**
- Specifies the reference key in child that points to parent
- Used with BYVALUE relationships

**WITH**
- Specifies the parent attribute used for linking
- Typically the parent's primary key

**COLLECTION_CLASS**
- Defines collection types (ARRAY, LIST, etc.)
- Required for one-to-many relationships
- Specifies element class and primary key

### Advanced Relationship Features

#### Path Expressions

Query parent objects based on child attributes:
```bash
# Get all A objects where contained B object has bInt > 100
curl -X GET "http://localhost:80/gilhari/v1/A?filter=jdxObject.aB.bInt>100"
```

#### Shallow vs Deep Queries

**Deep (default)** - includes all relationships:
```bash
curl -X GET "http://localhost:80/gilhari/v1/A"
```

**Shallow** - excludes relationships:
```bash
curl -X GET "http://localhost:80/gilhari/v1/A?deep=false"
```

**Selective follow** - include specific relationships only:
```bash
curl -G "http://localhost:80/gilhari/v1/A?deep=false" \
  --data-urlencode 'operationDetails=[{"opType": "follow", "references": ["A", "aB"]}]'
```

#### Projections

Select specific attributes only:
```bash
curl -G "http://localhost:80/gilhari/v1/A?deep=false" \
  --data-urlencode 'operationDetails=[{"opType": "projections", "projectionsDetails": [{"type": "A", "attribs": ["aId", "aString"]}]}]'
```

---

## Compilation and Build

### Running Shell Scripts on Mac/Linux

After cloning an example repository or extracting the SDK, shell scripts may not have execute permissions.

**If you encounter permission errors:**
```bash
zsh: permission denied: ./build.sh
```

**Solution 1: Add execute permissions**
```bash
chmod +x build.sh compile.sh run_docker_app.sh
./build.sh
```

**Solution 2: Run with sh directly**
```bash
sh build.sh
sh compile.sh
sh run_docker_app.sh
```

**Why this happens:** Shell script execute permissions may not be preserved when:
- Extracting from ZIP/JAR archives
- Cloning on Windows and checking out on Mac/Linux
- Downloading source distributions

**Note:** We've configured our Git repositories to preserve execute permissions, but they may still be lost in certain distribution methods.


### Step 1: Prepare Source Files

Create `sources.txt` listing all container class source files:

```
src/com/softwaretree/gilhariexample1/model/User.java
```

For relationships example:
```
src/com/softwaretree/jdxjson2example/model/A.java
src/com/softwaretree/jdxjson2example/model/B.java
src/com/softwaretree/jdxjson2example/model/C.java
```

### Step 2: Create Compilation Script

**Windows (compile.cmd):**
```batch
@echo off
REM Compile container domain model classes targeting JDK 1.8

set CLASSPATH=%JX_HOME%\JDXAndroid\libs\jdxjson-2.0.jar;%JX_HOME%\JDXAndroid\libs\json-20090211.jar

javac -source 1.8 -target 1.8 -d bin @sources.txt

echo Compilation complete. Class files are in bin/ directory.
```

**Linux/Mac (compile.sh):**
```bash
#!/bin/bash
# Compile container domain model classes targeting JDK 1.8

export CLASSPATH=$JX_HOME/JDXAndroid/libs/jdxjson-2.0.jar:$JX_HOME/JDXAndroid/libs/json-20090211.jar

javac -source 1.8 -target 1.8 -d bin @sources.txt

echo "Compilation complete. Class files are in bin/ directory."
```

### Step 3: Compile

```bash
# Windows
compile.cmd

# Linux/Mac
chmod +x compile.sh
./compile.sh
```

**Requirements:**
- `JX_HOME` environment variable must be set
- JDK 1.8+ must be installed
- Creates .class files in `bin/` directory

### Step 4: Build Docker Image

**Windows (build.cmd):**
```batch
@echo off
docker build -t gilhari_example1:1.0 .
echo Docker image built: gilhari_example1:1.0
```

**Linux/Mac (build.sh):**
```bash
#!/bin/bash
docker build -t gilhari_example1:1.0 .
echo "Docker image built: gilhari_example1:1.0"
```

Run:
```bash
# Windows
build.cmd

# Linux/Mac
chmod +x build.sh
./build.sh
```

### Step 5: Run Docker Container

**Windows (run_docker_app.cmd):**
```batch
@echo off
docker run -d -p 80:8081 --name gilhari_example1 gilhari_example1:1.0
echo Service running at http://localhost:80
```

**Linux/Mac (run_docker_app.sh):**
```bash
#!/bin/bash
docker run -d -p 80:8081 --name gilhari_example1 gilhari_example1:1.0
echo "Service running at http://localhost:80"
```

Run:
```bash
# Windows
run_docker_app.cmd

# Linux/Mac
chmod +x run_docker_app.sh
./run_docker_app.sh
```

**Port Mapping:**
- `-p 80:8081` maps container port 8081 to host port 80
- Access service at `http://localhost:80`
- Change `80` to use different external port (e.g., `-p 8080:8081`)

---

## Additional Examples

The Gilhari framework includes several comprehensive examples demonstrating various patterns and features.

**📚 For a complete guide to all examples with detailed descriptions, learning paths, and usage instructions, see the [Examples Directory](../examples/).**

Explore these ready-to-use example repositories:

### Available Examples

1. **[gilhari_example1](https://github.com/SoftwareTree/gilhari_example1)** - Basic user management ⭐ **Start here**
   - Single entity (User) with simple attributes
   - Basic CRUD operations
   - Filtering and aggregate queries
   - Perfect introduction to Gilhari

2. **[gilhari_simple_example](https://github.com/SoftwareTree/gilhari_simple_example)** - Simple Employee objects
   - Basic employee management
   - Simple domain model
   - Fundamental patterns

3. **[gilhari_onetomany_example](https://github.com/SoftwareTree/gilhari_onetomany_example)** - One-to-many relationships
   - Parent-child relationships
   - BYVALUE containment
   - Collection handling

4. **[gilhari_relationships_example](https://github.com/SoftwareTree/gilhari_relationships_example)** - Complex relationships
   - One-to-one relationships (A to B)
   - One-to-many relationships (A to C array)
   - BYVALUE containment semantics
   - Path expressions and advanced projections
   - Used extensively in this guide

5. **[gilhari_manytomany_example](https://github.com/SoftwareTree/gilhari_manytomany_example)** - Many-to-many relationships
   - Complex relationship patterns
   - Join table handling
   - Bidirectional relationships

6. **[gilhari_streaming_example](https://github.com/SoftwareTree/gilhari_streaming_example)** - Large result sets
   - Efficient streaming of large datasets
   - Memory-efficient processing
   - Pagination patterns

7. **[gilhari_autoincrement_example](https://github.com/SoftwareTree/gilhari_autoincrement_example)** - DBMS-generated keys
   - Auto-increment primary keys
   - Database-generated IDs
   - Different database configurations

### ORMCP Integration Examples

For AI-powered database interactions using ORMCP Server with Gilhari:
- **ORMCP Documentation**: [https://github.com/softwaretree/ormcp-docs](https://github.com/softwaretree/ormcp-docs)
- **ORMCP Examples**: [https://github.com/softwaretree/ormcp-docs#examples](https://github.com/softwaretree/ormcp-docs#examples)

**Note:** All examples include pre-compiled classes for immediate use. Download, build with Docker, and run. The Gilhari SDK is only needed if you want to modify the object models or create your own microservices.

---