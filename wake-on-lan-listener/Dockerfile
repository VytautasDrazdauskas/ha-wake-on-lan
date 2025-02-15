FROM ghcr.io/hassio-addons/base-python:latest

# Set the working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .

# Install dependencies
RUN pip install -r requirements.txt

# Run the script
CMD ["python", "/app/main.py"]
