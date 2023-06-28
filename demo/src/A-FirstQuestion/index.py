from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'your_database',
}

# API endpoint for phone number login
@app.route('/login', methods=['POST'])
def phone_number_login():
    # Get phone number from request body
    phone_number = request.json.get('phone_number')

    # Validate phone number (e.g., check length, format, etc.)
    if not phone_number:
        return jsonify({'error': 'Phone number is required.'}), 400

    # Perform phone number login logic
    # (e.g., generate OTP, send SMS, verify OTP, etc.)
    # Replace this with your own implementation

    # Return success response
    return jsonify({'message': 'Phone number login successful.'})

# API endpoint for adding a customer
@app.route('/customers', methods=['POST'])
def add_customer():
    # Get customer data from request body
    customer_data = request.json

    # Validate customer data (e.g., check required fields, format, etc.)
    if not customer_data:
        return jsonify({'error': 'Customer data is required.'}), 400

    # Extract customer details
    name = customer_data.get('name')
    email = customer_data.get('email')
    phone_number = customer_data.get('phone_number')

    # Validate input params
    if not name or not email or not phone_number:
        return jsonify({'error': 'Name, email, and phone number are required.'}), 400

    # Check for duplicates (e.g., by email or phone number)
    if is_duplicate(email=email) or is_duplicate(phone_number=phone_number):
        return jsonify({'error': 'Duplicate customer found.'}), 400

    # Add customer to database
    customer_id = add_customer_to_database(name, email, phone_number)

    if customer_id is None:
        return jsonify({'error': 'Failed to add customer.'}), 500

    return jsonify({'message': 'Customer added successfully.', 'customer_id': customer_id})

# Function to check for duplicate customers by email or phone number
def is_duplicate(email=None, phone_number=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM customers WHERE email = %s OR phone_number = %s"
        params = (email, phone_number)
        cursor.execute(query, params)

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count > 0

    except mysql.connector.Error as error:
        print(f"Error checking duplicate customer: {error}")
        return False

# Function to add a customer to the database
def add_customer_to_database(name, email, phone_number):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Start a transaction
        conn.start_transaction()

        # Insert customer details into the database
        insert_query = "INSERT INTO customers (name, email, phone_number) VALUES (%s, %s, %s)"
        insert_params = (name, email, phone_number)
        cursor.execute(insert_query, insert_params)

        # Get the generated customer ID
        customer_id = cursor.lastrowid

        # Commit the transaction
        conn.commit()

        cursor.close()
        conn.close()

        return customer_id

    except mysql.connector.Error as error:
        print(f"Error adding customer to database: {error}")

        # Rollback the transaction on error
        conn.rollback()

        return None

if __name__ == '__main__':
    app.run()
