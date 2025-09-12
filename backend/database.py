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
        # Rainbond 平台環境變數處理
        # 根據 Rainbond 文檔，依賴服務的環境變數會自動注入
        self.host = self._get_str_env('DB_HOST', 'localhost')
        self.port = self._get_int_env('DB_PORT', 3306)
        self.user = self._get_str_env('DB_USER', 'hellouser')
        self.password = self._get_str_env('DB_PASSWORD', 'hellopassword')
        # DB_DATABASE 是 Rainbond MySQL 服務常用的變數名稱
        self.db_name = (self._get_str_env('DB_DATABASE') or 
                       self._get_str_env('DB_NAME') or 
                       self._get_str_env('MYSQL_DATABASE', 'helloapp'))
        
        # 記錄連線配置（不包含敏感資訊）
        logger.info(f"Database configuration: host={self.host}, port={self.port}, user={self.user}, db={self.db_name}")
        
        # 輸出環境變數除錯資訊
        self._debug_env_vars()
        
        self.pool: Optional[aiomysql.Pool] = None

    def _get_str_env(self, key: str, default: str = '') -> str:
        """安全獲取字串類型環境變數"""
        value = os.getenv(key, default)
        # 處理可能的 ${} 語法殘留
        if value.startswith('${') and value.endswith('}'):
            logger.warning(f"環境變數 {key} 包含未解析的變數語法: {value}")
            return default
        return value

    def _get_int_env(self, key: str, default: int) -> int:
        """安全獲取整數類型環境變數"""
        value = os.getenv(key)
        if not value:
            return default
        
        # 處理可能的 ${} 語法
        if value.startswith('${') and value.endswith('}'):
            logger.warning(f"環境變數 {key} 包含未解析的變數語法: {value}，使用預設值 {default}")
            return default
        
        try:
            return int(value)
        except ValueError:
            logger.warning(f"無法將環境變數 {key} 的值 '{value}' 轉換為整數，使用預設值 {default}")
            return default

    def _debug_env_vars(self):
        """輸出環境變數除錯資訊"""
        logger.info("=== Rainbond 環境變數除錯 ===")
        env_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_DATABASE', 'DB_NAME', 'MYSQL_DATABASE']
        for var in env_vars:
            value = os.getenv(var)
            if var == 'DB_PASSWORD':
                logger.info(f"{var}: {'***設定***' if value else '未設定'}")
            else:
                logger.info(f"{var}: {repr(value)}")
        logger.info("============================")

    async def wait_for_database(self, max_wait_time=60):
        """等待資料庫服務就緒（適合 Rainbond 容器啟動順序）"""
        logger.info(f"等待資料庫服務就緒，最多等待 {max_wait_time} 秒")
        start_time = asyncio.get_event_loop().time()
        
        while True:
            try:
                # 嘗試建立簡單連線測試
                conn = await aiomysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    connect_timeout=5
                )
                await conn.ensure_closed()
                logger.info("資料庫服務已就緒")
                return True
            except Exception as e:
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed >= max_wait_time:
                    logger.error(f"等待資料庫服務超時：{e}")
                    return False
                
                logger.info(f"資料庫尚未就緒，{int(max_wait_time - elapsed)} 秒後重試...")
                await asyncio.sleep(5)

    async def init_pool(self, max_retries=5, retry_delay=5):
        """初始化連線池，包含重試機制"""
        # 首先等待資料庫服務就緒
        if not await self.wait_for_database():
            raise Exception("資料庫服務未在預期時間內就緒")
        
        for attempt in range(max_retries):
            try:
                logger.info(f"嘗試建立資料庫連線池 {self.host}:{self.port} (嘗試 {attempt + 1}/{max_retries})")
                self.pool = await aiomysql.create_pool(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db_name,
                    minsize=1,
                    maxsize=10,
                    autocommit=True,
                    charset='utf8mb4',  # 支援完整的 UTF-8
                    connect_timeout=10,
                    pool_recycle=3600,  # 1小時回收連線
                )
                logger.info("成功建立 MySQL 資料庫連線池")
                
                # 測試連線池
                await self._test_connection()
                return
                
            except Exception as e:
                logger.error(f"建立資料庫連線池失敗 (嘗試 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"{retry_delay} 秒後重試...")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error("達到最大重試次數，無法連接到資料庫")
                    raise

    async def _test_connection(self):
        """測試資料庫連線"""
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT 1")
                    result = await cursor.fetchone()
                    if result[0] == 1:
                        logger.info("資料庫連線測試成功")
        except Exception as e:
            logger.error(f"資料庫連線測試失敗: {e}")
            raise

    async def close_pool(self):
        """關閉連線池"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("資料庫連線池已關閉")

    async def get_connection(self):
        """從連線池獲取資料庫連線"""
        if not self.pool:
            await self.init_pool()
        return await self.pool.acquire()

    async def execute_schema_init(self):
        """初始化資料庫結構（適合 Rainbond 部署時使用）"""
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    # 創建 messages 表（如果不存在）
                    create_table_sql = """
                    CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        message TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                    """
                    await cursor.execute(create_table_sql)
                    logger.info("資料庫結構初始化完成")
        except Exception as e:
            logger.error(f"資料庫結構初始化失敗: {e}")
            raise

    async def insert_message(self, name: str, message: str) -> int:
        """插入新訊息到資料庫"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = "INSERT INTO messages (name, message) VALUES (%s, %s)"
                await cursor.execute(sql, (name, message))
                return cursor.lastrowid

    async def get_messages(self, limit: int = 100) -> list:
        """從資料庫獲取訊息"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                sql = "SELECT * FROM messages ORDER BY created_at DESC LIMIT %s"
                await cursor.execute(sql, (limit,))
                return await cursor.fetchall()

    async def get_message_by_id(self, message_id: int) -> Optional[dict]:
        """根據 ID 獲取特定訊息"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                sql = "SELECT * FROM messages WHERE id = %s"
                await cursor.execute(sql, (message_id,))
                return await cursor.fetchone()

    async def health_check(self) -> dict:
        """資料庫健康檢查（適合 Rainbond 健康檢查）"""
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT 1")
                    await cursor.execute("SELECT COUNT(*) FROM messages")
                    count = await cursor.fetchone()
                    
            return {
                "status": "healthy",
                "connection": "ok",
                "message_count": count[0] if count else 0,
                "pool_size": self.pool.size if self.pool else 0,
                "pool_free": self.pool.freesize if self.pool else 0
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

# 全域資料庫實例
db = Database()