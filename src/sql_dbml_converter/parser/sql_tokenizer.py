"""
SQL tokenizer for breaking down SQL statements into manageable tokens.
"""

import re
from typing import List, Tuple, Optional
from enum import Enum


class TokenType(Enum):
    """Types of SQL tokens."""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    PUNCTUATION = "PUNCTUATION"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    UNKNOWN = "UNKNOWN"


class Token:
    """Represents a SQL token."""
    
    def __init__(self, token_type: TokenType, value: str, position: int):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.position})"


class SQLTokenizer:
    """Tokenizer for SQL statements."""
    
    # MySQL keywords relevant to CREATE TABLE statements
    KEYWORDS = {
        'CREATE', 'TABLE', 'IF', 'NOT', 'EXISTS', 'TEMPORARY',
        'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'UNIQUE',
        'INDEX', 'CONSTRAINT', 'CHECK', 'DEFAULT', 'NULL',
        'AUTO_INCREMENT', 'COMMENT', 'ENGINE', 'CHARSET',
        'COLLATE', 'ON', 'DELETE', 'UPDATE', 'CASCADE',
        'RESTRICT', 'SET', 'NO', 'ACTION', 'GENERATED',
        'ALWAYS', 'AS', 'STORED', 'VIRTUAL'
    }
    
    # Data types
    DATA_TYPES = {
        'INT', 'INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT',
        'VARCHAR', 'CHAR', 'TEXT', 'LONGTEXT', 'MEDIUMTEXT',
        'DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE', 'REAL',
        'DATE', 'TIME', 'DATETIME', 'TIMESTAMP', 'YEAR',
        'BOOLEAN', 'BOOL', 'JSON', 'BLOB', 'LONGBLOB',
        'MEDIUMBLOB', 'TINYBLOB', 'BINARY', 'VARBINARY',
        'ENUM', 'SET', 'GEOMETRY', 'POINT', 'LINESTRING',
        'POLYGON', 'MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON',
        'GEOMETRYCOLLECTION'
    }
    
    def __init__(self):
        self.tokens = []
        self.position = 0
        self.text = ""
    
    def tokenize(self, sql_text: str) -> List[Token]:
        """
        Tokenize SQL text into a list of tokens.
        
        Args:
            sql_text: SQL statement text
            
        Returns:
            List of Token objects
        """
        self.text = sql_text
        self.position = 0
        self.tokens = []
        
        while self.position < len(self.text):
            self._skip_whitespace()
            
            if self.position >= len(self.text):
                break
            
            token = self._next_token()
            if token:
                self.tokens.append(token)
        
        return self.tokens
    
    def _next_token(self) -> Optional[Token]:
        """Get the next token from the current position."""
        if self.position >= len(self.text):
            return None
        
        char = self.text[self.position]
        
        # Comments
        if char == '-' and self._peek() == '-':
            return self._read_line_comment()
        elif char == '/' and self._peek() == '*':
            return self._read_block_comment()
        
        # Strings
        elif char in ('"', "'", '`'):
            return self._read_string(char)
        
        # Numbers
        elif char.isdigit():
            return self._read_number()
        
        # Identifiers and keywords
        elif char.isalpha() or char == '_':
            return self._read_identifier()
        
        # Operators and punctuation
        elif char in '()[]{},.;':
            token = Token(TokenType.PUNCTUATION, char, self.position)
            self.position += 1
            return token
        
        elif char in '=<>!':
            return self._read_operator()
        
        else:
            # Unknown character
            token = Token(TokenType.UNKNOWN, char, self.position)
            self.position += 1
            return token
    
    def _peek(self, offset: int = 1) -> str:
        """Peek at the character at current position + offset."""
        pos = self.position + offset
        return self.text[pos] if pos < len(self.text) else ''
    
    def _skip_whitespace(self):
        """Skip whitespace characters."""
        while (self.position < len(self.text) and 
               self.text[self.position].isspace()):
            self.position += 1
    
    def _read_string(self, quote_char: str) -> Token:
        """Read a quoted string token."""
        start_pos = self.position
        value = quote_char
        self.position += 1
        
        while self.position < len(self.text):
            char = self.text[self.position]
            value += char
            self.position += 1
            
            if char == quote_char:
                break
            elif char == '\\' and self.position < len(self.text):
                # Handle escaped characters
                value += self.text[self.position]
                self.position += 1
        
        return Token(TokenType.STRING, value, start_pos)
    
    def _read_number(self) -> Token:
        """Read a numeric token."""
        start_pos = self.position
        value = ""
        
        while (self.position < len(self.text) and 
               (self.text[self.position].isdigit() or 
                self.text[self.position] == '.')):
            value += self.text[self.position]
            self.position += 1
        
        return Token(TokenType.NUMBER, value, start_pos)
    
    def _read_identifier(self) -> Token:
        """Read an identifier or keyword token."""
        start_pos = self.position
        value = ""
        
        while (self.position < len(self.text) and 
               (self.text[self.position].isalnum() or 
                self.text[self.position] == '_')):
            value += self.text[self.position]
            self.position += 1
        
        # Check if it's a keyword or data type
        upper_value = value.upper()
        if upper_value in self.KEYWORDS or upper_value in self.DATA_TYPES:
            token_type = TokenType.KEYWORD
        else:
            token_type = TokenType.IDENTIFIER
        
        return Token(token_type, value, start_pos)
    
    def _read_operator(self) -> Token:
        """Read an operator token."""
        start_pos = self.position
        char = self.text[self.position]
        value = char
        self.position += 1
        
        # Handle multi-character operators
        if char == '<' and self._peek(0) == '=':
            value += '='
            self.position += 1
        elif char == '>' and self._peek(0) == '=':
            value += '='
            self.position += 1
        elif char == '!' and self._peek(0) == '=':
            value += '='
            self.position += 1
        elif char == '<' and self._peek(0) == '>':
            value += '>'
            self.position += 1
        
        return Token(TokenType.OPERATOR, value, start_pos)
    
    def _read_line_comment(self) -> Token:
        """Read a line comment (-- comment)."""
        start_pos = self.position
        value = ""
        
        while (self.position < len(self.text) and 
               self.text[self.position] != '\n'):
            value += self.text[self.position]
            self.position += 1
        
        return Token(TokenType.COMMENT, value, start_pos)
    
    def _read_block_comment(self) -> Token:
        """Read a block comment (/* comment */)."""
        start_pos = self.position
        value = ""
        self.position += 2  # Skip /*
        value += "/*"
        
        while self.position < len(self.text) - 1:
            if (self.text[self.position] == '*' and 
                self.text[self.position + 1] == '/'):
                value += "*/"
                self.position += 2
                break
            else:
                value += self.text[self.position]
                self.position += 1
        
        return Token(TokenType.COMMENT, value, start_pos)
    
    def filter_tokens(self, tokens: List[Token], 
                     exclude_types: List[TokenType] = None) -> List[Token]:
        """
        Filter tokens by excluding certain types.
        
        Args:
            tokens: List of tokens to filter
            exclude_types: List of token types to exclude
            
        Returns:
            Filtered list of tokens
        """
        if exclude_types is None:
            exclude_types = [TokenType.WHITESPACE, TokenType.COMMENT]
        
        return [token for token in tokens if token.type not in exclude_types]
