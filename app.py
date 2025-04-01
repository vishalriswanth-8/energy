from flask import Flask, request, jsonify
from flask_cors import CORS

# Define the Flask app
app = Flask(__name__)

# Enable CORS (Make sure 'app' is defined before using CORS)
CORS(app, origins=["https://energydata.netlify.app"])

# Database configuration
db_config = {
    "host": "bsdqka6tftdhsm5y9suy-mysql.services.clever-cloud.com",
    "user": "uqdu3jvmoqilcgdj",
    "password": "Yq6jZZhqCD2rIOqhgyDA",
    "database": "bsdqka6tftdhsm5y9suy",
    "port": 3306
}

# Example GET route for fetching data
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM meter_data")  # Replace 'meter_data' with your table name
        result = cursor.fetchall()
        connection.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Example POST route for inserting data
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO meter_data (voltage, current, power, frequency, pf, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['voltage'], data['current'], data['power'], data['frequency'], data['pf'], data['timestamp'])
        )
        connection.commit()
        connection.close()
        return jsonify({"message": "Data added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
