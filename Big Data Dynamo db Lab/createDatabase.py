import boto3

# DynamoDB configuration
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # DynamoDB Local
    region_name='us-west-2',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

def create_table(table_name, key_schema, attribute_definitions):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table {table_name} created successfully")

# Create Customers table
create_table(
    'Customers',
    key_schema=[
        {'AttributeName': 'customer_id', 'KeyType': 'HASH'}
    ],
    attribute_definitions=[
        {'AttributeName': 'customer_id', 'AttributeType': 'S'}
    ]
)

# Create OrderItems table
create_table(
    'OrderItems',
    key_schema=[
        {'AttributeName': 'order_id', 'KeyType': 'HASH'},
        {'AttributeName': 'product_id', 'KeyType': 'RANGE'}
    ],
    attribute_definitions=[
        {'AttributeName': 'order_id', 'AttributeType': 'S'},
        {'AttributeName': 'product_id', 'AttributeType': 'S'}
    ]
)

# Create Orders table
create_table(
    'Orders',
    key_schema=[
        {'AttributeName': 'order_id', 'KeyType': 'HASH'}
    ],
    attribute_definitions=[
        {'AttributeName': 'order_id', 'AttributeType': 'S'}
    ]
)

# Create Products table
create_table(
    'Products',
    key_schema=[
        {'AttributeName': 'product_id', 'KeyType': 'HASH'}
    ],
    attribute_definitions=[
        {'AttributeName': 'product_id', 'AttributeType': 'S'}
    ]
)
