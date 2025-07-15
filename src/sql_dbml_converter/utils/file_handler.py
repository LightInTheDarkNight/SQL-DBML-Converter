"""
File handling utilities for the SQL-DBML-Converter.
"""

import os
from pathlib import Path
from typing import Optional


class FileHandler:
    """Handles file I/O operations for the converter."""
    
    def __init__(self):
        pass
    
    def read_file(self, file_path: Path) -> str:
        """
        Read content from a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except IOError as e:
            raise IOError(f"Error reading file {file_path}: {str(e)}")
    
    def write_file(self, file_path: Path, content: str) -> None:
        """
        Write content to a file.
        
        Args:
            file_path: Path to the file to write
            content: Content to write
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except IOError as e:
            raise IOError(f"Error writing file {file_path}: {str(e)}")
    
    def file_exists(self, file_path: Path) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return file_path.exists() and file_path.is_file()
    
    def get_file_extension(self, file_path: Path) -> str:
        """
        Get file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File extension (without dot)
        """
        return file_path.suffix.lstrip('.')
    
    def validate_file_path(self, file_path: Path, must_exist: bool = True) -> bool:
        """
        Validate file path.
        
        Args:
            file_path: Path to validate
            must_exist: Whether file must exist
            
        Returns:
            True if path is valid
        """
        if must_exist:
            return self.file_exists(file_path)
        
        # Check if parent directory exists or can be created
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except (OSError, PermissionError):
            return False
    
    def get_file_size(self, file_path: Path) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not self.file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return file_path.stat().st_size
    
    def backup_file(self, file_path: Path, backup_suffix: str = ".bak") -> Path:
        """
        Create a backup of a file.
        
        Args:
            file_path: Path to the file to backup
            backup_suffix: Suffix for backup file
            
        Returns:
            Path to backup file
            
        Raises:
            FileNotFoundError: If original file doesn't exist
            IOError: If backup cannot be created
        """
        if not self.file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
        
        try:
            content = self.read_file(file_path)
            self.write_file(backup_path, content)
            return backup_path
        except IOError as e:
            raise IOError(f"Error creating backup: {str(e)}")
    
    def read_file_lines(self, file_path: Path) -> list[str]:
        """
        Read file content as list of lines.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            List of lines from the file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        content = self.read_file(file_path)
        return content.splitlines()
    
    def append_to_file(self, file_path: Path, content: str) -> None:
        """
        Append content to a file.
        
        Args:
            file_path: Path to the file
            content: Content to append
            
        Raises:
            IOError: If file cannot be written
        """
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(content)
        except IOError as e:
            raise IOError(f"Error appending to file {file_path}: {str(e)}")
    
    def is_sql_file(self, file_path: Path) -> bool:
        """
        Check if file is a SQL file based on extension.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file has SQL extension
        """
        sql_extensions = {'sql', 'ddl', 'dml'}
        return self.get_file_extension(file_path).lower() in sql_extensions
    
    def is_dbml_file(self, file_path: Path) -> bool:
        """
        Check if file is a DBML file based on extension.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file has DBML extension
        """
        dbml_extensions = {'dbml'}
        return self.get_file_extension(file_path).lower() in dbml_extensions
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename by removing invalid characters.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        sanitized = filename
        
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        
        # Ensure filename is not empty
        if not sanitized:
            sanitized = "untitled"
        
        return sanitized
