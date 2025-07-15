"""
DBML generator for converting parsed SQL schema to DBML format.
"""

from typing import List, Dict, Any, Optional
from ..parser.sql_parser import Schema, Table, Column, Index, ForeignKey
from .schema_mapper import SchemaMapper


class DBMLGenerator:
    """Generator for DBML output from parsed SQL schema."""
    
    def __init__(self):
        self.schema_mapper = SchemaMapper()
        self.indent_size = 2
    
    def generate(self, schema: Schema) -> str:
        """
        Generate DBML output from a parsed schema.
        
        Args:
            schema: Parsed schema object
            
        Returns:
            DBML formatted string
        """
        dbml_parts = []
        
        # Generate project definition if schema has a name
        if schema.name:
            dbml_parts.append(self._generate_project(schema.name))
            dbml_parts.append("")
        
        # Generate tables
        for table in schema.tables:
            dbml_parts.append(self._generate_table(table))
            dbml_parts.append("")
        
        # Generate relationships
        relationships = self._extract_relationships(schema)
        if relationships:
            dbml_parts.extend(relationships)
        
        return "\n".join(dbml_parts).strip()
    
    def _generate_project(self, name: str) -> str:
        """Generate project definition."""
        return f"""Project {name} {{
  database_type: 'MySQL'
  Note: 'Generated from MySQL CREATE TABLE statements'
}}"""
    
    def _generate_table(self, table: Table) -> str:
        """
        Generate DBML table definition.
        
        Args:
            table: Table object
            
        Returns:
            DBML table definition string
        """
        lines = []
        
        # Table header with settings
        table_settings = self._generate_table_settings(table)
        if table_settings:
            lines.append(f"Table {table.name} {table_settings} {{")
        else:
            lines.append(f"Table {table.name} {{")
        
        # Columns
        for column in table.columns:
            column_line = self._generate_column(column)
            lines.append(f"  {column_line}")
        
        # Indexes
        if table.indexes:
            lines.append("")
            lines.append("  indexes {")
            for index in table.indexes:
                index_line = self._generate_index(index)
                lines.append(f"    {index_line}")
            lines.append("  }")
        
        # Table note
        if table.comment:
            lines.append("")
            lines.append(f"  Note: '{self._escape_string(table.comment)}'")
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_table_settings(self, table: Table) -> str:
        """Generate table settings string."""
        settings = []
        
        # TODO: Add table color based on engine or other properties
        # if table.engine:
        #     settings.append(f"headercolor: #{self._get_engine_color(table.engine)}")
        
        if settings:
            return f"[{', '.join(settings)}]"
        return ""
    
    def _generate_column(self, column: Column) -> str:
        """
        Generate DBML column definition.
        
        Args:
            column: Column object
            
        Returns:
            DBML column definition string
        """
        # Map SQL data type to DBML compatible type
        dbml_type = self.schema_mapper.map_data_type(column.data_type)
        
        # Build column definition
        parts = [column.name, dbml_type]
        
        # Column settings
        settings = self._generate_column_settings(column)
        if settings:
            parts.append(f"[{settings}]")
        
        return " ".join(parts)
    
    def _generate_column_settings(self, column: Column) -> str:
        """Generate column settings string."""
        settings = []
        
        if column.primary_key:
            settings.append("pk")
        
        if not column.nullable:
            settings.append("not null")
        
        if column.unique and not column.primary_key:
            settings.append("unique")
        
        if column.auto_increment:
            settings.append("increment")
        
        if column.default_value is not None:
            default_val = self._format_default_value(column.default_value)
            settings.append(f"default: {default_val}")
        
        if column.comment:
            escaped_comment = self._escape_string(column.comment)
            settings.append(f"note: '{escaped_comment}'")
        
        return ", ".join(settings)
    
    def _generate_index(self, index: Index) -> str:
        """
        Generate DBML index definition.
        
        Args:
            index: Index object
            
        Returns:
            DBML index definition string
        """
        # Format column list
        if len(index.columns) == 1:
            columns_str = index.columns[0]
        else:
            columns_str = f"({', '.join(index.columns)})"
        
        # Index settings
        settings = []
        
        if index.primary:
            settings.append("pk")
        elif index.unique:
            settings.append("unique")
        
        if index.name:
            settings.append(f"name: '{index.name}'")
        
        if index.index_type:
            settings.append(f"type: {index.index_type}")
        
        # Build index line
        if settings:
            return f"{columns_str} [{', '.join(settings)}]"
        else:
            return columns_str
    
    def _extract_relationships(self, schema: Schema) -> List[str]:
        """
        Extract and generate relationship definitions.
        
        Args:
            schema: Schema object
            
        Returns:
            List of DBML relationship strings
        """
        relationships = []
        
        for table in schema.tables:
            for fk in table.foreign_keys:
                rel_line = self._generate_relationship(table.name, fk)
                relationships.append(rel_line)
        
        return relationships
    
    def _generate_relationship(self, table_name: str, foreign_key: ForeignKey) -> str:
        """
        Generate DBML relationship definition.
        
        Args:
            table_name: Name of the table containing the foreign key
            foreign_key: ForeignKey object
            
        Returns:
            DBML relationship string
        """
        # Format column references
        if len(foreign_key.columns) == 1:
            source_cols = f"{table_name}.{foreign_key.columns[0]}"
            target_cols = f"{foreign_key.referenced_table}.{foreign_key.referenced_columns[0]}"
        else:
            source_cols = f"{table_name}.({', '.join(foreign_key.columns)})"
            target_cols = f"{foreign_key.referenced_table}.({', '.join(foreign_key.referenced_columns)})"
        
        # Relationship type (assuming many-to-one for foreign keys)
        relationship = f"Ref: {source_cols} > {target_cols}"
        
        # Add relationship settings
        settings = []
        if foreign_key.on_delete:
            settings.append(f"delete: {foreign_key.on_delete.lower()}")
        if foreign_key.on_update:
            settings.append(f"update: {foreign_key.on_update.lower()}")
        
        if settings:
            relationship += f" [{', '.join(settings)}]"
        
        return relationship
    
    def _format_default_value(self, default_value: str) -> str:
        """
        Format default value for DBML output.
        
        Args:
            default_value: Raw default value
            
        Returns:
            Formatted default value
        """
        # Handle different types of default values
        if default_value.upper() in ('NULL', 'TRUE', 'FALSE'):
            return default_value.lower()
        elif default_value.startswith("'") and default_value.endswith("'"):
            return default_value
        elif self._is_function_call(default_value):
            return f"`{default_value}`"
        elif default_value.isdigit() or self._is_numeric(default_value):
            return default_value
        else:
            return f"'{default_value}'"
    
    def _is_function_call(self, value: str) -> bool:
        """Check if value is a function call."""
        function_patterns = [
            'NOW()', 'CURRENT_TIMESTAMP', 'CURRENT_DATE', 'CURRENT_TIME',
            'UUID()', 'RAND()', 'USER()', 'CONNECTION_ID()'
        ]
        return any(pattern in value.upper() for pattern in function_patterns)
    
    def _is_numeric(self, value: str) -> bool:
        """Check if value is numeric."""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _escape_string(self, text: str) -> str:
        """
        Escape string for DBML output.
        
        Args:
            text: String to escape
            
        Returns:
            Escaped string
        """
        # Escape single quotes and backslashes
        return text.replace("\\", "\\\\").replace("'", "\\'")
    
    def _get_engine_color(self, engine: str) -> str:
        """
        Get color code for database engine.
        
        Args:
            engine: Database engine name
            
        Returns:
            Hex color code
        """
        engine_colors = {
            'InnoDB': '3498DB',
            'MyISAM': 'E74C3C',
            'Memory': 'F39C12',
            'Archive': '9B59B6'
        }
        return engine_colors.get(engine, '95A5A6')
