# fastapi_streamlit_test
This application developed using FastAPI, Streamlit web packages. 
The work flow begins by reading by option pricing data in either CSV or Excel format, then it stores the data in a sqlite db.
User can also provide the market data in a JSON formatted text or call the api endpoint with with a json text.
This application renders the web pages using streamlit package to provide interface for various CRUD operations.
When user select the option to calculate option prices, it calculates the option prices using Black76 model and shows the ressults in tabular format as well as in a  interactive line plot(by using Python Bokeh package). It also provides the option to download the option prices in a CSV file. 


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

<img src="docs/MarketData_Analysis_Page2.png" alt="Market Data Analysis page-2" title="Market Data Analysis page-2" width="900" height="600">



