"""
Test database connectivity
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.services.database import Database


async def test_database():
    """Test database connection"""
    logger.info("Testing database connection...")
    
    db = Database()
    
    try:
        # Connect to database
        await db.connect()
        logger.info("✓ Database connected")
        
        # Test query
        async with db.pool.acquire() as conn:
            # Check tables
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            if tables:
                logger.info(f"✓ Found {len(tables)} tables:")
                for table in tables:
                    logger.info(f"  - {table['table_name']}")
            else:
                logger.warning("⚠ No tables found. Run 'python scripts/init_db.py' first")
        
        logger.info("\n✓ Database test complete!")
        
    except Exception as e:
        logger.error(f"✗ Database test failed: {e}")
        logger.error("\nMake sure you have:")
        logger.error("1. Created a .env file with DATABASE_URL")
        logger.error("2. Set up a Supabase database")
        logger.error("3. Run 'python scripts/init_db.py' to create tables")
        sys.exit(1)
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(test_database())

