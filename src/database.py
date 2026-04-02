import logging
from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings

logger = logging.getLogger(__name__)

class Database:
    _client: AsyncIOMotorClient = None
    _db = None

    @classmethod
    async def init_db(cls):
        try:
            cls._client = AsyncIOMotorClient(settings.MONGODB_URI)
            cls._db = cls._client[settings.DB_NAME]
            await cls._client.admin.command("ping")
            logger.info(f"Connected to MongoDB: {settings.DB_NAME}")
            return cls._db
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
            raise e

    @classmethod
    def get_db(cls):
        if cls._db is None:
            raise RuntimeError("Database not initialized. Call init_db() first.")
        return cls._db

init_db = Database.init_db
get_db = Database.get_db
