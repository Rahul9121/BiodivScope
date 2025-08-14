#!/bin/bash

# BiodivProScope Deployment Script
# This script helps you deploy the BiodivProScope application quickly

echo "🌿 BiodivProScope Deployment Script"
echo "===================================="

# Function to display colored output
print_status() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Starting BiodivProScope deployment..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your specific configurations before proceeding!"
    read -p "Press enter to continue after editing .env file..."
fi

# Build and start services
print_status "Building Docker images..."
docker-compose build

print_status "Starting services..."
docker-compose up -d

# Wait for services to be healthy
print_status "Waiting for services to start..."
sleep 30

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_success "Services are running!"
else
    print_error "Some services failed to start. Check logs with: docker-compose logs"
    exit 1
fi

# Initialize database
print_status "Initializing database..."
docker-compose exec -T backend python database/user_table.py

# Setup ChromaDB
print_status "Setting up ChromaDB..."
docker-compose exec -T backend python "ML Strategy/chromaDB_ingest_invasive.py"

print_success "🎉 BiodivProScope deployed successfully!"
echo
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5001"
echo "   ChromaDB: http://localhost:8000"
echo
echo "🔧 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   View running services: docker-compose ps"
echo
print_warning "Remember to:"
echo "   1. Configure your environment variables in .env"
echo "   2. Set up your database with proper data"
echo "   3. Configure CORS settings for production"
echo "   4. Set up SSL certificates for HTTPS"
