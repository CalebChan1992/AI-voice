# AI Voice Application

A web application for AI voice generation with Vue 3 frontend and Python Flask backend.

## Project Structure

- `frontend/` - Vue 3 + TypeScript frontend
- `backend/` - Python Flask backend with JWT authentication

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

## Backend Setup

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
python init_db.py  # Initialize the database with a test user
python run.py
```

The backend API will be available at http://localhost:5000

## Features

- Vue 3 with TypeScript
- Pinia for state management
- JWT authentication
- AI-themed visuals
- Python Flask backend

## API Endpoints

### Authentication

- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get access token
- `POST /api/refresh` - Refresh access token

### User

- `GET /api/user` - Get current user info (protected)

### Voice

- `POST /api/voice/generate` - Generate AI voice (protected, placeholder)
