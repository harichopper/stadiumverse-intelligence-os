#!/bin/bash
# StadiumVerse AI - Development Setup Script
# FIFA World Cup 2026 Stadium Digital Twin System

set -e

echo "🏟️  Setting up StadiumVerse AI Development Environment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if required tools are installed
check_requirements() {
    echo -e "${BLUE}📋 Checking requirements...${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is required but not installed${NC}"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose is required but not installed${NC}"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}⚠️  Node.js not found. Using Docker for frontend.${NC}"
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}⚠️  Python3 not found. Using Docker for backend.${NC}"
    fi
    
    echo -e "${GREEN}✅ Requirements check completed${NC}"
}

# Setup environment variables
setup_env() {
    echo -e "${BLUE}🔧 Setting up environment variables...${NC}"
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env file from template${NC}"
        echo -e "${YELLOW}⚠️  Please update .env with your actual API keys${NC}"
    else
        echo -e "${YELLOW}⚠️  .env file already exists${NC}"
    fi
}

# Create required directories
setup_directories() {
    echo -e "${BLUE}📁 Creating required directories...${NC}"
    
    directories=(
        "data/uploads"
        "logs"
        "infrastructure/docker/ssl"
        "infrastructure/monitoring"
        "tests/reports"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        echo "Created directory: $dir"
    done
    
    echo -e "${GREEN}✅ Directories created${NC}"
}

# Setup database
setup_database() {
    echo -e "${BLUE}🗄️  Setting up database...${NC}"
    
    # Start PostgreSQL container
    docker-compose up -d postgres redis
    
    # Wait for database to be ready
    echo "Waiting for database to be ready..."
    sleep 10
    
    # Run database migrations
    if [ -f "backend/requirements.txt" ]; then
        echo "Installing Python dependencies and running migrations..."
        cd backend
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        
        source venv/bin/activate
        pip install -r requirements.txt
        
        # Run Alembic migrations
        if [ -d "alembic" ]; then
            alembic upgrade head
        fi
        
        cd ..
    else
        echo "Using Docker for database setup..."
        docker-compose exec backend alembic upgrade head
    fi
    
    echo -e "${GREEN}✅ Database setup completed${NC}"
}

# Generate mock data
generate_mock_data() {
    echo -e "${BLUE}🎭 Generating mock data...${NC}"
    
    # Run the mock data generation script
    if [ -f "scripts/generate_demo_data.py" ]; then
        cd backend
        source venv/bin/activate 2>/dev/null || true
        python ../scripts/generate_demo_data.py
        cd ..
    else
        docker-compose exec backend python scripts/generate_demo_data.py
    fi
    
    echo -e "${GREEN}✅ Mock data generated${NC}"
}

# Setup frontend
setup_frontend() {
    echo -e "${BLUE}⚛️  Setting up frontend...${NC}"
    
    if command -v node &> /dev/null; then
        cd frontend
        
        # Install dependencies
        if [ -f "package.json" ]; then
            echo "Installing Node.js dependencies..."
            npm install
        fi
        
        cd ..
    else
        echo "Using Docker for frontend setup..."
    fi
    
    echo -e "${GREEN}✅ Frontend setup completed${NC}"
}

# Build and start services
start_services() {
    echo -e "${BLUE}🚀 Building and starting services...${NC}"
    
    # Build all services
    docker-compose build
    
    # Start all services
    docker-compose up -d
    
    # Wait for services to be ready
    echo "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    echo -e "${BLUE}🏥 Checking service health...${NC}"
    
    services=("backend" "frontend" "postgres" "redis")
    for service in "${services[@]}"; do
        if docker-compose ps $service | grep -q "Up"; then
            echo -e "${GREEN}✅ $service is running${NC}"
        else
            echo -e "${RED}❌ $service is not running${NC}"
        fi
    done
}

# Display access information
show_access_info() {
    echo -e "${GREEN}🎉 StadiumVerse AI setup completed!${NC}"
    echo "=================================================="
    echo ""
    echo -e "${BLUE}🌐 Access Points:${NC}"
    echo "Frontend Dashboard: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "API Documentation: http://localhost:8000/docs"
    echo "Database Admin: http://localhost:8080 (adminer)"
    echo "Monitoring: http://localhost:3001 (grafana)"
    echo ""
    echo -e "${BLUE}📊 Default Credentials:${NC}"
    echo "Database: postgres/password"
    echo "Grafana: admin/admin"
    echo ""
    echo -e "${BLUE}🔧 Management Commands:${NC}"
    echo "Start services: docker-compose up -d"
    echo "Stop services: docker-compose down"
    echo "View logs: docker-compose logs -f [service]"
    echo "Restart service: docker-compose restart [service]"
    echo ""
    echo -e "${YELLOW}⚠️  Remember to:${NC}"
    echo "1. Update .env with your actual API keys"
    echo "2. Configure OpenAI API key for AI features"
    echo "3. Set up SSL certificates for production"
    echo ""
    echo -e "${GREEN}🏟️  Welcome to StadiumVerse AI - FIFA World Cup 2026!${NC}"
}

# Main execution
main() {
    echo -e "${GREEN}Starting StadiumVerse AI setup...${NC}"
    echo ""
    
    check_requirements
    setup_env
    setup_directories
    setup_database
    generate_mock_data
    setup_frontend
    start_services
    show_access_info
}

# Run main function
main "$@"