
# Habit Tracker API

A modern, fast, and secure RESTful API for tracking daily habits and building positive routines. Built with **FastAPI** and **PostgreSQL**, featuring JWT authentication, habit completion tracking, and comprehensive analytics.

## 🚀 Features

- **JWT Authentication** - Secure user authentication with token-based access
- **User Registration & Login** - Complete auth system with password hashing
- **RESTful API** - Clean, standardized API endpoints
- **PostgreSQL Database** - Persistent data storage with SQLAlchemy ORM
- **Docker Support** - Easy database setup with Docker Compose
- **Habit Management** - Create, read, update, and delete user-specific habits
- **Habit Completion Tracking** - Mark habits as completed with notes and ratings
- **Advanced Analytics** - Completion rates, streaks, and performance statistics
- **Pagination & Filtering** - Efficient data retrieval for large datasets
- **Automatic Documentation** - Interactive API docs with Swagger UI
- **Data Validation** - Strong typing with Pydantic models
- **Asynchronous** - High performance with async/await
- **Code Quality** - Static analysis with flake8, black, isort, mypy, and pylint
- **Standards Compliant** - OpenAPI, JSON Schema, REST best practices
- **Token Expiration** - Secure 30-minute JWT token lifespan

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
- **JWT** - JSON Web Tokens for secure authentication
- **bcrypt** - Password hashing library
- **Docker** - Containerization for database
- **Python 3.11+** - Programming language
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI web server implementation
- **Poetry** - Python dependency management and packaging
- **Alembic** - Database migrations
- **Static Analysis** - flake8, black, isort, mypy, pylint

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
| `owner_id` | Integer | Foreign key to users table |

### Habit Completions Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `habit_id` | Integer | Foreign key to habits table |
| `completed_date` | Date | Date when habit was completed |
| `completed_at` | DateTime | Automatic timestamp of completion |
| `notes` | Text | Optional notes about completion |
| `rating` | Integer | Optional rating (1-5) |

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/habit_tracker.git
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

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Run the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Open your browser**
   Navigate to http://localhost:8000/docs to see the interactive API documentation.

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
  "login": "user@example.com",  # Can use email or username
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
| `GET` | `/habits` | Get all user's habits (with pagination) | 200, 401 |
| `GET` | `/habits/{id}` | Get specific habit by ID | 200, 401, 404 |
| `POST` | `/habits` | Create a new habit | 201, 400, 401 |
| `PUT` | `/habits/{id}` | Update a habit | 200, 401, 404 |
| `DELETE` | `/habits/{id}` | Delete a habit | 200, 401, 404 |
| `GET` | `/habits/today` | Get today's habits with completion status | 200, 401 |
| `GET` | `/habits/{id}/detailed` | Get detailed habit info with statistics | 200, 401, 404 |

### Habit Completions (Require Authentication)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/completions` | Mark habit as completed | 201, 400, 401, 404 |
| `GET` | `/habits/{id}/completions` | Get all completions for a habit | 200, 401, 404 |
| `DELETE` | `/completions/{id}` | Delete a completion record | 200, 401, 404 |
| `POST` | `/completions/bulk` | Mark multiple habits as completed | 201, 400, 401 |

### Analytics & Statistics (Require Authentication)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/stats/overview` | Get user's overall statistics | 200, 401 |
| `GET` | `/habits/{id}/detailed` | Get detailed analytics for a habit | 200, 401, 404 |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |

## 🎯 Usage Examples

### Complete Habit Tracking Flow

1. **Register and login to get token**
```http
POST /auth/register
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}

POST /auth/login
{
  "login": "user@example.com",
  "password": "securepassword123"
}
```

2. **Create a habit**
```http
POST /habits
Authorization: Bearer your-jwt-token
{
  "name": "Morning Meditation",
  "description": "10 minutes of mindfulness meditation",
  "frequency": "daily"
}
```

3. **Mark habit as completed**
```http
POST /completions
Authorization: Bearer your-jwt-token
{
  "habit_id": 1,
  "notes": "Felt very focused today",
  "rating": 5
}
```

4. **View today's habits**
```http
GET /habits/today
Authorization: Bearer your-jwt-token
```

5. **Get detailed analytics**
```http
GET /habits/1/detailed
Authorization: Bearer your-jwt-token

GET /stats/overview
Authorization: Bearer your-jwt-token
```

### Advanced Usage

**Filter habits by frequency:**
```http
GET /habits/?frequency=daily
Authorization: Bearer your-jwt-token
```

**Pagination:**
```http
GET /habits/?skip=0&limit=10
Authorization: Bearer your-jwt-token
```

**Bulk completions:**
```http
POST /completions/bulk
Authorization: Bearer your-jwt-token
{
  "habit_ids": [1, 2, 3],
  "completed_date": "2024-01-15"
}
```

## 📊 Analytics Features

### Individual Habit Statistics
- **Completion Rate** - Percentage of days habit was completed
- **Current Streak** - Number of consecutive days habit was completed
- **Completion History** - All past completions with notes and ratings

### User Overview Statistics
- **Total Habits** - Number of active habits
- **Total Completions** - All-time completed habit instances
- **Longest Streaks** - Top 5 habits with longest current streaks

## 🔒 Security Features

- **Password Hashing** - All passwords are hashed using bcrypt
- **JWT Tokens** - Secure token-based authentication
- **Token Expiration** - Automatic token expiry after 30 minutes
- **User Isolation** - Users can only access their own data
- **Input Validation** - Comprehensive data validation with Pydantic
- **Duplicate Prevention** - Cannot mark same habit completed twice on same day

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

## 🔧 Development

### Code Quality Tools
```bash
# Install development dependencies
poetry add --group dev black isort flake8 mypy pylint autopep8

# Format code
poetry run format

# Run linting and type checking
poetry run lint

# Run specific tools
poetry run black app/
poetry run isort app/
poetry run flake8 app/
poetry run mypy app/
poetry run pylint app/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Running Tests
```bash
# Start services
docker-compose up -d

# Run the application
uvicorn app.main:app --reload

# Test API endpoints via Swagger UI at http://localhost:8000/docs
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
│   ├── dependencies.py      # FastAPI dependencies for auth
│   ├── utils.py             # Utility functions for analytics
│   └── serializers.py       # Model serialization utilities
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
├── scripts/                 # Development scripts
│   ├── lint.py
│   ├── format.py
│   └── fix_all.py
├── docker-compose.yml       # Docker configuration for PostgreSQL
├── .env                     # Environment variables
├── .flake8                  # Flake8 configuration
├── .pylintrc                # Pylint configuration
├── alembic.ini              # Alembic configuration
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Poetry lock file
└── README.md                # Project documentation
```

## 🌐 Environment Variables

Create a `.env` file in the root directory:

```ini
DATABASE_URL=postgresql://postgres:password@localhost:5432/habit_tracker
JWT_SECRET_KEY=your-super-secret-jwt-key-here-make-it-very-long-and-secure
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

## 📈 Development Progress

### ✅ Completed Features (Days 1-4)

**Day 1-2: Basic API & Database**
- REST API with FastAPI
- PostgreSQL database with SQLAlchemy
- Docker containerization for database
- Full CRUD operations for habits
- Automatic API documentation

**Day 3: Authentication & Security**
- JWT Authentication & Authorization
- User registration and login
- Password hashing with bcrypt
- User-specific data isolation
- Protected endpoints

**Day 4: Advanced Features & Analytics**
- Habit completion tracking system
- Advanced analytics and statistics
- Completion rates and streak tracking
- Pagination and filtering
- Bulk operations
- Code quality tools and static analysis
- Enhanced error handling

### 🚧 Planned Enhancements
- [ ] Email reminders and notifications
- [ ] Social features (friend system, sharing)
- [ ] Mobile application (React Native)
- [ ] Deployment to cloud platform (AWS/Azure)
- [ ] Rate limiting and API throttling
- [ ] Advanced filtering and search for habits
- [ ] Habit categories and tags
- [ ] Export data (CSV, PDF reports)

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