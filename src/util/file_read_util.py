import configparser
import requests
import streamlit as st
import datetime
import pandas as pd
from fastapi import  HTTPException
import os
from typing import Set

class DataProcessingUtilities():
    """
    A utility class with methods for validating and processing option data files.
    """

    @staticmethod
    def validate_header(option_data: pd.DataFrame, required_columns: Set[str]) -> None:
        """
        Validates if the DataFrame contains the required columns.
        Args:
            option_data (pd.DataFrame): DataFrame containing option data.
            required_columns (Set[str]): Set of required column names.
        Raises:
            ValueError: If the DataFrame does not contain all required columns.
        """
        if set(option_data.columns) != required_columns:
            error_message = "The uploaded file does not contain all required columns. Required columns: " + ", ".join(required_columns)
            raise ValueError(error_message)

    @staticmethod
    def validate_file_type(filename: str) -> None:
        """
        Validates if the uploaded file is in CSV or Excel format.
        Args:
            filename (str): Name of the uploaded file.
        Raises:
            ValueError: If the file format is not CSV or Excel.
        """
        if filename.endswith('.csv'):
            option_data = pd.read_csv(filename)
        elif filename.endswith('.xlsx'):
            option_data = pd.read_excel(filename)
        else:
            raise ValueError("Invalid file format. Please upload a CSV or Excel file.")

    @staticmethod
    def convert_value_error_to_http_error(e: ValueError) -> HTTPException:
        """
        Converts a ValueError to an HTTPException with status code 400.
        Args:
            e (ValueError): The ValueError to convert.
        Returns:
            HTTPException: The resulting HTTPException with status code 400 and the original error message.
        """
        error_message = str(e)
        return HTTPException(status_code=400, detail=error_message)

    @staticmethod
    def read_file(filename: str) -> pd.DataFrame:
        """
        Reads the uploaded file and returns the data as a DataFrame.
        Args:
            filename (str): Name of the uploaded file.
        Returns:
            pd.DataFrame: DataFrame containing the data from the uploaded file.
        Raises:
            ValueError: If the file format is not CSV or Excel.
        """
        DataProcessingUtilities.validate_file_type(filename)
        with open(filename, 'rb') as file:
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        return df
