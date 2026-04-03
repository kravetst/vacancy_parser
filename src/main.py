import asyncio
import logging
import sys
from src.database import init_db
from src.parser import parser
from src.telegram_service import telegram_service
from src.google_service import google_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def run_pipeline(keyword: str):
    logger.info(f"--- Starting pipeline for: {keyword} ---")

    await init_db()
    await parser.parse_by_keyword(keyword)

    logger.info("Checking Telegram queue...")
    await telegram_service.send_new_vacancies()

    logger.info("Checking Google Sheets queue...")
    await google_service.export_new_vacancies()

    logger.info("Pipeline finished.")


if __name__ == "__main__":
    try:
        asyncio.run(run_pipeline("Python developer"))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Critical error: {e}")
