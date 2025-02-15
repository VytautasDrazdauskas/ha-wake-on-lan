FROM python:3.10-slim

# Set shell and working directory
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /app

# Install dependencies
RUN apt update && apt install -y \
    bash \
    libpcap-dev \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir wakeonlan scapy psutil

# Copy add-on files
COPY run.sh /run.sh
COPY main.py /app/main.py

# Set permissions
RUN chmod +x /run.sh

# Start the service directly
CMD ["/run.sh"]
