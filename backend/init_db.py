from app import app, db, User, Organization

# Create database tables
with app.app_context():
    db.drop_all()  # Drop all tables first (careful in production!)
    db.create_all()  # Create tables

    # Create default organizations
    default_org = Organization(name="Default Organization", plan="free")
    premium_org = Organization(name="Premium Organization", plan="premium")
    db.session.add(default_org)
    db.session.add(premium_org)
    db.session.flush()  # Flush to get IDs

    # Create users with different roles
    # Admin user
    admin_user = User(
        username="admin",
        email="admin@example.com",
        role="admin",
        first_name="Admin",
        last_name="User",
        organization_id=default_org.id
    )
    admin_user.set_password("password")
    db.session.add(admin_user)

    # Manager user
    manager_user = User(
        username="manager",
        email="manager@example.com",
        role="manager",
        first_name="Manager",
        last_name="User",
        organization_id=default_org.id
    )
    manager_user.set_password("password")
    db.session.add(manager_user)

    # Regular user
    regular_user = User(
        username="user",
        email="user@example.com",
        role="user",
        first_name="Regular",
        last_name="User",
        organization_id=default_org.id
    )
    regular_user.set_password("password")
    db.session.add(regular_user)

    # Premium organization user
    premium_user = User(
        username="premium",
        email="premium@example.com",
        role="user",
        first_name="Premium",
        last_name="User",
        organization_id=premium_org.id
    )
    premium_user.set_password("password")
    db.session.add(premium_user)

    db.session.commit()

    print("Database initialized with test users and organizations:")
    print("Admin - Username: admin, Password: password")
    print("Manager - Username: manager, Password: password")
    print("User - Username: user, Password: password")
    print("Premium User - Username: premium, Password: password")
