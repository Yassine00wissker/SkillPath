# SkillPath - Learning Platform

A full-stack learning platform with AI-powered recommendations for courses and jobs.

## Features

- **User Authentication**: JWT-based authentication for users and admins
- **Recommendation Engine**: 
  - Keyword-based recommendations
  - AI-powered recommendations using Google Gemini
- **Course Management**: Browse and manage formations
- **Job Recommendations**: Get personalized job suggestions based on skills
- **Admin Panel**: Manage categories, formations, and users

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy (async)
- MySQL
- JWT Authentication
- Google Gemini API

### Frontend
- React 19
- Vite
- Tailwind CSS
- React Router
- Axios

## Setup Instructions

### Backend Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

3. **Create MySQL database:**
   ```sql
   CREATE DATABASE skillpath;
   ```

4. **Update database URL in `app/config/database.py`:**
   ```python
   DATABASE_URL = "mysql+aiomysql://user:password@localhost/skillpath"
   ```

5. **Seed the database (optional):**
   ```bash
   python seed_db.py
   ```
   Or use the SQL file:
   ```bash
   mysql -u root -p skillpath < dummy_data.sql
   ```

6. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL (default: http://localhost:8000)
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## Gemini API Configuration

### Enable Mock Mode (for testing without API key)

Set `MOCK_MODE=true` in your `.env` file. This will return deterministic mock responses.

### Using Real Gemini API

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your-api-key-here
   MOCK_MODE=false
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login (returns JWT token)
- `POST /auth/admin/login` - Admin login

### Users
- `GET /users/me` - Get current user
- `GET /users/{id}` - Get user by ID
- `PUT /users/me` - Update current user

### Formations
- `GET /formations` - Get all formations
- `GET /formations/{id}` - Get formation by ID
- `POST /formations` - Create formation (Admin only)

### Recommendations
- `POST /api/recommend/keyword` - Keyword-based recommendations
- `POST /api/recommend/ai` - AI-powered recommendations

## Default Credentials

After seeding the database:

**User:**
- Email: `sophie.martin@email.com`
- Password: `password123`

**Admin:**
- Email: `admin@skillpath.com`
- Password: `admin123`

## Project Structure

```
backend/
├── app/
│   ├── config/       # Database configuration
│   ├── core/         # Security, recommender, Gemini client
│   ├── crud/         # Database operations
│   ├── models/       # SQLAlchemy models
│   ├── routes/       # API routes
│   └── schemas/      # Pydantic schemas
├── requirements.txt
└── seed_db.py

frontend/
├── src/
│   ├── api/          # API client
│   ├── components/   # React components
│   ├── pages/        # Page components
│   └── styles/       # Global styles
└── package.json
```

## Development

### Running Tests

Backend tests (when implemented):
```bash
cd backend
pytest
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

Backend:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## License

MIT

