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