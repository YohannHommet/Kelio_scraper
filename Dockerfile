FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 --retries=3 -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Copy project files
COPY . .

# Expose port for Flask app
EXPOSE 5000

# Set Python path
ENV PYTHONPATH=/app

# Command to run Flask app
CMD ["python", "src/app.py"]
