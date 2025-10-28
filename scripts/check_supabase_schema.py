"""Check actual Supabase table schema"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

client = create_client(supabase_url, supabase_key)

print("=== CHECKING SUPABASE TABLES ===\n")

# Check users table
print("1. USERS TABLE:")
try:
    result = client.table("users").select("*").limit(1).execute()
    if result.data:
        print(f"   Columns: {list(result.data[0].keys())}")
    else:
        print("   Table is empty, trying to get schema...")
        # Try inserting a test row to see what columns are expected
        print("   Please tell me what columns you created in the users table")
except Exception as e:
    print(f"   Error: {e}")

print("\n2. TRADES TABLE:")
try:
    result = client.table("trades").select("*").limit(1).execute()
    if result.data:
        print(f"   Columns: {list(result.data[0].keys())}")
    else:
        print("   Table is empty")
except Exception as e:
    print(f"   Error: {e}")

print("\n3. WHALES TABLE:")
try:
    result = client.table("whales").select("*").limit(1).execute()
    if result.data:
        print(f"   Columns: {list(result.data[0].keys())}")
    else:
        print("   Table is empty")
except Exception as e:
    print(f"   Error: {e}")

print("\n4. MARKETS TABLE:")
try:
    result = client.table("markets").select("*").limit(1).execute()
    if result.data:
        print(f"   Columns: {list(result.data[0].keys())}")
    else:
        print("   Table is empty")
except Exception as e:
    print(f"   Error: {e}")

print("\n5. TRACKED_WHALES TABLE:")
try:
    result = client.table("tracked_whales").select("*").limit(1).execute()
    if result.data:
        print(f"   Columns: {list(result.data[0].keys())}")
    else:
        print("   Table is empty")
except Exception as e:
    print(f"   Error: {e}")

print("\n6. ALERTS TABLE:")
try:
    result = client.table("alerts").select("*").limit(1).execute()
    if result.data:
        print(f"   Columns: {list(result.data[0].keys())}")
    else:
        print("   Table is empty")
except Exception as e:
    print(f"   Error: {e}")

print("\n7. NOTIFICATIONS TABLE:")
try:
    result = client.table("notifications").select("*").limit(1).execute()
    if result.data:
        print(f"   Columns: {list(result.data[0].keys())}")
    else:
        print("   Table is empty")
except Exception as e:
    print(f"   Error: {e}")

