import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from api.option_pricer import OptionPricer
from dbutil.optiondata_dao import DataPersistence
import pandas as pd
import json

"""
This module contains test cases for the OptionPricer class in the api.option_pricer module.
It uses the MockDataPersistence_Call and MockDataPersistence_Put classes to provide mock data for testing.
The test cases validate the correctness of the calculate_market_prices method for both call and put options.
"""

# Mock DataPersistence class to avoid database calls
class MockDataPersistence_Call(DataPersistence):
    """
    A mock DataPersistence class for call options that returns sample data instead of making database calls.
    """

    def fetch_records(self, *args, **kwargs):
        # Return sample data instead of making a database call
        data = {
            "DateAsOf": [20220101],
            "FutureExpiryDate": [20230130],
            "OptionType": ["Call"],
            "StrikePrice": [50.0],
            "CurrentPrice": [40],
            "ImpliedVol": [0.15]
        }
        return pd.DataFrame(data)

    # Added for mocking as DataPersistence its an Interface and inherited class be instantiated without out the overriding the methods
    def add_records(self, *args, **kwargs):
        # Added for mocking
        pass

    def create_table(self, *args, **kwargs):
        # Added for mocking
        pass

    def delete_records(self, *args, **kwargs):
        # Do nothing or return a default value
        pass

    def update_records(self, *args, **kwargs):
        # Do nothing or return a default value
        pass
        
class MockDataPersistence_Put(DataPersistence):
   """
    A mock DataPersistence class for put options that returns sample data instead of making database calls.
    """
   def fetch_records(self, *args, **kwargs):
        # Return sample data instead of making a database call
        data = {
            "DateAsOf": [20220101],
            "FutureExpiryDate": [20230130],
            "OptionType": ["Put"],
            "StrikePrice": [50.0],
            "CurrentPrice": [30],
            "ImpliedVol": [0.20]
        }
        return pd.DataFrame(data)
   
   def add_records(self, *args, **kwargs):
        pass

   def create_table(self, *args, **kwargs):
        pass

   def delete_records(self, *args, **kwargs):
        pass

   def update_records(self, *args, **kwargs):
        pass
        

@pytest.fixture
def option_pricer_call():
    """
    Pytest fixture for initializing an instance of OptionPricer with the MockDataPersistence_Call instance.
    Returns: OptionPricer instance.
    """
    mock_persistence = MockDataPersistence_Call()
    return OptionPricer(mock_persistence)


@pytest.fixture
def option_pricer_put():
    """
    Pytest fixture for initializing an instance of OptionPricer with the MockDataPersistence_Put instance.
    Returns: OptionPricer instance.
    """
    mock_persistence = MockDataPersistence_Put()
    return OptionPricer(mock_persistence)


@pytest.mark.asyncio
async def test_validate_call_prices(option_pricer_call):
    """
        Test case for the calculate_market_prices method of the OptionPricer class for call options.
        It checks whether the calculated option price is equal to the expected call option value within
        
    Args:
        option_pricer_call (OptionPricer): Instance of the OptionPricer class initialized with MockDataPersistence_Call.
    """

    date_as_of = 20220101
    CALL_OPTION_VALUE = 0.1068075255
    response = await option_pricer_call.calculate_market_prices(date_as_of)

    assert response.status_code == 200
    json_content = response.body
    
    #Validate the content body.
    import json
    json_data = json.loads(json_content)
    
    assert "success" in json_data
    success_data = json.loads(json_data["success"])
    option_price = success_data[0]["OptionPrice"]
    
    tolerance_value = 1e-6
    assert option_price == pytest.approx(CALL_OPTION_VALUE, abs=tolerance_value)

@pytest.mark.asyncio
async def test_validate_put_prices(option_pricer_put):
    """
        See the comments of above test_validate_call_prices
    """
    date_as_of = 20220101
    PUT_OPTION_VALUE = 19.11287473
    response = await option_pricer_put.calculate_market_prices(date_as_of)

    assert response.status_code == 200
    json_content = response.body
    
    #Validate the content body.
    import json
    json_data = json.loads(json_content)
    
    assert "success" in json_data
    success_data = json.loads(json_data["success"])
    option_price = success_data[0]["OptionPrice"]
    
    tolerance_value = 1e-6
    assert option_price == pytest.approx(PUT_OPTION_VALUE, abs=tolerance_value)