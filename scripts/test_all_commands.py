"""Test all bot functionality and verify Polymarket URLs"""
import asyncio
import aiohttp
import json

async def test_polymarket_urls():
    """Test actual Polymarket URLs to verify format"""
    print("=" * 80)
    print("TESTING POLYMARKET URL FORMATS")
    print("=" * 80)
    
    async with aiohttp.ClientSession() as session:
        # Get a real trade
        url = "https://data-api.polymarket.com/trades?limit=5"
        async with session.get(url) as response:
            trades = await response.json()
            
            if trades:
                trade = trades[0]
                print("\n📊 SAMPLE TRADE DATA:")
                print(f"Trader Name: {trade.get('name', 'N/A')}")
                print(f"Trader Pseudonym: {trade.get('pseudonym', 'N/A')}")
                print(f"Proxy Wallet: {trade.get('proxyWallet', 'N/A')}")
                print(f"Market Title: {trade.get('title', 'N/A')}")
                print(f"Market Slug: {trade.get('slug', 'N/A')}")
                print(f"Event Slug: {trade.get('eventSlug', 'N/A')}")
                
                # Test profile URL
                if trade.get('name'):
                    profile_url = f"https://polymarket.com/profile/{trade['name']}"
                    print(f"\n🔗 PROFILE URL: {profile_url}")
                    
                    # Test if URL works
                    async with session.get(profile_url) as resp:
                        print(f"   Status: {resp.status}")
                        if resp.status == 200:
                            print("   ✅ Profile URL works!")
                        else:
                            print("   ❌ Profile URL doesn't work")
                
                # Test market URL with slug
                if trade.get('slug'):
                    market_url = f"https://polymarket.com/event/{trade['slug']}"
                    print(f"\n🔗 MARKET URL (slug): {market_url}")
                    
                    async with session.get(market_url) as resp:
                        print(f"   Status: {resp.status}")
                        if resp.status == 200:
                            print("   ✅ Market URL works!")
                        else:
                            print("   ❌ Market URL doesn't work")
                
                # Test market URL with eventSlug
                if trade.get('eventSlug'):
                    event_url = f"https://polymarket.com/event/{trade['eventSlug']}"
                    print(f"\n🔗 EVENT URL (eventSlug): {event_url}")
                    
                    async with session.get(event_url) as resp:
                        print(f"   Status: {resp.status}")
                        if resp.status == 200:
                            print("   ✅ Event URL works!")
                        else:
                            print("   ❌ Event URL doesn't work")
        
        # Get a real market
        print("\n" + "=" * 80)
        print("TESTING MARKET URLS")
        print("=" * 80)
        
        url = "https://gamma-api.polymarket.com/markets?limit=3&closed=false"
        async with session.get(url) as response:
            markets = await response.json()
            
            if markets:
                market = markets[0]
                print(f"\n📊 SAMPLE MARKET DATA:")
                print(f"Question: {market.get('question', 'N/A')}")
                print(f"Slug: {market.get('slug', 'N/A')}")
                print(f"ID: {market.get('id', 'N/A')}")
                
                # Test market URL
                if market.get('slug'):
                    market_url = f"https://polymarket.com/event/{market['slug']}"
                    print(f"\n🔗 MARKET URL: {market_url}")
                    
                    async with session.get(market_url) as resp:
                        print(f"   Status: {resp.status}")
                        if resp.status == 200:
                            print("   ✅ Market URL works!")
                        else:
                            print("   ❌ Market URL doesn't work")
                            
                            # Try alternative format
                            alt_url = f"https://polymarket.com/market/{market['slug']}"
                            print(f"\n🔗 TRYING ALTERNATIVE: {alt_url}")
                            async with session.get(alt_url) as resp2:
                                print(f"   Status: {resp2.status}")
                                if resp2.status == 200:
                                    print("   ✅ Alternative URL works!")

async def main():
    await test_polymarket_urls()
    
    print("\n" + "=" * 80)
    print("URL FORMAT RECOMMENDATIONS:")
    print("=" * 80)
    print("Profile: https://polymarket.com/profile/{name}")
    print("Market:  https://polymarket.com/event/{slug}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

