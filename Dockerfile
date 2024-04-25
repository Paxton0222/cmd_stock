# Use the official Alpine Linux image
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

RUN apk update && apk add git

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN twstock -U
RUN apk --purge del apk-tools

# Copy project files into the working directory
COPY . /app/
