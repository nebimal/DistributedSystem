#!/bin/bash

# Build all services
echo "Building all services..."
docker-compose build

# Start the system
echo "Starting the distributed e-commerce system..."
docker-compose up -d

echo "System is starting up... Check logs with: docker-compose logs -f"
