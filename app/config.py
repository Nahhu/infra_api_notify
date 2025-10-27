# app/config.py
API_KEY = "super-secreta"

# el remitente DEBE ser el mismo que verificaste en SendGrid (Single Sender)
DEFAULT_FROM = "nahuelmartinez0077@gmail.com"

# --- SMTP (SendGrid) ---
SMTP_HOST = "smtp.sendgrid.net"
SMTP_PORT = 587
SMTP_USER = "apikey"  # literal
SMTP_PASS = "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"
SMTP_TLS  = True

# --- SES por API (no lo usás ahora) ---
USE_SES_API = False
AWS_REGION = "us-east-1"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
