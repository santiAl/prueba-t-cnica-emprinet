from marshmallow import Schema, fields

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    pacient_id = fields.Int(required=True)
    date_time = fields.DateTime(required=True, format='%Y-%m-%d %H:%M:%S')
    reason = fields.Str()
    state = fields.Str()

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
