from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import boto3
import uuid

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure LocalStack resources
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566')
s3 = boto3.client('s3', endpoint_url='http://localhost:4566')

# DynamoDB tables
user_table = dynamodb.Table('Users')
post_table = dynamodb.Table('Posts')

# S3 Bucket for storing media
BUCKET_NAME = 'media-bucket'

# Helper: Upload a file to S3
def upload_to_s3(file, key):
    s3.upload_fileobj(file, BUCKET_NAME, key)
    return f"https://{BUCKET_NAME}.s3.localhost.localstack.cloud:4566/{key}"

# API: Create a User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.form
    file = request.files['image']

    # Upload user image to S3
    image_url = upload_to_s3(file, f"users/{data['email']}/profile.jpg")

    # Save user info in DynamoDB
    user = {
        'email': data['email'],
        'name': data['name'],
        'password': data['password'],  # Ideally, hash the password in production
        'image': image_url
    }
    user_table.put_item(Item=user)
    return jsonify(user), 201

# API: Create a Post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.form
    file = request.files.get('media')

    # Upload media to S3 if provided
    media_url = None
    if file:
        media_url = upload_to_s3(file, f"posts/{uuid.uuid4()}.jpg")

    # Save post info in DynamoDB
    post_id = str(uuid.uuid4())
    post = {
        'post_id': post_id,
        'email': data['email'],  # User who created the post
        'content': data['content'],
        'media': media_url,
        'likes': 0,
        'comments': []
    }
    post_table.put_item(Item=post)
    return jsonify(post), 201

# API: Like a Post
@app.route('/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    # Increment the like count
    response = post_table.update_item(
        Key={'post_id': post_id},
        UpdateExpression='SET likes = likes + :val',
        ExpressionAttributeValues={':val': 1},
        ReturnValues='UPDATED_NEW'
    )
    return jsonify(response['Attributes']), 200

# API: Comment on a Post
@app.route('/posts/<post_id>/comment', methods=['POST'])
def comment_post(post_id):
    data = request.json
    comment = {'email': data['email'], 'text': data['text']}

    # Add the comment to the post
    response = post_table.update_item(
        Key={'post_id': post_id},
        UpdateExpression='SET comments = list_append(comments, :val)',
        ExpressionAttributeValues={':val': [comment]},
        ReturnValues='UPDATED_NEW'
    )
    return jsonify(response['Attributes']), 200

# API: Get All Posts
@app.route('/posts', methods=['GET'])
def get_posts():
    response = post_table.scan()
    return jsonify(response['Items']), 200

if __name__ == '__main__':
    app.run(debug=True)
