CREATE DATABASE facebook;
USE facebook;

-- Users table with primary key
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),        -- Limited space for the name to 50 characters
    email VARCHAR(50),       -- Reduced email length to 50 characters
    password CHAR(12),       -- Exactly 12 characters for password
    phone VARCHAR(15)        -- Minimal space for phone numbers (15 characters)
);

-- Posts table with user_id and primary key
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,             -- Foreign key relationship (not enforced here)
    content VARCHAR(255)     -- Limited post content to 255 characters
);

-- Likes table with primary key and post_id, user_id
CREATE TABLE likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,             -- Foreign key to posts (not enforced here)
    user_id INT              -- Foreign key to users (not enforced here)
);

-- Comments table with primary key and post_id, user_id
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT,             -- Foreign key to posts (not enforced here)
    user_id INT,             -- Foreign key to users (not enforced here)
    comment VARCHAR(255)     -- Limited comment content to 255 characters
);

-- 	ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';

