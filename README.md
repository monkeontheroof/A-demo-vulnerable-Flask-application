<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/monkeontheroof/">
    <img src="https://github.com/user-attachments/assets/62eedf6e-3812-4080-8185-db49e32dfdb8" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">A Vulnerable Flask application</h3>

  <p align="center">
    This project is created for security enthusiasts, researchers for learning purposes only, please consider before installing.
    <br /> 
  </p>
</div>
    <!-- <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a> -->
    
---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git
- Python

### Development environment
```bash
python3 -m venv .venv
pip install -r requirements.txt
```

- Linux:
```sh
.venv/Scripts/activate
```

- Windows:
```cmd
.venv\Scripts\activate.bat
```

### Production environment at local (Docker)

```bash
docker compose up -d --build
```

## 📝 Example Environment Variables (.env)
```CRLF
DB_USER=root
DB_PASSWORD=password123
DB_HOST=db
DB_PORT=3306
DB_NAME=test_db

APP_SECRET_KEY=Admin@123
FLASK_DEBUG=True
COOKIE_SECURE=False
COOKIE_HTTPONLY=False
# COOKIE_SAMESITE=Lax
```
