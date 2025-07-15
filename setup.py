"""
Setup script for SQL-DBML-Converter package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="sql-dbml-converter",
    version="0.1.0",
    author="SQL-DBML-Converter Team",
    author_email="",
    description="Convert MySQL CREATE TABLE statements to DBML format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LightInTheDarkNight/SQL-DBML-Converter",
    project_urls={
        "Bug Reports": "https://github.com/LightInTheDarkNight/SQL-DBML-Converter/issues",
        "Source": "https://github.com/LightInTheDarkNight/SQL-DBML-Converter",
        "Documentation": "https://github.com/LightInTheDarkNight/SQL-DBML-Converter/blob/main/docs/usage.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sql-dbml-converter=sql_dbml_converter.main:main",
        ],
    },
    keywords=[
        "sql", "dbml", "database", "schema", "mysql", "converter", 
        "dbdiagram", "database-design", "sql-parser"
    ],
    include_package_data=True,
    package_data={
        "sql_dbml_converter": ["py.typed"],
    },
    zip_safe=False,
)
