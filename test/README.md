# AI Voice Testing

This directory contains tests for both the frontend and backend components of the AI Voice application.

## Structure

- `frontend/` - Tests for the Vue 3 frontend
  - `unit/` - Unit tests for individual functions and utilities
  - `components/` - Component tests for Vue components

- `backend/` - Tests for the Flask backend
  - `unit/` - Unit tests for individual functions and classes
  - `integration/` - Integration tests for API endpoints

## Running Tests

### Frontend Tests

```bash
# Navigate to the frontend directory
cd frontend

# Run tests
npm test           # Run tests once
npm run test:watch # Run tests in watch mode
npm run test:coverage # Run tests with coverage report
```

### Backend Tests

```bash
# Navigate to the backend directory
cd backend

# Run tests
pytest ../test/backend          # Run all backend tests
pytest ../test/backend/unit     # Run only unit tests
pytest ../test/backend/integration # Run only integration tests
pytest ../test/backend --cov=app # Run tests with coverage report
```

## Adding New Tests

### Frontend

Add new component tests in `frontend/components/` and unit tests in `frontend/unit/`.
Test files should follow the naming convention `*.test.ts` or `*.spec.ts`.

### Backend

Add new unit tests in `backend/unit/` and integration tests in `backend/integration/`.
Test files should follow the naming convention `test_*.py`.
