# Use Python 3.12.2 as base image
FROM python:3.12.2-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY . /app

# Expose port 8003
EXPOSE 8003

# Run FastAPI app with uvicorn
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8003"]
