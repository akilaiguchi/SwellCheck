# 1. Install lightweight python image
FROM python:3.11-slim

# 2. Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent straight to the terminal (useful for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory inside the container
WORKDIR /app

# 4. Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy rest of bot code
COPY . .

# 7. Run the bot application
# Note: Update this CMD based on your bot's entry point file
CMD ["python", "main.py"]
