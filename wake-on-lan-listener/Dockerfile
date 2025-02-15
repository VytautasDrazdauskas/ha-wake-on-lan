ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:3.10
FROM $BUILD_FROM

# Set shell and working directory
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /app

# Ensure system dependencies are installed
RUN apk add --no-cache \
    bash \
    python3 \
    py3-pip \
    py3-setuptools \
    py3-wheel \
    gcc \
    musl-dev \
    python3-dev

# Print Python and pip versions for debugging
RUN python3 --version && pip3 --version

# Copy add-on files
COPY run.sh /
COPY requirements.txt /app/
COPY main.py /app/

# Set permissions
RUN chmod +x /run.sh

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt || exit 0

# Start the service
CMD [ "/run.sh" ]
