# 🏠 MoveIn API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqldatabase&logoColor=white)

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

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL server running locally or remotely

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/kostantingolovenko/move-in.git](https://github.com/kostantingolovenko/move-in.git)
   cd move-in
Create and activate a virtual environment:

Bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory based on .env.example:

Фрагмент коду
DATABASE_URL=postgresql://username:password@localhost:5432/movein_db
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
Run the application:

Bash

uvicorn main:app --reload
📚 API Documentation (Swagger UI)
FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

🗄️ Project Structure
Plaintext
move-in/

├── routers/          # API endpoints (users, listings, reviews)

├── main.py           # FastAPI application instance & entry point

├── models.py         # SQLAlchemy database models

├── database.py       # Database connection and session management

├── config.py         # Environment variables and configuration

├── .env.example      # Example of required environment variables

├── .gitignore        # Git ignore rules

└── requirements.txt  # Python dependencies