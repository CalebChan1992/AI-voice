from app import app, db, User

# Create database tables
with app.app_context():
    db.drop_all()  # Drop all tables first (careful in production!)
    db.create_all()  # Create tables
    
    # Create a test user
    test_user = User(username="test")
    test_user.set_password("password")
    db.session.add(test_user)
    db.session.commit()
    
    print("Database initialized with test user:")
    print("Username: test")
    print("Password: password")
