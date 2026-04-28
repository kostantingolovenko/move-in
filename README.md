# 🏠 MoveIn API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqldatabase&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📖 Overview
MoveIn API is a robust backend service for a real estate platform. It provides RESTful endpoints for user authentication, property listing management, and user reviews. Built with modern Python web frameworks, it ensures high performance, automatic documentation, and reliable data validation.

## ✨ Features
- **User Authentication:** Secure signup and login using JWT (JSON Web Tokens) and password hashing (Bcrypt).
- **Property Listings:** Complete CRUD (Create, Read, Update, Delete) operations for real estate properties.
- **Review System:** Users can leave ratings and comments on specific properties.
- **Favorites:** Users can save their favorite listings for quick access.
- **Data Validation:** Strict input validation and serialization using Pydantic models.

## 🛠️ Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (OAuth2 with Password (and hashing), Bearer with JWT tokens)
- **Server:** Uvicorn

## 🐳 Docker

The image is available on Docker Hub: [kostiantin777/move-in-web](https://hub.docker.com/repository/docker/kostiantin777/move-in-web/general)

### Pull the image

```bash
docker pull kostiantin777/move-in-web:latest
```

### Run with Docker

```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://username:password@host:5432/movein_db \
  -e SECRET_KEY=your_super_secret_key \
  -e ALGORITHM=HS256 \
  --name move-in-web \
  kostiantin777/move-in-web:latest
```

### Run with Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  web:
    image: kostiantin777/move-in-web:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/movein_db
      - SECRET_KEY=your_super_secret_key
      - ALGORITHM=HS256
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=movein_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Then run:

```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL server running locally or remotely

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kostantingolovenko/move-in.git
   cd move-in
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv

   # Windows:
   .venv\Scripts\activate

   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory based on `.env.example`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/movein_db
   SECRET_KEY=your_super_secret_key
   ALGORITHM=HS256
   ```

5. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

## 📚 API Documentation (Swagger UI)
FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## 🗄️ Project Structure
```
move-in/
├── routers/          # API endpoints (users, listings, reviews)
├── main.py           # FastAPI application instance & entry point
├── models.py         # SQLAlchemy database models
├── database.py       # Database connection and session management
├── config.py         # Environment variables and configuration
├── Dockerfile        # Docker image definition
├── docker-compose.yml# Docker Compose configuration
├── .env.example      # Example of required environment variables
├── .gitignore        # Git ignore rules
└── requirements.txt  # Python dependencies
```
