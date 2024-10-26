import boto3
import pandas as pd
from decimal import Decimal

# Configure DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='us-west-2',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

def sanitize_item(item):
    """Replace NaN and Infinity values in the item."""
    for key, value in item.items():
        if isinstance(value, float):
            # Replace NaN with None
            if pd.isna(value) or value == float('inf') or value == float('-inf'):
                item[key] = None  # or you can set a default value, e.g., 0
            else:
                item[key] = Decimal(str(value))  # Convert float to Decimal for DynamoDB
    return item
# Convert float values to Decimal for DynamoDB
def float_to_decimal(item):
    for key, value in item.items():
        if isinstance(value, float):
            item[key] = Decimal(str(value))  # Convert float to Decimal
        elif isinstance(value, dict):
            float_to_decimal(value)  # Recursively handle nested dictionaries
    return item

# Insert data into DynamoDB table with Decimal handling
def insert_data_into_table(table_name, data):
    table = dynamodb.Table(table_name)
    for _, row in data.iterrows():
        item = row.to_dict()
        item = sanitize_item(item)  # Ensure float values are converted to Decimal
        table.put_item(Item=item)
    print(f"Data inserted into {table_name} table successfully!")

# Insert Customers data
def insert_customers_data():
    df_customers = pd.read_csv(r'E:\University\Semester 7\Big Data\Dynamo lab\Dynamo lab\LabTasks\Data\df_Customers.csv')
    insert_data_into_table('Customers', df_customers)

# Insert OrderItems data
def insert_order_items_data():
    df_order_items = pd.read_csv(r'E:\University\Semester 7\Big Data\Dynamo lab\Dynamo lab\LabTasks\Data\df_OrderItems.csv')
    insert_data_into_table('OrderItems', df_order_items)

# Insert Orders data
def insert_orders_data():
    df_orders = pd.read_csv(r'E:\University\Semester 7\Big Data\Dynamo lab\Dynamo lab\LabTasks\Data\df_Orders.csv')
    insert_data_into_table('Orders', df_orders)

# Insert Products data
def insert_products_data():
    df_products = pd.read_csv(r'E:\University\Semester 7\Big Data\Dynamo lab\Dynamo lab\LabTasks\Data\df_Products.csv')
    insert_data_into_table('Products', df_products)

# Main function to insert all data
def main():
    # insert_customers_data()
    # insert_order_items_data()
    insert_orders_data()
    insert_products_data()

if __name__ == '__main__':
    main()

