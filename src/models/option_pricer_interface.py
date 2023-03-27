from abc import ABC, abstractmethod
import configparser
import requests
import streamlit as st
import pandas as pd
from typing import Optional

class IOptionPricer(ABC):
    """
    An abstract base class to represent option pricing models.
    Attributes
    ----------
    model_name : str
        The name of the option pricing model.
    market_data : pd.DataFrame
        A DataFrame containing the market data for option pricing.

    Methods
    -------
    calculate_option_prices()
        An abstract method to be implemented by subclasses for calculating option prices.
    """

    def __init__(self, model_name: str, market_data: pd.DataFrame):
        self.model_name = model_name
        self.market_data = market_data

    @abstractmethod
    def calculate_option_prices(self) -> pd.DataFrame:
        pass
