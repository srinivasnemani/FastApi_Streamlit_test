"""

This package provides classes and functions for working with market data in a 
database using Object-Relational Mapping (ORM). The package contains the following classes:

BrentOptionData: A class representing the BrentOptionData table in the database, used in 
Object Relational Mapping libraries to create a table in the databases.

get_brent_option_data_schema: A function that returns the BrentOptionData schema.

DataPersistenceORM: A class responsible for persisting data to a database using 
Object-Relational Mapping (ORM). It has several methods for 
creating, adding, fetching, deleting, and updating records in a database table 
for a given SQLAlchemy Base class. 
The class has attributes for the database URL, SQLAlchemy engine, and session objects used for interacting with the database.

"""