"""
Initialize database with schema
"""
import asyncio
import asyncpg
from pathlib import Path
from loguru import logger
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings


async def init_database():
    """Initialize database with schema"""
    logger.info("Initializing database...")
    
    try:
        # Read schema file
        schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
        with open(schema_path, "r") as f:
            schema_sql = f.read()
        
        logger.info(f"Read schema from {schema_path}")
        
        # Connect to database
        conn = await asyncpg.connect(settings.DATABASE_URL)
        logger.info("Connected to database")
        
        # Execute schema
        await conn.execute(schema_sql)
        logger.info("✓ Schema executed successfully")
        
        # Verify tables
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        logger.info(f"✓ Created {len(tables)} tables:")
        for table in tables:
            logger.info(f"  - {table['table_name']}")
        
        await conn.close()
        logger.info("✓ Database initialization complete!")
        
    except FileNotFoundError:
        logger.error("✗ Schema file not found!")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init_database())

