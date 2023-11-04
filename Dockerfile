# Use an official Python runtime as a parent image
FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    openssl \
    python3-venv \
    supervisor

RUN mkdir -p /var/log/supervisor
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Create virtual enviroment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin"
# Install any needed packages
RUN python setup.py develop

# Make port available to the world outside this container
EXPOSE 1337
CMD ["/usr/bin/supervisord"]