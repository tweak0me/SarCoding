# SarCoding — website

Responsive landing page for SarCoding, built with FastAPI, Jinja2, CSS and vanilla JavaScript. Contact form sends leads to a configured Telegram chat and does not store them in a database.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000.

Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in your environment or local `.env` (never commit real secrets). `PUBLIC_TELEGRAM` is the public contact link shown/used in configuration.

## Render

Connect this repository to Render and use the included `render.yaml`, or create a Docker Web Service. Configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as secret environment variables in the Render dashboard.

## Notes

- `/health` provides a simple health check.
- Contact submissions are delivered to Telegram; no database is used.
- The product card describes StudCRM at a high level and avoids claiming every planned feature is production-ready.
- Before production, configure rate limiting at the edge (or add application-level rate limiting), privacy/legal text suitable for your jurisdiction, and test Telegram delivery.
