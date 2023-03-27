# fastapi_streamlit_test
fastapi_streamlit_test


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


### SCreen shots of the application
<img src="docs/fasapi_swagger_ui.PNG" alt="FastAPI Swagger UI" title="FastAPI Swagger UI" width="600" height="500">

<img src="docs/MarketData_Upload_Page.PNG" alt="Market Data Upload page" title="Market Data Upload page" width="900" height="600">

<img src="docs/MarketData_Analysis_Page1.png" alt="Market Data Analysis page-1" title="Market Data Analysis page-1" width="900" height="600">

<img src="docs/MarketData_Analysis_Page2.png" alt="Market Data Analysis page-2" title="Market Data Analysis page-2" width="900" height="600">



