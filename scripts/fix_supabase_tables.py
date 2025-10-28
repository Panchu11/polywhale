"""
Fix Supabase tables to match the bot's expected schema
Run this to create/update tables with correct columns
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("This script will help you create the correct table structure.")
print("\nGo to your Supabase dashboard:")
print(f"https://supabase.com/dashboard/project/hkcdmrhamilgukuyfigd/editor")
print("\nClick on 'SQL Editor' and run this SQL:\n")

sql = """
-- Drop existing tables if they have wrong schema
-- DROP TABLE IF EXISTS users CASCADE;
-- DROP TABLE IF EXISTS whales CASCADE;
-- DROP TABLE IF EXISTS trades CASCADE;
-- DROP TABLE IF EXISTS markets CASCADE;
-- DROP TABLE IF EXISTS alerts CASCADE;
-- DROP TABLE IF EXISTS tracked_whales CASCADE;
-- DROP TABLE IF EXISTS notifications CASCADE;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    whale_threshold INTEGER DEFAULT 10000,
    notifications_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create whales table
CREATE TABLE IF NOT EXISTS whales (
    id BIGSERIAL PRIMARY KEY,
    address TEXT UNIQUE NOT NULL,
    nickname TEXT,
    total_volume NUMERIC DEFAULT 0,
    total_trades INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    last_trade_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create markets table
CREATE TABLE IF NOT EXISTS markets (
    id BIGSERIAL PRIMARY KEY,
    market_id TEXT UNIQUE NOT NULL,
    question TEXT NOT NULL,
    description TEXT,
    category TEXT,
    end_date TIMESTAMP WITH TIME ZONE,
    volume NUMERIC DEFAULT 0,
    liquidity NUMERIC DEFAULT 0,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create trades table
CREATE TABLE IF NOT EXISTS trades (
    id BIGSERIAL PRIMARY KEY,
    trade_id TEXT UNIQUE NOT NULL,
    trader_address TEXT NOT NULL,
    market_id TEXT NOT NULL,
    market_name TEXT,
    side TEXT,
    size NUMERIC NOT NULL,
    price NUMERIC,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    transaction_hash TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    alert_type TEXT NOT NULL,
    threshold NUMERIC,
    market_id TEXT,
    whale_address TEXT,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create tracked_whales table
CREATE TABLE IF NOT EXISTS tracked_whales (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    whale_address TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, whale_address)
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
    notification_type TEXT NOT NULL,
    message TEXT,
    trade_id TEXT,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_trades_trader ON trades(trader_address);
CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_trades_size ON trades(size DESC);
CREATE INDEX IF NOT EXISTS idx_tracked_whales_user ON tracked_whales(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_user ON alerts(user_id);
"""

print(sql)
print("\n" + "="*80)
print("After running this SQL, press Enter to test the connection...")
input()

# Test connection
client = create_client(supabase_url, supabase_key)

print("\nTesting tables...")
try:
    # Test users table
    result = client.table("users").select("telegram_id").limit(1).execute()
    print("✅ users table OK")
except Exception as e:
    print(f"❌ users table error: {e}")

try:
    # Test trades table
    result = client.table("trades").select("trade_id").limit(1).execute()
    print("✅ trades table OK")
except Exception as e:
    print(f"❌ trades table error: {e}")

try:
    # Test whales table
    result = client.table("whales").select("address").limit(1).execute()
    print("✅ whales table OK")
except Exception as e:
    print(f"❌ whales table error: {e}")

try:
    # Test markets table
    result = client.table("markets").select("market_id").limit(1).execute()
    print("✅ markets table OK")
except Exception as e:
    print(f"❌ markets table error: {e}")

try:
    # Test tracked_whales table
    result = client.table("tracked_whales").select("user_id").limit(1).execute()
    print("✅ tracked_whales table OK")
except Exception as e:
    print(f"❌ tracked_whales table error: {e}")

print("\n✅ All tables ready!")

