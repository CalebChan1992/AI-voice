import pytest
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app import app, db, User

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(username="testuser", role="user")
            test_user.set_password("password")
            db.session.add(test_user)
            db.session.commit()
        yield client
        
        # Clean up
        with app.app_context():
            db.drop_all()

@pytest.fixture
def auth_headers():
    """Get authentication headers with a valid token."""
    from flask_jwt_extended import create_access_token
    
    with app.app_context():
        # Get the test user
        user = User.query.filter_by(username="testuser").first()
        if not user:
            return {}
            
        # Create an access token
        access_token = create_access_token(identity=user.id)
        return {'Authorization': f'Bearer {access_token}'}
