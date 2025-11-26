#!/bin/bash

# Start script for the Dockerized application

echo "Starting the application..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start all services
docker-compose up --build

echo "Application started successfully!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "Database: localhost:5432 (PostgreSQL)"