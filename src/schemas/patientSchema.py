from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime
import re

class PatientSchema(Schema):
    ''' Esquema para validar la informacion de los pacientes. '''

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    birthdate = fields.Date(format='%Y-%m-%d', allow_none=True)
    phone_number = fields.Str(allow_none=True)
    dni = fields.Str(required=True, unique=True)
    
    @validates("name")
    def validate_name(self, value):
        '''Valida que el nombre solo contenga letras y espacios.'''
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", value):
            raise ValidationError("El nombre solo puede contener letras y espacios.")

    @validates("last_name")
    def validate_last_name(self, value):
        '''Valida que el apellido solo contenga letras y espacios.'''
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", value):
            raise ValidationError("El apellido solo puede contener letras y espacios.")

    @validates('birthdate')
    def validate_birthdate(self, value):
        '''Valida que la fecha de nacimento sea una fecha pasada.'''
        if value and value > datetime.now().date():
            raise ValidationError("La fecha de nacimiento no puede ser una fecha futura.")

# Instancias para usar en las rutas
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)