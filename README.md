# 🌿 BiodivProScope - Biodiversity Risk Assessment Platform

[![Deploy BiodivProScope](https://github.com/Rahul9121/BiodivScope/actions/workflows/deploy.yml/badge.svg)](https://github.com/Rahul9121/BiodivScope/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://reactjs.org/)

BiodivProScope is a comprehensive web-based platform for biodiversity risk assessment and environmental impact mitigation. It combines geospatial analysis, machine learning, and extensive environmental databases to provide data-driven insights for biodiversity conservation and protection.

## 🌟 Features

### 🔍 Risk Assessment Engine
- **Multi-layered Risk Analysis**: IUCN Red List species, invasive species, freshwater, marine, and terrestrial risks
- **Geographic Focus**: Specialized for New Jersey environmental data
- **Real-time Assessment**: Location-based risk evaluation using coordinates or addresses
- **Threat Level Classification**: High, moderate, and low risk categorization

### 🤖 AI-Powered Mitigation
- **Intelligent Recommendations**: ChromaDB vector database with semantic search
- **Context-Aware Actions**: Tailored mitigation strategies based on risk type and threat level
- **RAG Implementation**: Retrieval-Augmented Generation for enhanced recommendations
- **Knowledge Base**: Extensive environmental mitigation action database

### 🗺️ Interactive Mapping
- **Leaflet Integration**: Interactive maps with marker clustering
- **Risk Visualization**: Color-coded threat level indicators
- **Geographic Search**: Address autocomplete and ZIP code support
- **Real-time Updates**: Dynamic risk data loading based on map movement

### 📊 Reporting & Analytics
- **Multi-format Export**: PDF, CSV, and Excel report generation
- **Comprehensive Reports**: Detailed mitigation action plans
- **Data Visualization**: Risk level statistics and trend analysis
- **Session Management**: Persistent user data and preferences

### 👤 User Management
- **Secure Authentication**: Password hashing and session management
- **Account Dashboard**: Profile management and settings
- **Multi-user Support**: Isolated user experiences and data

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React.js      │    │   Flask API     │    │  PostgreSQL     │
│   Frontend      │◄──►│   Backend       │◄──►│   Database      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   ChromaDB      │    │   Redis Cache   │
│   Load Balancer │    │   Vector DB     │    │   (Optional)    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

### 🐳 Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rahul9121/BiodivScope.git
   cd BiodivScope
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your specific configurations
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   docker-compose exec backend python database/user_table.py
   docker-compose exec backend python database/invasive_species.py
   # Run other database setup scripts as needed
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001
   - ChromaDB: http://localhost:8000

### 🔧 Local Development

1. **Backend Setup**
   ```bash
   cd FullStackApp/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend Setup**
   ```bash
   cd FullStackApp/frontend
   npm install
   npm start
   ```

3. **Database Setup**
   ```bash
   # Install and start PostgreSQL
   # Create database and run migration scripts
   python database/user_table.py
   ```

## 🌐 Deployment Options

### Option 1: Vercel + Railway (Recommended for Beginners)

#### Frontend (Vercel)
1. Push your code to GitHub
2. Connect Vercel to your repository
3. Set environment variables:
   ```
   REACT_APP_API_BASE_URL=https://your-backend-url.railway.app
   ```
4. Deploy automatically on git push

#### Backend (Railway)
1. Create a new Railway project
2. Connect to your GitHub repository
3. Add PostgreSQL database service
4. Set environment variables:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=your-secret-key
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

### Option 2: AWS Deployment

#### Infrastructure Components
- **EC2**: Backend API hosting
- **RDS**: PostgreSQL database
- **S3**: File storage for reports
- **CloudFront**: CDN for frontend
- **Route 53**: Domain management
- **ELB**: Load balancing

#### Deployment Steps
1. Create VPC and security groups
2. Launch RDS PostgreSQL instance
3. Deploy backend to EC2 with Auto Scaling
4. Set up S3 bucket for static files
5. Configure CloudFront distribution
6. Deploy frontend to S3 + CloudFront

### Option 3: DigitalOcean Droplet

```bash
# On your droplet
git clone https://github.com/Rahul9121/BiodivScope.git
cd BiodivScope
docker-compose up -d
```

### Option 4: Google Cloud Platform

- **Cloud Run**: Containerized services
- **Cloud SQL**: PostgreSQL database
- **Cloud Storage**: File storage
- **Cloud CDN**: Content delivery

## 🔒 Security Configuration

### Environment Variables
```bash
# Required
SECRET_KEY=your-super-secure-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
POSTGRES_PASSWORD=secure-database-password

# Optional but Recommended
SENTRY_DSN=your-sentry-dsn
REDIS_URL=redis://localhost:6379
```

### Security Features
- ✅ Password hashing (Werkzeug)
- ✅ CORS configuration
- ✅ Session management
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection headers
- ✅ Rate limiting
- ✅ Non-root Docker containers

## 📊 Database Schema

### Core Tables
- `users`: User authentication and profiles
- `invasive_species`: Invasive species risk data
- `iucn_data`: IUCN Red List species information
- `freshwater_risk`: Freshwater ecosystem risks
- `marine_hci`: Marine Human Coexistence Index
- `terrestrial_risk`: Land-based biodiversity risks

### Performance Optimizations
- Spatial indexing on coordinate columns
- Composite indexes on frequently queried fields
- Connection pooling
- Query optimization

## 🧪 Testing

### Backend Testing
```bash
cd FullStackApp/backend
pytest --cov=. --cov-report=html
```

### Frontend Testing
```bash
cd FullStackApp/frontend
npm test -- --coverage
```

### Integration Testing
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📈 Monitoring & Maintenance

### Monitoring Stack
- **Sentry**: Error tracking and performance monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Uptime Robot**: Availability monitoring

### Health Checks
- `/health`: Application health endpoint
- Database connectivity checks
- External API availability
- ChromaDB connection status

### Backup Strategy
- Daily automated database backups
- Configuration versioning in Git
- Container image versioning
- Data migration scripts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write tests for new features
- Update documentation for API changes
- Maintain backward compatibility

## 📝 API Documentation

### Authentication Endpoints
- `POST /register` - User registration
- `POST /login` - User authentication
- `POST /logout` - User logout
- `GET /session-status` - Check session validity

### Risk Assessment Endpoints
- `POST /search` - Location-based risk assessment
- `GET /session-risks` - Retrieve session risk data
- `POST /download-report-direct` - Generate reports

### User Management Endpoints
- `PUT /account/update-profile` - Update user profile
- `POST /account/change-password` - Change password

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check PostgreSQL status
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

#### ChromaDB Issues
```bash
# Rebuild ChromaDB data
docker-compose exec backend python ML\ Strategy/chromaDB_ingest_invasive.py
```

#### Frontend Build Errors
```bash
# Clear npm cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- IUCN Red List for species data
- OpenStreetMap for geocoding services
- New Jersey Department of Environmental Protection
- ChromaDB team for vector database technology
- React and Flask communities

## 📞 Support

- 📧 Email: support@biodivproscope.com
- 🐛 Issues: [GitHub Issues](https://github.com/Rahul9121/BiodivScope/issues)
- 📖 Documentation: [Wiki](https://github.com/Rahul9121/BiodivScope/wiki)
- 💬 Discussions: [GitHub Discussions](https://github.com/Rahul9121/BiodivScope/discussions)

---

**Built with ❤️ for biodiversity conservation**
