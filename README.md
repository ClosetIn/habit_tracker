# Habit Tracker API

A modern, fast, and RESTful API for tracking daily habits and building positive routines. Built with **FastAPI** and following REST architecture principles.

## 🚀 Features

- **RESTful API** - Clean, standardized API endpoints
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
- **Python 3.11+** - Programming language
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI web server implementation
- **Poetry** - Python dependency management and packaging

## 📋 Prerequisites

- Python 3.8+
- pip or Poetry

## ⚡ Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/habit_tracker.git
   cd habit_tracker
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Activate virtual environment**
   ```bash
   poetry shell
   ```

   *Or using traditional venv:*
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open your browser**
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
  "created_at": "2024-01-15"
}
```

### Get All Habits
```http
GET /habits
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Morning Meditation",
    "description": "10 minutes of mindfulness meditation",
    "frequency": "daily",
    "created_at": "2024-01-15"
  }
]
```

### Get Specific Habit
```http
GET /habits/1
```

### Update a Habit
```http
PUT /habits/1
Content-Type: application/json

{
  "name": "Morning Meditation",
  "description": "15 minutes of mindfulness and breathing exercises",
  "frequency": "daily"
}
```

## 🏗️ Project Structure

```
habit_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── schemas.py       # Pydantic models for data validation
│   ├── models.py        # Database models (for future use)
│   └── database.py      # Database configuration (for future use)
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Poetry configuration
├── poetry.lock         # Poetry lock file
└── README.md           # Project documentation
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
# Create a habit
curl -X POST "http://localhost:8000/habits/" \
     -H "Content-Type: application/json" \
     -d '{"name":"Reading","description":"Read 20 pages daily","frequency":"daily"}'

# Get all habits
curl "http://localhost:8000/habits/"

# Get specific habit
curl "http://localhost:8000/habits/1"
```

## 🌐 REST API Principles

This API follows REST architectural principles:

- **Resource-Based** - Everything is a resource (habits)
- **HTTP Methods** - Proper use of GET, POST, PUT, DELETE
- **Stateless** - Each request contains all necessary information
- **Uniform Interface** - Consistent naming and structure
- **Code on Demand** - Optional: servers can extend client functionality

## 🚧 Current Limitations

- In-memory storage (data lost on server restart)
- Basic CRUD operations only
- No authentication/authorization
- No habit tracking history

## 📈 Future Enhancements

- [ ] PostgreSQL database integration
- [ ] User authentication with JWT
- [ ] Habit completion tracking
- [ ] Analytics and statistics
- [ ] Mobile app frontend
- [ ] Email reminders
- [ ] Social features

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
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- [Uvicorn](https://www.uvicorn.org/) for the ASGI server

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

**Happy habit building!** 🎯

*This README is a living document and will be updated as the project evolves.*