# Globant Tech Assessment - Flask API with SQLite Database Juan Afanador

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


## Dockerization
The application has been Dockerized, which means it has been packaged into a Docker container along with its dependencies, libraries, and environment settings. This allows for consistent deployment and execution across different environments.

A Dockerfile was used to define the configuration for building the Docker image. The official Python 3.9 image was chosen as the base image, as the application is built on the Flask web framework.

The working directory inside the container was set to /app, and all the contents from the current directory of the project were copied to the /app directory inside the container. The necessary dependencies, such as Flask and Pandas, were installed using pip.

Port 5000 was exposed to enable external access to the Flask app running inside the container. The command python app.py was specified to start the Flask app when the container launches.

Azure Deployment
For deployment on Azure, the following steps were taken:

1. An Azure Container Registry (ACR) named "GlobantContainerReg" was created to store the Docker image of the application.

2. The Docker image of the application was built using the Dockerfile.

3. The image was tagged with the name of the Container Registry.

4. Authentication was performed by logging in to the Azure Container Registry.

5. The Docker image was pushed to the Azure Container Registry for storage.

6. A Resource Group named "globent" was created to group related resources.

7. An Azure Web App with the name "globent" was created using the previously established Resource Group.

8. The Azure Web App was configured to use the Docker image from the Azure Container Registry.

9. The Web App was successfully deployed and is now accessible at "globent.azurewebsites.net".

s://imgur.com/2u97akd.png)

Note: Cautionary information was provided regarding the public access of endpoints using Postman in the development environment. For production environments, it is essential to implement proper authentication and authorization mechanisms to secure the endpoints.

By following this Dockerization and deployment process, the application can be consistently and reliably run in different environments, making it easier to scale and manage.

## Quick Tips for Improvements
The application has been Dockerized to ensure consistent deployment and execution across different environments. By packaging it into a Docker container, all dependencies, libraries, and environment settings are encapsulated, making it easier to manage and scale the application.

Furthermore, the deployment process has been simplified and made more agile through cloud-based services like Azure Data Factory and Azure Databricks. While these cloud services enable more efficient data processing and analytics for larger datasets, for this particular exercise with relatively small data, deploying the application directly to the cloud using Azure Web App and Azure Container Registry provides a cost-effective solution with pay-as-you-go pricing.

By leveraging Azure Web App, the application can be accessed through a secure and customizable domain (e.g., "globent.azurewebsites.net") without the need to manage infrastructure. The Azure Container Registry stores the Docker image, ensuring version control and consistency in deployment.

For more data-intensive scenarios, Azure Data Factory and Azure Databricks can be seamlessly integrated to orchestrate data pipelines, perform ETL (Extract, Transform, Load) operations, and carry out advanced data analytics. The cloud-native approach empowers organizations to focus on developing data-driven applications without the burden of managing infrastructure, making development faster and more efficient.
# Demo images
![Web App](https://imgur.com/Z4o8yy5.png)

![Postman test](https://imgur.com/2u97akd.png)

![Docker](https://imgur.com/TxqvZh7.png)
