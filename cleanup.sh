#!/bin/bash

# Cleanup script for the Dockerized application

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running."
    exit 1
fi

# Parse command line arguments
if [ "$1" == "--all" ]; then
    echo "Cleaning up ALL Docker resources (WARNING: This affects all Docker projects!)"
    echo "Are you sure you want to continue? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Cleanup cancelled."
        exit 0
    fi
    
    # Stop all running containers
    echo "Stopping all containers..."
    docker stop $(docker ps -aq) 2>/dev/null
    
    # Remove all containers
    echo "Removing all containers..."
    docker rm $(docker ps -aq) 2>/dev/null
    
    # Remove all images
    echo "Removing all images..."
    docker rmi $(docker images -q) 2>/dev/null
    
    # Remove all volumes
    echo "Removing all volumes..."
    docker volume rm $(docker volume ls -q) 2>/dev/null
    
    # Remove all networks
    echo "Removing all networks..."
    docker network prune -f
    
    # Remove build cache
    echo "Removing build cache..."
    docker builder prune -a -f
    
    echo "Complete cleanup completed!"
else
    echo "Cleaning up project Docker resources..."
    
    # Stop all running containers
    echo "Stopping all containers..."
    docker stop $(docker ps -aq) 2>/dev/null
    
    # Remove all containers
    echo "Removing all containers..."
    docker rm $(docker ps -aq) 2>/dev/null
    
    # Remove all images related to this project
    echo "Removing project images..."
    docker rmi $(docker images | grep "practice" | awk '{print $3}') 2>/dev/null
    
    # Remove volumes
    echo "Removing volumes..."
    docker volume rm $(docker volume ls -q) 2>/dev/null
    
    # Prune unused networks
    echo "Pruning unused networks..."
    docker network prune -f
    
    echo "Project cleanup completed!"
fi