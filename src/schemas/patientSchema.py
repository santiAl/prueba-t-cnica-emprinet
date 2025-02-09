from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    birthdate = fields.Date(format='%Y-%m-%d', allow_none=True)
    phone_number = fields.Str(allow_none=True)
    dni = fields.Str(required=True, unique=True)
        
    @validates('birthdate')
    def validate_birthdate(self, value):
        if value and value > datetime.now().date():
            raise ValidationError("La fecha de nacimiento no puede ser una fecha futura.")

# Instancias para usar en las rutas
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)