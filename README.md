[![Python Build](https://github.com/srinivasnemani/FastApi_Streamlit_test/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/srinivasnemani/FastApi_Streamlit_test/actions/workflows/python-package-conda.yml)

# fastapi_streamlit_test
This application is developed using the FastAPI and Streamlit packages. 
The workflow begins by reading the option pricing data from either CSV or Excel format files, and then stores the data in an SQLite database. Users can also provide market data in JSON-formatted text or call the API endpoint with JSON text. 
The application renders web pages using the Streamlit package to provide an interface for various CRUD operations.

When users select the option to calculate option prices, the application calculates the option prices using the Black76 model and displays the results in a tabular format, as well as an interactive line plot (using the Python Bokeh package). It also provides the option to download the option prices in a CSV file.


### Build Setup in Windows
(needed only one time to setup the environment)

```
python -m venv .venv
.\.venv\Scripts\activate.ps1
python -m pip install -r ./requirements.txt
```
### Running the application

```
Activate Virtual Environment:
.\.venv\Scripts\activate.ps1 

Run API server
python .\src\api_manager.py

Run Web server
streamlit run .\src\gui_manager.py

Run the test cases
pytest .\src\tests\test_b76_option_model.py
pytest .\src\tests\test_option_pricer_api.py
```


### Screen shots of the application
<img src="docs/fasapi_swagger_ui.PNG" alt="FastAPI Swagger UI" title="FastAPI Swagger UI" width="600" height="500">

<img src="docs/MarketData_Upload_Page.PNG" alt="Market Data Upload page" title="Market Data Upload page" width="900" height="600">

<img src="docs/MarketData_Analysis_Page1.png" alt="Market Data Analysis page-1" title="Market Data Analysis page-1" width="900" height="600">

<img src="docs/MarketData_Analysis_Page2.png" alt="Market Data Analysis page-2" title="Market Data Analysis page-2" width="600" height="900">


