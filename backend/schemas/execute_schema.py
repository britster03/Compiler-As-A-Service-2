# backend/schemas/execute_schema.py

from marshmallow import Schema, fields, validate, ValidationError

def validate_language(value):
    supported_languages = ['python', 'javascript']
    if value.lower() not in supported_languages:
        raise ValidationError('Unsupported language.')

class ExecuteSchema(Schema):
    language = fields.Str(required=True, validate=validate_language)
    code = fields.Str(required=True, validate=validate.Length(min=1))
