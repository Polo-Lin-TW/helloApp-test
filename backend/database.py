import aiomysql
import os
import asyncio
import logging
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        # Rainbond-style environment variables with fallbacks
        # Rainbond will inject these through dependency relationships
        self.host = os.getenv('DB_HOST') or os.getenv('MYSQL_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT') or os.getenv('MYSQL_PORT', 3306))
        self.user = os.getenv('DB_USER') or os.getenv('MYSQL_USER', 'hellouser')
        self.password = os.getenv('DB_PASSWORD') or os.getenv('MYSQL_PASSWORD', 'hellopassword')
        self.db_name = os.getenv('DB_NAME') or os.getenv('MYSQL_DATABASE', 'helloapp')
        self.pool: Optional[aiomysql.Pool] = None

    async def init_pool(self, max_retries=5, retry_delay=5):
        """Initialize connection pool with retry mechanism"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to connect to MySQL at {self.host}:{self.port} (attempt {attempt + 1}/{max_retries})")
                self.pool = await aiomysql.create_pool(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db_name,
                    minsize=1,
                    maxsize=10,
                    autocommit=True
                )
                logger.info("Successfully connected to MySQL database")
                return
            except Exception as e:
                logger.error(f"Failed to connect to database (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error("Max retries reached. Unable to connect to database.")
                    raise

    async def close_pool(self):
        """Close connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            await self.init_pool()
        return await self.pool.acquire()

    async def insert_message(self, name: str, message: str) -> int:
        """Insert a new message into the database"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = "INSERT INTO messages (name, message) VALUES (%s, %s)"
                await cursor.execute(sql, (name, message))
                return cursor.lastrowid

    async def get_messages(self, limit: int = 100) -> list:
        """Get messages from the database"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                sql = "SELECT * FROM messages ORDER BY created_at DESC LIMIT %s"
                await cursor.execute(sql, (limit,))
                return await cursor.fetchall()

    async def get_message_by_id(self, message_id: int) -> Optional[dict]:
        """Get a specific message by ID"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                sql = "SELECT * FROM messages WHERE id = %s"
                await cursor.execute(sql, (message_id,))
                return await cursor.fetchone()

# Global database instance
db = Database()