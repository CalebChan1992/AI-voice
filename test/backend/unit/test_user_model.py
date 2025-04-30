import pytest
from app import User

def test_user_creation():
    """Test that a user can be created and password hashing works."""
    user = User(username="newuser", role="user")
    user.set_password("securepassword")
    
    assert user.username == "newuser"
    assert user.role == "user"
    assert user.password != "securepassword"  # Password should be hashed
    assert user.check_password("securepassword") is True
    assert user.check_password("wrongpassword") is False
