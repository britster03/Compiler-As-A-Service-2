# backend/schemas/execute_schema.py (create this file)

from marshmallow import Schema, fields, validate

class ExecuteSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    language = fields.Str(required=True, validate=validate.Length(max=50))
    code = fields.Str(required=True)
    output = fields.Str(dump_only=True)
    error = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
