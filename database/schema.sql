-- PolyWhale Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    referrer_id BIGINT,
    referral_count INT DEFAULT 0,
    settings JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_users_referrer ON users(referrer_id);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = TRUE;

-- Whales table
CREATE TABLE IF NOT EXISTS whales (
    address VARCHAR(66) PRIMARY KEY,
    nickname VARCHAR(255),
    total_volume DECIMAL(20, 2) DEFAULT 0,
    total_trades INT DEFAULT 0,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    win_rate DECIMAL(5, 2) DEFAULT 0,
    last_trade_at TIMESTAMP,
    first_seen_at TIMESTAMP DEFAULT NOW(),
    is_tracked BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_whales_volume ON whales(total_volume DESC);
CREATE INDEX idx_whales_win_rate ON whales(win_rate DESC);
CREATE INDEX idx_whales_tracked ON whales(is_tracked) WHERE is_tracked = TRUE;
CREATE INDEX idx_whales_last_trade ON whales(last_trade_at DESC);

-- Trades table
CREATE TABLE IF NOT EXISTS trades (
    id VARCHAR(255) PRIMARY KEY,
    trader_address VARCHAR(66) NOT NULL,
    market_id VARCHAR(255) NOT NULL,
    market_name TEXT,
    side VARCHAR(10),
    size DECIMAL(20, 2) NOT NULL,
    price DECIMAL(10, 6),
    timestamp TIMESTAMP NOT NULL,
    transaction_hash VARCHAR(255),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_trades_trader ON trades(trader_address);
CREATE INDEX idx_trades_market ON trades(market_id);
CREATE INDEX idx_trades_timestamp ON trades(timestamp DESC);
CREATE INDEX idx_trades_size ON trades(size DESC);
CREATE INDEX idx_trades_created ON trades(created_at DESC);

-- Markets table
CREATE TABLE IF NOT EXISTS markets (
    market_id VARCHAR(255) PRIMARY KEY,
    question TEXT NOT NULL,
    description TEXT,
    category VARCHAR(100),
    end_date TIMESTAMP,
    volume DECIMAL(20, 2) DEFAULT 0,
    liquidity DECIMAL(20, 2) DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    last_updated TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_markets_category ON markets(category);
CREATE INDEX idx_markets_active ON markets(active) WHERE active = TRUE;
CREATE INDEX idx_markets_end_date ON markets(end_date);
CREATE INDEX idx_markets_volume ON markets(volume DESC);

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    filters JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_user ON alerts(user_id);
CREATE INDEX idx_alerts_active ON alerts(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_alerts_type ON alerts(alert_type);

-- Tracked whales table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS tracked_whales (
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    whale_address VARCHAR(66) NOT NULL REFERENCES whales(address) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, whale_address)
);

CREATE INDEX idx_tracked_user ON tracked_whales(user_id);
CREATE INDEX idx_tracked_whale ON tracked_whales(whale_address);

-- Notifications log (for tracking sent alerts)
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    trade_id VARCHAR(255) REFERENCES trades(id),
    notification_type VARCHAR(50) NOT NULL,
    sent_at TIMESTAMP DEFAULT NOW(),
    success BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_sent ON notifications(sent_at DESC);
CREATE INDEX idx_notifications_trade ON notifications(trade_id);

-- Create a function to update last_active timestamp
CREATE OR REPLACE FUNCTION update_last_active()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users SET last_active = NOW() WHERE user_id = NEW.user_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to auto-update last_active
CREATE TRIGGER trigger_update_last_active
AFTER INSERT ON notifications
FOR EACH ROW
EXECUTE FUNCTION update_last_active();

-- Create a view for whale leaderboard
CREATE OR REPLACE VIEW whale_leaderboard AS
SELECT 
    address,
    nickname,
    total_volume,
    total_trades,
    wins,
    losses,
    win_rate,
    last_trade_at,
    ROW_NUMBER() OVER (ORDER BY win_rate DESC, total_volume DESC) as rank
FROM whales
WHERE total_trades >= 10  -- Minimum 10 trades to be on leaderboard
ORDER BY win_rate DESC, total_volume DESC;

-- Create a view for market activity
CREATE OR REPLACE VIEW market_activity AS
SELECT 
    m.market_id,
    m.question,
    m.category,
    m.end_date,
    COUNT(t.id) as whale_trades_24h,
    SUM(t.size) as whale_volume_24h,
    m.volume as total_volume
FROM markets m
LEFT JOIN trades t ON m.market_id = t.market_id 
    AND t.timestamp > NOW() - INTERVAL '24 hours'
    AND t.size >= 10000
GROUP BY m.market_id, m.question, m.category, m.end_date, m.volume
ORDER BY whale_volume_24h DESC NULLS LAST;

-- Insert default admin user (optional)
-- INSERT INTO users (user_id, username, first_name, is_active)
-- VALUES (123456789, 'admin', 'Admin', TRUE)
-- ON CONFLICT (user_id) DO NOTHING;

COMMENT ON TABLE users IS 'Telegram bot users';
COMMENT ON TABLE whales IS 'Tracked whale traders';
COMMENT ON TABLE trades IS 'All trades from Polymarket';
COMMENT ON TABLE markets IS 'Polymarket markets';
COMMENT ON TABLE alerts IS 'User alert configurations';
COMMENT ON TABLE tracked_whales IS 'User-whale tracking relationships';
COMMENT ON TABLE notifications IS 'Sent notification log';

