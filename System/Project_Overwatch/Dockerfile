# Base Image: Lightweight Python
FROM python:3.12-slim

# Set Working Directory
WORKDIR /app

# Install System Dependencies (for Chrome/Selenium if needed later, and build tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Requirements
COPY requirements.txt .

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy The Everything (Source Code)
COPY . .

# Expose Streamlit Port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Entrypoint: Launch the Cockpit
CMD ["streamlit", "run", "monolith_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
