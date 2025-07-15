# SQL-DBML-Converter Usage Guide

This guide explains how to use the SQL-DBML-Converter to convert MySQL CREATE TABLE statements to DBML format.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/LightInTheDarkNight/SQL-DBML-Converter.git
cd SQL-DBML-Converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### Command Line Interface

The converter provides a command-line interface with the following options:

```bash
python -m src.sql_dbml_converter.main [OPTIONS]
```

#### Options:

- `-i, --input PATH`: Input SQL file containing CREATE TABLE statements
- `-o, --output PATH`: Output DBML file path
- `-v, --verbose`: Enable verbose output
- `--version`: Show version information
- `--help`: Show help message

### Examples

#### Convert a file:
```bash
python -m src.sql_dbml_converter.main -i examples/input/sample_schema.sql -o output.dbml
```

#### Convert with verbose output:
```bash
python -m src.sql_dbml_converter.main -i schema.sql -o schema.dbml -v
```

#### Read from stdin, write to stdout:
```bash
cat schema.sql | python -m src.sql_dbml_converter.main
```

#### Read from stdin, write to file:
```bash
cat schema.sql | python -m src.sql_dbml_converter.main -o output.dbml
```

## Supported MySQL Features

### Table Definition
- Basic table creation with columns
- Table comments
- Engine specifications (InnoDB, MyISAM, etc.)
- Character set and collation settings

### Column Types
- Integer types: `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT`
- Decimal types: `DECIMAL`, `NUMERIC`, `FLOAT`, `DOUBLE`
- String types: `CHAR`, `VARCHAR`, `TEXT`, `LONGTEXT`, etc.
- Date/Time types: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, `YEAR`
- Other types: `BOOLEAN`, `JSON`, `ENUM`, `SET`
- Binary types: `BINARY`, `VARBINARY`, `BLOB`, etc.

### Column Constraints
- `PRIMARY KEY`
- `NOT NULL` / `NULL`
- `UNIQUE`
- `AUTO_INCREMENT`
- `DEFAULT` values (literals, functions, expressions)
- Column comments

### Indexes
- Primary key indexes
- Unique indexes
- Regular indexes
- Composite indexes
- Named indexes

### Foreign Keys
- Basic foreign key constraints
- Referential actions: `CASCADE`, `SET NULL`, `RESTRICT`, `NO ACTION`
- Composite foreign keys
- Named foreign key constraints

### Advanced Features
- Self-referencing foreign keys
- Multiple foreign keys per table
- Complex default values and expressions
- ENUM value extraction and documentation

## DBML Output Format

The converter generates DBML that includes:

### Project Definition
```dbml
Project project_name {
  database_type: 'MySQL'
  Note: 'Generated from MySQL CREATE TABLE statements'
}
```

### Table Definitions
```dbml
Table table_name {
  column_name data_type [constraints]
  
  indexes {
    column_name [settings]
    (col1, col2) [composite_settings]
  }
  
  Note: 'Table description'
}
```

### Relationships
```dbml
Ref: table1.column > table2.column [delete: cascade, update: restrict]
```

## Input Requirements

### File Format
- Input should contain valid MySQL CREATE TABLE statements
- Multiple statements can be separated by semicolons
- Comments (both `--` and `/* */` style) are supported
- Files should be UTF-8 encoded

### Validation
The converter performs basic validation:
- Checks for CREATE TABLE statements
- Validates balanced parentheses
- Basic security checks for malicious patterns
- File size limits (default: 10MB)

## Error Handling

### Common Errors
1. **No CREATE TABLE statements found**: Input doesn't contain valid CREATE TABLE syntax
2. **Unbalanced parentheses**: SQL syntax errors in table definitions
3. **File not found**: Input file path is incorrect
4. **Permission denied**: Insufficient permissions to read input or write output

### Troubleshooting
- Use `-v` flag for verbose output to see detailed processing steps
- Check that input file contains valid MySQL syntax
- Ensure output directory exists and is writable
- Verify file permissions

## Limitations

### Current Limitations
- Only supports MySQL CREATE TABLE statements
- Some advanced MySQL features may not be fully supported
- Generated DBML may require manual review for complex schemas
- Stored procedures, triggers, and views are not supported

### Planned Improvements
- Support for additional SQL dialects
- Enhanced error reporting
- Configuration file support
- Batch processing capabilities

## Examples

See the `examples/` directory for:
- `input/sample_schema.sql`: Example MySQL schema
- `output/sample_schema.dbml`: Expected DBML output

## Integration

### With dbdiagram.io
1. Convert your MySQL schema to DBML
2. Copy the generated DBML content
3. Paste into [dbdiagram.io](https://dbdiagram.io) editor
4. Generate visual database diagrams

### In CI/CD Pipelines
```bash
# Example GitHub Actions step
- name: Convert Schema to DBML
  run: |
    python -m src.sql_dbml_converter.main \
      -i database/schema.sql \
      -o docs/schema.dbml \
      -v
```

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/LightInTheDarkNight/SQL-DBML-Converter).
