# Kelio Job Scraper - Project Index

## Project Overview

**Kelio Job Scraper** is a Flask web application that scrapes job listings from the Kelio company's career page. It features an adaptive scraping system using both Requests and Selenium, AI-powered job formatting, email notifications, and a modern web interface for viewing scraped jobs.

**Repository**: https://github.com/YohannHommet/scraper  
**Language**: Python 3.7+  
**Framework**: Flask  
**License**: MIT

## Project Structure

```
scraper/
├── .git/                    # Git repository
├── data/                    # Data storage (CSV files)
├── logs/                    # Application logs
├── scripts/                 # Deployment and utility scripts
├── src/                     # Source code
│   ├── core/               # Core scraping logic
│   │   ├── ai_formatter.py # AI-powered job formatting
│   │   ├── data_handler.py # CSV data management
│   │   ├── notifier.py     # Email notifications
│   │   └── scraper.py      # Main scraping engine
│   ├── static/             # Static assets
│   │   ├── js/            # JavaScript files
│   │   └── style.css      # CSS styling
│   ├── templates/          # HTML templates
│   │   └── index.html     # Main web interface
│   ├── utils/              # Utility modules
│   │   ├── error_handler.py # Error handling utilities
│   │   └── logger.py       # Logging configuration
│   ├── __init__.py         # Package initialization
│   └── app.py              # Flask web application
├── tests/                   # Test suite
│   ├── integration/        # Integration tests
│   └── unit/              # Unit tests
├── .env                     # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
├── CLAUDE.md               # Project documentation
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Docker Compose configuration
├── LICENSE                 # MIT license
├── Procfile                # Heroku deployment
├── README.md               # Project documentation
├── render.yaml             # Render deployment configuration
└── requirements.txt        # Python dependencies
```

## Key Components

### 1. Core Scraping Engine (`src/core/scraper.py`)
- **Adaptive Scraping**: Uses Requests first, falls back to Selenium for JavaScript-heavy pages
- **Retry Logic**: Implements exponential backoff with tenacity library
- **Job Parsing**: Extracts job titles, companies, locations, dates, and links
- **Data Validation**: Ensures scraped data meets quality standards

### 2. AI Formatter (`src/core/ai_formatter.py`)
- **Groq API Integration**: Uses Llama 3.3 70B model for intelligent job formatting
- **Email-Optimized HTML**: Generates email-safe HTML with inline CSS
- **Location Grouping**: Organizes jobs by location for better readability
- **Fallback Formatting**: Basic formatting when AI service is unavailable

### 3. Data Handler (`src/core/data_handler.py`)
- **CSV Management**: Handles job data storage and retrieval
- **Duplicate Detection**: Prevents storing duplicate job listings
- **Data Persistence**: Maintains job history across scraping sessions

### 4. Notification System (`src/core/notifier.py`)
- **Resend API Integration**: Sends formatted job notifications via email
- **Configurable Recipients**: Supports multiple email addresses
- **Error Handling**: Graceful fallback when email service fails

### 5. Web Interface (`src/app.py`)
- **Flask Application**: Modern web interface for viewing scraped jobs
- **Real-time Scraping**: On-demand job scraping via web interface
- **Health Monitoring**: Health check endpoint for deployment monitoring
- **Data Management**: Clear jobs functionality for maintenance

## Technology Stack

### Backend
- **Python 3.7+**: Core programming language
- **Flask 2.3.3**: Web framework
- **Requests 2.31.0**: HTTP library for web scraping
- **BeautifulSoup4 4.12.3**: HTML parsing
- **Selenium 4.21.0**: Browser automation for JavaScript-heavy pages
- **Pandas 2.2.2**: Data manipulation and CSV handling
- **Loguru 0.7.2**: Advanced logging
- **Tenacity 8.2.3**: Retry logic and resilience

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with responsive design
- **JavaScript**: Interactive web interface
- **Bootstrap-like**: Custom CSS framework for job cards

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Chrome/Chromium**: Headless browser for Selenium
- **Render**: Cloud deployment platform

## Configuration & Environment Variables

### Required Environment Variables
```bash
SCRAPER_URL=https://www.bodet.com/fr/nos-offres-d-emploi.html?list%5Bcompany%5D=kelio
```

### Optional Environment Variables
```bash
SEND_EMAIL=true/false                    # Enable/disable email notifications
RESEND_API_KEY=your_resend_api_key      # Resend API key for email service
EMAIL_SENDER=verified@yourdomain.com    # Verified sender email address
EMAIL_RECEIVER=receiver@example.com     # Recipient email address
GROQ_API_KEY=your_groq_api_key         # Groq API key for AI formatting
FLASK_SECRET_KEY=your_secret_key       # Flask secret key
APP_DEBUG=true/false                    # Debug mode flag
JOBS_CSV_PATH=data/jobs.csv            # Path to jobs CSV file
```

## Development Workflow

### Local Development
1. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

2. **Run Scraper**:
   ```bash
   python src/core/scraper.py
   ```

3. **Run Web Interface**:
   ```bash
   python src/app.py
   ```

### Docker Development
1. **Build and Run**:
   ```bash
   docker-compose up -d
   ```

2. **View Logs**:
   ```bash
   docker-compose logs -f scraper
   docker-compose logs -f web
   ```

## API Endpoints

### Web Interface Routes
- `GET /` - Display all scraped jobs
- `GET /health` - Health check endpoint
- `POST /run-scraper` - Execute job scraping
- `POST /clear-jobs` - Clear all stored jobs

### Response Formats
- **Success Response**:
  ```json
  {
    "success": true,
    "message": "Operation completed successfully"
  }
  ```

- **Error Response**:
  ```json
  {
    "success": false,
    "message": "Error description"
  }
  ```

## Data Schema

### Job Data Structure
```python
{
    'title': str,      # Job title
    'link': str,       # Job application URL
    'company': str,    # Company name
    'location': str,   # Job location
    'date': str        # Job posting date
}
```

### CSV File Format
- **Location**: `data/jobs.csv`
- **Encoding**: UTF-8
- **Delimiter**: Comma
- **Headers**: title, link, company, location, date

## Testing Strategy

### Test Structure
- **Unit Tests**: `tests/unit/` - Individual component testing
- **Integration Tests**: `tests/integration/` - End-to-end workflow testing

### Test Coverage
- Core scraping functionality
- Data handling and persistence
- Web interface endpoints
- Error handling and edge cases

## Deployment

### Docker Deployment
1. **Build Image**:
   ```bash
   docker build -t kelio-app .
   ```

2. **Run Container**:
   ```bash
   docker run -d -p 5000:5000 kelio-app
   ```

### Render Deployment
- **Configuration**: `render.yaml` for automatic setup
- **Environment**: Production-ready with health checks
- **Scaling**: Automatic scaling based on traffic

## Monitoring & Logging

### Log Files
- **Location**: `/app/logs/scraper.log`
- **Rotation**: Weekly log rotation
- **Levels**: DEBUG, INFO, WARNING, ERROR

### Health Checks
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts

## Error Handling

### Scraping Failures
- **Retry Logic**: Exponential backoff with 3 attempts
- **Fallback Methods**: Requests → Selenium → Error logging
- **Graceful Degradation**: Continue operation with partial data

### API Failures
- **AI Service**: Fallback to basic formatting
- **Email Service**: Log errors without blocking scraping
- **Data Storage**: Ensure data persistence even with partial failures

## Performance Considerations

### Scraping Optimization
- **Headless Browsing**: Chrome in headless mode for Selenium
- **Request Throttling**: Configurable delays between requests
- **Resource Management**: Proper cleanup of browser instances

### Data Management
- **Efficient Parsing**: BeautifulSoup for fast HTML processing
- **Memory Management**: Pandas DataFrames for data manipulation
- **CSV Optimization**: Streamlined data storage format

## Security Features

### Input Validation
- **URL Sanitization**: Validate scraping URLs
- **Data Filtering**: Sanitize scraped content
- **CSRF Protection**: Flask secret key configuration

### Environment Security
- **API Key Management**: Secure storage of external service keys
- **Container Security**: Non-root user in Docker containers
- **Network Security**: Limited port exposure

## Contributing Guidelines

### Code Standards
- **Python**: PEP 8 compliance
- **Documentation**: Docstrings for all functions
- **Type Hints**: Type annotations where applicable
- **Error Handling**: Comprehensive exception handling

### Development Process
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request
5. Code review and merge

## Troubleshooting

### Common Issues
1. **ChromeDriver Issues**: Ensure Chrome/Chromium is installed
2. **API Rate Limits**: Check external service quotas
3. **Memory Issues**: Monitor container resource usage
4. **Network Issues**: Verify URL accessibility and firewall settings

### Debug Mode
- **Environment Variable**: `APP_DEBUG=true`
- **Log Level**: DEBUG logging enabled
- **Error Display**: Detailed error messages in web interface

## Future Enhancements

### Planned Features
- **Job Search Filtering**: Advanced search and filtering
- **Notification Preferences**: Customizable notification settings
- **Data Analytics**: Job market insights and trends
- **Multi-Source Scraping**: Support for additional job sites
- **API Endpoints**: RESTful API for external integrations

### Technical Improvements
- **Async Scraping**: Asynchronous job processing
- **Database Integration**: PostgreSQL/MongoDB for data storage
- **Caching Layer**: Redis for performance optimization
- **Microservices**: Service-oriented architecture
- **CI/CD Pipeline**: Automated testing and deployment

---

*This index serves as a comprehensive guide for coding agents working on the Kelio Job Scraper project. For detailed implementation, refer to individual source files and the main README.md.*