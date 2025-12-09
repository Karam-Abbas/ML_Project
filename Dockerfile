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
COPY wsgi.py .
COPY .dvc ./.dvc
COPY .git ./.git
COPY models.dvc ./

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

RUN dvc pull models.dvc

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