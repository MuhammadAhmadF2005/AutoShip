markdown
# AutoShip 

A containerized Python code analysis and deployment dashboard built with FastAPI.
Paste Python code, get instant linting scores, complexity analysis, and history tracking.

## Live Demo
http://51.20.72.125:8000

## Tech Stack
- FastAPI + Jinja2
- SQLite + SQLAlchemy
- Docker + Docker Compose
- GitHub Actions CI/CD
- AWS EC2

## Run Locally

### Prerequisites
- Python 3.11+
- Docker Desktop

### Without Docker
bash
pip install -r requirements.txt
uvicorn app.main:app --reload

Visit http://localhost:8000

### With Docker
bash
docker compose up --build

Visit http://localhost:8000

## Project Structure

autoship/
├── app/
│   ├── main.py         # FastAPI routes
│   ├── database.py     # SQLAlchemy setup
│   ├── models.py       # Database models
│   ├── templates/      # Jinja2 HTML templates
│   └── static/         # CSS files
├── .github/workflows/  # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
└── requirements.txt


## CI/CD Pipeline
1. Push to main branch
2. GitHub Actions triggers
3. Docker image built and pushed to Docker Hub
4. EC2 instance pulls latest image
5. Container restarted with zero downtime

## Team
- Muhammad Ahmad — DevOps Pipeline, FastAPI App, AWS EC2
- Muhammad Haider  — Documentation, Testing
- Muhammad Zaid — Infrastructure as Code (Terraform)
