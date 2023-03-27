from fastapi import UploadFile, HTTPException, File, Header, Request
from pydantic import BaseModel
from dbutil.dbschema import BrentOptionData
from dbutil.optiondata_dao import DataPersistence, DataPersistenceORM
import pandas as pd
from util.file_read_util import DataProcessingUtilities
import io
import json
from typing import Optional, List
import gzip
import os
from util.app_logger import logger_decorator

REQUIRED_COLUMNS = {'DateAsOf', 'FutureExpiryDate', 'OptionType', 'StrikePrice', 'CurrentPrice', 'ImpliedVol'}

class MarketDataPydantic(BaseModel):
    """
        Represents structure for validating the received JSON body
    """
    DateAsOf: Optional[int]
    FutureExpiryDate: Optional[int]
    OptionType: Optional[str]
    StrikePrice: Optional[float]
    CurrentPrice: Optional[float]
    ImpliedVol: Optional[float]

class MarketDataList(BaseModel):
    data: List[MarketDataPydantic]

column_names = ['DateAsOf', 'FutureExpiryDate', 'OptionType', 'StrikePrice', 'CurrentPrice', 'ImpliedVol']

class OptionDataUploader:
    """
    OptionDataUploader class is responsible for uploading option data
    to the database using the DataPersistence object.
    
    Attributes:
    -----------
    persistence : DataPersistence
        An instance of the DataPersistence class for uploading option data.

    Methods:
    --------
    load_market_data_json(market_data_list: MarketDataList) -> dict
        Uploads market data from a JSON formatted list to the database.

    load_market_data_file(file: UploadFile) -> dict
        Uploads market data from a file to the database.

    load_market_data_iostream(request: Request, content_encoding: str) -> dict
        Processes a market data file compressed in gzip format or provided as an iostream.
    """

    def __init__(self, persistence: DataPersistence):
        self.persistence = persistence

    @logger_decorator
    async def load_market_data_json(self, market_data_list: MarketDataList) -> dict:
        os.system('cls' if os.name == 'nt' else 'clear')
        item = market_data_list.data
        df = pd.DataFrame(item, columns=column_names)
        for column in column_names:
            df[column] = df[column].apply(lambda x: x[1])

        self.persistence.add_records(BrentOptionData, df)
        return {"success": "Json market data uploaded to database."}

    @logger_decorator
    async def load_market_data_file(self, file: UploadFile) -> dict:
        try:
            DataProcessingUtilities.validate_file_type(file.filename)
            market_data_df = DataProcessingUtilities.read_file(file.filename)
            DataProcessingUtilities.validate_header(market_data_df, REQUIRED_COLUMNS)
        except ValueError as e:
            DataProcessingUtilities.convert_value_error_to_http_error(ValueError)

        self.persistence.add_records(BrentOptionData, market_data_df)
        return {"success": "Market data from the given file uploaded successfully."}

    @logger_decorator
    async def load_market_data_iostream(self, request: Request, content_encoding: str = Header(None)) -> dict:
        #Note: This funciton is a place holder api end point for retrieving stream data from another api end point or 
        # from other streaming servers/services. Its not fully implemented and tested..
        try:
            if content_encoding == "gzip":
                compressed_data = io.BytesIO(content_encoding)
                market_data = gzip.open(compressed_data, "rb")
            else:
                market_data = io.BytesIO(content_encoding).getvalue()
        except ValueError as e:
            DataProcessingUtilities.convert_value_error_to_http_error(ValueError)
        return {"success": "gzip or iostream file is processed."}
