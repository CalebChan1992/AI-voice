# AI Voice Backend

This is the backend for the AI Voice application, built with Flask and JWT authentication.

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   flask run
   ```

## API Endpoints

### Authentication

- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get access token
- `POST /api/refresh` - Refresh access token

### User

- `GET /api/user` - Get current user info (protected)

### Voice

- `POST /api/voice/generate` - Generate AI voice (protected, placeholder)
