"""Test database connection with psycopg2"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Testing database connection...")
print(f"Database URL: {DATABASE_URL[:50]}...")

try:
    # Try to connect
    conn = psycopg2.connect(DATABASE_URL)
    print("✓ Successfully connected to database!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✓ PostgreSQL version: {version[0]}")
    
    cursor.close()
    conn.close()
    print("✓ Connection closed successfully")
    
except Exception as e:
    print(f"✗ Connection failed: {e}")
    print(f"\nTroubleshooting:")
    print(f"1. Check if your Supabase project is active")
    print(f"2. Verify the database password is correct")
    print(f"3. Check if you have internet connection")
    print(f"4. Make sure the database host is accessible")

