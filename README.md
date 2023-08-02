# Flask API with SQLite Database

This is a simple Flask API that uses a SQLite database to store information about departments, jobs, and employees. The API allows users to upload CSV files to populate the database tables and provides various endpoints to fetch metrics and information from the database.

## Installation

To run the application, follow these steps:

1. Clone the repository to your local machine.
2. Make sure you have Python 3.x installed on your system.
3. Install the required dependencies using pip:
pip install flask pandas


## Usage

1. Start the application by running the following command:

python app.py


2. The API will be accessible at `http://127.0.0.1:5000/`.

3. You can use tools like `curl` or Postman to interact with the API, or build your frontend to make HTTP requests to the API endpoints.

## API Endpoints

### Upload CSV

- **Endpoint**: `/upload`
- **Method**: POST
- **Description**: Uploads CSV files to populate the database tables.
- **Parameters**: Each CSV file should be sent as a form-data file with a corresponding key. The key should be the name of the table (e.g., 'departments', 'hired_employees', 'jobs').
- **Response**: JSON response with a success message or an error message.

### Insert Batch

- **Endpoint**: `/insert_batch?table=<table_name>`
- **Method**: POST
- **Description**: Inserts a batch of transactions into the specified table in the database.
- **Parameters**: The table name should be specified as a query parameter (e.g., 'departments', 'hired_employees', 'jobs').
- **Data**: The data should be sent in JSON format as a list of dictionaries.
- **Response**: JSON response with a success message or an error message.

### Metrics

- **Endpoint**: `/metrics`
- **Method**: GET
- **Description**: Fetches the number of employees hired for each job and department in 2021, divided by quarter.
- **Response**: JSON response with the metrics data.

### Departments Hired More Than Mean

- **Endpoint**: `/departments/hired_more_than_mean`
- **Method**: GET
- **Description**: Fetches departments that hired more employees than the mean number of employees hired in 2021.
- **Response**: JSON response with the departments' data.

## Database Schema

The SQLite database has three tables:

1. `departments`: Holds information about different departments. It has columns: `id` and `department`.

2. `jobs`: Stores information about various job roles. It has columns: `id` and `job`.

3. `employees`: Contains data about the hired employees. It has columns: `id`, `name`, `hire_datetime`, `department_id`, and `job_id`. The `department_id` and `job_id` columns are foreign keys referencing the `departments` and `jobs` tables, respectively.
