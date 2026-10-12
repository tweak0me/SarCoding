# SarCoding

Landing page for SarCoding with a Telegram contact form.

## Local run

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Telegram setup

Create a bot with @BotFather and obtain its token.

Set:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Do not commit the real `.env` or bot token to GitHub.

## Render

Create a Web Service from this repository.

Build:
`pip install -r requirements.txt`

Start:
`uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Important

The contact form sends data to the configured Telegram chat. It does not store submissions in a database.
