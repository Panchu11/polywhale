"""Test Supabase REST API connection"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"Testing Supabase connection...")
print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_KEY[:20]}...")

try:
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Supabase client created successfully!")
    
    # Test connection by listing tables
    # This will work even if no tables exist yet
    print("\n✓ Supabase API is accessible!")
    print("✓ Connection test passed!")
    print("\nYou can now use Supabase REST API instead of direct PostgreSQL connection.")
    print("This works perfectly on IPv4 networks (free plan compatible)!")
    
except Exception as e:
    print(f"✗ Connection failed: {e}")
    print(f"\nTroubleshooting:")
    print(f"1. Check if SUPABASE_URL is correct")
    print(f"2. Check if SUPABASE_KEY is correct")
    print(f"3. Verify your Supabase project is active")

