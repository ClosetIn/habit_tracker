# Habit Tracker API

A modern, fast, and secure RESTful API for tracking daily habits and building positive routines. Built with **FastAPI** and **PostgreSQL**, featuring JWT authentication and user-specific data isolation.

## 🚀 Features

- **JWT Authentication** - Secure user authentication with token-based access
- **User Registration & Login** - Complete auth system with password hashing
- **RESTful API** - Clean, standardized API endpoints
- **PostgreSQL Database** - Persistent data storage with SQLAlchemy ORM
- **Docker Support** - Easy database setup with Docker Compose
- **Habit Management** - Create, read, update, and delete user-specific habits
- **Automatic Documentation** - Interactive API docs with Swagger UI
- **Data Validation** - Strong typing with Pydantic models
- **Asynchronous** - High performance with async/await
- **Standards Compliant** - OpenAPI, JSON Schema, REST best practices
- **Token Expiration** - Secure 30-minute JWT token lifespan

## 📚 API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Base URL
```
http://localhost:8080
```

## 🛠️ Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Powerful, open-source relational database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **JWT** - JSON Web Tokens for secure authentication
- **bcrypt** - Password hashing library
- **Docker** - Containerization for database
- **Python 3.11+** - Programming language
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI web server implementation
- **Poetry** - Python dependency management and packaging

## 🗄️ Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `email` | String(255) | Unique email address |
| `username` | String(100) | Unique username |
| `hashed_password` | String(255) | Bcrypt hashed password |
| `created_at` | DateTime | Automatic timestamp on creation |

### Habits Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `name` | String(100) | Habit name (required) |
| `description` | Text | Optional description |
| `frequency` | String(20) | daily, weekly, monthly (default: daily) |
| `created_at` | DateTime | Automatic timestamp on creation |
| `updated_at` | DateTime | Automatic timestamp on update |
| `user_id` | Integer | Foreign key to users table |

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ClosetIn/habit_tracker.git
   cd habit_tracker
   ```

2. **Start PostgreSQL with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Install Python dependencies**
   ```bash
   poetry install
   poetry shell
   ```

   *Or using traditional venv:*
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   cat > .env << EOF
   DATABASE_URL=postgresql://postgres:password@localhost:5432/habit_tracker
   JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-very-long-and-secure
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_MINUTES=30
   EOF
   ```

5. **Run the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

6. **Open your browser**
   Navigate to http://localhost:8080/docs to see the interactive API documentation.

## 🔐 Authentication

### Register a New User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Using the Access Token
Add the token to your requests in the Authorization header:
```
Authorization: Bearer your-jwt-token-here
```

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/auth/register` | Register new user | 200, 400, 422 |
| `POST` | `/auth/login` | Login and get access token | 200, 401, 422 |
| `GET` | `/auth/me` | Get current user info | 200, 401, 403 |

### Habits (Require Authentication)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/habits` | Get all user's habits | 200, 401 |
| `GET` | `/habits/{id}` | Get specific habit by ID | 200, 401, 404 |
| `POST` | `/habits` | Create a new habit | 201, 400, 401 |
| `PUT` | `/habits/{id}` | Update a habit | 200, 401, 404 |
| `DELETE` | `/habits/{id}` | Delete a habit | 200, 401, 404 |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |

## 🎯 Usage Examples

### Register and Login Flow

1. **Register a new user:**
```http
POST /auth/register
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

2. **Login to get access token:**
```http
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

3. **Use token to access protected endpoints:**
```http
GET /habits
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Create a New Habit (Authenticated)
```http
POST /habits
Authorization: Bearer your-jwt-token
Content-Type: application/json

{
  "name": "Morning Meditation",
  "description": "10 minutes of mindfulness meditation",
  "frequency": "daily"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Morning Meditation",
  "description": "10 minutes of mindfulness meditation",
  "frequency": "daily",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "user_id": 1
}
```

### Get Current User Info
```http
GET /auth/me
Authorization: Bearer your-jwt-token
```

## 🔒 Security Features

- **Password Hashing** - All passwords are hashed using bcrypt
- **JWT Tokens** - Secure token-based authentication
- **Token Expiration** - Automatic token expiry after 30 minutes
- **User Isolation** - Users can only access their own habits
- **Input Validation** - Comprehensive data validation with Pydantic

## 🐳 Docker Database Management

### Start and Stop Database
```bash
# Start database
docker-compose up -d

# Stop database
docker-compose down

# Stop and remove volumes (warning: deletes data)
docker-compose down -v
```

### Database Operations
```bash
# View database logs
docker-compose logs postgres

# Connect to database directly
docker-compose exec postgres psql -U postgres -d habit_tracker

# Backup database
docker-compose exec postgres pg_dump -U postgres habit_tracker > backup.sql
```

## 🏗️ Project Structure

```
habit_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── schemas.py           # Pydantic models for data validation
│   ├── models.py            # SQLAlchemy database models
│   ├── database.py          # Database configuration and connection
│   ├── auth.py              # Authentication utilities and JWT handling
│   └── dependencies.py      # FastAPI dependencies for auth
├── docker-compose.yml       # Docker configuration for PostgreSQL
├── .env                     # Environment variables (create this)
├── .gitignore
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Poetry configuration
├── poetry.lock             # Poetry lock file
└── README.md               # Project documentation
```

## 🔧 Development

### Running Tests
```bash
# To be implemented
pytest
```

### Code Formatting
```bash
# Install development dependencies
poetry add --dev black isort flake8

# Format code
black app/
isort app/
```

### API Testing with curl
```bash
# Register a new user
curl -X POST "http://localhost:8080/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","username":"testuser","password":"testpass123"}'

# Login and save token
TOKEN=$(curl -s -X POST "http://localhost:8080/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"testpass123"}' | \
     python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Create a habit with the token
curl -X POST "http://localhost:8080/habits/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"name":"Reading","description":"Read 20 pages daily","frequency":"daily"}'

# Get all habits
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8080/habits/"
```

## 🌐 Environment Variables

Create a `.env` file in the root directory:

```ini
DATABASE_URL=postgresql://postgres:password@localhost:5432/habit_tracker
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-very-long-and-secure
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

## 🚧 Current Limitations & Next Steps

### ✅ Completed (Day 1-3)
- REST API with FastAPI
- PostgreSQL database with SQLAlchemy
- Docker containerization for database
- Full CRUD operations for habits
- Automatic API documentation
- JWT Authentication & Authorization
- User registration and login
- Password hashing with bcrypt
- User-specific data isolation

### 📋 Planned Features
- [ ] Habit completion tracking and streaks
- [ ] Analytics and statistics dashboard
- [ ] Email reminders and notifications
- [ ] Social features (friend system, sharing)
- [ ] Mobile application (React Native)
- [ ] Deployment to cloud platform (AWS/Azure)
- [ ] Rate limiting and API throttling
- [ ] Advanced filtering and search for habits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [PostgreSQL](https://www.postgresql.org/) for the powerful database
- [SQLAlchemy](https://www.sqlalchemy.org/) for the Python ORM
- [Docker](https://www.docker.com/) for containerization
- [JWT](https://jwt.io/) for authentication standard

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

**Happy habit building!** 🎯

*This README is a living document and will be updated as the project evolves.*