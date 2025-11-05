Copyright (c) 2025 Software Tree

# JDX_DATABASE and JDBC_DRIVER Configuration in the ORM specification (.jdx) file

This guide provides examples of how to specify the `JDX_DATABASE` and `JDBC_DRIVER` statements in the Object Relationa Mapping (ORM) specification `.jdx` file for different types of databases. Please make sure to substitute the placeholders (e.g., `<DatabaseName>`, `<UserName>`, etc.) with your actual database configurations.

These specifications go at the top of the mapping file before declaring the ORM specifications for the domain model object classes.

---

## Table of Contents

* [General Instructions](#general-instructions)
* [Database URL Formats](#database-url-formats)
* [JDX Configuration Examples](#jdx-configuration-examples)

  * [SQLite](#sqlite)
  * [MySQL](#mysql)
  * [PostgreSQL](#postgresql)
  * [Microsoft SQL Server](#microsoft-sql-server)
  * [Oracle](#oracle)

---

## General Instructions

* Replace `<DatabaseName>`, `<UserName>`, `<Password>`, `<JDX_DBTYPE>`, etc., with your actual database configurations.
* A particular database may require additional properties (e.g., `useSSL`, `integratedSecurity`)
* Ensure the appropriate JDBC driver for your database is available in the CLASSPATH.
* You can place the JDBC driver `.jar` file in the `config` directory alongside the `.jdx` mapping file.

---

## Database URL Formats

### Localhost

For databases running locally (e.g., MySQL, PostgreSQL), you can use the following format:

```
localhost:<PortNumber>
```

### Docker Container

If your database is outside of a Docker container where your app is running, use one of these formats:

```
host.docker.internal:<PortNumber>
<DatabaseServer_IP_Address>:<PortNumber>
```

* In Docker, `host.docker.internal` allows access to the host machine.
* `<DatabaseServer_IP_Address>` is the absolute IP address of the machine hosting the database server.


### Cloud Database Server

For databases hosted in the cloud, use the following format:

```
<DatabaseServer_Cloud_IP_Address>:<PortNumber>
```

### Windows 10: Get IP Address for Local Database

To get the IP address of your machine in Windows 10:

1. Open Command Prompt and run: `ipconfig /all`
2. Look for the IPv4 Address under the Ethernet adapter (e.g., `174.18.38.81`).

Use this address as `<DatabaseServer_IP_Address>` for local databases.

---

## JDX Configuration Examples

Below are examples of how to specify `JDX_DATABASE` and `JDBC_DRIVER` for different databases.

---

### SQLite

```properties
// SQLite (Local Database File)
JDX_DATABASE JDX:jdbc:sqlite:./config/<DatabaseFilename>;USER=sa;PASSWORD=sa;JDX_DBTYPE=SQLITE;DEBUG_LEVEL=5
JDBC_DRIVER org.sqlite.JDBC
```

---

### MySQL

```properties
// MySQL (Local)
JDX_DATABASE JDX:jdbc:mysql://localhost:3306/<DatabaseName>?useSSL=false;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=MYSQL;DEBUG_LEVEL=5

// MySQL (To access from within a Docker Container)
JDX_DATABASE JDX:jdbc:mysql://host.docker.internal:3306/JDXTestDB?useSSL=false;USER=dperiwal;PASSWORD=secretOne;JDX_DBTYPE=MYSQL;DEBUG_LEVEL=5

// MySQL (Local or Remote Server)
JDX_DATABASE JDX:jdbc:mysql://<MySQL_IP_Address>:3306/JDXTestDB?useSSL=false;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=MYSQL;DEBUG_LEVEL=5

// MySQL JDBC Driver
JDBC_DRIVER com.mysql.cj.jdbc.Driver
```

---

### PostgreSQL

```properties
// PostgreSQL (Local)
JDX_DATABASE JDX:jdbc:postgresql://localhost:5432/<DatabaseName>;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=POSTGRES;DEBUG_LEVEL=5

// PostgreSQL (To access from within a Docker Container)
JDX_DATABASE JDX:jdbc:postgresql://host.docker.internal:5432/<DatabaseName>;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=POSTGRES;DEBUG_LEVEL=5

// PostgreSQL (Local or Remote Server)
JDX_DATABASE JDX:jdbc:postgresql://<Postgresql_IP_Address>:5432/<DatabaseName>;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=POSTGRES;DEBUG_LEVEL=5

// PostgreSQL (Cloud Example: Supabase)
JDX_DATABASE JDX:jdbc:postgresql://db.lxbznecvjwlzdtpckxyz.supabase.co:5432/postgres?user=postgres&password=DPSupaPost_SQL;JDX_DBTYPE=POSTGRES;DEBUG_LEVEL=5

// PostgreSQL JDBC Driver
JDBC_DRIVER org.postgresql.Driver
```

---

### Microsoft SQL Server

```properties
// SQL Server (Local)
JDX_DATABASE JDX:jdbc:sqlserver://localhost:1433;database=<DatabaseName>;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=MSSQL;DEBUG_LEVEL=5

// SQL Server (Windows Integrated Security)
JDX_DATABASE JDX:jdbc:sqlserver://localhost;database=<DatabaseName>;integratedSecurity=true;JDX_DBTYPE=MSSQL;DEBUG_LEVEL=5

// SQL Server (To access from within a Docker Container)
JDX_DATABASE JDX:jdbc:sqlserver://host.docker.internal:1433;database=<DatabaseName>;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=MSSQL;DEBUG_LEVEL=5

// SQL Server JDBC Driver
JDBC_DRIVER com.microsoft.sqlserver.jdbc.SQLServerDriver
```

---

### Oracle

In the URL below, `hostname` refers to the name or IP address of the machine where the Oracle database server is running. `sid` (System Identifier) refers to a unique name that identifies a specific Oracle database instance running on a particular host. `port` is typically 1521.

```properties
// Oracle (Local)
JDX_DATABASE JDX:jdbc:oracle:thin:@<hostname>:<port>:<sid>;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=Oracle;DEBUG_LEVEL=5

// Oracle (To access from within a Docker Container)
JDX_DATABASE JDX:jdbc:oracle:thin://host.docker.internal:<port>:<sid>;USER=<UserName>;PASSWORD=<Password>;JDX_DBTYPE=Oracle;DEBUG_LEVEL=5

// Oracle JDBC Driver
JDBC_DRIVER oracle.jdbc.driver.OracleDriver
```

---

## Notes:

* Ensure the correct JDBC driver is added to the classpath for your database type.
* Always verify that the database connection details (username, password, database name, IP address, port) are correctly specified.

---

By following this guide, you should be able to set up the appropriate JDBC connection strings for your database setup.
