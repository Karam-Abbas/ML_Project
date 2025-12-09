FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY models/ ./models/
COPY wsgi.py .

# Create upload directory
RUN mkdir -p /tmp/uploads

# Set environment variables
ENV FLASK_ENV=production
ENV MODEL_PATH=/app/models/best_vit_brain_tumor.pth
ENV UPLOAD_FOLDER=/tmp/uploads
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "120", "wsgi:app"]