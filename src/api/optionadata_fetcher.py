from typing import Any
from fastapi.responses import JSONResponse
from dbutil.optiondata_dao import DataPersistence
from dbutil.dbschema import BrentOptionData
from util.app_logger import logger_decorator
import pandas as pd

class OptionDataFetcher:
    """
    OptionDataFetcher class is responsible for fetching option data
    from the database using the DataPersistence object.

    Attributes:
    -----------
    persistence : DataPersistence
        An instance of the DataPersistence class for fetching option data.

    Methods:
    --------
    fetch_records_asof(date_as_of: int) -> JSONResponse
        Fetches option data records for the given date_as_of and returns a JSONResponse.

    fetch_distinct_dates() -> JSONResponse
        Fetches all distinct dates available in the option data and returns a JSONResponse.
    """

    def __init__(self, persistence: DataPersistence):
        self.persistence = persistence

    @logger_decorator
    async def fetch_records_asof(self, date_as_of: int) -> JSONResponse:
        query = (BrentOptionData.DateAsOf == date_as_of,)
        fetched_data = self.persistence.fetch_records(BrentOptionData, query)
        json_str = fetched_data.to_json(orient="records")
        return JSONResponse(content={"success": json_str})

    @logger_decorator
    async def fetch_distinct_dates(self) -> JSONResponse:
        query = (BrentOptionData.DateAsOf,)
        fetched_data = self.persistence.fetch_records(BrentOptionData, query)
        unique_dates = fetched_data["DateAsOf"].unique()

        # Convert the unique_dates Series to a JSON string and return it.
        json_str = pd.Series(unique_dates).to_json(orient="values")
        return JSONResponse(content={"success": json_str})
