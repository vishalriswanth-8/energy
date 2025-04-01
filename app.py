from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    "host": "bsdqka6tftdhsm5y9suy-mysql.services.clever-cloud.com",
    "user": "uqdu3jvmoqilcgdj",
    "password": "Yq6jZZhqCD2rIOqhgyDA",
    "database": "bsdqka6tftdhsm5y9suy",
    "port": 3306
}

# Route to fetch data (GET request)
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sensor_data")  # Replace "sensor_data" with your table name
        result = cursor.fetchall()
        connection.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to insert data (POST request)
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO sensor_data (voltage, current, power, frequency, pf, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['voltage'], data['current'], data['power'], data['frequency'], data['pf'], data['timestamp'])
        )
        connection.commit()
        connection.close()
        return jsonify({"message": "Data added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)