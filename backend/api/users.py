from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models import db
from marshmallow import Schema, fields, ValidationError

users_bp = Blueprint('users', __name__)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

user_schema = UserSchema()

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return user_schema.jsonify(user), 200

