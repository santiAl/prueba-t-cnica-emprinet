from marshmallow import Schema, fields
from marshmallow import Schema, fields, validates, ValidationError

class AppointmentSchema(Schema):
    """ Esquema para validar informacion de los appointments. """
    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    date_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M')
    reason = fields.Str()
    state = fields.Str()

    # Valores permitidos para el campo 'state'
    VALID_STATES = ['pendiente', 'confirmado', 'cancelado', 'finalizado']

    @validates('state')
    def validate_state(self, value):
        """Valida que el estado sea uno de los valores permitidos."""
        if value not in self.VALID_STATES:
            raise ValidationError(f"El estado debe ser uno de los siguientes: {', '.join(self.VALID_STATES)}")

# Instancias para usar en las rutas
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
