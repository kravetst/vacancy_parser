# Job Parser (Robota.ua)

Asynchronous job parser from Robota.ua website by keywords.
The project implements data collection via GraphQL API (Dracula), storage in MongoDB, notifications in Telegram and export to Google spreadsheet.

## Main functionality
* **Parser:** Obtained via Robota.ua internal API, avoiding duplicates in the database using `upsert`.
* **Database:** Use MongoDB for reliable storage and tracking of sending statuses (Telegram/Google).
* **Notification:** Sending new jobs to Telegram group using HTML markup and protection from Flood Control.
* **Google Sheets:** Export data to spreadsheet via Google Apps Script (POST requests).

## Technology Stack
* **Python 3.12**
* **Motor** (asynchronous driver for MongoDB)
* **Pydantic v2** (data validation and configuration)
* **HTTPX** (asynchronous HTTP requests)
* **Docker & Docker Compose**

## Quick Start

### 1. Environment Setup
Create a `.env` file in the root of your project based on `.env.example`:
```env
MONGODB_URI=your_mongodb_uri
DB_NAME=candidate_13
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_SHEET_URL=your_apps_script_url
```
### 2. Running via Docker
```bash
docker-compose up --build
```
### 3. Local launch (without Docker)
```bash
python -m venv .venv
source .venv/bin/activate  # for macOS/Linux
source .venv/Scripts/actavate  # for Windows
pip install -r requirements.txt
python -m src.main
```
## 📂Project Architecture
The project is built on a service-oriented structure:

* src/parser.py — logic for interacting with the Robota.ua API.

* src/telegram_service.py — notification service.

* src/google_service.py — table export service.

* src/database.py — initialization and management of the connection to the database.

* src/models.py — Pydantic schemas for validating vacancies.

## 🛠 Implementation features
To ensure stable operation, the following solutions were implemented:

* 🔒 **Security:** `html.escape` is used to escape special characters, which prevents HTML markup rendering errors in Telegram.
* ⏳ **Stability:** `asyncio.sleep` is added between requests to the Telegram API to comply with limits (*Flood Control*).
* 🔄 **Data integrity:** `upsert` (update + insert) logic has been implemented at the database level. This ensures that there are no duplicate vacancies when the parser is run multiple times.
* 🐳 **Containerization:** The project is fully ready for deployment via Docker, which minimizes problems with the environment.