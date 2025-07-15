"""
SQL-DBML-Converter: A Python tool to convert MySQL CREATE TABLE statements to DBML format.
"""

__version__ = "0.1.0"
__author__ = "SQL-DBML-Converter Team"
__description__ = "Convert MySQL CREATE TABLE statements to DBML format"

from .main import main
from .parser.sql_parser import SQLParser
from .converter.dbml_generator import DBMLGenerator

__all__ = ["main", "SQLParser", "DBMLGenerator"]
