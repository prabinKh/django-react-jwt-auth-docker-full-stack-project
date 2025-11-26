#!/bin/bash

# Stop script for the Dockerized application

echo "Stopping the application..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running."
    exit 1
fi

# Stop all services
docker-compose down

echo "Application stopped successfully!"