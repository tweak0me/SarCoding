import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI(title="SarCoding")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/contact")
async def contact(
    name: str = Form(...),
    contact: str = Form(...),
    message: str = Form(""),
):
    name = name.strip()
    contact = contact.strip()
    message = message.strip()

    if not name or not contact:
        return JSONResponse({"ok": False, "message": "Заполните имя и контакт."}, status_code=400)

    if len(name) > 100 or len(contact) > 200 or len(message) > 2000:
        return JSONResponse({"ok": False, "message": "Слишком длинные данные."}, status_code=400)

    if not BOT_TOKEN or not CHAT_ID:
        return JSONResponse({"ok": False, "message": "Telegram ещё не настроен."}, status_code=503)

    text = (
        "🚀 Новая заявка с sarcoding.uz\n\n"
        f"👤 Имя: {name}\n"
        f"📩 Контакт: {contact}\n"
        f"💬 Сообщение: {message or '—'}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                url,
                json={"chat_id": CHAT_ID, "text": text},
            )
            response.raise_for_status()
    except Exception:
        return JSONResponse(
            {"ok": False, "message": "Не удалось отправить заявку. Попробуйте ещё раз."},
            status_code=502,
        )

    return {"ok": True, "message": "Заявка отправлена. Мы свяжемся с вами."}
