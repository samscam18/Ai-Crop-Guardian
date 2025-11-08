dockerfile = '''FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads models/saved_models data/datasets

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=backend/app.py
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

