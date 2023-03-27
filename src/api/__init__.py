"""

"api"  package contains following 3 important classes to handle the logic for api end points to perform CRUD operations on databases to
store the market data. It also contains the class to fetch the required market data from database and returns the calculated option prices.

OptionDataFetcher: This class is responsible for fetching option data from a database using an instance of the DataPersistence class. It has two methods: fetch_records_asof and fetch_distinct_dates, which respectively fetch option data records for a given date and fetch all distinct dates available in the option data.

OptionDataUploader: This class is responsible for uploading option data to a database using an instance of the DataPersistence class. It has three methods: load_market_data_json, load_market_data_file, and load_market_data_iostream, which respectively upload market data from a JSON formatted list, a file, or an iostream.

OptionPricer: This class is responsible for calculating option prices for a given date using an instance of the DataPersistence class and the B76OptionPricer model. It has one method: calculate_market_prices, which calculates option prices for a given date and returns a JSONResponse with the calculated option prices.

"""