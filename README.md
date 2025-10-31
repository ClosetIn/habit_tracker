# Habit Tracker API

A modern, fast, and RESTful API for tracking daily habits and building positive routines. Built with **FastAPI** and **PostgreSQL**, following REST architecture principles.

## 🚀 Features

- **RESTful API** - Clean, standardized API endpoints
- **PostgreSQL Database** - Persistent data storage with SQLAlchemy ORM
- **Docker Support** - Easy database setup with Docker Compose
- **Habit Management** - Create, read, update, and delete habits
- **Automatic Documentation** - Interactive API docs with Swagger UI
- **Data Validation** - Strong typing with Pydantic models
- **Asynchronous** - High performance with async/await
- **Standards Compliant** - OpenAPI, JSON Schema, REST best practices

## 📚 API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base URL
```
http://localhost:8000
```

## 🛠️ Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Powerful, open-source relational database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Docker** - Containerization for database
- **Python 3.11+** - Programming language
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI web server implementation
- **Poetry** - Python dependency management and packaging

## 🗄️ Database Schema

### Habits Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `name` | String(100) | Habit name (required) |
| `description` | Text | Optional description |
| `frequency` | String(20) | daily, weekly, monthly (default: daily) |
| `created_at` | DateTime | Automatic timestamp on creation |
| `updated_at` | DateTime | Automatic timestamp on update |

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
   echo "DATABASE_URL=postgresql://postgres:password@localhost:5432/habit_tracker" > .env
   ```

5. **Run the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Open your browser**
   Navigate to http://localhost:8000/docs to see the interactive API documentation.

## 📡 API Endpoints

### Habits

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/habits` | Get all habits | 200 |
| `GET` | `/habits/{id}` | Get specific habit by ID | 200, 404 |
| `POST` | `/habits` | Create a new habit | 201, 400 |
| `PUT` | `/habits/{id}` | Update a habit | 200, 404 |
| `DELETE` | `/habits/{id}` | Delete a habit | 200, 404 |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |

## 🎯 Usage Examples

### Create a New Habit
```http
POST /habits
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
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Get All Habits
```http
GET /habits
```

### Update a Habit
```http
PUT /habits/1
Content-Type: application/json

{
  "name": "Morning Meditation",
  "description": "15 minutes of mindfulness and breathing",
  "frequency": "daily"
}
```

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
│   └── database.py          # Database configuration and connection
├── alembic/                 # Database migrations (optional)
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

### Database Migrations with Alembic
```bash
# Initialize Alembic (if not done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description of changes"

# Apply migration
alembic upgrade head
```

### API Testing with curl
```bash
# Create a habit
curl -X POST "http://localhost:8000/habits/" \
     -H "Content-Type: application/json" \
     -d '{"name":"Reading","description":"Read 20 pages daily","frequency":"daily"}'

# Get all habits
curl "http://localhost:8000/habits/"

# Update a habit
curl -X PUT "http://localhost:8000/habits/1" \
     -H "Content-Type: application/json" \
     -d '{"name":"Updated Habit Name"}'
```

## 🌐 Environment Variables

Create a `.env` file in the root directory:

```ini
DATABASE_URL=postgresql://postgres:password@localhost:5432/habit_tracker
```

## 🚧 Current Limitations & Next Steps

### ✅ Completed
- REST API with FastAPI
- PostgreSQL database with SQLAlchemy
- Docker containerization for database
- Full CRUD operations for habits
- Automatic API documentation

### 🔄 In Progress
- Database migrations setup
- Error handling improvements

### 📋 Planned
- [ ] User authentication with JWT
- [ ] Habit completion tracking
- [ ] Analytics and statistics
- [ ] Frontend application (React/Vue)
- [ ] Email reminders
- [ ] Social features
- [ ] Deployment to cloud platform

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

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

**Happy habit building!** 🎯

*This README is a living document and will be updated as the project evolves.*