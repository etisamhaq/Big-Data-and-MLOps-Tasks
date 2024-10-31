from flask import Flask, request, jsonify
import boto3
import uuid
from datetime import datetime
import os
import pymysql

# Flask App
app = Flask(__name__)

# AWS S3 Configuration (pointing to LocalStack)
s3 = boto3.client(
    's3',
    aws_access_key_id='dummy',  # Use dummy credentials
    aws_secret_access_key='dummy',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1'
)
BUCKET_NAME = 'media-bucket'

# DynamoDB Configuration (pointing to LocalStack)
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1'
)
posts_table = dynamodb.Table('fb_Posts')
likes_table = dynamodb.Table('fb_Likes')
comments_table = dynamodb.Table('fb_Comments')

# MySQL Database Configuration
db = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='facebook_database'
)
cursor = db.cursor()

# Helper function: Upload to S3
def upload_to_s3(file, key):
    try:
        s3.upload_fileobj(file, BUCKET_NAME, key)
        return f"http://localhost:4566/{BUCKET_NAME}/{key}"
    except Exception as e:
        return str(e)

# 1. API: Create User

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.form
    username = data['username']
    email = data['email']
    profile_pic = request.files['profile_pic']

    user_id = str(uuid.uuid4())
    profile_pic_url = upload_to_s3(profile_pic, f"profile_pics/{user_id}.jpg")

    query = "INSERT INTO users (username, email, profile_pic) VALUES (%s, %s, %s)"
    values = (username, email, profile_pic_url)
    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "User created", "user_id": user_id}), 201

# 2. API: Create Post
@app.route('/create_post', methods=['POST'])
def create_post():
    data = request.form
    user_id = data['user_id']
    content = data['content']
    media = request.files.get('media')

    post_id = str(uuid.uuid4())
    media_url = upload_to_s3(media, f"posts/{post_id}.jpg") if media else None

    posts_table.put_item(Item={
        'post_id': post_id,
        'user_id': user_id,
        'content': content,
        'media_url': media_url,
        'created_at': datetime.utcnow().isoformat()
    })

    return jsonify({"message": "Post created", "post_id": post_id}), 201

# 3. API: Add Like
@app.route('/add_like', methods=['POST'])
def add_like():
    data = request.json
    post_id = data['post_id']
    user_id = data['user_id']

    like_id = str(uuid.uuid4())
    likes_table.put_item(Item={
        'like_id': like_id,
        'post_id': post_id,
        'user_id': user_id,
        'liked_at': datetime.utcnow().isoformat()
    })

    return jsonify({"message": "Like added", "like_id": like_id}), 201

# 4. API: Add Comment
@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    post_id = data['post_id']
    user_id = data['user_id']
    comment_text = data['comment_text']

    comment_id = str(uuid.uuid4())
    comments_table.put_item(Item={
        'comment_id': comment_id,
        'post_id': post_id,
        'user_id': user_id,
        'comment_text': comment_text,
        'commented_at': datetime.utcnow().isoformat()
    })

    return jsonify({"message": "Comment added", "comment_id": comment_id}), 201

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
