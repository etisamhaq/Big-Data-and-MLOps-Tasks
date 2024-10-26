import boto3

# Configure DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # Change if using a different endpoint
    region_name='us-west-2',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

def delete_table(table_name):
    table = dynamodb.Table(table_name)
    
    # Check if the table exists
    try:
        table.load()  # Load the table details
        print(f"Deleting table: {table_name}")
        table.delete()  # Delete the table
        table.wait_until_not_exists()  # Wait until the table is deleted
        print(f"Table {table_name} deleted successfully!")
    except Exception as e:
        print(f"Error deleting table {table_name}: {e}")

def main():
    # List of tables to delete
    tables_to_delete = ['Orders', 'Products']
    
    for table_name in tables_to_delete:
        delete_table(table_name)

if __name__ == '__main__':
    main()
