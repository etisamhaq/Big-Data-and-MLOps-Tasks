from flask import Flask, jsonify, request, render_template
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

# Initialize DynamoDB local instance
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # Use DynamoDB Local
    region_name='us-west-2',               # You can use any region
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

# Function to create a table with GSI and LSI
def create_orders_table():
    try:
        table = dynamodb.create_table(
            TableName='Orders',
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'},  # Partition Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},  # Primary key
                {'AttributeName': 'product_id', 'AttributeType': 'S'},  # GSI
                {'AttributeName': 'order_date', 'AttributeType': 'S'},  # LSI
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10,
            },
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'ProductIndex',  # GSI on product_id
                    'KeySchema': [
                        {'AttributeName': 'product_id', 'KeyType': 'HASH'},  # GSI Partition Key
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10,
                    }
                }
            ],
            LocalSecondaryIndexes=[
                {
                    'IndexName': 'OrderDateIndex',  # LSI on order_date
                    'KeySchema': [
                        {'AttributeName': 'order_id', 'KeyType': 'HASH'},  # Partition Key
                        {'AttributeName': 'order_date', 'KeyType': 'RANGE'},  # Sort Key for LSI
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ]
        )
        print(f"Creating table: {table.name}...")
        table.meta.client.get_waiter('table_exists').wait(TableName='Orders')
        print(f"Table {table.name} created successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Call the function to create the Orders table
create_orders_table()

# Serve the index.html file
@app.route('/')
def home():
    return render_template('index.html')

# Route to add order to DynamoDB
@app.route('/add_order', methods=['POST'])
def add_order():
    table = dynamodb.Table('Orders')
    
    order_id = request.json['order_id']
    product_id = request.json['product_id']
    customer_id = request.json['customer_id']
    order_date = request.json['order_date']
    quantity = request.json['quantity']
    status = request.json['status']
    total_price = request.json['total_price']

    table.put_item(
        Item={
            'order_id': order_id,
            'product_id': product_id,
            'customer_id': customer_id,
            'order_date': order_date,
            'quantity': quantity,
            'status': status,
            'total_price': total_price
        }
    )

    return jsonify({"message": "Order added successfully!"})

# Route to query by product_id (using GSI)
@app.route('/query_by_product/<product_id>', methods=['GET'])
def query_by_product(product_id):
    table = dynamodb.Table('Orders')
    
    response = table.query(
        IndexName='ProductIndex',
        KeyConditionExpression=Key('product_id').eq(product_id)
    )

    return jsonify(response['Items'])

# Route to query by order_id and order_date (using LSI)
@app.route('/query_by_order_date/<order_id>/<order_date>', methods=['GET'])
def query_by_order_date(order_id, order_date):
    table = dynamodb.Table('Orders')
    
    response = table.query(
        IndexName='OrderDateIndex',
        KeyConditionExpression=Key('order_id').eq(order_id) & Key('order_date').eq(order_date)
    )

    return jsonify(response['Items'])

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)

