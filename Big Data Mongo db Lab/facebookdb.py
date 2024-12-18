from pymongo import MongoClient
from datetime import datetime
import uuid

class FacebookDB:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['facebook_db']
        self.users = self.db['users']

    def create_user(self, name, email):
        """Create a new user"""
        user = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "posts": [],
            "created_at": datetime.now()
        }
        return self.users.insert_one(user)

    def create_post(self, user_id, text):
        """Create a new post for a user"""
        post = {
            "post_id": str(uuid.uuid4()),
            "text": text,
            "likes": [],
            "comments": [],
            "created_at": datetime.now()
        }
        
        return self.users.update_one(
            {"_id": user_id},
            {"$push": {"posts": post}}
        )

    def add_like(self, post_user_id, post_id, liker_id):
        """Add a like to a post"""
        return self.users.update_one(
            {
                "_id": post_user_id,
                "posts.post_id": post_id
            },
            {"$addToSet": {"posts.$.likes": liker_id}}
        )

    def add_comment(self, post_user_id, post_id, commenter_id, comment_text):
        """Add a comment to a post"""
        comment = {
            "comment_id": str(uuid.uuid4()),
            "user_id": commenter_id,
            "text": comment_text,
            "created_at": datetime.now()
        }
        
        return self.users.update_one(
            {
                "_id": post_user_id,
                "posts.post_id": post_id
            },
            {"$push": {"posts.$.comments": comment}}
        )

    def get_user_posts(self, user_id):
        """Get all posts for a user"""
        user = self.users.find_one({"_id": user_id})
        return user.get('posts', []) if user else []

    def get_post(self, user_id, post_id):
        """Get a specific post"""
        user = self.users.find_one(
            {"_id": user_id},
            {"posts": {"$elemMatch": {"post_id": post_id}}}
        )
        return user.get('posts', [None])[0] if user else None

# Example usage
def main():
    fb_db = FacebookDB()

    # Create users
    user1 = fb_db.create_user("John Doe", "john@example.com")
    user2 = fb_db.create_user("Jane Smith", "jane@example.com")
    
    user1_id = user1.inserted_id
    user2_id = user2.inserted_id

    # Create posts
    fb_db.create_post(user1_id, "Hello, this is my first post!")
    fb_db.create_post(user1_id, "Another amazing day!")

    # Get user's posts
    posts = fb_db.get_user_posts(user1_id)
    first_post_id = posts[0]['post_id']

    # Add likes
    fb_db.add_like(user1_id, first_post_id, user2_id)

    # Add comments
    fb_db.add_comment(user1_id, first_post_id, user2_id, "Great post!")

    # Display the post with likes and comments
    updated_post = fb_db.get_post(user1_id, first_post_id)
    print("\nUpdated Post:")
    print(f"Text: {updated_post['text']}")
    print(f"Likes: {len(updated_post['likes'])}")
    print("Comments:")
    for comment in updated_post['comments']:
        print(f"- {comment['text']}")

if __name__ == "__main__":
    main()
