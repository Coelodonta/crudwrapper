# crudwrapper
Python 3 script to generate wrapper classes for SQL CRUD (Create Read Update Delete) stored procedures from PHP and Python

The script uses SQL DDL scripts generated by crudomatic (https://github.com/Coelodonta/crudomatic) as input. 
It's possible that it will work with scripts generated by other tools, but this has not been tested. 

Current vesrion supports PHP and Python CRUD wrappers for MySQL.

Usage:

./crudwrapper.py

Requirements:

Python 3

Road Map:
- PHP Wrappers for PostgresQL
- Python Wrappers for PostgresQL
- Support for command line (currently always uses input file named "./crudomatic_procedures.sql" and fixed names for output files)
- MS SQL wrappers in PHP and Python?
- Support for other programming languages




