from ..models import Appointment  
from ..exceptions.servicesExceptions import PatientAlreadyExistsError,NotFoundError

class AppointmentService:
    
    def __init__(self, db):
        self.db = db  

    def get_all_appointments(self):
        patients = self.db.session.query(Appointment).all()
        return patients
    

    def get_appointment_by_id(self, appointment_id):
        """ Obtiene un turno por su ID """
        appointment = self.db.session.query(Appointment).filter_by(id=appointment_id).first()
        if not appointment:
            raise NotFoundError(f"No se encontró el turno con ID {appointment_id}")
        return appointment

    def create_appointment(self, data):
        """ Crea un nuevo turno """
        new_appointment = Appointment(
            pacient_id=data['pacient_id'],
            date_time=data['date_time'],
            reason=data.get('reason'),
            state=data.get('state', 'pendiente')
        )

        self.db.session.add(new_appointment)
        self.db.session.commit()
        return new_appointment
    
    def update_appointment(self, appointment_id, data):
        """ Actualiza un turno por su ID """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            raise NotFoundError(f"No se encontró el turno con ID {appointment_id}")

        appointment.date_time = data.get('date_time', appointment.date_time)
        appointment.reason = data.get('reason', appointment.reason)
        appointment.state = data.get('state', appointment.state)

        self.db.session.commit()
        return appointment
    def delete_appointment(self, appointment_id):
        """ Elimina un turno por su ID """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            raise NotFoundError(f"No se encontró el turno con ID {appointment_id}")

        self.db.session.delete(appointment)
        self.db.session.commit()
        return appointment
