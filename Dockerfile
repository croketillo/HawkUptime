
# Use official Python image
FROM python:3.12-slim

# Metadata for documentation and registry visibility
LABEL maintainer="your_email@example.com"
LABEL version="0.1.2"
LABEL description="Uptime Monitor - Periodic uptime and latency monitoring with real-time web dashboard"


# Environment variables for better runtime behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install Python dependencies and your package in editable mode
RUN pip install --upgrade pip && pip install .

# Default command when container starts
CMD ["uptime-monitor", "start"]
