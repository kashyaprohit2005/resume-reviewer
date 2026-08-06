# Use official Python lightweight image
FROM python:3.10-slim

# Prevent writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port (Render automatically sets $PORT)
EXPOSE 8000

# Start production server
CMD exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} app.main:app
