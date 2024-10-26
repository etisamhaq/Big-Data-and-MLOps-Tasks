from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

# DynamoDB configuration
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-west-2',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

# API to insert Customers
@app.route('/add_customer', methods=['POST'])
def add_customer():
    table = dynamodb.Table('Customers')
    data = request.get_json()
    table.put_item(Item=data)
    return jsonify({"message": "Customer added successfully!"})

# API to insert OrderItems
@app.route('/add_order_item', methods=['POST'])
def add_order_item():
    table = dynamodb.Table('OrderItems')
    data = request.get_json()
    table.put_item(Item=data)
    return jsonify({"message": "Order item added successfully!"})

# API to insert Orders
@app.route('/add_order', methods=['POST'])
def add_order():
    table = dynamodb.Table('Orders')
    data = request.get_json()
    table.put_item(Item=data)
    return jsonify({"message": "Order added successfully!"})

# API to insert Products
@app.route('/add_product', methods=['POST'])
def add_product():
    table = dynamodb.Table('Products')
    data = request.get_json()
    table.put_item(Item=data)
    return jsonify({"message": "Product added successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
