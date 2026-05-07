# Team Task Manager Backend

A FastAPI-based backend for a team task management application with JWT authentication, PostgreSQL database, and Railway deployment.

## Features

- **User Authentication**: Register, login with JWT tokens
- **Team Management**: Create teams, add members, manage roles
- **Task Management**: Create, assign, update, and delete tasks
- **Dashboard**: Statistics and recent tasks overview
- **CORS Support**: Ready for frontend integration
- **Railway Deployment**: Production-ready configuration

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Railway)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **Deployment**: Railway

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /me` - Get current user profile

### Teams
- `POST /teams/` - Create a new team
- `GET /teams/` - List user's teams
- `GET /teams/{team_id}` - Get team details
- `POST /teams/{team_id}/members` - Add member to team
- `GET /teams/{team_id}/members` - List team members

### Tasks
- `POST /tasks` - Create a new task
- `GET /tasks` - Get tasks assigned to current user
- `GET /teams/{team_id}/tasks` - Get all tasks in a team
- `PATCH /tasks/{task_id}` - Update task (status, priority, etc.)
- `DELETE /tasks/{task_id}` - Delete task

### Dashboard
- `GET /dashboard/stats` - Get dashboard statistics
- `GET /dashboard/recent-tasks` - Get recent tasks

## Local Development

### Prerequisites

- Python 3.8+
- PostgreSQL database (or Railway PostgreSQL)

### Setup

1. **Clone and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and JWT secret
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API:**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## Railway Deployment

### Prerequisites

- Railway account
- GitHub repository

### Deployment Steps

1. **Create Railway Project:**
   - Go to [Railway.app](https://railway.app)
   - Create a new project
   - Connect your GitHub repository

2. **Add PostgreSQL Database:**
   - In your Railway project, add a PostgreSQL database
   - Copy the `DATABASE_URL` from the database settings

3. **Configure Environment Variables:**
   - In Railway project settings, add these environment variables:
     ```
     DATABASE_URL=postgresql://username:password@host:port/database
     JWT_SECRET_KEY=your-super-secret-jwt-key-here-change-in-production
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     PROJECT_NAME=Team Task Manager API
     ALLOWED_ORIGINS=*
     ```

4. **Deploy:**
   - Railway will automatically detect the `Procfile` and deploy
   - Your API will be available at the generated Railway URL

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `JWT_SECRET_KEY` | Secret key for JWT signing | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | 30 |
| `PROJECT_NAME` | API title in documentation | "Team Task Manager API" |
| `ALLOWED_ORIGINS` | CORS allowed origins | "*" |

## Database Schema

The application uses the following tables:

- `users` - User accounts
- `teams` - Team information
- `team_members` - Team membership and roles
- `tasks` - Task details and assignments

Tables are automatically created on startup using SQLAlchemy.

## API Testing

### Using Swagger UI

1. Start the server locally
2. Go to http://127.0.0.1:8000/docs
3. Use the interactive documentation to test endpoints

### Manual Testing Example

```bash
# Register a user
curl -X POST "http://127.0.0.1:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'

# Login
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Use the returned access_token for authenticated requests
```

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI application and CORS setup
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Authentication logic
│   ├── utils.py         # Utility functions
│   └── routes/          # API route modules
│       ├── team.py      # Team management endpoints
│       ├── task.py      # Task management endpoints
│       ├── dashboard.py # Dashboard endpoints
│       └── __init__.py
├── requirements.txt     # Python dependencies
├── Procfile            # Railway deployment configuration
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Security Notes

- JWT tokens expire after 30 minutes by default
- Passwords are hashed using bcrypt
- CORS is configured for frontend integration
- All sensitive data is stored in environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.