# app/main.py
from fastapi import FastAPI, BackgroundTasks, Header, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .config import API_KEY
from .mailer import send_mail

class NotifyEvent(BaseModel):
    event: str
    to: List[EmailStr]
    subject: str
    html: Optional[str] = ""
    text: Optional[str] = ""

app = FastAPI(title="notification-service", version="1.0")

@app.get("/healthz")
def healthz():
    return {"ok": True}

def check_key(x_api_key: Optional[str]):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.post("/notify")
def notify(evt: NotifyEvent,
          bg: BackgroundTasks,
          x_api_key: Optional[str] = Header(None)): 
    check_key(x_api_key)
    bg.add_task(send_mail, evt.to, evt.subject, evt.text or "", evt.html or "")
    return {"status": "queued", "to": evt.to, "subject": evt.subject}