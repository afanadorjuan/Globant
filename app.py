from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


from flask import request, jsonify

@app.route('/upload', methods=['POST'])
def upload_csv():
    try:
        # Obtener el archivo CSV enviado en la solicitud
        csv_file = request.files['file']

        # Validar que se envió un archivo
        if csv_file and csv_file.filename.endswith('.csv'):
            # Implementar aquí la lógica para procesar el archivo CSV y guardar los datos en la base de datos
            # Por ahora, simplemente retornamos un mensaje
            return jsonify({'message': 'CSV uploaded successfully!'})

        else:
            return jsonify({'error': 'Invalid file. Please upload a CSV file.'}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the CSV file.', 'details': str(e)}), 500
