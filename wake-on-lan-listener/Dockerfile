ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:3.10
FROM $BUILD_FROM

# Set shell and working directory
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache bash python3 py3-pip

# Copy add-on files
COPY run.sh /
COPY requirements.txt /app/
COPY main.py /app/

# Set permissions
RUN chmod +x /run.sh

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Start the service
CMD [ "/run.sh" ]
