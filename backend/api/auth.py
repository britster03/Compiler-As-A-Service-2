# backend/api/auth.py
from flask import Blueprint, request, jsonify
from models import db
from models.user import User
from flask_jwt_extended import create_access_token
from datetime import timedelta
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth', __name__)

# Marshmallow Schemas
class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

register_schema = RegisterSchema()
login_schema = LoginSchema()

@auth_bp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    try:
        data = register_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
