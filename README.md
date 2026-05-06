# AutoShip: Automated Python Code Quality Analysis

A web-based application for automated Python code quality analysis and reporting using FastAPI and pylint.

## Features

- **Real-time Code Analysis**: Analyze Python code quality instantly using pylint
- **Historical Tracking**: Keep records of all analyses with timestamps
- **Dashboard Statistics**: View trends, pass rates, and average scores
- **Pass/Fail Assessment**: Automatic qualification based on configurable thresholds
- **Responsive Interface**: Modern web UI built with HTML5 and CSS3
- **RESTful API**: Well-documented API endpoints for integration
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoShip
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

### Docker Deployment

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## Project Structure

```
AutoShip/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy ORM models
│   ├── database.py          # Database configuration
│   ├── static/              # CSS and static assets
│   │   └── style.css
│   └── templates/           # Jinja2 HTML templates
│       ├── base.html
│       ├── index.html
│       ├── analyze.html
│       ├── results.html
│       └── history.html
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
├── report.tex              # Detailed technical documentation
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guidelines
└── LICENSE                 # License information
```

## API Endpoints

- **GET** `/` - Dashboard with statistics and recent analyses
- **GET** `/health` - Health check endpoint

## Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pylint**: Python code quality analysis
- **Uvicorn**: ASGI server

### Frontend
- **Jinja2**: Template engine for dynamic content
- **HTML5 & CSS3**: Web interface

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Service orchestration

## Configuration

Configuration is managed through environment variables and application settings:

- Database URL: Set via SQLAlchemy configuration in `app/database.py`
- Pylint settings: Customizable in analysis functions
- Server port: Configurable in deployment (default: 8000)

## Development

### Running Tests

```bash
pytest
```

### Code Style

We follow PEP 8 standards. Use `pylint` and `black` for code quality:

```bash
pylint app/
black app/
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:

1. Check existing [issues](https://github.com/username/AutoShip/issues)
2. Create a new issue with detailed description
3. Contact the development team

## Roadmap

- [ ] Integration with additional code quality tools (flake8, mypy)
- [ ] User authentication and authorization
- [ ] Advanced filtering and search
- [ ] Export to PDF/CSV/JSON
- [ ] CI/CD pipeline integration
- [ ] Performance optimization
- [ ] Real-time notifications

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Core code analysis functionality
- Dashboard with statistics
- Historical tracking

## Authors

- Development Team

## Acknowledgments

- FastAPI community for excellent documentation
- SQLAlchemy for robust ORM capabilities
- Pylint for comprehensive code analysis
