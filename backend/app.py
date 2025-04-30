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
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

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

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

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

    # Create tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

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

    return jsonify({"username": user.username}), 200

# AI voice-related routes (placeholder for now)
@app.route('/api/voice/generate', methods=['POST'])
@jwt_required()
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
