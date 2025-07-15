"""
Tests for SQL parser functionality.
"""

import pytest
from src.sql_dbml_converter.parser.sql_parser import SQLParser, Column, Table, Index, ForeignKey, Schema


class TestSQLParser:
    """Test cases for SQLParser class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = SQLParser()
    
    def test_parser_initialization(self):
        """Test parser initializes correctly."""
        assert self.parser is not None
        assert hasattr(self.parser, 'tokenizer')
    
    def test_parse_empty_input(self):
        """Test parsing empty input."""
        result = self.parser.parse("")
        assert isinstance(result, Schema)
        assert len(result.tables) == 0
    
    def test_parse_simple_create_table(self):
        """Test parsing a simple CREATE TABLE statement."""
        sql = """
        CREATE TABLE users (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE
        );
        """
        # TODO: Implement actual parsing logic
        result = self.parser.parse(sql)
        assert isinstance(result, Schema)
        # Add more assertions once parsing is implemented
    
    def test_parse_table_with_foreign_key(self):
        """Test parsing table with foreign key constraints."""
        sql = """
        CREATE TABLE posts (
            id INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
        # TODO: Implement actual parsing logic
        result = self.parser.parse(sql)
        assert isinstance(result, Schema)
        # Add more assertions once parsing is implemented
    
    def test_parse_table_with_indexes(self):
        """Test parsing table with index definitions."""
        sql = """
        CREATE TABLE products (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category_id INT,
            price DECIMAL(10,2),
            INDEX idx_category (category_id),
            UNIQUE INDEX idx_name (name)
        );
        """
        # TODO: Implement actual parsing logic
        result = self.parser.parse(sql)
        assert isinstance(result, Schema)
        # Add more assertions once parsing is implemented
    
    def test_parse_multiple_tables(self):
        """Test parsing multiple CREATE TABLE statements."""
        sql = """
        CREATE TABLE users (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        
        CREATE TABLE posts (
            id INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
        # TODO: Implement actual parsing logic
        result = self.parser.parse(sql)
        assert isinstance(result, Schema)
        # Add more assertions once parsing is implemented
    
    def test_parse_table_with_comments(self):
        """Test parsing table with comments."""
        sql = """
        CREATE TABLE users (
            id INT PRIMARY KEY COMMENT 'User ID',
            name VARCHAR(255) NOT NULL COMMENT 'User name',
            email VARCHAR(255) UNIQUE
        ) COMMENT='User information table';
        """
        # TODO: Implement actual parsing logic
        result = self.parser.parse(sql)
        assert isinstance(result, Schema)
        # Add more assertions once parsing is implemented
    
    def test_parse_table_with_engine_options(self):
        """Test parsing table with MySQL engine options."""
        sql = """
        CREATE TABLE logs (
            id INT PRIMARY KEY,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        # TODO: Implement actual parsing logic
        result = self.parser.parse(sql)
        assert isinstance(result, Schema)
        # Add more assertions once parsing is implemented
    
    def test_is_create_table_statement(self):
        """Test identification of CREATE TABLE statements."""
        # TODO: Implement _is_create_table_statement method
        pass
    
    def test_extract_table_name(self):
        """Test table name extraction."""
        # TODO: Implement _extract_table_name method
        pass
    
    def test_parse_columns(self):
        """Test column parsing."""
        # TODO: Implement _parse_columns method
        pass
    
    def test_parse_column_definition(self):
        """Test individual column definition parsing."""
        # TODO: Implement _parse_column_definition method
        pass
    
    def test_parse_indexes(self):
        """Test index parsing."""
        # TODO: Implement _parse_indexes method
        pass
    
    def test_parse_foreign_keys(self):
        """Test foreign key parsing."""
        # TODO: Implement _parse_foreign_keys method
        pass
    
    def test_parse_table_options(self):
        """Test table options parsing."""
        # TODO: Implement _parse_table_options method
        pass
    
    def test_parse_data_type(self):
        """Test data type parsing."""
        # TODO: Implement _parse_data_type method
        pass
    
    def test_parse_column_constraints(self):
        """Test column constraint parsing."""
        # TODO: Implement _parse_column_constraints method
        pass


class TestDataClasses:
    """Test cases for data classes."""
    
    def test_column_creation(self):
        """Test Column dataclass creation."""
        column = Column(
            name="id",
            data_type="INT",
            nullable=False,
            primary_key=True
        )
        assert column.name == "id"
        assert column.data_type == "INT"
        assert column.nullable is False
        assert column.primary_key is True
        assert column.auto_increment is False  # default value
    
    def test_index_creation(self):
        """Test Index dataclass creation."""
        index = Index(
            name="idx_name",
            columns=["name"],
            unique=True
        )
        assert index.name == "idx_name"
        assert index.columns == ["name"]
        assert index.unique is True
        assert index.primary is False  # default value
    
    def test_foreign_key_creation(self):
        """Test ForeignKey dataclass creation."""
        fk = ForeignKey(
            name="fk_user",
            columns=["user_id"],
            referenced_table="users",
            referenced_columns=["id"],
            on_delete="CASCADE"
        )
        assert fk.name == "fk_user"
        assert fk.columns == ["user_id"]
        assert fk.referenced_table == "users"
        assert fk.referenced_columns == ["id"]
        assert fk.on_delete == "CASCADE"
    
    def test_table_creation(self):
        """Test Table dataclass creation."""
        columns = [
            Column("id", "INT", nullable=False, primary_key=True),
            Column("name", "VARCHAR(255)", nullable=False)
        ]
        table = Table(
            name="users",
            columns=columns,
            indexes=[],
            foreign_keys=[]
        )
        assert table.name == "users"
        assert len(table.columns) == 2
        assert table.columns[0].name == "id"
        assert table.columns[1].name == "name"
    
    def test_schema_creation(self):
        """Test Schema dataclass creation."""
        table = Table("users", [], [], [])
        schema = Schema(tables=[table], name="test_db")
        assert schema.name == "test_db"
        assert len(schema.tables) == 1
        assert schema.tables[0].name == "users"
