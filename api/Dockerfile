# 1. Install lightweight python image
FROM python:3.11-slim

# 2. Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent straight to the terminal (useful for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory inside the container
WORKDIR /app

# 4. Install system dependencies required for MySql drivers
# 'default-libmysqlcliend-dev' andn 'gcc' are necessary for mysql-connector/SQLAlchemy
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# 6. Intall Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy rest of API code
COPY . .

# 8. Expose the port FastAPI will run on
EXPOSE 8000

# 9. Run application using Unicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]