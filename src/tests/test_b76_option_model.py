import pytest
import pandas as pd
from models.b76_model import B76OptionPricer

"""
This module contains test cases for the B76OptionPricer class in the b76_model module.
It uses sample_market_data and expected_option_prices to test the correctness of the calculate_option_prices method.
"""

# Sample market data for testing
sample_market_data = pd.DataFrame({
    'DateAsOf': [20220101, 20220101],
    'FutureExpiryDate': [20230130, 20230130],
    'OptionType': ['Call', 'Put'],
    'StrikePrice': [50.0, 50.0],
    'CurrentPrice': [40, 40],
    'ImpliedVol': [0.15, 0.15]
})

# Expected option prices for the sample market data
expected_option_prices = [0.1068075255, 9.66089102470656]  # Replace with the correct expected prices

@pytest.fixture
def b76_option_pricer():
    """
    Pytest fixture for initializing an instance of B76OptionPricer with the sample_market_data.
    Returns: B76OptionPricer instance.
    """
    return B76OptionPricer(sample_market_data)

def test_b76_option_pricer(b76_option_pricer):
    """
    Test case for the calculate_option_prices method of the B76OptionPricer class.
    It checks whether the calculated option prices are equal to the expected_option_prices within a given tolerance.
    
    Args:
        b76_option_pricer (B76OptionPricer): Instance of the B76OptionPricer class initialized with sample_market_data.
    """
    calculated_option_prices = b76_option_pricer.calculate_option_prices()
    assert len(calculated_option_prices) == len(sample_market_data)
    
    for index, row in calculated_option_prices.iterrows():
        assert row['OptionPrice'] == pytest.approx(expected_option_prices[index], abs=1e-6)
