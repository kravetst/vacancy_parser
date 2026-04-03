import httpx
import logging
from src.database import get_db
from src.models import Vacancy

logger = logging.getLogger(__name__)


class RobotaParser:
    API_URL = "https://dracula.robota.ua/?q=getPublishedVacanciesList"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Origin": "https://robota.ua",
            "Referer": "https://robota.ua/"
        }

    async def parse_by_keyword(self, keyword: str):
        db = get_db()
        collection = db["vacancies"]

        payload = {
            "operationName": "getPublishedVacanciesList",
            "variables": {
                "pagination": {"count": 20, "page": 0},
                "filter": {"keywords": keyword},
                "sort": "BY_DATE"
            },
            "query": """
                query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!, $pagination: PublishedVacanciesPaginationInput!, $sort: PublishedVacanciesSortType!) {
                  publishedVacancies(filter: $filter, pagination: $pagination, sort: $sort) {
                    items {
                      id
                      title
                      company { id name }
                      sortDateText
                    }
                  }
                }
            """
        }

        async with httpx.AsyncClient(headers=self.headers, timeout=15.0) as client:
            try:
                response = await client.post(self.API_URL, json=payload)
                data = response.json()

                if "errors" in data:
                    logger.error(f"GraphQL Errors: {data['errors']}")
                    return

                items = data.get("data", {}).get("publishedVacancies", {}).get("items", [])
                if not items:
                    logger.info(f"No vacancies found for: {keyword}")
                    return

                new_count = 0
                for item in items:
                    v_id = item.get("id")
                    company = item.get("company") or {}
                    if not v_id: continue

                    v_url = f"https://robota.ua/ua/company{company.get('id', 0)}/vacancy{v_id}"

                    vacancy = Vacancy(
                        title=item.get("title"),
                        company=company.get("name"),
                        url=v_url,
                        published_at=item.get("sortDateText", "щойно"),
                        keyword=keyword
                    )

                    result = await collection.update_one(
                        {"url": v_url},
                        {"$setOnInsert": vacancy.model_dump()},
                        upsert=True
                    )
                    if result.upserted_id:
                        new_count += 1

                logger.info(f"Parsed {len(items)} items. New: {new_count}")
            except Exception as e:
                logger.error(f"Parser error: {e}")

parser = RobotaParser()
