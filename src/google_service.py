import httpx
import logging
from src.database import get_db
from src.config import settings

logger = logging.getLogger(__name__)


class GoogleSheetService:
    async def export_new_vacancies(self):
        db = get_db()
        collection = db["vacancies"]
        vacancies = await collection.find({"is_written_to_google": False}).to_list(length=100)

        async with httpx.AsyncClient(follow_redirects=True) as client:
            for vac in vacancies:
                data = {
                    "published_at": vac.get("published_at"),
                    "keyword": vac.get("keyword"),
                    "title": vac.get("title"),
                    "company": vac.get("company"),
                    "url": vac.get("url")
                }
                try:
                    res = await client.post(settings.GOOGLE_SHEET_URL, json=data)
                    if res.status_code == 200:
                        await collection.update_one({"_id": vac["_id"]}, {"$set": {"is_written_to_google": True}})
                        logger.info(f"Exported to Sheets: {vac.get('title')}")
                except Exception as e:
                    logger.error(f"Google Sheets Error: {e}")

google_service = GoogleSheetService()
