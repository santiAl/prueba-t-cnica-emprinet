from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=lambda x: len(x) > 3)
    email = fields.Email(required=True)
    password_hash = fields.Str(required=True, load_only=True, validate=lambda x: len(x) >= 6)

user_schema = UserSchema()
users_schema = UserSchema(many=True)