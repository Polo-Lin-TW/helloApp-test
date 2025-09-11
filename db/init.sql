-- Initialize database schema
CREATE DATABASE IF NOT EXISTS helloapp;
USE helloapp;

-- Create messages table to store user messages
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO messages (name, message) VALUES 
('System', 'Welcome to HelloApp database!'),
('Demo User', 'Hello from the database!');