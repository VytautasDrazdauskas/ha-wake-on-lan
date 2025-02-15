ARG BUILD_FROM=ghcr.io/hassio-addons/base:latest
FROM $BUILD_FROM

# Set shell and working directory
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /app

# Ensure necessary system dependencies are installed
RUN apk add --no-cache \
    bash \
    python3 \
    py3-pip \
    py3-setuptools \
    py3-wheel

# Print Python and pip versions for debugging
RUN python3 --version && pip3 --version

# Copy add-on files
COPY run.sh /
COPY requirements.txt /app/
COPY main.py /app/

# Set permissions
RUN chmod +x /run.sh

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Start the service
CMD [ "/run.sh" ]
