# Use Python 3.12.2 as the base image
FROM python:3.12.2-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt into the container
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose port 8003 for FastAPI
EXPOSE 8003

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8003"]
