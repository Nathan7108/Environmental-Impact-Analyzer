# SQLite Database Setup
import sqlite3
from pathlib import Path

# Define the database file path
DB_FILE = Path(__file__).parent / "products.db"

# Create and initialize the database
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL
    )
    """)
    conn.commit()

    # Seed the database with sample data
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:  # Only seed if table is empty
        sample_products = [
            ("Smartphone", "Electronics"),
            ("T-shirt", "Clothing"),
            ("Laptop", "Electronics"),
        ]
        cursor.executemany("INSERT INTO products (name, category) VALUES (?, ?)", sample_products)
        conn.commit()

    conn.close()

# Dependency to create a new SQLite connection for each request
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This allows fetching results as dictionaries
    return conn
