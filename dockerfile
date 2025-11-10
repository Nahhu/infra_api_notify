FROM python:3.12-slim

# Evita archivos pyc y salida bufferizada
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Ejecutar el servidor FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
