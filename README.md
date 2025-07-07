<div align="center">

# ImagineApps Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.0-red.svg?style=for-the-badge&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A modern, high-performance backend API built with FastAPI and Python.

</div>

## 📋 Overview

ImagineApps Backend is a robust REST API service built using FastAPI, a modern, high-performance web framework for building APIs with Python. The project implements industry best practices including comprehensive CRUD operations, JWT authentication, automated documentation, and a scalable architecture.

## ✨ Features

- **Complete CRUD Operations**: Efficient database interactions for all resources
- **JWT Authentication & Authorization**: Secure API endpoints with role-based access control
- **Automatic Documentation**: Interactive API documentation with Swagger UI and ReDoc
- **Data Validation**: Runtime validation with Pydantic models
- **Modular & Scalable Architecture**: Well-organized codebase for maintainability and growth
- **ORM Integration**: Database interaction using SQLAlchemy
- **Comprehensive Testing**: Automated tests with pytest
- **Docker Support**: Containerization for consistent deployment

## 🔧 Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- Pydantic
- Additional dependencies in `requirements.txt`

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/imagineapps-backend.git
cd imagineapps-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```
DATABASE_URL=postgresql://user:password@postgresserver/db
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

A sample configuration file is provided in `.env.example`.

## 🏃‍♂️ Running the Application

### Start the development server

```bash
uvicorn app.main:app --reload
```

- API service: [http://localhost:8000](http://localhost:8000)
- Swagger UI documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📁 Project Structure

```
imagineapps-backend/
│
├── app/                    # Main application code
│   ├── api/                # API endpoints
│   │   ├── dependencies/   # Endpoint dependencies
│   │   ├── routes/         # API routes organized by resource
│   │   └── api.py          # Main API router
│   ├── core/               # Core configuration
│   │   ├── config.py       # Application settings
│   │   └── security.py     # Security functions
│   ├── db/                 # Database definitions
│   │   ├── base_class.py   # Base model class
│   │   └── session.py      # DB session configuration
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── crud/               # CRUD operations
│   └── main.py             # Application entry point
│
├── tests/                  # Automated tests
├── .env                    # Environment variables (do not commit)
├── .env.example            # Example environment configuration
├── .gitignore              # Git ignore rules
├── requirements.txt        # Project dependencies
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

Run tests with coverage reports:

```bash
pytest --cov=app tests/
```

## 🐳 Deployment

### Using Docker

#### 1. Build the image

```bash
docker build -t imagineapps-backend .
```

#### 2. Run the container

```bash
docker run -d -p 8000:8000 --name imagineapps-api imagineapps-backend
```

### Environment Variables

For production deployment, ensure you set appropriate environment variables for:

- Database connection
- JWT secret key
- Logging configuration
- CORS settings

## 📚 API Documentation

Complete API documentation is available at:

- **Swagger UI**: `/docs` - Interactive API documentation
- **ReDoc**: `/redoc` - Alternative documentation interface

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - your.email@example.com

Project Link: [https://github.com/yourusername/imagineapps-backend](https://github.com/yourusername/imagineapps-backend)

---

<div align="center">

**Built with ❤️ by the ImagineApps Team**

</div>
