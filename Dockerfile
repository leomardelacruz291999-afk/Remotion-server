# Use lightweight Python base
FROM python:3.10-slim

# Install system dependencies (ffmpeg required for moviepy)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy app file
COPY render.py .

# Expose port
EXPOSE 8080

# Run Flask app
CMD ["python", "render.py"]
