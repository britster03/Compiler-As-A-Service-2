# backend/app_schemas/execute_schema.py

from marshmallow import Schema, fields, ValidationError

class ExecuteSchema(Schema):
    language = fields.Str(required=True, validate=lambda x: x.lower() in ['python', 'javascript'])
    code = fields.Str(required=True)
