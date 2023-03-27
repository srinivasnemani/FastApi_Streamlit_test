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
```
