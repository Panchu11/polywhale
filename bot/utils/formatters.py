"""
Formatting utilities
"""
from datetime import datetime


def format_size(size: float) -> str:
    """Format trade size for display"""
    if size >= 1_000_000:
        return f"${size / 1_000_000:.2f}M"
    elif size >= 1_000:
        return f"${size / 1_000:.1f}k"
    return f"${size:.2f}"


def format_price(price: float) -> str:
    """Format price as percentage"""
    return f"{price * 100:.1f}%"


def shorten_address(address: str) -> str:
    """Shorten Ethereum address"""
    if len(address) < 10:
        return address
    return f"{address[:6]}...{address[-4:]}"


def format_time_ago(timestamp: datetime) -> str:
    """Format timestamp as time ago (assumes naive UTC when tzinfo is None)."""
    from datetime import timezone
    now = datetime.utcnow()

    # Normalize to naive UTC
    if getattr(timestamp, "tzinfo", None) is not None:
        timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)

    delta = now - timestamp
    total_seconds = int(delta.total_seconds())

    if total_seconds < 60:
        return "just now"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes}m ago"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours}h ago"
    elif delta.days == 1:
        return "yesterday"
    elif delta.days < 7:
        return f"{delta.days}d ago"
    else:
        return timestamp.strftime("%Y-%m-%d")


def get_whale_emoji(size: float) -> str:
    """Get emoji based on trade size"""
    if size >= 100000:
        return "🐋"  # Large whale
    elif size >= 50000:
        return "🐳"  # Medium whale
    else:
        return "🐬"  # Small whale


def format_percentage(value: float) -> str:
    """Format value as percentage"""
    return f"{value:.1f}%"


def format_number(value: float) -> str:
    """Format number with commas"""
    return f"{value:,.0f}"

