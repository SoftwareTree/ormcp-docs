Copyright (c) 2025, Software Tree

# ORMCP Server - MCP Tools API Reference

This document provides detailed technical specifications for all MCP tools provided by ORMCP Server. This reference is intended for:

- Developers building integrations with ORMCP Server
- Advanced users who need detailed parameter specifications
- Troubleshooting complex queries and operations

For a user-friendly overview of these tools, see the [main README](../README.md#mcp-tools-reference).

## About MCP Tools

ORMCP Server exposes database operations as MCP (Model Context Protocol) tools that can be called by AI clients. Each tool corresponds to a specific database operation and accepts structured parameters.

## Parameter Conventions

- `className`: Always refers to your domain model class name. If the class belongs to a package, the full class name (including the package name) should be specified.
- `deep`: Controls whether related objects are included in results (default: True)
- `operationDetails`: Advanced query customization supporting GraphQL-like operations
- `filter`: SQL-like WHERE clause conditions. Filters use the **attribute names** shown by `getObjectModelSummary`, never database column names. Where a column name contains characters other than letters, digits and `_`, the attribute name replaces them with `_`: for example, the column `All_Traffic.action` is the attribute `All_Traffic_action`, and `tag::eventtype` is `tag__eventtype`. A filter written with a column name fails.
- Classes marked `DB_PRIMARY_KEY_EXISTS FALSE` in the object model summary have no unique primary key in the database (several objects may share the same key values). For them, use `query`, `access` and `getAggregate`, and `update2`/`delete2` with a filter; `getObjectById`, `update` and `delete` are not supported.
- Results: the read tools and `update2`/`delete2` return JSON; `insert`, `update` and `delete` return a short plain-text confirmation. Each tool's **Returns** below gives the details. Failures are reported as errors.

## Operation Details

The `operationDetails` parameter supports GraphQL-like operations for fine-tuning queries:

- **`projections`**: Select only specific attributes
- **`ignore`**: Skip certain referenced object branches  
- **`follow`**: Include specific referenced object branches
- **`filters`**: Apply predicates to referenced objects

For **`projections`**, the projected attributes (`attribs`) of a class must include all of its primary-key attributes, as shown in the object model summary. Exception: classes marked `DB_PRIMARY_KEY_EXISTS FALSE` have no real primary key, so their projections need not include the key attributes.

**Example:**
```json
[{"opType": "projections", "projectionsDetails": [{"type": "Employee", "attribs": ["name", "id"]}]}]
```

---

## Core Operations

### `getObjectModelSummary`

Get information about the underlying object model, such as classes (types), attributes, primary keys, relationships, etc.

**Parameters:** None

**Returns:** A summary of the information about the underlying object model, including:
- Available classes (types) in your domain model
- Attributes for each class
- Primary key definitions
- Relationship mappings between classes

---

### `query`

Query all qualifying objects of a particular type (class) based on the filter condition.

**Parameters:**
- `className` (string, required): Name of the type (class) whose objects need to be retrieved. If the class belongs to a package, the full class name (including the package name) should be specified.
- `filter` (string, optional): Search condition (WHERE clause) for the objects. May also include an 'ORDER BY' specification. A null or empty string means don't apply any search (filter) condition for qualifying objects while retrieving the objects.
- `maxObjects` (integer, optional): Maximum number of objects to be retrieved (-1 => all qualified objects, default: -1)
- `deep` (boolean, optional): Whether to retrieve referenced objects as well (default: True)
- `operationDetails` (string, optional): JSON array of operational directives for fine-tuning queries. Supports GraphQL-like operations: 'projections' (select specific attributes), 'ignore' (skip references), 'follow' (include references), 'filters' (apply predicates). Example: `[{"opType": "projections", "projectionsDetails": [{"type": "Employee", "attribs": ["name", "id"]}]}]`. Leave empty for no operational directives.
- `allowDuplicates` (boolean, optional): Return every qualifying row as its own object, even when rows have identical primary key values (default: False). Rows of classes marked `DB_PRIMARY_KEY_EXISTS FALSE` are always returned this way; set this to True only if identical rows of other classes must not be merged. Works with deep and shallow queries. Requires Gilhari 0.8.7 or later.

**Returns:** A JSON array of the qualifying objects (an empty array `[]` if none qualify)

**Example:**
```json
{
  "className": "User",
  "filter": "age >= 30 ORDER BY name",
  "maxObjects": 10,
  "deep": true
}
```

---

### `getObjectById`

Query the object of a particular type (class) based on the id (primary key attribute values) of the object. The object is first checked in the cache (if configured for the class) before going to the database.

**Not supported** for classes marked `DB_PRIMARY_KEY_EXISTS FALSE` (their primary key values are not unique); use `query` with a filter instead.

**Parameters:**
- `className` (string, required): Name of the type (class) whose object needs to be retrieved. If the class belongs to a package, the full class name (including the package name) should be specified.
- `primaryKey` (object, required): id (primary key attribute values in JSON format) of the object
- `deep` (boolean, optional): Whether to retrieve referenced objects as well (default: True)
- `operationDetails` (string, optional): JSON array of operational directives for fine-tuning queries. Supports GraphQL-like operations: 'projections' (select specific attributes: Not supported), 'ignore' (skip references), 'follow' (include references), 'filters' (apply predicates). Example: `[{"opType": "filters", "predicates": [{"type":"Address", "predicate": "zip='95007'"}]}]`. Leave empty for no operational directives.

**Returns:** The object as a single JSON object (not an array), or `null` if no object has that id

**Example:**
```json
{
  "className": "User",
  "primaryKey": {"id": 123},
  "deep": true
}
```

---

### `access`

Retrieve the object(s) referenced by the attributeName attribute of a referencing object of a particular type (class).

**Parameters:**
- `className` (string, required): Name of the type (class) of the referencing object. If the class belongs to a package, the full class name (including the package name) should be specified.
- `jsonObject` (object, required): The referencing object whose attribute needs to be retrieved
- `attributeName` (string, required): Name of the attribute whose value needs to be retrieved
- `deep` (boolean, optional): Whether to retrieve referenced objects of the retrieved object as well (default: True)
- `operationDetails` (string, optional): JSON array of operational directives for fine-tuning queries. Supports GraphQL-like operations: 'projections' (select specific attributes), 'ignore' (skip references), 'follow' (include references), 'filters' (apply predicates). Example: `[{"opType": "projections", "projectionsDetails": [{"type": "Employee", "attribs": ["name", "id"]}]}]`. Leave empty for no operational directives.

**Returns:** If the attribute is a collection (e.g., List or Array), a JSON array of the referenced objects (an empty array `[]` if there are none); otherwise the referenced object

**Example:**
```json
{
  "className": "User",
  "jsonObject": {"id": 123, "name": "John"},
  "attributeName": "address",
  "deep": false
}
```

---

### `getAggregate`

Query an aggregate value (COUNT, SUM, AVG, MIN, MAX) for an attribute of all qualifying objects of a particular type (class) based on the filter condition.

**Parameters:**
- `className` (string, required): Name of the type (class) whose objects need to be aggregated. If the class belongs to a package, the full class name (including the package name) should be specified.
- `attributeName` (string, required): Name of the attribute to aggregate
- `aggregateType` (string, required): Type of aggregation (COUNT, SUM, AVG, MIN, MAX)
- `filter` (string, optional): Search condition for the objects to be aggregated. A SQL-like WHERE clause (optional). **WARNING:** Default is include all objects for aggregation.

**Returns:** The aggregate as a single JSON value, not a list of objects: a number for COUNT, SUM and AVG (e.g. `1000`, `2.980000`), and for MIN/MAX a value of the attribute's type (e.g. `"ACADEMY DINOSAUR"` for a string attribute)

**Example:**
```json
{
  "className": "User",
  "attributeName": "age",
  "aggregateType": "AVG",
  "filter": "city='Boston'"
}
```

---

## Data Modification Operations

### `insert`

Save (Insert) one or more JSON objects.

**Parameters:**
- `className` (string, required): Name of the type (class) whose objects need to be saved. If the class belongs to a package, the full class name (including the package name) should be specified.
- `jsonObjects` (array, required): A list of one or more objects in JSON format; one or more JSON objects can be passed in an array ([...]).
- `deep` (boolean, optional): Whether to save referenced objects as well (default: True)

**Returns:** A short confirmation message (plain text, not JSON) when the operation succeeds; failures are reported as errors

**Example:**
```json
{
  "className": "User",
  "jsonObjects": [
    {"name": "John Doe", "age": 30, "city": "Boston"},
    {"name": "Jane Smith", "age": 25, "city": "New York"}
  ],
  "deep": true
}
```

---

### `update`

Update one or more JSON objects. `update` replaces each stored object with the one given (matched by primary key), so include all of its attributes. To change only some attributes, use `update2` with a filter on the primary key.

**Not supported** for classes marked `DB_PRIMARY_KEY_EXISTS FALSE` (an object can't be identified by its primary key values); use `update2` with a filter instead.

**Parameters:**
- `className` (string, required): Name of the type (class) whose objects need to be updated. If the class belongs to a package, the full class name (including the package name) should be specified.
- `jsonObjects` (array, required): A list of one or more objects in JSON format; one or more JSON objects can be passed in an array ([...]).
- `deep` (boolean, optional): Whether to update referenced (contained) objects as well (default: True)

**Returns:** A short confirmation message (plain text, not JSON) when the operation succeeds; failures are reported as errors

**Example:**
```json
{
  "className": "User",
  "jsonObjects": [
    {"id": 123, "name": "John Doe Updated", "age": 31, "city": "Boston", "state": "MA"}
  ],
  "deep": true
}
```

---

### `update2`

Bulk update selected attributes of all qualifying objects of a particular type (class) based on the filter condition with the new attribute values. If deep parameter is true, all the contained objects are also updated.

**Parameters:**
- `className` (string, required): Name of the type (class) whose objects need to be updated. If the class belongs to a package, the full class name (including the package name) should be specified.
- `filter` (string, required): Search condition for the objects to be updated, as a SQL-like WHERE clause. **WARNING:** An empty string updates all objects of the class.
- `newValues` (array, required): An alternating list of attribute names and their new values, `["attrName1", value1, "attrName2", value2, ...]`; an even number of elements, at least one name/value pair. For example, `["attribInt", 100, "attribString", "value"]`
- `deep` (boolean, optional): Whether to update referenced objects as well (default: True)

**Returns:** The number of top-level objects updated, as a JSON number

**Example:**
```json
{
  "className": "User",
  "filter": "city='Boston'",
  "newValues": ["status", "active", "lastLogin", "2024-01-15"],
  "deep": false
}
```

---

### `delete`

Delete one or more JSON objects.

**Not supported** for classes marked `DB_PRIMARY_KEY_EXISTS FALSE` (an object can't be identified by its primary key values); use `delete2` with a filter instead.

**Parameters:**
- `className` (string, required): Name of the type (class) whose objects need to be deleted. If the class belongs to a package, the full class name (including the package name) should be specified.
- `jsonObjects` (array, required): A list of one or more objects in JSON format; one or more JSON objects can be passed in an array ([...]). Only the primary key attributes of an object need to be specified. The other attributes may be specified but will be ignored.
- `deep` (boolean, optional): Whether to delete referenced (contained) objects as well (default: True)

**Returns:** A short confirmation message (plain text, not JSON) when the operation succeeds; failures are reported as errors

**Example:**
```json
{
  "className": "User",
  "jsonObjects": [
    {"id": 123},
    {"id": 124}
  ],
  "deep": true
}
```

---

### `delete2`

Bulk delete all qualifying objects of a particular type (class) based on the filter condition. If deep parameter is true, all the contained objects are also deleted.

**Parameters:**
- `className` (string, required): Name of the type (class) whose objects need to be deleted. If the class belongs to a package, the full class name (including the package name) should be specified.
- `filter` (string, optional): Search condition for the objects to be deleted, as a SQL-like WHERE clause. **WARNING:** If omitted or empty, all objects of the class are deleted.
- `deep` (boolean, optional): Whether to delete referenced (contained) objects as well (default: True)

**Returns:** The number of top-level objects deleted, as a JSON number

**Example:**
```json
{
  "className": "User",
  "filter": "lastLogin < '2023-01-01'",
  "deep": false
}
```

---

## Important Notes

### Read-Only Mode
`READONLY_MODE` defaults to `True`: the MCP tools for data modification operations (`insert`, `update`, `update2`, `delete`, `delete2`) are not exposed to MCP clients unless `READONLY_MODE=False` is set.

### Error Handling
All tools provide detailed error messages when operations fail, including:
- Invalid class names or attributes
- Database connectivity issues
- Constraint violations
- Permission errors

### Performance Considerations
- Use `maxObjects` parameter to limit large result sets
- Consider using `deep=false` for better performance when related objects aren't needed
- Utilize database indexes for frequently filtered attributes
- Use `operationDetails` projections to retrieve only necessary attributes

### Caching
Objects retrieved via `getObjectById` are checked in the cache (if configured for the class) before querying the database, improving performance for frequently accessed data.
