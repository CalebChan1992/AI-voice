from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
import bcrypt

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow requests from the frontend
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5174"]}})

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')  # Change this in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define Organization model for multi-tenancy
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plan = db.Column(db.String(50), default='free')  # free, basic, premium, enterprise
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    users = db.relationship('User', backref='organization', lazy=True)

    def __repr__(self):
        return f'<Organization {self.name}>'

# Define User model with enhanced role management
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    # Roles: admin, manager, user, guest
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        """Convert user object to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'organization_id': self.organization_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400

    # Create new user
    user = User(username=data['username'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # Find user by username
    user = User.query.filter_by(username=data['username']).first()

    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({"msg": "Invalid username or password"}), 401

    # Create tokens with additional claims
    additional_claims = {
        'username': user.username,
        'role': user.role
    }

    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id))

    # Return user info along with tokens
    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        username=user.username,
        role=user.role
    ), 200

@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return jsonify(access_token=access_token), 200

# Protected route example
@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }), 200

# Import the role-based authorization helpers
from auth_helpers import admin_required, manager_required, user_required

# User management routes (admin only)
@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)"""
    users = User.query.all()
    return jsonify({
        "users": [user.to_dict() for user in users]
    }), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_by_id(user_id):
    """Get a specific user by ID (admin only)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user.to_dict()), 200

@app.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    """Create a new user (admin only)"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'password', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing required field: {field}"}), 400

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400

    # Check if email already exists (if provided)
    if 'email' in data and data['email'] and User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400

    # Create new user
    new_user = User(
        username=data['username'],
        email=data.get('email'),
        role=data['role'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        organization_id=data.get('organization_id')
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg": "User created successfully",
        "user": new_user.to_dict()
    }), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update a user (admin only)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()

    # Update user fields
    if 'username' in data and data['username'] != user.username:
        # Check if new username already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"msg": "Username already exists"}), 400
        user.username = data['username']

    if 'email' in data and data['email'] != user.email:
        # Check if new email already exists
        if data['email'] and User.query.filter_by(email=data['email']).first():
            return jsonify({"msg": "Email already exists"}), 400
        user.email = data['email']

    if 'password' in data:
        user.set_password(data['password'])

    if 'role' in data:
        user.role = data['role']

    if 'first_name' in data:
        user.first_name = data['first_name']

    if 'last_name' in data:
        user.last_name = data['last_name']

    if 'is_active' in data:
        user.is_active = data['is_active']

    if 'organization_id' in data:
        user.organization_id = data['organization_id']

    db.session.commit()

    return jsonify({
        "msg": "User updated successfully",
        "user": user.to_dict()
    }), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"}), 200

# Organization management routes
@app.route('/api/organizations', methods=['GET'])
@admin_required
def get_organizations():
    """Get all organizations (admin only)"""
    organizations = Organization.query.all()
    return jsonify({
        "organizations": [{
            "id": org.id,
            "name": org.name,
            "plan": org.plan,
            "created_at": org.created_at.isoformat() if org.created_at else None
        } for org in organizations]
    }), 200

@app.route('/api/organizations/<int:org_id>', methods=['GET'])
@admin_required
def get_organization(org_id):
    """Get a specific organization by ID (admin only)"""
    org = Organization.query.get(org_id)
    if not org:
        return jsonify({"msg": "Organization not found"}), 404

    return jsonify({
        "id": org.id,
        "name": org.name,
        "plan": org.plan,
        "created_at": org.created_at.isoformat() if org.created_at else None
    }), 200

# AI voice-related routes (protected by role)
@app.route('/api/voice/generate', methods=['POST'])
@user_required
def generate_voice():
    # This would be where you implement AI voice generation
    # For now, just return a placeholder response
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({"msg": "Voice generation endpoint (to be implemented)", "user": user.username}), 200

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
