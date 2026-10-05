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
- [Quick Reference](#quick-reference)
- [Conclusion](#conclusion)

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

> **Tip:** For an existing database, [ORM_Skyway](https://github.com/SoftwareTree/orm_skyway_automation) generates all of these — classes, ORM specification, service configuration and Dockerfile — from the database schema, builds the image, and creates scripts to run it.

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

A typical Gilhari microservice project has the following structure (the same layout is used by the [example repositories](../examples/) and by the projects that [ORM_Skyway](https://github.com/SoftwareTree/orm_skyway_automation) generates):

```
my_gilhari_service/
├── src/                                 # Source files
│   └── com/mycompany/myapp/model/       # Container domain model classes
│       ├── MyClass1.java
│       ├── MyClass2.java
│       └── ...
├── bin/                                 # Compiled .class files
│   └── com/mycompany/myapp/model/
│       ├── MyClass1.class
│       ├── MyClass2.class
│       └── ...
├── config/                              # Configuration files
│   ├── my_service.jdx                   # ORM specification
│   ├── classnames_map.json              # Class name mappings (optional)
│   └── [jdbc-driver.jar]                # JDBC driver (recommended location)
├── scripts/                             # Development scripts
│   └── compile.cmd / .sh                # Compiles the container domain model classes
├── gilhari/                             # Gilhari microservice (Docker) related files
│   ├── Dockerfile                       # Docker image definition
│   ├── gilhari_service.config           # Service configuration
│   ├── build.cmd / .sh                  # Builds the Docker image
│   ├── run_docker_app.cmd / .sh         # Runs the Docker container
│   └── curlCommands.cmd / .sh           # REST API testing scripts (optional)
└── .dockerignore                        # Keeps unneeded files out of the Docker build context
```

All scripts are run from the project root directory, for example `./gilhari/build.sh` (Linux/Mac) or `gilhari\build.cmd` (Windows). The compile script generates `sources.txt` (the list of Java source files to compile) each time it runs.

**Key directories:**
- **src/** - Contains Java source files for container domain model classes
- **bin/** - Contains compiled .class files (generated from src/)
- **config/** - Contains ORM specification, JDBC driver, and optional mappings
- **scripts/** - Contains the compile script
- **gilhari/** - Contains the Dockerfile, service configuration, and build, run and test scripts

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

See the [JDX_DATABASE and JDBC_DRIVER Specification Guide](https://github.com/SoftwareTree/jdx-docs/blob/main/guides/JDX_DATABASE_JDBC_DRIVER_Specification_Guide.md) for database configuration examples.

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

The `gilhari_service.config` file (located in the `gilhari/` directory) specifies runtime parameters for your Gilhari microservice. The Dockerfile copies it into the image's working directory, and the paths in it are paths inside the container, relative to that directory.

#### Example 1: Basic Configuration

From `gilhari_example1/gilhari/gilhari_service.config`:

```json
{
  "gilhari_microservice_name": "gilhari_example1",
  "jdx_orm_spec_file": "./config/gilhari_example1.jdx",
  "jdbc_driver_path": "/node/node_modules/jdxnode/external_libs/sqlite-jdbc-3.50.3.0.jar",
  "jdx_debug_level": 3,
  "jdx_force_create_schema": "true",
  "jdx_persistent_classes_location": "./bin",
  "classnames_map_file": "config/classnames_map_example.json",
  "gilhari_rest_server_port": 8081
}
```

#### Example 2: Relationships Configuration

From `gilhari_relationships_example/gilhari/gilhari_service.config`:

```json
{
  "gilhari_microservice_name": "gilhari_relationships_example",
  "jdx_orm_spec_file": "./config/gilhari_relationships_example.jdx",
  "jdbc_driver_path": "/node/node_modules/jdxnode/external_libs/sqlite-jdbc-3.50.3.0.jar",
  "jdx_debug_level": 5,
  "jdx_force_create_schema": "true",
  "jdx_persistent_classes_location": "./bin",
  "classnames_map_file": "config/classnames_map_example.json",
  "gilhari_rest_server_port": 8081
}
```

#### Configuration Parameters

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `gilhari_microservice_name` | Identifies the microservice (logged at startup) | - | Optional but recommended |
| `jdx_orm_spec_file` | Path to ORM specification (.jdx) file | - | **Required** |
| `jdbc_driver_path` | Path to JDBC driver JAR file | - | **Required** (default SQLite included) |
| `jdx_debug_level` | Debug verbosity (0=most, 5=least) | 5 | Level 3 shows all SQL statements; level 0 also logs connection details (passwords masked since JDX 5.29) |
| `jdx_force_create_schema` | Drop and recreate the mapped tables on each startup | false | Development only: **existing data in the mapped tables is lost**. Refused (with an error) when the database connection is read-only |
| `jdx_persistent_classes_location` | Root path to compiled .class files | - | **Required** (directory or JAR) |
| `classnames_map_file` | Optional simplified class name mappings | - | Optional |
| `gilhari_rest_server_port` | Service port inside container | 8081 | Map to different port with Docker |
| `db_username` | Database user; overrides `USER` in the ORM specification | - | Optional; see [Database Credentials](#database-credentials) |
| `db_password` | Database password; overrides `PASSWORD` in the ORM specification | - | Optional; see [Database Credentials](#database-credentials) |

#### Database Credentials

The database user and password can come from three places. The first one that is set (and not empty) wins:

1. The environment variables `JDX_DB_USER` and `JDX_DB_PASSWORD` of the running container (Gilhari 0.8.8+)
2. `db_username` / `db_password` in `gilhari_service.config`
3. `USER=` / `PASSWORD=` in the `JDX_DATABASE` line of the ORM specification (`.jdx`)

Files added to a Docker image (the `.jdx` file and `gilhari_service.config`) are part of the image: anyone who can pull the image can read credentials in them. For anything beyond local development, leave them out of these files and pass them when the container starts:

```bash
docker run -e JDX_DB_USER=myuser -e JDX_DB_PASSWORD=mypassword -p 80:8081 my_service:1.0
# or keep them in a file that is not committed or added to the image:
docker run --env-file db_credentials.env -p 80:8081 my_service:1.0
```

If the credentials are wrong, the service stops at start-up with a one-line message (`JDX ORM initialization failed: ...`) and exit status 1 (Gilhari 0.8.9+).

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

From `config/classnames_map_example.json`:

```json
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
"classnames_map_file": "config/classnames_map_example.json"
```

**Note:** This is optional. If not provided, use fully-qualified class names in REST URLs.

---

### 5. Dockerfile

The Dockerfile builds your application-specific Gilhari microservice image from the base Gilhari image.

#### Example 1: Basic Dockerfile

From `gilhari_example1/gilhari/Dockerfile`:

```dockerfile
# Create docker image for RESTful server providing JSON object persistence
# Starting with base Gilhari image that includes jdxnode_rest_server 
# and required environment variables (JX_HOME, NODE_PATH)

FROM softwaretree/gilhari
WORKDIR /opt/gilhari_example1

# The build context is the project root (see gilhari/build.cmd and build.sh:
# docker build -f gilhari/Dockerfile .), so the ADD source paths below are
# relative to the project root, not to this gilhari/ directory.
ADD bin ./bin
ADD config ./config
ADD gilhari/gilhari_service.config .

# Expose the service port
EXPOSE 8081 

# Start the Gilhari REST server with the service configuration
CMD ["node", "/node/node_modules/gilhari_rest_server/gilhari_rest_server.js", "gilhari_service.config"]
```

#### Example 2: Relationships Dockerfile

From `gilhari_relationships_example/gilhari/Dockerfile`:

```dockerfile
FROM softwaretree/gilhari
WORKDIR /opt/gilhari_relationships_example

ADD bin ./bin
ADD config ./config
ADD gilhari/gilhari_service.config .

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
- The Dockerfile is in `gilhari/`, but the Docker build context is the project root (`docker build -f gilhari/Dockerfile .`), so the source paths are relative to the project root
- `ADD bin ./bin` - Copies compiled .class files
- `ADD config ./config` - Copies ORM spec, JDBC driver, and mappings
- `ADD gilhari/gilhari_service.config .` - Copies the service configuration into the working directory

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

All scripts are run from the project root directory. They also work when started from another directory, because each one first switches to the project root.

### Running Shell Scripts on Mac/Linux

The example repositories keep the execute permission of their `.sh` files, but it can be lost when a project is extracted from a ZIP/JAR archive, copied from Windows, or downloaded as a source distribution.

**If you encounter permission errors:**
```bash
zsh: permission denied: ./gilhari/build.sh
```

**Solution 1: Add execute permissions**
```bash
chmod +x scripts/*.sh gilhari/*.sh
./gilhari/build.sh
```

**Solution 2: Run with sh directly**
```bash
sh scripts/compile.sh
sh gilhari/build.sh
sh gilhari/run_docker_app.sh
```

### Step 1: Compile the Container Classes

The compile script (`scripts/compile.cmd` / `scripts/compile.sh`) compiles every `.java` file under `src/` into `bin/`. It first writes the list of source files to `sources.txt`, so that file is generated each time and does not need to be maintained by hand or committed. It then runs `javac` with Java 8 compatibility (`--release 8` on JDK 9 and later), as required by the current Gilhari version.

**Linux/Mac (`scripts/compile.sh` from gilhari_example1, shortened):**
```bash
#!/bin/bash
cd "$(dirname "$0")/.."            # switch to the project root
JX_HOME="${JX_HOME:-$PWD/../..}"   # root directory of the Gilhari SDK
mkdir -p ./bin

# List all the .java files under src/ for javac
find src -name "*.java" | sort > sources.txt

# JDK 9 or higher: --release 8 produces Java 8 compatible classes
RELEASE_FLAG=""
if javac -help 2>&1 | grep -q -- "--release"; then
    RELEASE_FLAG="--release 8 -Xlint:-options"
fi

javac $RELEASE_FLAG -d ./bin -cp ".:$JX_HOME/libs/jxclasses.jar:$JX_HOME/external_libs/json-20240303.jar" @sources.txt
```

The Windows script (`scripts\compile.cmd`) does the same.

Run:
```bash
# Windows
scripts\compile.cmd

# Linux/Mac
./scripts/compile.sh
```

**Requirements:**
- `JX_HOME` set to the root directory of the Gilhari SDK. If it is not set, the scripts use `../..` (relative to the project root), which is the SDK root when the project is in the SDK's `examples` directory; they stop with a message if the SDK libraries are not found
- JDK 1.8+ installed
- Creates .class files in `bin/`

### Step 2: Build the Docker Image

The Dockerfile is in `gilhari/`, but the Docker build context is the project root, because the image needs `bin/` and `config/`.

**Linux/Mac (`gilhari/build.sh`):**
```bash
#!/bin/bash
cd "$(dirname "$0")/.."     # the build context must be the project root
docker build --platform linux/amd64 -f gilhari/Dockerfile -t gilhari_example1:1.0 .
docker images
```

**Windows (`gilhari\build.cmd`):**
```batch
@echo off
cd /d "%~dp0.."
docker build --platform linux/amd64 -f gilhari/Dockerfile -t gilhari_example1:1.0 .
docker images
```

`--platform linux/amd64` is used because the `softwaretree/gilhari` base image is published for linux/amd64 only (it runs under emulation on Apple Silicon). A `.dockerignore` file in the project root keeps files the image does not need (such as `src/`, `scripts/` and `.git`) out of the build context; Docker reads it from the build context, so it must stay in the project root.

Run:
```bash
# Windows
gilhari\build.cmd

# Linux/Mac
./gilhari/build.sh
```

### Step 3: Run the Docker Container

**Linux/Mac (`gilhari/run_docker_app.sh`)** and **Windows (`gilhari\run_docker_app.cmd`)** run:
```bash
docker run --platform linux/amd64 -p 80:8081 gilhari_example1:1.0
```

Run:
```bash
# Windows
gilhari\run_docker_app.cmd

# Linux/Mac
./gilhari/run_docker_app.sh
```

**Port Mapping:**
- `-p 80:8081` maps container port 8081 to host port 80
- Access service at `http://localhost:80`
- Change `80` to use different external port (e.g., `-p 8080:8081`)

### Step 4: Test with the curl Scripts (Optional)

```bash
# Windows
gilhari\curlCommands.cmd

# Linux/Mac
./gilhari/curlCommands.sh
```

The curl scripts first call `http://localhost:<port>/gilhari/v1/health/check` and stop with a message if the microservice is not responding. They take an optional port number as the first argument (default 80), for example `./gilhari/curlCommands.sh 8080`, and write the responses to `curl.log`.

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
- **ORMCP Examples**: [https://github.com/SoftwareTree/ormcp-docs/tree/main/examples](https://github.com/SoftwareTree/ormcp-docs/tree/main/examples)

**Note:** All examples include pre-compiled classes for immediate use. Download, build with Docker, and run. The Gilhari SDK is only needed if you want to modify the object models or create your own microservices.

---

---

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
- **Solution**: Stop the service that is using port 80, or change the port mapping in the `gilhari/run_docker_app` script
- **Example**: `-p 8080:8081` instead of `-p 80:8081`

#### Runtime Issues

**Problem**: Container starts but immediately exits
- **Solution**: Check container logs: `docker logs <container-id>`
- **Common causes**: 
  - Missing or incorrect `gilhari_service.config`
  - Invalid `.jdx` file syntax
  - Missing JDBC driver
  - Database not reachable or wrong credentials — the log then shows `JDX ORM initialization failed: <reason>` (Gilhari 0.8.9+)

**Problem**: `Database connection failed`
- **Solution**: Verify database URL in `.jdx` file, and the credentials (see [Database Credentials](#database-credentials))
- **For Docker**: Use `host.docker.internal` instead of `localhost` for host databases
- **Example**: `jdbc:mysql://host.docker.internal:3306/mydb`

**Problem**: `ClassNotFoundException` for container classes
- **Solution**: Verify `jdx_persistent_classes_location` points to correct directory
- **Check**: `.class` files exist in `bin/` directory with correct package structure

**Problem**: `JDBC Driver not found`
- **Solution**: 
  - Verify JDBC driver path in `gilhari/gilhari_service.config`
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

**Problem**: Understanding error status codes (Gilhari 0.8.9+)
- **400**: Invalid request parameter or body (for example `deep=maybe`, `maxObjects=abc`, a missing `entity`, malformed `operationDetails`)
- **404**: Unsupported API version in the URL (only `v1` exists); also the code for errors raised while executing a read (unknown class, invalid filter, database errors)
- **500**: Errors raised while executing a write
- The response body is a plain-text message describing the error

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
  - Verify username and password — in `.jdx`, `gilhari_service.config` or `JDX_DB_USER`/`JDX_DB_PASSWORD`; see [Database Credentials](#database-credentials) for which one is used
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
   - Level 0: Maximum verbosity (troubleshooting); passwords in the logged connection details are masked (JDX 5.29+)

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
   - Don't commit database passwords to version control, and don't put them in files added to the image
   - Pass them at container start with `JDX_DB_USER` / `JDX_DB_PASSWORD` (see [Database Credentials](#database-credentials)), or use secrets management
   - Restrict database user permissions (principle of least privilege)
   - Consider using encrypted connections (SSL/TLS)

3. **Performance**
   - Configure caching in `.jdx` file for frequently accessed data
   - Use indexes on frequently queried attributes
   - Monitor database query performance
   - Consider using projections to limit data transfer

4. **Monitoring**
   - Set up health check endpoints: `/gilhari/v1/health/check` (it reports whether the service is running; it does not query the database)
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
- **[Database Configuration Guide](https://github.com/SoftwareTree/jdx-docs/blob/main/guides/JDX_DATABASE_JDBC_DRIVER_Specification_Guide.md)** - Database-specific configurations (in jdx-docs)
- **[operationDetails Documentation](https://github.com/SoftwareTree/gilhari-docs/blob/main/reference/operationDetails.md)** - Advanced query capabilities (in gilhari-docs)
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
- [ ] Service configuration (`gilhari_service.config`) in `gilhari/`
- [ ] Dockerfile in `gilhari/`
- [ ] `.dockerignore` in the project root
- [ ] Compilation script (`scripts/compile.cmd` / `.sh`)
- [ ] Build script (`gilhari/build.cmd` / `.sh`)
- [ ] Run script (`gilhari/run_docker_app.cmd` / `.sh`)
- [ ] Optional: classnames_map file in `config/`
- [ ] Optional: curl test scripts

### Common Commands

**Compilation:**
```bash
# Windows
scripts\compile.cmd

# Linux/Mac
./scripts/compile.sh
```

**Build Docker Image:**
```bash
# Windows
gilhari\build.cmd

# Linux/Mac
./gilhari/build.sh
```

**Run Service:**
```bash
# Windows
gilhari\run_docker_app.cmd

# Linux/Mac
./gilhari/run_docker_app.sh
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

**Document Version:** 1.2  
**Last Updated:** 2026-10-04 (Gilhari 0.8.9, JDX 5.29; scripts/ and gilhari/ project layout)  
**Copyright:** Software Tree  

For the latest documentation and updates, visit [https://www.softwaretree.com](https://www.softwaretree.com)
