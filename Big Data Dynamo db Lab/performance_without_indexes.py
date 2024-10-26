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
products_table = dynamodb.Table('Products')

# Helper function to measure query execution time
def measure_query_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)  # Execute the function
        end = time.time()
        print(f"Query executed in: {end - start:.4f} seconds")
    return wrapper

# 1. Query Orders by Product ID and Date Range (Without Index)
@measure_query_time
def query_orders_by_product_and_date(product_id, start_date, end_date):
    response = order_items_table.scan(
        FilterExpression=Attr('product_id').eq(product_id)
    )
    order_ids = [item['order_id'] for item in response['Items']]
    
    # Retrieve orders and filter by date range
    for order_id in order_ids:
        order = orders_table.get_item(Key={'order_id': order_id}).get('Item')
        if order and start_date <= order['order_purchase_timestamp'] <= end_date:
            pass  # Process order (if needed)

# 2. Sort Products by Price (Using OrderItems Table)
@measure_query_time
def sort_products_by_price():
    response = order_items_table.scan()
    items = response['Items']
    sorted(items, key=lambda x: float(x['price']))  # Sort the items by price

# 3. Filter Orders by Status and Customer ID (Without Index)
@measure_query_time
def filter_orders_by_status_and_customer(status, customer_id):
    response = orders_table.scan()
    [
        order for order in response['Items']
        if order.get('status') == status and order.get('customer_id') == customer_id
    ]  # Filter matching orders

# 4. Query Orders for a Specific Customer and Sort by Order Date (Without Index)
@measure_query_time
def query_orders_by_customer(customer_id):
    response = orders_table.scan(
        FilterExpression=Attr('customer_id').eq(customer_id)
    )
    sorted(response['Items'], key=lambda x: x['order_purchase_timestamp'])  # Sort orders

# Test the queries

print("Query 1: Orders by Product and Date Range")
query_orders_by_product_and_date('1slxdgbgWFax', '2017-01-01', '2018-12-31')

print("\nQuery 2: Sort Products by Price")
sort_products_by_price()

print("\nQuery 3: Filter Orders by Status and Customer")
filter_orders_by_status_and_customer('delivered', 'I74lXDOfoqsp')

print("\nQuery 4: Orders for a Specific Customer")
query_orders_by_customer('I74lXDOfoqsp')
