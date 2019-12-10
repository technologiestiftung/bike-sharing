# bike-sharing

## Data Collection
src/data-preprocessing

**Script src/data-processing/query_bike_apis.py is used to query provider API data**
API requests to receive all current locations of bikes from nextbike, lidlbike and mobike in Berlin (inner circle) and store them into a single database.

Add config.py file to src/ with API Keys for Deutsche Bahn API (https://developer.deutschebahn.com/store/) and database credentials. (see Example **src/data-processing/config-example.py**)

### Query other cities or providers
To query APIs for different cities the *src/data-processing/query_bike_apis.py* script has to be adapted accordingly.
To query other providers [this documentation](https://github.com/ubahnverleih/WoBike/) is a good source of information.

For access to lime bike API insert phone_no to config.py and follow steps in lime_access.py (three manual steps required).

## Data Analysis
src/analysis

Jupyter Notebook to analyse data.

- preprocess.ipynb contains the preprossing steps of the raw data to a usable format. 
    - raw.csv contains the data from the database
    - preprocessed.csv contains the data with added columns and fixed lat / lng
    - routed.csv contains the data with distance and waypoints
    - cleaned.csv is the cleaned routed dataset (unplausible data is removed)
    - pseudonomysed.csv is the anonymized, cleaned data, following [this standard](https://data.louisvilleky.gov/dataset/dockless-vehicles) 
    - pseudonomysed_raw.csv ist the anonymized data (NOT cleaned).

- analysis.ipynb includes analysis about provider and bike specific data

- pseudonomysed.ipynb includes analysis using the anonymized dataset (without information on providers.)
