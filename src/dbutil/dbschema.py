from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, PrimaryKeyConstraint

Base = declarative_base()

class BrentOptionData(Base):
    """
        A class representing the BrentOptionData table in the database.
        Used in Object Relational Mapping libraries to create a table in the databases.
    """
    __tablename__ = 'BrentOptionData'
    DateAsOf = Column(Integer)
    FutureExpiryDate = Column(Integer)
    OptionType = Column(String(10))
    StrikePrice = Column(Float)
    CurrentPrice = Column(Float)
    ImpliedVol = Column(Float)
    __table_args__ = (PrimaryKeyConstraint('DateAsOf', 'FutureExpiryDate', 'OptionType', 'StrikePrice'), {})


def get_optiondata_dbschmea():
    """
    A function that returns the BrentOptionData schema.
    Returns : "Base" schema of BrentOptionData table.
    """
    return Base