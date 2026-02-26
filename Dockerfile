# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Install system dependencies for media processing if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the asynchronous server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]