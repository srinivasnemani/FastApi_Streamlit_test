from dbutil.dbschema import BrentOptionData
from dbutil.optiondata_dao import DataPersistence
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models.b76_model import B76OptionPricer
from typing import List

class OptionPricer:
    """
    OptionPricer class is responsible for calculating the option prices for the given date_as_of value
    using the B76OptionPricer model and returns a JSONResponse with the calculated option prices.
    Attributes:
    -----------
    persistence : DataPersistence
    An instance of the DataPersistence class for fetching option data.
    Methods:
    --------
    calculate_market_prices(date_as_of: int) -> JSONResponse:
    Calculates option prices for the given date_as_of value using B76OptionPricer model
    and returns a JSONResponse with the calculated option prices.
    """
    def __init__(self, persistence: DataPersistence):
        self.persistence = persistence
        
    async def calculate_market_prices(self, date_as_of: int) -> JSONResponse:
        query = (BrentOptionData.DateAsOf == date_as_of,)
        fetched_data = self.persistence.fetch_records(BrentOptionData, query)
        option_pricer = B76OptionPricer(fetched_data)
        option_prices = option_pricer.calculate_option_prices()
        
        json_str = fetched_data.to_json(orient="records")
        return JSONResponse(content={"success": json_str})
