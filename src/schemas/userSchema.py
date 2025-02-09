from marshmallow import Schema, fields

class UserSchema(Schema):
    """ Esquema para validar los datos de usuario """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=lambda x: len(x) > 3)
    password_hash = fields.Str(required=True, load_only=True, validate=lambda x: len(x) >= 6)

# Instancias para usar en las rutas
user_schema = UserSchema()
users_schema = UserSchema(many=True)