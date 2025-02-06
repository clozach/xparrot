"""Database migration script for xParrot."""
import os
import mysql.connector
from dotenv import load_dotenv
from .database import init_db

load_dotenv()

def create_database():
    """Create the database if it doesn't exist."""
    DB_USER = os.getenv('MYSQL_USER', 'root')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
    DB_NAME = os.getenv('MYSQL_DATABASE', 'xparrot')
    
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = connection.cursor()
    
    try:
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully")
        
        # Initialize SQLAlchemy models
        init_db()
        print("Database tables created successfully")
        
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    create_database()
