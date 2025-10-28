"""Test different profile URL formats"""
import asyncio
import aiohttp

async def test_profile_formats():
    """Test different profile URL formats"""
    
    async with aiohttp.ClientSession() as session:
        # Get a real trade
        url = "https://data-api.polymarket.com/trades?limit=1"
        async with session.get(url) as response:
            trades = await response.json()
            
            if trades:
                trade = trades[0]
                name = trade.get('name', '')
                wallet = trade.get('proxyWallet', '')
                
                print(f"Testing profile URLs for:")
                print(f"  Name: {name}")
                print(f"  Wallet: {wallet}")
                print()
                
                # Test different formats
                formats = [
                    f"https://polymarket.com/profile/{name}",
                    f"https://polymarket.com/profile/{wallet}",
                    f"https://polymarket.com/profile?address={wallet}",
                    f"https://polymarket.com/profile?user={name}",
                    f"https://polymarket.com/@{name}",
                    f"https://polymarket.com/u/{name}",
                ]
                
                for url_format in formats:
                    try:
                        async with session.get(url_format, allow_redirects=True) as resp:
                            status = resp.status
                            final_url = str(resp.url)
                            
                            if status == 200:
                                print(f"✅ {url_format}")
                                print(f"   Final URL: {final_url}")
                            else:
                                print(f"❌ {url_format} (Status: {status})")
                    except Exception as e:
                        print(f"❌ {url_format} (Error: {e})")

asyncio.run(test_profile_formats())

