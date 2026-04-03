import asyncio
import httpx
import logging
from html import escape
from src.database import get_db
from src.config import settings

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    async def send_new_vacancies(self):
        db = get_db()
        collection = db["vacancies"]

        vacancies = await collection.find({"is_sent_to_telegram": False}).to_list(length=20)

        if not vacancies:
            return

        async with httpx.AsyncClient() as client:
            for vac in vacancies:
                title = escape(vac.get('title', 'N/A'))
                company = escape(vac.get('company', 'N/A'))
                keyword = escape(vac.get('keyword', 'python'))
                url = vac.get('url', '#')

                message = (
                    f"<b>NEW VACANCY</b>\n\n"
                    f"Keyword: #{keyword}\n"
                    f"Title: {title}\n"
                    f"Company: {company}\n"
                    f"Date: {vac.get('published_at', '-')}\n\n"
                    f"<a href='{url}'>Open Link</a>"
                )

                payload = {
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                }

                try:
                    res = await client.post(self.api_url, json=payload)
                    if res.status_code == 200:
                        await collection.update_one(
                            {"_id": vac["_id"]},
                            {"$set": {"is_sent_to_telegram": True}}
                        )
                        logger.info(f"Notification sent: {title}")

                    await asyncio.sleep(1.5)
                except Exception as e:
                    logger.error(f"Telegram notification error: {e}")


telegram_service = TelegramService()
