#!/bin/bash
# Optimized Deployment script for Scrap Kelio

set -e # Exit immediately if a command exits with a non-zero status.

APP_NAME="kelio-scraper"
IMAGE_NAME="scrap-kelio"
TAG="latest" # You can use commit hash or version number for tagging
COMPOSE_FILE="docker-compose.yml"

echo "Deploying $APP_NAME..."

# 1. Pull latest code from Git (optional, if your deployment process requires it)
echo "Pulling latest code from Git..."
git pull origin main || true # Use || true to prevent script from failing if already up-to-date

# 2. Build Docker image with tag
echo "Building Docker image: $IMAGE_NAME:$TAG"
docker build -t $IMAGE_NAME:$TAG .

# 3. Stop and remove the old container (if running)
echo "Stopping and removing old container..."
docker stop $APP_NAME || true # Use || true to prevent script from failing if container doesn't exist
docker rm $APP_NAME || true   # Use || true to prevent script from failing if container doesn't exist

# 4. Run the Docker container using docker-compose
echo "Starting Docker container using docker-compose..."
docker-compose -f $COMPOSE_FILE up -d --remove-orphans

# 5. Verify deployment (optional)
echo "Verifying deployment..."
docker ps --filter "name=$APP_NAME" --format "table {{.Names}}\t{{.Status}}"

echo "$APP_NAME deployment completed successfully."
