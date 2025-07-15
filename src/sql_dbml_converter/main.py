"""
Main CLI entry point for the SQL-DBML-Converter.
"""

import click
import sys
from pathlib import Path
from typing import Optional

from .parser.sql_parser import SQLParser
from .converter.dbml_generator import DBMLGenerator
from .utils.file_handler import FileHandler
from .utils.validators import InputValidator


@click.command()
@click.option(
    "--input", "-i",
    type=click.Path(exists=True, path_type=Path),
    help="Input SQL file containing CREATE TABLE statements"
)
@click.option(
    "--output", "-o",
    type=click.Path(path_type=Path),
    help="Output DBML file path"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.version_option()
def main(input: Optional[Path], output: Optional[Path], verbose: bool) -> None:
    """
    Convert MySQL CREATE TABLE statements to DBML format.
    
    If no input file is specified, reads from stdin.
    If no output file is specified, writes to stdout.
    """
    try:
        # Initialize components
        file_handler = FileHandler()
        validator = InputValidator()
        parser = SQLParser()
        generator = DBMLGenerator()
        
        # Read input
        if input:
            if verbose:
                click.echo(f"Reading from file: {input}")
            sql_content = file_handler.read_file(input)
        else:
            if verbose:
                click.echo("Reading from stdin...")
            sql_content = sys.stdin.read()
        
        # Validate input
        if not validator.validate_sql_input(sql_content):
            click.echo("Error: Invalid SQL input", err=True)
            sys.exit(1)
        
        # Parse SQL
        if verbose:
            click.echo("Parsing SQL statements...")
        parsed_schema = parser.parse(sql_content)
        
        # Generate DBML
        if verbose:
            click.echo("Generating DBML...")
        dbml_output = generator.generate(parsed_schema)
        
        # Write output
        if output:
            if verbose:
                click.echo(f"Writing to file: {output}")
            file_handler.write_file(output, dbml_output)
        else:
            click.echo(dbml_output)
        
        if verbose:
            click.echo("Conversion completed successfully!")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
