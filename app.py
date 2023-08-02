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
        # Obtener el archivo CSV enviado en la solicitud
        csv_file = request.files['file']

        # Validar que se envió un archivo
        if csv_file and csv_file.filename.endswith('.csv'):
            # Leer el archivo CSV con pandas
            df = pd.read_csv(csv_file)

            # Guardar los datos en la base de datos SQLite
            conn = sqlite3.connect(os.path.join(db_folder, 'database.db'))
            df.to_sql('data_table', conn, if_exists='replace', index=False)

            return jsonify({'message': 'CSV uploaded successfully!'})

        else:
            return jsonify({'error': 'Invalid file. Please upload a CSV file.'}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the CSV file.', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
