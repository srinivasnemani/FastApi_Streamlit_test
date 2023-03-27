import configparser
import requests
from fastapi import HTTPException
import streamlit as st
from gui.webpage_interface import IWebPage
import pandas as pd
import json
from datetime import datetime
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Span, Label, Legend
import base64
import numpy as np

class DataAnalysisPage(IWebPage):

    """
    The code defines a DataAnalysisPage class which inherits from an IWebPage class. 
    This web page contains options to fetch and dispaly unique number of data dates available in the database.
    When user selects a particular date, it calculates the option prices and shows the data in tabular format.
    It also shows the option prices in graphs and provides options to download the data.
    """
    
    def __init__(self, config_file, session_state):
        super().__init__(config_file, session_state)

    def render_the_page(self):
        # Create two columns
        left_column, right_column = st.columns([1, 4])
        
        #Add some session data variables.
        if "page2_selected_date" not in st.session_state:
            st.session_state["page2_selected_date"] = None

        # Add two containers to the left column

        with right_column:
            container_R1 = st.container()
            container_R2 = st.container()
            
        with left_column:
            container_L1 = st.container()
            #container_L2 = st.container()  
            with container_L1:
                st.markdown('<div style="background-color: #f4f4f4; padding: 10px;">Avaialble Data Dates</div>', unsafe_allow_html=True)

                unique_dates = None
                if "unique_dates" not in st.session_state:
                    st.session_state["unique_dates"] = None

                if st.button("Fetch Unique Data dates"):
                
                    config_url_fetch_unique_dates = self.config.get("GUI_URLS", "fetchuniqutedatesURL")
                    host = self.config.get("API", "host")
                    port = self.config.get("API", "port")
                    url_fetch_unique_dates =  "http://" + host + ":" + port  + config_url_fetch_unique_dates                
                    response_unique_dates = requests.get(url_fetch_unique_dates)
                    response_unique_dates_str = response_unique_dates.text

                    # Parse the top-level JSON object
                    response_unique_dates_obj = json.loads(response_unique_dates_str)

                    # Extract the "success" value as a string
                    dates_str = response_unique_dates_obj["success"]
                    dates_arr = json.loads(dates_str)
                    unique_dates = pd.DataFrame(dates_arr, columns=["date"])
                    # Convert the date column to datetime objects (for formatting)
                    unique_dates["date"] = pd.to_datetime(unique_dates["date"], format="%Y%m%d")
                    unique_dates["date"] = unique_dates["date"].dt.strftime("%Y-%m-%d")
                    st.session_state.unique_dates = unique_dates
                
                
                if st.session_state.unique_dates is not None:
                    selected_date = st.session_state.get("selected_date", None)
                    st.session_state.selected_date = st.selectbox('Select a date from the drop-down:', st.session_state.unique_dates["date"], key="date_selectbox")
                    selected_date = st.session_state.selected_date
                    st.session_state.page2_selected_date   = selected_date


                if st.session_state["page2_selected_date"] is not None:                
                    st.write(f"Selected Date is: ", st.session_state.page2_selected_date)
                    
                    
                if st.button("Fecth Option Data for the Selected Dates"):
                    try:
                        if st.session_state["page2_selected_date"] is not None:
                            #st.write(f"Feching market data for the Date is: ", st.session_state.page2_selected_date)
                            selected_date_obj = datetime.strptime(st.session_state.page2_selected_date, "%Y-%m-%d")
                            selected_date_yyyymmdd = selected_date_obj.strftime("%Y%m%d")
                            
                            config_url_fetch_data_as_of = self.config.get("GUI_URLS", "calculateoptionpricesURL")
                            host = self.config.get("API", "host")
                            port = self.config.get("API", "port")
                            market_data_fetch_api_end_point =  "http://" + host + ":" + port  + "/" + config_url_fetch_data_as_of                              
                            url_option_price_data_fetch_asof =  market_data_fetch_api_end_point + selected_date_yyyymmdd 
                            
                            response_marekt_data_selected_date = requests.get(url_option_price_data_fetch_asof)
                            response_selected_market_data = response_marekt_data_selected_date.text
                            response_selected_dates_obj = json.loads(response_selected_market_data)
                            response_selected_dates_str = response_selected_dates_obj["success"]
                            response_selected_dates_str =  json.loads(response_selected_dates_str)
                            option_price_data_df = self.format_the_data_frame_for_printing(pd.DataFrame(response_selected_dates_str))

                            self.write_this_data_in_C1(container_R1, option_price_data_df)
                            self.create_option_pricing_plot(container_R2, option_price_data_df)
                    except HTTPException as e:
                        st.error(e.detail)    
                        
    def write_this_data_in_C1(self, container_R1, option_price_data_df):
        with container_R1:
            st.write(option_price_data_df)
            filename_option_prices = "OptionPricesData.csv"
            csv = option_price_data_df.to_csv(index=False).encode('utf-8')
            st.download_button('Press to Download Option Prices CSV', csv, filename_option_prices, "text/csv", key='download-csv')
         
    def create_option_pricing_plot(self, container_R2, option_price_data_df):
        with container_R2:
            df = option_price_data_df
            df = df.reset_index(drop=True)

            option_types = df['OptionType'].unique()
            for option_type in option_types:
                filtered_data = df[df['OptionType'] == option_type]
                number_of_rows = filtered_data.shape[0]

                x = filtered_data["StrikePrice"].tolist()
                y1 = filtered_data["OptionPrice"].tolist()
                y2 = filtered_data["CurrentPrice"].tolist()
                chart_loc_current_price_line = int(y2[0])

                source = ColumnDataSource(data=dict(x=x, y1=y1, y2=y2))
                y1_range = np.ptp(filtered_data["OptionPrice"])
                y1_20pct_range = y1_range * 0.2
                y_axis_min_point = min(y1) - y1_20pct_range
                y_axis_max_point = max(y1) + y1_20pct_range

                y_axis_label_updated = f"{option_type} Price"
                p = figure(title=f"{option_type} Option Price vs Current Price", x_axis_label='Strike Price', y_axis_label=y_axis_label_updated, y_range=(y_axis_min_point, y_axis_max_point))

                p.line('x', 'y1', source=source, color='blue', line_width=2, legend_label=f'{option_type} Option Price')
                vline = Span(location=chart_loc_current_price_line, dimension='height', line_color='orange', line_width=2, line_dash='dashed')
                p.add_layout(vline)
                my_label = Label(x=chart_loc_current_price_line, y=30, y_units='screen', text='Current Price of the future')
                p.add_layout(my_label)

                p.legend.location = "top_left"
                p.legend.click_policy="hide"

                st.bokeh_chart(p)

    def format_the_data_frame_for_printing(self, option_price_data_df):
        # Sort the columns in the specified order
        sorted_columns = ["DateAsOf", "FutureExpiryDate", "OptionType", "StrikePrice", "CurrentPrice", "ImpliedVol", "OptionPrice"]
        sorted_df = option_price_data_df[sorted_columns]
        
        # Format DateAsOf and FutureExpiryDate columns to "YYYY-MM-DD"
        sorted_df["DateAsOf"] = pd.to_datetime(sorted_df["DateAsOf"], format="%Y%m%d").dt.strftime("%Y-%m-%d")
        sorted_df["FutureExpiryDate"] = pd.to_datetime(sorted_df["FutureExpiryDate"], format="%Y%m%d").dt.strftime("%Y-%m-%d")
        return sorted_df

