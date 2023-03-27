"""
This package is meant for centralizing various generic utility functions that are 
frequently used across all modules and packages. The following utility functions are added in this package.

1. File extension validations (To check only CSV or Excel files are uploaded)

2. Reading data from XLSX or CSVs and converting to Pandas dataframe.

3. Validatting the file to check if all the required columsn are present in the file.

4. Converting a generic exception to HTTP exception to be used in API responses.

5. A logger decarator functions for logging the info during various function executions. 
    
"""