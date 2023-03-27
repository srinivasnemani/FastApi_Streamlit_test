from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
from sqlalchemy.sql.expression import ClauseElement
import pandas as pd
import os
import datetime
from typing import List


Base = declarative_base()

class DataPersistence(ABC):
    """
    Abstract base class for defining data persistence methods.

    Attributes:
    -----------
    This class has no attributes.

    Methods:
    --------
    create_table(table_class: Base) -> None:
        Abstract method to create a table in a database for a given SQLAlchemy model class.

    add_records(table_class: Base, data: pd.DataFrame) -> None:
        Abstract method to add records to a database table for a given SQLAlchemy model class using a Pandas DataFrame.

    fetch_records(table_class: Base, query) -> pd.DataFrame:
        Abstract method to fetch records from a database table for a given SQLAlchemy model class based on a query and return a Pandas DataFrame.

    delete_records(table_class: Base, query) -> None:
        Abstract method to delete records from a database table for a given SQLAlchemy model class based on a query.

    update_records(table_class: Base, query, update_data) -> None:
        Abstract method to update records in a database table for a given SQLAlchemy model class based on a query and new data.
    """
    
    @abstractmethod
    def create_table(self, table_class: Base):
        pass

    @abstractmethod
    def add_records(self, table_class: Base, data: pd.DataFrame):
        pass

    @abstractmethod
    def fetch_records(self, table_class: Base, query):
        pass

    @abstractmethod
    def delete_records(self, table_class: Base, query):
        pass

    @abstractmethod
    def update_records(self, table_class: Base, query, update_data):
        pass
        
        
class DataPersistenceORM(DataPersistence):
    """
    DataPersistenceORM class is responsible for persisting data to a database using Object-Relational Mapping (ORM).

    Attributes:
    -----------
    database_url : str
        The URL of the database to persist data to.
    engine : sqlalchemy.engine.base.Engine
        The SQLAlchemy engine object used for connecting to the database.
    Session : sqlalchemy.orm.session.sessionmaker
        The SQLAlchemy session object used for interacting with the database.

    Methods:
    --------
    create_table(table_class: sqlalchemy.ext.declarative.api.Base) -> None
        Creates a new database table for the given SQLAlchemy Base class.

    add_records(table_class: sqlalchemy.ext.declarative.api.Base, data: pandas.DataFrame) -> None
        Adds records to the database table for the given SQLAlchemy Base class using ORM and a pandas DataFrame.

    fetch_records(table_class: sqlalchemy.ext.declarative.api.Base, query: Union[str, List[ClauseElement]]=None) -> pandas.DataFrame
        Fetches records from the database table for the given SQLAlchemy Base class based on the query and returns as a DataFrame.

    delete_records(table_class: sqlalchemy.ext.declarative.api.Base, query: List[ClauseElement]) -> None
        Deletes records from the database table for the given SQLAlchemy Base class based on the query.

    update_records(table_class: sqlalchemy.ext.declarative.api.Base, query: List[ClauseElement], update_data: dict) -> None
        Updates records in the database table for the given SQLAlchemy Base class based on the query and update data.

    """
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_table(self, table_class: Base) -> None:
        Base.metadata.create_all(self.engine)

    def add_records(self, table_class: Base, data: pd.DataFrame) -> None:
        session = self.Session()
        try:
            data.to_sql(table_class.__tablename__, self.engine, if_exists='append', index=False)
            ct = datetime.datetime.now()
        except Exception as err_msg:
            raise ValueError(f"Error adding records: {err_msg}")
        finally:
            session.commit()
            session.close()

    def fetch_records(self, table_class: Base, query: ClauseElement = None) -> pd.DataFrame:
        try:
            session = self.Session()
            ct = datetime.datetime.now()

            with self.Session() as session:
                if isinstance(query, str):
                    records = session.query(table_class).filter(text(query))
                else:
                    records = session.query(table_class).filter(and_(*query)).all()

            records_dict = [record.__dict__ for record in records]
            for record in records_dict:
                record.pop('_sa_instance_state', None)
            df = pd.DataFrame(records_dict)
            return df
        except Exception as err_msg:
            ct = datetime.datetime.now()
            raise ValueError(f"Error adding records: {err_msg}")
        finally:
            session.commit()
            session.close()

    def delete_records(self, table_class: Base, query: List[ClauseElement]) -> None:
        session = self.Session()
        try:
            session.query(table_class).filter(and_(*query)).delete()
            session.commit()
        except Exception as err_msg:
            raise ValueError(f"Error deleting records: {err_msg}")
        finally:
            session.close()

    def update_records(self, table_class: Base, query: List[ClauseElement], update_data: dict) -> None:
        session = self.Session()
        try:
            session.query(table_class).filter(and_(*query)).update(update_data)
            session.commit()
        except Exception as err_msg:
            raise ValueError(f"Error updating records: {err_msg}")
        finally:
            session.close()