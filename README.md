# SkillBridge

A modern FastAPI-based platform that connects students with qualified tutors, enabling personalized learning experiences across various subjects and education levels.

## 🚀 Features

### Authentication & Authorization

- **JWT-based Authentication**: Secure user authentication with token-based sessions
- **Password Management**: Secure password hashing with bcrypt
- **User Registration & Login**: Complete authentication flow
- **Protected Routes**: Role-based access control for API endpoints

### User Profile Management

- **Comprehensive Profiles**: Detailed tutor profiles with bio, qualifications, and experience
- **Skills & Subjects**: Array-based storage for multiple teaching subjects
- **Education Levels**: Support for primary, secondary, and university level teaching
- **Teaching Methods**: Online, in-person, or hybrid teaching options
- **Location-based Services**: Geographic filtering for nearby tutors
- **Hourly Rates**: Flexible pricing with currency support

### Advanced Search & Filtering

- **Multi-criteria Search**: Filter by subject, education level, location, teaching method
- **Full-text Search**: Search across profiles, bios, and skills
- **Pagination**: Efficient data loading with skip/limit controls
- **Geolocation**: Find tutors within specific radius (ready for PostGIS integration)

### API Features

- **RESTful Design**: Clean, intuitive API endpoints
- **Comprehensive Documentation**: Auto-generated OpenAPI/Swagger docs
- **Rate Limiting**: Request throttling for API protection
- **CORS Support**: Cross-origin resource sharing configuration
- **Structured Logging**: Detailed application logging with configurable levels

## 🛠️ Technology Stack

### Backend Framework

- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.10+**: Latest Python features and performance improvements

### Database

- **PostgreSQL**: Robust relational database with advanced features
- **SQLAlchemy**: Powerful ORM with declarative models
- **Alembic**: Database migration management (ready for integration)

### Security

- **JWT**: JSON Web Tokens for stateless authentication
- **bcrypt**: Industry-standard password hashing
- **Passlib**: Password handling utilities

### Additional Tools

- **Pydantic**: Data validation and serialization
- **Uvicorn**: Lightning-fast ASGI server
- **python-dotenv**: Environment variable management
- **SlowAPI**: Rate limiting middleware

## 📁 Project Structure

```
SkillBridge/
├── src/
│   ├── api.py                 # API route registration
│   ├── main.py               # Application entry point
│   ├── exceptions.py         # Custom exception definitions
│   ├── logging.py           # Logging configuration
│   ├── rate_limiting.py     # Rate limiting setup
│   │
│   ├── auth/                # Authentication module
│   │   ├── controller.py    # Auth endpoints (login, register)
│   │   ├── service.py       # Auth business logic
│   │   └── model.py         # Auth Pydantic models
│   │
│   ├── users/              # User management module
│   │   ├── controller.py   # User endpoints
│   │   ├── service.py      # User business logic
│   │   └── model.py        # User Pydantic models
│   │
│   ├── profiles/           # Profile management module
│   │   ├── controller.py   # Profile endpoints
│   │   ├── service.py      # Profile business logic
│   │   └── model.py        # Profile Pydantic models
│   │
│   ├── entities/           # Database models
│   │   ├── base.py         # Base entity with timestamps
│   │   ├── user.py         # User SQLAlchemy model
│   │   ├── profile.py      # Profile SQLAlchemy model
│   │
│   │
│   └── database/           # Database configuration
│       ├── core.py         # Database connection & session
│       └── __init__.py
│
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── README.md              # Project documentation
```

## 🚦 Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ghazi-Chaftar/SkillBridge.git
   cd SkillBridge
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:

   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/skillbridge
   SECRET_KEY=your-super-secret-jwt-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Set up the database**

   ```bash
   # Create the database
   createdb skillbridge

   # Run the application to create tables
   python -m src.main
   ```

6. **Run the application**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once the application is running, you can access:

- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Code Quality

```bash
# Format code with black
black src/

# Lint with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

## 🐳 Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI community for the excellent framework
- SQLAlchemy team for the powerful ORM
- PostgreSQL team for the robust database system

## 📞 Contact

**Ghazi Chaftar** - [@Ghazi-Chaftar](https://github.com/Ghazi-Chaftar)

Project Link: [https://github.com/Ghazi-Chaftar/SkillBridge](https://github.com/Ghazi-Chaftar/SkillBridge)

---

**Built with ❤️ using FastAPI and PostgreSQL**
