from app import app, db, User

# Create database tables
with app.app_context():
    db.drop_all()  # Drop all tables first (careful in production!)
    db.create_all()  # Create tables

    # Create a test user
    test_user = User(username="test", role="admin")
    test_user.set_password("password")
    db.session.add(test_user)

    # Create a regular user
    regular_user = User(username="user", role="user")
    regular_user.set_password("password")
    db.session.add(regular_user)

    db.session.commit()

    print("Database initialized with test users:")
    print("Admin - Username: test, Password: password")
    print("User - Username: user, Password: password")
