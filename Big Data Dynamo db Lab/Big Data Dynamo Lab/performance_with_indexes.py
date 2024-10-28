import boto3
import time
from boto3.dynamodb.conditions import Key, Attr

# DynamoDB configuration
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-west-2',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

# Table references
orders_table = dynamodb.Table('Orders')
order_items_table = dynamodb.Table('OrderItems')

# Helper function to measure query execution time
def measure_query_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)  # Execute the function
        end = time.time()
        print(f"Query executed in: {end - start:.4f} seconds")
    return wrapper

# ===================
# Create Indexes
# ===================
def create_indexes():
    # Create GSI for customer_id on Orders table
    orders_table.update(
        AttributeDefinitions=[
            {'AttributeName': 'customer_id', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexUpdates=[
            {
                'Create': {
                    'IndexName': 'customer_id-index',
                    'KeySchema': [{'AttributeName': 'customer_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            }
        ]
    )

    # Create GSI for product_id on OrderItems table
    order_items_table.update(
        AttributeDefinitions=[
            {'AttributeName': 'product_id', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexUpdates=[
            {
                'Create': {
                    'IndexName': 'product_id-index',
                    'KeySchema': [{'AttributeName': 'product_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            }
        ]
    )

    print("Indexes created. Waiting for them to be active...")
    time.sleep(10)  # Ensure indexes are active before running queries


# ===================
# Query Functions
# ===================

@measure_query_time
def query_orders_by_product_and_date(product_id, start_date, end_date):
    response = order_items_table.query(
        IndexName='product_id-index',
        KeyConditionExpression=Key('product_id').eq(product_id)
    )
    order_ids = [item['order_id'] for item in response['Items']]
    
    for order_id in order_ids:
        order = orders_table.get_item(Key={'order_id': order_id}).get('Item')
        if order and start_date <= order['order_purchase_timestamp'] <= end_date:
            pass  # Process order (if needed)

@measure_query_time
def sort_products_by_price():
    response = order_items_table.scan()
    sorted(response['Items'], key=lambda x: float(x['price']))  # Sort the items by price

@measure_query_time
def filter_orders_by_status_and_customer(status, customer_id):
    response = orders_table.query(
        IndexName='customer_id-index',
        KeyConditionExpression=Key('customer_id').eq(customer_id)
    )
    for order in response['Items']:
        if order.get('status') == status:
            pass  # Process order (if needed)

@measure_query_time
def query_orders_by_customer(customer_id):
    response = orders_table.query(
        IndexName='customer_id-index',
        KeyConditionExpression=Key('customer_id').eq(customer_id)
    )
    sorted(response['Items'], key=lambda x: x['order_purchase_timestamp'])


# ===================
# Main Execution
# ===================
if __name__ == '__main__':
    # Step 1: Create Indexes
    create_indexes()

    # Step 2: Run Queries and Print Execution Time
    print("Query 1: Orders by Product and Date Range")
    query_orders_by_product_and_date('1slxdgbgWFax', '2017-01-01', '2018-12-31')

    print("\nQuery 2: Sort Products by Price")
    sort_products_by_price()

    print("\nQuery 3: Filter Orders by Status and Customer")
    filter_orders_by_status_and_customer('delivered', 'I74lXDOfoqsp')

    print("\nQuery 4: Orders for a Specific Customer")
    query_orders_by_customer('I74lXDOfoqsp')
