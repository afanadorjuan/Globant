from flask import Flask, request, jsonify
import os
import pandas as pd
import sqlite3

app = Flask(__name__)


# Ruta a la carpeta que contiene la base de datos SQLite
db_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

@app.route('/upload', methods=['POST'])
def upload_csv():
    try:
        # Get the CSV files sent in the request
        departments_csv = request.files['departments']
        jobs_csv = request.files['jobs']
        employees_csv = request.files['hired_employees']

        # Validate that all three files are present and have the correct extension
        if all(csv_file and csv_file.filename.endswith('.csv') for csv_file in [departments_csv, jobs_csv, employees_csv]):
            # Read the CSV files with pandas
            departments_df = pd.read_csv(departments_csv)
            jobs_df = pd.read_csv(jobs_csv)
            employees_df = pd.read_csv(employees_csv)

            # Connect to the SQLite database
            conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))

            # Insert data into the departments table
            departments_df.to_sql('departments', conn, if_exists='replace', index=False)

            # Insert data into the jobs table
            jobs_df.to_sql('jobs', conn, if_exists='replace', index=False)

            # Insert data into the employees table
            employees_df.to_sql('employees', conn, if_exists='replace', index=False)

            # Close the connection
            conn.close()

            return jsonify({'message': 'CSV files uploaded and data inserted successfully!'})

        else:
            return jsonify({'error': 'Invalid files. Please upload CSV files for departments, jobs, and employees.'}), 400

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


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Establecer conexión con la base de datos SQLite
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))

        # Ejecutar una consulta SQL para obtener todos los datos de la tabla data_table
        cursor = conn.execute('SELECT * FROM data_table')

        # Obtener los resultados de la consulta
        data = cursor.fetchall()

        # Cerrar la conexión con la base de datos
        conn.close()

        # Devolver los datos en formato JSON
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': 'An error occurred while querying the database.', 'details': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        # Establecer conexión con la base de datos SQLite
        conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))

        # Query to get the number of employees hired for each job and department in 2021 divided by quarter
        query = """
            SELECT department, job,
                SUM(CASE WHEN strftime('%m', hire_date) BETWEEN '01' AND '03' THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN strftime('%m', hire_date) BETWEEN '04' AND '06' THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN strftime('%m', hire_date) BETWEEN '07' AND '09' THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN strftime('%m', hire_date) BETWEEN '10' AND '12' THEN 1 ELSE 0 END) AS Q4
            FROM data_table
            WHERE strftime('%Y', hire_date) = '2021'
            GROUP BY department, job
            ORDER BY department, job
        """

        # Execute the query and fetch the results
        cursor = conn.execute(query)
        results = cursor.fetchall()

        # Cerrar la conexión con la base de datos
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

        # Devolver los datos en formato JSON
        return jsonify(metrics)

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching the metrics.', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
