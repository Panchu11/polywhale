"""
Backfill historical whale trades into Neon Postgres so leaderboards differ immediately.

Usage examples:
  # Backfill last 7 days
  DATABASE_URL=... python scripts/backfill_trades.py --days 7

  # Backfill last 30 days with a hard cap on pages
  python scripts/backfill_trades.py --days 30 --max-pages 500 --limit 200
"""
import argparse
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import os
import sys
# Ensure project root is on sys.path when running from scripts/
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

import aiohttp
from loguru import logger

from config.settings import settings
from bot.models import Trade
from bot.services.database import Database

DATA_API_BASE = settings.POLYMARKET_DATA_API.rstrip("/")


def parse_iso(dt: str) -> datetime:
    try:
        return datetime.fromisoformat(dt.replace("Z", "+00:00"))
    except Exception:
        return datetime.now(timezone.utc)


def parse_trade_item(item: Dict[str, Any]) -> Optional[Trade]:
    """Parse a Polymarket trade item into our Trade model.
    Returns None if parsing fails.
    """
    try:
        ts = item.get("timestamp")
        if isinstance(ts, int):
            # Convert to UTC then make naive (UTC)
            ts_dt = datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None)
        elif isinstance(ts, str):
            # Parse as aware then convert to naive UTC
            aware = parse_iso(ts)
            if aware.tzinfo is not None:
                ts_dt = aware.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                ts_dt = aware
        else:
            ts_dt = datetime.utcnow()

        size = float(item.get("size", 0) or 0)
        price = float(item.get("price", 0) or 0)
        value_usd = size * price

        trade = Trade(
            id=item.get("transactionHash", item.get("transaction_hash", "")),
            trader_address=item.get("proxyWallet", item.get("trader_address", "")),
            trader_name=item.get("name", None),
            trader_pseudonym=item.get("pseudonym", None),
            market_id=item.get("conditionId", item.get("asset", "")),
            market_name=item.get("title", item.get("market", "Unknown Market")),
            market_slug=item.get("slug", None),
            event_slug=item.get("eventSlug", None),
            outcome=item.get("outcome", None),
            side=item.get("side", "BUY"),
            size=value_usd,
            price=price,
            timestamp=ts_dt,
            transaction_hash=item.get("transactionHash", item.get("transaction_hash", "")),
        )
        return trade
    except Exception as e:
        logger.warning(f"Failed to parse trade item: {e}")
        return None


async def fetch_trades_page(
    session: aiohttp.ClientSession,
    limit: int = 200,
    before_iso: Optional[str] = None,
    offset: Optional[int] = None,
    cursor: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Fetch one page from the Polymarket trades endpoint.

    Returns (items, next_cursor). Items are raw dicts from the API.
    """
    params: Dict[str, str] = {"limit": str(limit)}
    if before_iso:
        params["before"] = before_iso
    if offset is not None:
        params["offset"] = str(offset)
    if cursor:
        params["cursor"] = cursor

    url = f"{DATA_API_BASE}/trades"
    async with session.get(url, params=params, timeout=30) as resp:
        if resp.status != 200:
            text = await resp.text()
            logger.error(f"GET {url} {params} -> {resp.status} {text[:200]}")
            return [], None
        data = await resp.json()

    # Many variants: list of trades OR dict with data + next/ cursor
    items: List[Dict[str, Any]]
    next_cursor: Optional[str] = None

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if isinstance(data.get("data"), list):
            items = data.get("data", [])
        elif isinstance(data.get("trades"), list):
            items = data.get("trades", [])
        else:
            # best effort: try to find a list value
            items = []
            for v in data.values():
                if isinstance(v, list):
                    items = v
                    break
        next_cursor = (
            data.get("next")
            or data.get("cursor")
            or data.get("nextCursor")
            or data.get("next_page_token")
        )
    else:
        items = []

    return items, next_cursor


async def backfill(days: int, limit: int, max_pages: int) -> None:
    cutoff = datetime.utcnow() - timedelta(days=days)  # naive UTC to match DB TIMESTAMP
    logger.info(
        f"Starting backfill for last {days}d (cutoff {cutoff.isoformat()}) with limit={limit}, max_pages={max_pages}"
    )

    db = Database()
    await db.connect()

    total_seen = 0
    total_saved = 0
    total_whale = 0

    strategy = "auto"  # will become one of: cursor | before | offset
    cursor: Optional[str] = None
    before_iso: Optional[str] = None
    offset: int = 0

    async with aiohttp.ClientSession() as session:
        prev_oldest: Optional[datetime] = None
        for page in range(1, max_pages + 1):
            items, next_cursor = await fetch_trades_page(
                session, limit=limit, before_iso=before_iso, offset=(offset if strategy == "offset" else None), cursor=cursor
            )
            if not items:
                logger.info("No items returned; stopping backfill.")
                break

            # Detect and lock in strategy if auto
            if strategy == "auto":
                if next_cursor:
                    strategy = "cursor"
                    cursor = next_cursor
                    logger.info("Pagination strategy: cursor")
                else:
                    # Estimate using timestamps
                    timestamps = []
                    for it in items:
                        ts = it.get("timestamp")
                        if isinstance(ts, int):
                            timestamps.append(datetime.fromtimestamp(ts, tz=timezone.utc))
                        elif isinstance(ts, str):
                            timestamps.append(parse_iso(ts))
                    if timestamps:
                        oldest = min(timestamps)
                        before_iso = (oldest - timedelta(seconds=1)).isoformat()
                        strategy = "before"
                        prev_oldest = oldest
                        logger.info("Pagination strategy: before=<iso>")
                    else:
                        strategy = "offset"
                        offset += limit
                        logger.info("Pagination strategy: offset")
            else:
                # Advance according to chosen strategy
                if strategy == "cursor":
                    cursor = next_cursor
                    if not cursor:
                        logger.info("Cursor exhausted; stopping.")
                        break
                elif strategy == "before":
                    # compute next before from this page
                    timestamps = []
                    for it in items:
                        ts = it.get("timestamp")
                        if isinstance(ts, int):
                            timestamps.append(datetime.fromtimestamp(ts, tz=timezone.utc))
                        elif isinstance(ts, str):
                            timestamps.append(parse_iso(ts))
                    if timestamps:
                        oldest = min(timestamps)
                        # If not getting older, fallback to offset
                        if prev_oldest and oldest >= prev_oldest:
                            logger.warning("'before' did not yield older data; switching to offset")
                            strategy = "offset"
                            offset += limit
                        else:
                            prev_oldest = oldest
                            before_iso = (oldest - timedelta(seconds=1)).isoformat()
                    else:
                        logger.warning("No timestamps found; switching to offset")
                        strategy = "offset"
                        offset += limit
                elif strategy == "offset":
                    offset += limit

            # Parse and store
            page_saved = 0
            page_whale = 0
            page_earliest: Optional[datetime] = None

            for item in items:
                trade = parse_trade_item(item)
                if not trade:
                    continue
                total_seen += 1

                # Track earliest ts in this page
                if not page_earliest or trade.timestamp < page_earliest:
                    page_earliest = trade.timestamp

                # Stop after we crossed the cutoff substantially
                if trade.timestamp < cutoff:
                    continue  # older than our window; we still check rest of items

                # Filter to whales
                if trade.size < settings.WHALE_THRESHOLD:
                    continue
                page_whale += 1

                # Save
                try:
                    await db.save_trade(trade)
                    await db.update_whale_stats(trade.trader_address)
                    page_saved += 1
                except Exception as e:
                    logger.warning(f"Failed to save trade {trade.id[:10]}...: {e}")

            total_saved += page_saved
            total_whale += page_whale

            logger.info(
                f"Page {page}: items={len(items)}, whales={page_whale}, saved={page_saved}, total_saved={total_saved}"
            )

            # Stop if earliest trade in the page is older than cutoff and we're not on cursor strategy
            if page_earliest and page_earliest < cutoff and strategy in ("before", "offset"):
                logger.info("Reached cutoff; stopping backfill.")
                break

            # Modest rate limit to be polite
            await asyncio.sleep(max(1.0 / max(settings.API_RATE_LIMIT, 1), 0.2))

    await db.close()
    logger.info(
        f"Backfill complete: seen={total_seen}, whales={total_whale}, saved={total_saved} (days={days})"
    )


async def amain(args: argparse.Namespace) -> None:
    await backfill(days=args.days, limit=args.limit, max_pages=args.max_pages)


def main():
    parser = argparse.ArgumentParser(description="Backfill historical whale trades")
    parser.add_argument("--days", type=int, default=30, help="Days of history to backfill")
    parser.add_argument("--limit", type=int, default=200, help="Trades per page to request")
    parser.add_argument("--max-pages", type=int, default=1000, help="Max pages to fetch")
    args = parser.parse_args()

    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=settings.LOG_LEVEL)

    asyncio.run(amain(args))


if __name__ == "__main__":
    main()

