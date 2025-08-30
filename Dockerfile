# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create working directory
WORKDIR /code

# Install system dependencies (Postgres client for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl \
  && rm -rf /var/lib/apt/lists/*

# Install pipenv/poetry if you use them; here we use pip + requirements.txt
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Make entrypoint executable
COPY ./docker-entrypoint.sh /code/docker-entrypoint.sh
RUN chmod +x /code/docker-entrypoint.sh

# Expose port gunicorn will listen on
EXPOSE 8000

# Default entrypoint
ENTRYPOINT ["/code/docker-entrypoint.sh"]
