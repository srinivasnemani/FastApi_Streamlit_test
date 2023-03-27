import streamlit as st
from fastapi import HTTPException
import pandas as pd
from gui.webpage_interface import IWebPage
import requests
import os
import io        
import json
from util.file_read_util import DataProcessingUtilities

class DataUploadPage(IWebPage):
    """
        The DataAnalysisPage class is a subclass of the 'IWebPage' abstract base class. It renders a web page 
        to give option to upload the market data from a CSV or Excel. When any other file formatters are 
        provided it shows an error messages. When the data is successfully uploaded, it shows the uploaded data 
        in a data frame.
    """    
    def __init__(self, config_file, session_state):
        super().__init__(config_file=config_file, session_state=session_state)
        self.file = None      

    def render_the_page(self):
        st.title("Upload market data")        
        self.file = st.file_uploader("Upload a file", type=["csv", "xlsx"])
        if self.file is not None:
            if st.button("Submit"):
                try:
                    self.load_market_data_df()
                except HTTPException as e:
                    st.error(e.detail)
                
        if "session_count" not in st.session_state:
            st.session_state["session_count"] = 0   
            
        if "recent_uploaded_data_date" not in st.session_state:
            st.session_state["recent_uploaded_data_date"] = None
            st.session_state["recent_uploaded_market_data"] = None

        if st.session_state["recent_uploaded_data_date"] is not None:
            st.write("Below is the recently uploaded data.")
            st.write(st.session_state["recent_uploaded_market_data"])
        
        
    #@st.cache_resource 
    def load_market_data_df(_self):
        url_config = _self.config.get("GUI_URLS", "loadmarketdataURL")
        host = _self.config.get("API", "host")
        port = _self.config.get("API", "port")
        url =  "http://" + host + ":" + port  + url_config
        #Get Dynamically from Config file.
        #url =  "http://127.0.0.1:8080/loadmarketdatajson" 
        
        files = {"file": _self.file}
        st.write(_self.file.name)
        DataProcessingUtilities.validate_file_type(_self.file.name)
        market_data_df = DataProcessingUtilities.read_file(_self.file.name)
        
        market_data_df_for_json = market_data_df
        market_data_df_for_json.reset_index()
        json_market_data = market_data_df_for_json.to_json(orient='records')
        #json_market_data = market_data_df.to_json(orient='split')  
        json_object = json.loads(json_market_data)
        response = requests.post(url, json={"data": json_object})

        if response.status_code == 200:
            try:
                
                filename, extension = os.path.splitext(_self.file.name)
                recent_uploaded_data_date = market_data_df["DateAsOf"].unique()
                st.session_state.recent_uploaded_data_date   = recent_uploaded_data_date;
                market_data_df["DateAsOf"] = pd.to_datetime(market_data_df["DateAsOf"], format="%Y%m%d").dt.strftime("%Y-%m-%d")
                market_data_df["FutureExpiryDate"] = pd.to_datetime(market_data_df["FutureExpiryDate"], format="%Y%m%d").dt.strftime("%Y-%m-%d")

                st.session_state.json_market_data   = json_market_data;
                st.session_state["recent_uploaded_market_data"] = market_data_df;

            except Exception as e:
                raise ValueError(str(e))
        else:
            raise ValueError(response.text)
