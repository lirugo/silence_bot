# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .
COPY bot .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "main.py"]