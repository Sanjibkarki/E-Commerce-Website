FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=recommendation.settings

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "recommendation.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
