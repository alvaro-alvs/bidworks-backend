FROM python:3.11-slim-bookworm


WORKDIR /app

COPY requirements.txt requirements.txt

# COPY requirements.txt requirements.txtRUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bidworks_backend.wsgi:application"]
