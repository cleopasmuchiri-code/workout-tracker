from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=6)
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    notes = fields.Str()
    duration_minutes = fields.Int(validate=validate.Range(min=1))
    date = fields.Date()
    user_id = fields.Int(dump_only=True)
