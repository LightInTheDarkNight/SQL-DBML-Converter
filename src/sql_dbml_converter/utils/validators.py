"""
Input validation utilities for the SQL-DBML-Converter.
"""

import re
from typing import List, Optional


class InputValidator:
    """Validates input for the SQL-DBML converter."""
    
    def __init__(self):
        # Common SQL keywords that should appear in CREATE TABLE statements
        self.create_table_keywords = {
            'CREATE', 'TABLE', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES',
            'UNIQUE', 'INDEX', 'NOT', 'NULL', 'DEFAULT', 'AUTO_INCREMENT'
        }
        
        # SQL injection patterns to watch for
        self.suspicious_patterns = [
            r';\s*DROP\s+TABLE',
            r';\s*DELETE\s+FROM',
            r';\s*UPDATE\s+.*\s+SET',
            r';\s*INSERT\s+INTO',
            r'UNION\s+SELECT',
            r'--\s*[^\r\n]*(\r|\n|$)',  # SQL comments (might be legitimate)
        ]
    
    def validate_sql_input(self, sql_content: str) -> bool:
        """
        Validate SQL input content.
        
        Args:
            sql_content: SQL content to validate
            
        Returns:
            True if input appears to be valid SQL
        """
        if not sql_content or not sql_content.strip():
            return False
        
        # Check for basic SQL structure
        if not self._contains_create_table_statements(sql_content):
            return False
        
        # Check for suspicious patterns (basic security check)
        if self._contains_suspicious_patterns(sql_content):
            return False
        
        # Check for balanced parentheses
        if not self._has_balanced_parentheses(sql_content):
            return False
        
        return True
    
    def _contains_create_table_statements(self, sql_content: str) -> bool:
        """Check if content contains CREATE TABLE statements."""
        # Look for CREATE TABLE pattern (case insensitive)
        create_table_pattern = r'\bCREATE\s+(?:TEMPORARY\s+)?TABLE\b'
        return bool(re.search(create_table_pattern, sql_content, re.IGNORECASE))
    
    def _contains_suspicious_patterns(self, sql_content: str) -> bool:
        """Check for potentially malicious SQL patterns."""
        for pattern in self.suspicious_patterns:
            if re.search(pattern, sql_content, re.IGNORECASE):
                return True
        return False
    
    def _has_balanced_parentheses(self, sql_content: str) -> bool:
        """Check if parentheses are balanced in the SQL content."""
        stack = []
        brackets = {'(': ')', '[': ']', '{': '}'}
        
        in_string = False
        string_char = None
        
        for i, char in enumerate(sql_content):
            # Handle string literals
            if char in ('"', "'", '`') and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                # Check if it's escaped
                if i > 0 and sql_content[i-1] != '\\':
                    in_string = False
                    string_char = None
            
            # Skip bracket checking inside strings
            if in_string:
                continue
            
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                if not stack:
                    return False
                last_open = stack.pop()
                if brackets[last_open] != char:
                    return False
        
        return len(stack) == 0
    
    def validate_table_name(self, table_name: str) -> bool:
        """
        Validate table name format.
        
        Args:
            table_name: Table name to validate
            
        Returns:
            True if table name is valid
        """
        if not table_name:
            return False
        
        # Remove quotes if present
        clean_name = table_name.strip('`"\'')
        
        # Check length (MySQL limit is 64 characters)
        if len(clean_name) > 64:
            return False
        
        # Check for valid characters (letters, numbers, underscore, dollar sign)
        if not re.match(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$', clean_name):
            return False
        
        # Check if it's a reserved word (basic check)
        mysql_reserved = {
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP',
            'ALTER', 'INDEX', 'TABLE', 'DATABASE', 'SCHEMA', 'VIEW',
            'PROCEDURE', 'FUNCTION', 'TRIGGER', 'USER', 'ROLE'
        }
        
        if clean_name.upper() in mysql_reserved:
            return False
        
        return True
    
    def validate_column_name(self, column_name: str) -> bool:
        """
        Validate column name format.
        
        Args:
            column_name: Column name to validate
            
        Returns:
            True if column name is valid
        """
        # Similar validation to table name
        return self.validate_table_name(column_name)
    
    def validate_data_type(self, data_type: str) -> bool:
        """
        Validate SQL data type format.
        
        Args:
            data_type: Data type string to validate
            
        Returns:
            True if data type appears valid
        """
        if not data_type:
            return False
        
        # Common MySQL data types
        valid_types = {
            'TINYINT', 'SMALLINT', 'MEDIUMINT', 'INT', 'INTEGER', 'BIGINT',
            'DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE', 'REAL', 'BIT',
            'BOOLEAN', 'BOOL', 'SERIAL',
            'DATE', 'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR',
            'CHAR', 'VARCHAR', 'BINARY', 'VARBINARY',
            'TINYBLOB', 'BLOB', 'MEDIUMBLOB', 'LONGBLOB',
            'TINYTEXT', 'TEXT', 'MEDIUMTEXT', 'LONGTEXT',
            'ENUM', 'SET', 'JSON', 'GEOMETRY', 'POINT', 'LINESTRING',
            'POLYGON', 'MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON',
            'GEOMETRYCOLLECTION'
        }
        
        # Extract base type (remove parameters)
        base_type = data_type.split('(')[0].strip().upper()
        
        return base_type in valid_types
    
    def extract_create_table_statements(self, sql_content: str) -> List[str]:
        """
        Extract individual CREATE TABLE statements from SQL content.
        
        Args:
            sql_content: SQL content containing multiple statements
            
        Returns:
            List of individual CREATE TABLE statements
        """
        statements = []
        
        # Split by semicolons, but be careful about semicolons in strings
        current_statement = ""
        in_string = False
        string_char = None
        
        for i, char in enumerate(sql_content):
            # Handle string literals
            if char in ('"', "'", '`') and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                # Check if it's escaped
                if i > 0 and sql_content[i-1] != '\\':
                    in_string = False
                    string_char = None
            
            current_statement += char
            
            # Check for statement end
            if char == ';' and not in_string:
                statement = current_statement.strip()
                if statement and self._contains_create_table_statements(statement):
                    statements.append(statement)
                current_statement = ""
        
        # Handle last statement if it doesn't end with semicolon
        if current_statement.strip():
            statement = current_statement.strip()
            if self._contains_create_table_statements(statement):
                statements.append(statement)
        
        return statements
    
    def validate_file_content_size(self, content: str, max_size_mb: int = 10) -> bool:
        """
        Validate that file content is not too large.
        
        Args:
            content: File content
            max_size_mb: Maximum size in megabytes
            
        Returns:
            True if content size is acceptable
        """
        content_size_bytes = len(content.encode('utf-8'))
        max_size_bytes = max_size_mb * 1024 * 1024
        
        return content_size_bytes <= max_size_bytes
    
    def sanitize_sql_input(self, sql_content: str) -> str:
        """
        Basic sanitization of SQL input.
        
        Args:
            sql_content: Raw SQL content
            
        Returns:
            Sanitized SQL content
        """
        # Remove potentially dangerous patterns
        sanitized = sql_content
        
        # Remove SQL comments (-- style)
        sanitized = re.sub(r'--[^\r\n]*', '', sanitized)
        
        # Remove multi-line comments (/* */ style)
        sanitized = re.sub(r'/\*.*?\*/', '', sanitized, flags=re.DOTALL)
        
        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        return sanitized.strip()
    
    def get_validation_errors(self, sql_content: str) -> List[str]:
        """
        Get detailed validation errors for SQL content.
        
        Args:
            sql_content: SQL content to validate
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        if not sql_content or not sql_content.strip():
            errors.append("Input is empty")
            return errors
        
        if not self._contains_create_table_statements(sql_content):
            errors.append("No CREATE TABLE statements found")
        
        if self._contains_suspicious_patterns(sql_content):
            errors.append("Potentially unsafe SQL patterns detected")
        
        if not self._has_balanced_parentheses(sql_content):
            errors.append("Unbalanced parentheses, brackets, or braces")
        
        if not self.validate_file_content_size(sql_content):
            errors.append("Input content is too large (>10MB)")
        
        return errors
