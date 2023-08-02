# Data Migration API - README  
## Description 
This project consists of an API developed with Flask that allows data migration from CSV files to a SQLite database. It also provides functionalities to insert batches of transactions and query data stored in the database. 
## Requirements
  - Python 3.x installed on the system. 
  - - [Flask](https://flask.palletsprojects.com/en/2.1.x/installation/) installed in the development environment.
  -  - [Pandas](https://pandas.pydata.org/docs/getting_started/install.html) installed in the development environment. 
## Installation  
1. Clone the GitHub repository: git clone [https://github.com/afanadorjuan/Globant.git](https://github.com/afanadorjuan/Globant.git)
2. Navigate to the project directory:
cd Globant
3. Install project dependencies:
pip install -r requirements.txt


## Usage

### Endpoint `/upload` - Upload Data from CSV Files

This endpoint allows you to upload historical data from CSV files to the database. The CSV files should be in comma-separated format (.csv). The data will be inserted into the "data_table" in the SQLite database.

**Method**: `POST`
**URL**: `/upload`
**Parameters**:
- `file`: CSV file to upload (in the request body).

**Responses**:
- 200 OK: The CSV file was successfully uploaded.
- 400 Bad Request: Invalid file or incorrect format.
- 500 Internal Server Error: An error occurred while processing the file.

### Endpoint `/insert_batch` - Insert Batches of Transactions

This endpoint allows you to insert batches of transactions into the database. The batch of transactions should be a list of dictionaries, where each dictionary represents a data row to be inserted into the "data_table" in the SQLite database.

**Method**: `POST`
**URL**: `/insert_batch`
**Parameters**:
- JSON data (in the request body).

**Responses**:
- 200 OK: Batch of transactions inserted successfully.
- 400 Bad Request: Invalid data or incorrect format.
- 500 Internal Server Error: An error occurred while processing the batch of transactions.

### Endpoint `/get_data` - Query Stored Data

This endpoint allows you to query all the data stored in the "data_table" of the SQLite database.

**Method**: `GET`
**URL**: `/get_data`
**Responses**:
- 200 OK: Returns the data from the "data_table" in JSON format.
- 500 Internal Server Error: An error occurred while querying the database.

## Example Usage

1. Upload data from CSV file:
POST /upload Form Data:
-   file: [Select CSV file]
2. Insert batch of transactions:
POST /insert_batch
Content-Type: application/json
Body: [ {"column1": "value1", "column2": "value2", "column3": "value3"}, {"column1": "value4", "column2": "value5", "column3": "value6"}, {"column1": "value7", "column2": "value8", "column3": "value9"} ]
3. Query stored data:
GET /get_data

## Contributions
None, tech assessment
## Author
[Juan Afanador](https://github.com/afanadorjuan)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
