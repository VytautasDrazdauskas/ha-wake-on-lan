ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell and working directory
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /app

# Copy add-on files
COPY run.sh /
COPY requirements.txt /app/
COPY main.py /app/

# Set permissions
RUN chmod +x /run.sh

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Start the service
CMD [ "/run.sh" ]
