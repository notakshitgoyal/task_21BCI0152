FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for PyMuPDF
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Create start script properly
RUN echo "#!/bin/bash" > start.sh && \
    echo "gunicorn --worker-class eventlet -w 1 --bind \"0.0.0.0:\$PORT\" app:app" >> start.sh && \
    chmod +x start.sh

CMD ["./start.sh"]