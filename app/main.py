import os
import re
import html
import logging
from typing import Annotated

import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("sarcoding")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="SarCoding", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class ContactLead(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    contact: str = Field(min_length=3, max_length=160)
    message: str = Field(min_length=10, max_length=3000)

def clean(value: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", value).strip()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"telegram": os.getenv("PUBLIC_TELEGRAM", "https://t.me/")},
    )

@app.get("/studcrm", response_class=HTMLResponse)
async def studcrm_page(request: Request):
    return templates.TemplateResponse(request=request, name="studcrm.html", context={"telegram": os.getenv("PUBLIC_TELEGRAM", "https://t.me/")})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "sarcoding"}

@app.post("/contact")
async def contact(
    request: Request,
    name: Annotated[str, Form()],
    contact: Annotated[str, Form()],
    message: Annotated[str, Form()],
    website: Annotated[str, Form()] = "",  # honeypot: humans leave it empty
):
    # Basic bot trap. Return a neutral success to avoid teaching bots the field.
    if website.strip():
        return JSONResponse({"ok": True, "message": "Заявка отправлена."})

    try:
        lead = ContactLead(
            name=clean(name),
            contact=clean(contact),
            message=clean(message),
        )
    except ValidationError as exc:
        errors = "; ".join(
            f"{'.'.join(str(x) for x in e['loc'])}: {e['msg']}"
            for e in exc.errors()
        )
        return JSONResponse({"ok": False, "message": "Проверьте поля формы. " + errors}, status_code=422)

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        logger.error("Telegram contact form is not configured")
        return JSONResponse(
            {"ok": False, "message": "Форма временно недоступна. Напишите нам напрямую в Telegram."},
            status_code=503,
        )

    text = (
        "Новая заявка с сайта SarCoding\n\n"
        f"Имя: {lead.name}\n"
        f"Контакт: {lead.contact}\n"
        f"Задача: {lead.message}"
    )
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(url, json={"chat_id": chat_id, "text": text})
            response.raise_for_status()
            payload = response.json()
            if not payload.get("ok"):
                raise RuntimeError("Telegram API returned ok=false")
    except Exception:
        logger.exception("Unable to deliver contact lead to Telegram")
        return JSONResponse(
            {"ok": False, "message": "Не удалось отправить заявку. Попробуйте позже или напишите нам в Telegram."},
            status_code=502,
        )

    return JSONResponse({"ok": True, "message": "Спасибо! Заявка отправлена. Мы свяжемся с вами."})
