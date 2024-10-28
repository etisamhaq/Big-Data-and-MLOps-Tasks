import pyodbc
import time
import matplotlib.pyplot as plt
from faker import Faker
import random


# Connect to MS SQL Server database
server = "DESKTOP-RHT316C"
database = "facebook"

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
)
cursor = conn.cursor()


# Initialize Faker
fake = Faker()


# Create tables
cursor.execute(
    """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
    CREATE TABLE Users (
        UserID INT PRIMARY KEY IDENTITY(1,1),
        FirstName NVARCHAR(50),
        LastName NVARCHAR(50),
        Email NVARCHAR(100),
        ProfilePictureURL NVARCHAR(200)
    )
"""
)


cursor.execute(
    """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Posts')
    CREATE TABLE Posts (
        PostID INT PRIMARY KEY IDENTITY(1,1),
        UserID INT,
        PostContent NVARCHAR(200),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
"""
)


cursor.execute(
    """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Comments')
    CREATE TABLE Comments (
        CommentID INT PRIMARY KEY IDENTITY(1,1),
        PostID INT,
        UserID INT,
        CommentContent NVARCHAR(200),
        FOREIGN KEY (PostID) REFERENCES Posts(PostID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
"""
)


cursor.execute(
    """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Likes')
    CREATE TABLE Likes (
        LikeID INT PRIMARY KEY IDENTITY(1,1),
        PostID INT,
        UserID INT,
        FOREIGN KEY (PostID) REFERENCES Posts(PostID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
"""
)


# Function to get last ID from table
def get_last_id(table_name):
    cursor.execute(f"SELECT MAX({table_name[:-1]}ID) FROM {table_name}")
    last_id = cursor.fetchone()[0]
    return last_id if last_id else 0


# Function to populate Users table
def populate_users(num_records):
    users = [
        (
            fake.first_name(),
            fake.last_name(),
            fake.email(),
            fake.image_url(),
        )
        for _ in range(num_records)
    ]
    cursor.executemany(
        "INSERT INTO Users (FirstName, LastName, Email, ProfilePictureURL) VALUES (?, ?, ?, ?)",
        users,
    )
    conn.commit()


# Function to populate Posts table
def populate_posts(num_records):
    user_ids = [row[0] for row in cursor.execute("SELECT UserID FROM Users").fetchall()]
    posts = [
        (random.choice(user_ids), fake.text(max_nb_chars=50))
        for _ in range(num_records)
    ]
    cursor.executemany("INSERT INTO Posts (UserID, PostContent) VALUES (?, ?)", posts)
    conn.commit()


# Function to populate Comments table
def populate_comments(num_records):
    post_ids = [row[0] for row in cursor.execute("SELECT PostID FROM Posts").fetchall()]
    user_ids = [row[0] for row in cursor.execute("SELECT UserID FROM Users").fetchall()]
    comments = [
        (random.choice(post_ids), random.choice(user_ids), fake.text(max_nb_chars=50))
        for _ in range(num_records)
    ]
    cursor.executemany(
        "INSERT INTO Comments (PostID, UserID, CommentContent) VALUES (?, ?, ?)",
        comments,
    )
    conn.commit()


# Function to populate Likes table
def populate_likes(num_records):
    post_ids = [row[0] for row in cursor.execute("SELECT PostID FROM Posts").fetchall()]
    user_ids = [row[0] for row in cursor.execute("SELECT UserID FROM Users").fetchall()]
    likes = [
        (random.choice(post_ids), random.choice(user_ids))
        for _ in range(num_records)
    ]
    cursor.executemany("INSERT INTO Likes (PostID, UserID) VALUES (?, ?)", likes)
    conn.commit()


# Function to execute query and measure execution time
def execute_query(query_name, query):
    start_time = time.time()
    cursor.execute(query)
    cursor.fetchall()
    end_time = time.time()
    return end_time - start_time


# Function to run test with varying number of records
def run_test(users_records, posts_records, comments_records, likes_records):
    populate_users(users_records)
    populate_posts(posts_records)
    populate_comments(comments_records)
    populate_likes(likes_records)

    # Execute queries and measure execution time
    queries = {
        "Simple Query (Users)": "SELECT * FROM Users",
                "Simple Query (Posts)": "SELECT * FROM Posts",
        "Simple Query (Comments)": "SELECT * FROM Comments",
        "Complex Query (Comments with Posts and Users)": """
            SELECT * 
            FROM Comments 
            JOIN Posts ON Comments.PostID = Posts.PostID 
            JOIN Users ON Comments.UserID = Users.UserID
        """,
        "Complex Query (Users Name who liked and Post content)": """
            SELECT 
            p.PostID,
            p.PostContent,
            l.LikeID,
            u.FirstName, 
            u.LastName
        FROM 
            Likes l
        JOIN 
            Posts p ON l.PostID = p.PostID
        JOIN 
            Users u ON l.UserID = u.UserID
        ORDER BY 
            p.PostID
        """,
    }

    execution_times = {}
    for query_name, query in queries.items():
        execution_times[query_name] = execute_query(query_name, query)

    return execution_times


# Get number of users, posts, and comments from database
cursor.execute("SELECT COUNT(*) FROM Users")
num_users = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Posts")
num_posts = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Comments")
num_comments = cursor.fetchone()[0]

# Execute queries with varying number of records and store results
record_sizes = [
    (100, 500, 1000, 350),
    (1000, 5000, 10000, 3500),
    (10000, 50000, 100000, 40000),
    (100000, 500000, 1000000, 400000),
]

results = {}
for record_size in record_sizes:
    (
        users_records,
        posts_records,
        comments_records,
        likes_records,
    ) = record_size
    execution_times = run_test(
        users_records,
        posts_records,
        comments_records,
        likes_records,
    )
    results[record_size] = execution_times
    print(f"Record Size: {record_size}")
    for query_name, execution_time in execution_times.items():
        print(f"  {query_name}: {execution_time:.2f} seconds")


# Plot graph
for query_name in results[record_sizes[0]].keys():
    execution_times = [results[record_size][query_name] for record_size in record_sizes]
    plt.plot(
        [sum(record_size) for record_size in record_sizes],
        execution_times,
        label=query_name,
    )

plt.xlabel("Total Number of Records")
plt.ylabel("Query Execution Time (seconds)")
plt.title("Query Execution Time vs Number of Records (MS SQL Server)")
plt.legend()
plt.show()


# Close connection
conn.close()