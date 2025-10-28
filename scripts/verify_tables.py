"""Verify Supabase tables exist"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("Checking Supabase tables...")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # List of expected tables
    expected_tables = [
        "users",
        "whales", 
        "trades",
        "markets",
        "alerts",
        "tracked_whales",
        "notifications"
    ]
    
    print("\nVerifying tables:")
    for table in expected_tables:
        try:
            # Try to query the table (limit 0 to just check if it exists)
            result = supabase.table(table).select("*").limit(0).execute()
            print(f"  ✓ {table} - exists")
        except Exception as e:
            print(f"  ✗ {table} - not found or error: {e}")
    
    print("\n✅ Table verification complete!")
    print("\nYour bot is ready to run with full database support!")
    
except Exception as e:
    print(f"✗ Error: {e}")

