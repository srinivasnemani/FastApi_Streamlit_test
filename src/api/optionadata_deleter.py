from typing import Any
from fastapi.responses import JSONResponse
from dbutil.optiondata_dao import DataPersistence
from dbutil.dbschema import BrentOptionData
from util.app_logger import logger_decorator
import pandas as pd

class OptionDataDeleter:
    """
    OptionDataDeleter class is responsible for deleting the market data
    from the database using the DataPersistence object.

    Attributes:
    -----------
    persistence : DataPersistence
        An instance of the DataPersistence class for fetching option data.

    Methods:
    --------
    delete_records_asof(date_as_of: int) -> None
        Fetches option data records for the given date_as_of and returns a JSONResponse.

    """

    def __init__(self, persistence: DataPersistence):
        self.persistence = persistence

    @logger_decorator
    async def delete_records_asof(self, date_as_of: int) -> None:
        query = (BrentOptionData.DateAsOf == date_as_of,)
        fetched_data = self.persistence.delete_records(BrentOptionData, query)
        return JSONResponse(content={"success": "Records Deleted"})
