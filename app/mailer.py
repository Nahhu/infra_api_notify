# app/mailer.py
import base64, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from . import config as cfg

DEFAULT_FROM = cfg.DEFAULT_FROM

# SMTP (SendGrid)
SMTP_HOST = cfg.SMTP_HOST
SMTP_PORT = int(cfg.SMTP_PORT)
SMTP_USER = cfg.SMTP_USER
SMTP_PASS = cfg.SMTP_PASS
SMTP_TLS  = bool(cfg.SMTP_TLS)

# SES (no usado ahora, pero dejamos los campos)
USE_SES_API = bool(cfg.USE_SES_API)
AWS_REGION = cfg.AWS_REGION
AWS_ACCESS_KEY_ID = cfg.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = cfg.AWS_SECRET_ACCESS_KEY

def _build_message(to: list[str], subject: str, text: str = "", html: str = "", attachments=None):
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = DEFAULT_FROM
    msg["To"] = ", ".join(to)

    alt = MIMEMultipart("alternative")
    if text:
        alt.attach(MIMEText(text, "plain", "utf-8"))
    if html:
        alt.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(alt)

    for att in (attachments or []):
        part = MIMEApplication(base64.b64decode(att["content"]))
        part.add_header("Content-Disposition", "attachment", filename=att["filename"])
        msg.attach(part)
    return msg

def _send_smtp(msg, to: list[str]):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
        # s.set_debuglevel(1)  # descomentalo si querés ver el diálogo SMTP
        if SMTP_TLS:
            s.starttls()
        if SMTP_USER:
            s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(DEFAULT_FROM, to, msg.as_string())

def send_mail(to: list[str], subject: str, text: str = "", html: str = "", attachments=None):
    msg = _build_message(to, subject, text, html, attachments)
    return _send_smtp(msg, to)
