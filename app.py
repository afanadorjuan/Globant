from flask import Flask, request, jsonify
import os
import pandas as pd
import sqlite3

app = Flask(__name__)


# Ruta a la carpeta que contiene la base de datos SQLite
db_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def create_tables():
    try:
        # Establish connection with the SQLite database
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))
        cursor = conn.cursor()

        # Create the departments table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                department TEXT
            )
        ''')

        # Create the jobs table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                job TEXT
            )
        ''')

        # Create the employees table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                hire_datetime TEXT,
                department_id INTEGER,
                job_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments (id),
                FOREIGN KEY (job_id) REFERENCES jobs (id)
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    except Exception as e:
        print('Error creating tables:', e)

# Call the create_tables function on application startup
create_tables()



@app.route('/upload', methods=['POST'])
def upload_csv():
    try:
        # Obtener los archivos CSV enviados en la solicitud
        csv_files = request.files

        # Validar que se enviaron los archivos
        if not csv_files:
            return jsonify({'error': 'No CSV files were uploaded.'}), 400

        for file_key, csv_file in csv_files.items():
            # Validar que el archivo tiene la extensión CSV
            if csv_file and csv_file.filename.endswith('.csv'):
                # Leer el archivo CSV con pandas without headers and specific column names for departments table
                if file_key == 'departments':
                    df = pd.read_csv(csv_file, header=None, names=['id', 'department'])
                else:
                    df = pd.read_csv(csv_file, header=None)

                # Guardar los datos en la base de datos SQLite
                conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))
                table_name = file_key  # Keeping the table name identical to the file key
                df.to_sql(table_name, conn, if_exists='replace', index=False)

        return jsonify({'message': 'CSV files uploaded successfully!'})

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the CSV files.', 'details': str(e)}), 500
    try:
        # Obtener los archivos CSV enviados en la solicitud
        csv_files = request.files

        # Validar que se enviaron los archivos
        if not csv_files:
            return jsonify({'error': 'No CSV files were uploaded.'}), 400

        for file_key, csv_file in csv_files.items():
            # Validar que el archivo tiene la extensión CSV
            if csv_file and csv_file.filename.endswith('.csv'):
                # Leer el archivo CSV con pandas without headers
                df = pd.read_csv(csv_file, header=None)

                # Guardar los datos en la base de datos SQLite
                conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))
                table_name = file_key.replace('_', '')  # Assuming the file keys are 'departments', 'hired_employees', and 'jobs'
                df.to_sql(table_name, conn, if_exists='replace', index=False)

        return jsonify({'message': 'CSV files uploaded successfully!'})

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the CSV files.', 'details': str(e)}), 500

@app.route('/insert_batch', methods=['POST'])
def insert_batch():
    try:
        # Obtener los datos enviados en la solicitud
        data = request.json

        # Validar que se envió un lote de transacciones
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid data. Please send a batch of transactions as a list of dictionaries.'}), 400

        # Guardar el lote de transacciones en la base de datos SQLite
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))
        df = pd.DataFrame(data)
        df.to_sql('data_table', conn, if_exists='append', index=False)

        return jsonify({'message': 'Batch of transactions inserted successfully!'})

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the batch of transactions.', 'details': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        # Establecer conexión con la base de datos SQLite
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))

        # Query to get the number of employees hired for each job and department in 2021 divided by quarter
        query = """
            SELECT d.department, j.job,
                SUM(CASE WHEN strftime('%m', e.hire_datetime) BETWEEN '01' AND '03' THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN strftime('%m', e.hire_datetime) BETWEEN '04' AND '06' THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN strftime('%m', e.hire_datetime) BETWEEN '07' AND '09' THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN strftime('%m', e.hire_datetime) BETWEEN '10' AND '12' THEN 1 ELSE 0 END) AS Q4
            FROM hired_employees e
            JOIN jobs j ON e.job_id = j.id
            JOIN departments d ON e.department_id = d.id
            WHERE strftime('%Y', e.hire_datetime) = '2021'
            GROUP BY d.department, j.job
            ORDER BY d.department, j.job
        """

        # Execute the query and fetch the results
        cursor = conn.execute(query)
        results = cursor.fetchall()

        # Close the connection with the database
        conn.close()

        # Create a list of dictionaries to hold the results
        metrics = []
        for row in results:
            metric = {
                'department': row[0],
                'job': row[1],
                'Q1': row[2],
                'Q2': row[3],
                'Q3': row[4],
                'Q4': row[5]
            }
            metrics.append(metric)

        # Return the metrics as a JSON response
        return jsonify(metrics)

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching the metrics.', 'details': str(e)}), 500
    

@app.route('/departments', methods=['GET'])
def get_departments():
    try:
        # Establish connection with the SQLite database
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))

        # Query to fetch all data from the departments table
        query = "SELECT id,department FROM departments"

        # Execute the query and fetch the results
        cursor = conn.execute(query)
        results = cursor.fetchall()

        # Close the connection with the database
        conn.close()

        # Create a list of dictionaries to hold the results
        departments = []
        for row in results:
            department = {
                'id': row[0],
                'department': row[1]
            }
            departments.append(department)

        # Return the departments as a JSON response
        return jsonify(departments)

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching the departments.', 'details': str(e)}), 500


@app.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        # Establecer conexión con la base de datos SQLite
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))

        # Query to get all records from the jobs table
        query = "SELECT * FROM jobs"

        # Execute the query and fetch the results
        cursor = conn.execute(query)
        results = cursor.fetchall()

        # Close the connection with the database
        conn.close()

        # Create a list of dictionaries to hold the results
        jobs = []
        for row in results:
            job = {
                'id': row[0],
                'job': row[1]
            }
            jobs.append(job)

        # Return the jobs as a JSON response
        return jsonify(jobs)

    except Exception as e:
        return jsonify({'error': 'An error occurred while querying the jobs.', 'details': str(e)}), 500


@app.route('/hired_employees', methods=['GET'])
def get_hired_employees():
    try:
        # Establecer conexión con la base de datos SQLite
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))

        # Query to get all records from the hired_employees table
        query = "SELECT * FROM hired_employees"

        # Execute the query and fetch the results
        cursor = conn.execute(query)
        results = cursor.fetchall()

        # Close the connection with the database
        conn.close()

        # Create a list of dictionaries to hold the results
        hired_employees = []
        for row in results:
            employee = {
                'id': row[0],
                'name': row[1],
                'datetime': row[2],
                'department_id': row[3],
                'job_id': row[4]
            }
            hired_employees.append(employee)

        # Return the hired employees as a JSON response
        return jsonify(hired_employees)

    except Exception as e:
        return jsonify({'error': 'An error occurred while querying the hired employees.', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
