from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector  # Import MySQL connector

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

# New route to handle incoming SMS from Twilio
@app.route('/sms', methods=['POST'])
def receive_sms():
    # Extract SMS data from Twilio webhook
    message_body = request.form['Body']  # SMS content
    sender = request.form['From']       # Sender's phone number
    print(f"Received SMS: '{message_body}' from {sender}")

    # Parse the SMS content (assumes key=value pairs separated by '&')
    try:
        data = dict(param.split('=') for param in message_body.split('&'))
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert data into the database
        cursor.execute(
            "INSERT INTO meter_data (voltage, current, power, frequency, pf, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['voltage'], data['current'], data['power'], data['frequency'], data['pf'], data['timestamp'])
        )
        connection.commit()
        connection.close()
        print("Data stored successfully!")
        return "Data received and stored successfully.", 200
    except Exception as e:
        print("Error processing SMS:", str(e))
        return "Failed to process SMS data.", 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
