"""
Schema mapper for converting SQL data types and constraints to DBML equivalents.
"""

from typing import Dict, Any, Optional


class SchemaMapper:
    """Maps SQL schema elements to DBML equivalents."""
    
    # MySQL to DBML data type mappings
    DATA_TYPE_MAPPINGS = {
        # Integer types
        'TINYINT': 'int',
        'SMALLINT': 'int',
        'MEDIUMINT': 'int',
        'INT': 'int',
        'INTEGER': 'int',
        'BIGINT': 'bigint',
        
        # Decimal types
        'DECIMAL': 'decimal',
        'NUMERIC': 'decimal',
        'FLOAT': 'float',
        'DOUBLE': 'double',
        'REAL': 'double',
        
        # String types
        'CHAR': 'varchar',
        'VARCHAR': 'varchar',
        'TINYTEXT': 'text',
        'TEXT': 'text',
        'MEDIUMTEXT': 'text',
        'LONGTEXT': 'text',
        
        # Binary types
        'BINARY': 'varchar',
        'VARBINARY': 'varchar',
        'TINYBLOB': 'text',
        'BLOB': 'text',
        'MEDIUMBLOB': 'text',
        'LONGBLOB': 'text',
        
        # Date and time types
        'DATE': 'date',
        'TIME': 'time',
        'DATETIME': 'datetime',
        'TIMESTAMP': 'timestamp',
        'YEAR': 'int',
        
        # Other types
        'BOOLEAN': 'boolean',
        'BOOL': 'boolean',
        'JSON': 'json',
        'ENUM': 'varchar',
        'SET': 'varchar',
        
        # Spatial types (mapped to text for DBML compatibility)
        'GEOMETRY': 'text',
        'POINT': 'text',
        'LINESTRING': 'text',
        'POLYGON': 'text',
        'MULTIPOINT': 'text',
        'MULTILINESTRING': 'text',
        'MULTIPOLYGON': 'text',
        'GEOMETRYCOLLECTION': 'text',
    }
    
    def __init__(self):
        pass
    
    def map_data_type(self, sql_type: str) -> str:
        """
        Map SQL data type to DBML compatible type.
        
        Args:
            sql_type: SQL data type string (e.g., 'VARCHAR(255)', 'INT(11)')
            
        Returns:
            DBML compatible data type string
        """
        # Extract base type and parameters
        base_type, params = self._parse_data_type(sql_type)
        
        # Get DBML equivalent
        dbml_type = self.DATA_TYPE_MAPPINGS.get(base_type.upper(), base_type.lower())
        
        # Add parameters if applicable
        if params and self._should_include_params(dbml_type, params):
            return f"{dbml_type}({params})"
        
        return dbml_type
    
    def _parse_data_type(self, sql_type: str) -> tuple[str, Optional[str]]:
        """
        Parse SQL data type into base type and parameters.
        
        Args:
            sql_type: SQL data type string
            
        Returns:
            Tuple of (base_type, parameters)
        """
        sql_type = sql_type.strip()
        
        # Check for parameters in parentheses
        if '(' in sql_type and ')' in sql_type:
            base_type = sql_type[:sql_type.index('(')]
            params = sql_type[sql_type.index('(') + 1:sql_type.rindex(')')]
            return base_type.strip(), params.strip()
        
        return sql_type, None
    
    def _should_include_params(self, dbml_type: str, params: str) -> bool:
        """
        Determine if parameters should be included in DBML type.
        
        Args:
            dbml_type: DBML data type
            params: Parameter string
            
        Returns:
            True if parameters should be included
        """
        # Include parameters for these types
        param_types = {'varchar', 'char', 'decimal', 'numeric'}
        
        # Don't include default MySQL display widths for integers
        if dbml_type == 'int' and params.isdigit():
            return False
        
        return dbml_type in param_types
    
    def map_constraint(self, constraint_type: str, value: Any = None) -> Optional[str]:
        """
        Map SQL constraint to DBML equivalent.
        
        Args:
            constraint_type: Type of constraint
            value: Constraint value if applicable
            
        Returns:
            DBML constraint string or None
        """
        constraint_mappings = {
            'PRIMARY KEY': 'pk',
            'UNIQUE': 'unique',
            'NOT NULL': 'not null',
            'AUTO_INCREMENT': 'increment',
        }
        
        return constraint_mappings.get(constraint_type.upper())
    
    def map_index_type(self, mysql_index_type: str) -> Optional[str]:
        """
        Map MySQL index type to DBML equivalent.
        
        Args:
            mysql_index_type: MySQL index type
            
        Returns:
            DBML index type or None
        """
        index_type_mappings = {
            'BTREE': 'btree',
            'HASH': 'hash',
            'FULLTEXT': None,  # Not supported in DBML
            'SPATIAL': None,   # Not supported in DBML
        }
        
        return index_type_mappings.get(mysql_index_type.upper())
    
    def map_referential_action(self, mysql_action: str) -> str:
        """
        Map MySQL referential action to DBML equivalent.
        
        Args:
            mysql_action: MySQL referential action
            
        Returns:
            DBML referential action
        """
        action_mappings = {
            'CASCADE': 'cascade',
            'SET NULL': 'set null',
            'SET DEFAULT': 'set default',
            'RESTRICT': 'restrict',
            'NO ACTION': 'no action',
        }
        
        return action_mappings.get(mysql_action.upper(), mysql_action.lower())
    
    def normalize_identifier(self, identifier: str) -> str:
        """
        Normalize SQL identifier for DBML.
        
        Args:
            identifier: SQL identifier (table name, column name, etc.)
            
        Returns:
            Normalized identifier
        """
        # Remove backticks if present
        if identifier.startswith('`') and identifier.endswith('`'):
            identifier = identifier[1:-1]
        
        # Remove double quotes if present
        if identifier.startswith('"') and identifier.endswith('"'):
            identifier = identifier[1:-1]
        
        return identifier
    
    def should_quote_identifier(self, identifier: str) -> bool:
        """
        Determine if identifier should be quoted in DBML.
        
        Args:
            identifier: Identifier to check
            
        Returns:
            True if identifier should be quoted
        """
        # Quote if contains spaces or special characters
        return not identifier.replace('_', '').isalnum()
    
    def format_identifier(self, identifier: str) -> str:
        """
        Format identifier for DBML output.
        
        Args:
            identifier: Raw identifier
            
        Returns:
            Formatted identifier
        """
        normalized = self.normalize_identifier(identifier)
        
        if self.should_quote_identifier(normalized):
            return f'"{normalized}"'
        
        return normalized
    
    def extract_enum_values(self, enum_definition: str) -> list[str]:
        """
        Extract enum values from MySQL ENUM definition.
        
        Args:
            enum_definition: MySQL ENUM definition string
            
        Returns:
            List of enum values
        """
        # Remove ENUM( and closing )
        if enum_definition.upper().startswith('ENUM('):
            values_str = enum_definition[5:-1]
        else:
            values_str = enum_definition
        
        # Parse comma-separated quoted values
        values = []
        current_value = ""
        in_quotes = False
        quote_char = None
        
        for char in values_str:
            if not in_quotes and char in ("'", '"'):
                in_quotes = True
                quote_char = char
                current_value += char
            elif in_quotes and char == quote_char:
                in_quotes = False
                current_value += char
                quote_char = None
            elif not in_quotes and char == ',':
                if current_value.strip():
                    values.append(current_value.strip())
                current_value = ""
            else:
                current_value += char
        
        # Add the last value
        if current_value.strip():
            values.append(current_value.strip())
        
        return values
    
    def get_dbml_equivalent_note(self, mysql_feature: str) -> Optional[str]:
        """
        Get DBML note for MySQL features not directly supported.
        
        Args:
            mysql_feature: MySQL feature description
            
        Returns:
            Note text or None
        """
        feature_notes = {
            'FULLTEXT': 'MySQL FULLTEXT index',
            'SPATIAL': 'MySQL SPATIAL index',
            'GENERATED': 'MySQL generated column',
            'ON UPDATE CURRENT_TIMESTAMP': 'MySQL auto-update timestamp',
        }
        
        return feature_notes.get(mysql_feature.upper())
