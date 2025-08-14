# BiodivProScope Deployment Setup Guide

## 🔧 Pre-Deployment Tasks

### 1. Environment Configuration
Create `.env` files for different environments:

#### Backend `.env`:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/biodivproscope
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=biodivproscope

# API Configuration
FLASK_ENV=production
SECRET_KEY=your_super_secure_secret_key_here
CORS_ORIGINS=https://your-frontend-domain.com

# External APIs
NOMINATIM_API_URL=https://nominatim.openstreetmap.org/search
NOMINATIM_USER_AGENT=BiodivProScopeApp/1.0

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# File Storage (if using cloud storage)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=biodivproscope-reports
```

#### Frontend `.env`:
```env
REACT_APP_API_BASE_URL=https://your-backend-api.com
REACT_APP_ENVIRONMENT=production
```

### 2. Database Migration Scripts
Create proper database initialization:

#### `database_setup.sql`:
```sql
-- Create main database
CREATE DATABASE biodivproscope;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    hotel_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_invasive_species_coords ON invasive_species(latitude, longitude);
CREATE INDEX idx_iucn_data_coords ON iucn_data(latitude, longitude);
CREATE INDEX idx_freshwater_risk_coords ON freshwater_risk(x, y);
CREATE INDEX idx_marine_hci_coords ON marine_hci(x, y);
CREATE INDEX idx_terrestrial_risk_coords ON terrestrial_risk(x, y);
```

### 3. Security Updates

#### Remove hardcoded credentials:
- Replace database passwords in all files
- Use environment variables for all sensitive data
- Update Flask secret keys
- Remove debug mode in production

#### Files to update:
- `backend/app.py` - Remove hardcoded DB credentials
- `backend/services/db.py` - Use environment variables
- `backend/database/*.py` - Update all database connection strings

### 4. Performance Optimizations

#### Backend optimizations:
- Implement database connection pooling
- Add Redis for caching
- Optimize SQL queries with proper indexing
- Add request rate limiting

#### Frontend optimizations:
- Implement code splitting
- Add service worker for caching
- Optimize images and assets
- Use React.lazy for component loading

### 5. Production Requirements

#### Additional packages needed:
```txt
# Add to requirements.txt
gunicorn==21.2.0
redis==4.5.4
python-dotenv==1.0.0
psycopg2-binary==2.9.6
sqlalchemy-pool==1.0.1
```

#### Frontend build optimization:
```json
// Add to package.json
{
  "scripts": {
    "build": "react-app-rewired build",
    "build:analyze": "npm run build && npx webpack-bundle-analyzer build/static/js/*.js"
  }
}
```

## 🚀 Deployment Options

### Option 1: Vercel + Railway (Recommended)

#### Frontend (Vercel):
1. Push code to GitHub
2. Connect Vercel to repository
3. Set environment variables in Vercel dashboard
4. Deploy automatically on git push

#### Backend (Railway):
1. Connect Railway to GitHub repository
2. Create PostgreSQL database in Railway
3. Set environment variables
4. Deploy with automatic builds

### Option 2: AWS Deployment

#### Using AWS Services:
- **EC2**: For backend API hosting
- **RDS**: For PostgreSQL database
- **S3**: For static file storage
- **CloudFront**: For CDN
- **Route 53**: For domain management

### Option 3: Docker Deployment

#### Create production Dockerfile:
```dockerfile
# Production backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5001

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "app:app"]
```

## 🔒 Security Checklist

- [ ] Remove all hardcoded passwords
- [ ] Implement proper CORS configuration
- [ ] Add HTTPS/SSL certificates
- [ ] Set up proper authentication middleware
- [ ] Implement rate limiting
- [ ] Add input validation and sanitization
- [ ] Set secure cookie configurations
- [ ] Add security headers (CSRF, XSS protection)
- [ ] Implement proper error handling (don't expose stack traces)
- [ ] Add logging and monitoring

## 📊 Monitoring & Maintenance

### Add monitoring tools:
- **Sentry** for error tracking
- **DataDog** or **New Relic** for performance monitoring
- **Uptime Robot** for availability monitoring
- **PostgreSQL** query performance monitoring

### Backup strategy:
- Daily database backups
- Version control for all configuration
- Regular security updates
- Performance testing and optimization

## 🧪 Testing Before Deployment

### Create test scripts:
1. Database connection tests
2. API endpoint testing
3. Frontend-backend integration tests
4. Load testing for concurrent users
5. Security vulnerability scanning

This setup will ensure your BiodivProScope application is production-ready and scalable!
