"""
Broadcast service: periodically posts real-time whale highlights to a Telegram channel
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from loguru import logger

from config.settings import settings
from bot.services.database import Database


class BroadcastService:
    """Posts the largest whale trade in the last interval to a channel."""

    def __init__(self, db: Database, bot):
        self.db = db
        self.bot = bot
        self.is_running = False
        self.interval = int(getattr(settings, "BROADCAST_INTERVAL_SECONDS", 60) or 60)
        self.min_amount = int(getattr(settings, "BROADCAST_MIN_USD", 1000) or 1000)
        self.last_sent_trade_id: Optional[str] = None
        self._application = None  # set in start()
        # Track last tick to use non-overlapping time windows
        self._last_tick_at: Optional[datetime] = None

    def _get_channel_id(self) -> Optional[int]:
        """Resolve channel id from env or runtime capture (my_chat_member)."""
        # Prefer explicit env variable
        if getattr(settings, "TELEGRAM_CHANNEL_ID", ""):
            try:
                return int(settings.TELEGRAM_CHANNEL_ID)
            except ValueError:
                # If it's like @channelusername, bot API accepts it directly
                return settings.TELEGRAM_CHANNEL_ID  # type: ignore
        # Fallback to captured id in bot_data
        if self._application:
            cid = self._application.bot_data.get("broadcast_channel_id")
            return cid
        return None

    async def start(self, application) -> None:
        """Start the broadcast loop."""
        self._application = application
        if not getattr(settings, "BROADCAST_ENABLED", True):
            logger.info("BroadcastService disabled by settings (BROADCAST_ENABLED=false)")
            return

        # Ensure broadcast deduplication table exists
        try:
            await self.db.ensure_broadcast_log_table()
        except Exception as e:
            logger.warning(f"BroadcastService: failed to ensure broadcast_log table: {e}")

        self.is_running = True
        logger.info(
            f"BroadcastService started: interval={self.interval}s, min=${self.min_amount}"
        )
        try:
            while self.is_running:
                await self._tick()
                await asyncio.sleep(self.interval)
        except Exception as e:
            logger.error(f"BroadcastService error: {e}")
        finally:
            logger.info("BroadcastService loop ended")

    async def stop(self) -> None:
        self.is_running = False

    async def _tick(self) -> None:
        channel_id = self._get_channel_id()
        if not channel_id:
            logger.debug("BroadcastService: channel id not set yet; skipping this tick")
            return

        # Determine a non-overlapping window: [start, end)
        end = datetime.utcnow()
        start = self._last_tick_at or (end - timedelta(seconds=self.interval))
        # Move window forward for the next tick
        self._last_tick_at = end

        trade = await self.db.get_largest_whale_trade_between(start, end, self.min_amount)
        if not trade:
            logger.debug(
                f"BroadcastService: no qualifying trade in window {start.isoformat()} → {end.isoformat()}"
            )
            return

        # In-process guard against accidental double-send
        if trade.id == self.last_sent_trade_id:
            logger.debug("BroadcastService: trade already sent in this window; skipping")
            return

        # Cross-process dedup: only one instance should broadcast a given trade id
        inserted = await self.db.try_record_broadcast(trade.id)
        if not inserted:
            logger.debug("BroadcastService: trade already broadcasted previously; skipping")
            return

        agg = await self.db.get_trader_aggregate(trade.trader_address)
        message = self._format_message(trade, agg)

        try:
            await self.bot.send_message(chat_id=channel_id, text=message, parse_mode="Markdown")
            self.last_sent_trade_id = trade.id
            logger.info(
                f"BroadcastService: posted trade {trade.id} (${trade.size:,.0f}) to channel {channel_id}"
            )
        except Exception as e:
            logger.error(f"BroadcastService: failed to send message: {e}")

    def _format_message(self, trade, agg) -> str:
        # Profile URL
        profile_url = f"https://polymarket.com/profile/{trade.trader_address}"
        # Trader display
        trader_display = f"[{trade.trader_address[:6]}...{trade.trader_address[-4:]}]({profile_url})"
        # Side/price text
        side = (trade.side or "").upper()
        price_txt = f" @ {float(trade.price):.2f}" if trade.price is not None else ""
        # Market name
        market_name = trade.market_name or trade.market_id

        total_trades = agg.get("total_trades", 0)
        total_volume = agg.get("total_volume", 0.0)

        lines = [
            f"🔥 Biggest Whale Trade in the last {self.interval} seconds",
            f"• Trader: {trader_display}",
            f"• Trade: ${float(trade.size):,.0f} — {side}{price_txt}",
            f"• Market: {market_name}",
            f"• Lifetime: {total_trades} trades | ${float(total_volume):,.0f} volume",
            # PnL not reliably available yet; add later when outcome data exists
        ]
        return "\n".join(lines)

