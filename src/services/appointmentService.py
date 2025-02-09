from ..models import Appointment  
from ..exceptions.servicesExceptions import AlreadyExistsError,NotFoundError,ForeignKeyError

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
        if self.appointment_exists(data['patient_id'], data['date_time']):
            raise AlreadyExistsError("El paciente ya tiene un turno en esta fecha y hora.")

        new_appointment = Appointment(
            patient_id=data['patient_id'],
            date_time=data['date_time'],
            reason=data.get('reason'),
            state=data.get('state', 'pendiente')
        )

        try:
            self.db.session.add(new_appointment)
            self.db.session.commit()
            return new_appointment
        except Exception as e:
            self.db.session.rollback()
            # Verifica si el error es por clave foránea
            if "foreign key" in str(e.orig).lower():  
                raise ForeignKeyError("El paciente especificado no existe")  
            raise e  # Relanza la excepción si es otro error de integridad
    
    def update_appointment(self, appointment_id, data):
        """ Actualiza un turno por su ID """
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            raise NotFoundError(f"No se encontró el turno con ID {appointment_id}")

        if self.appointment_exists(data['patient_id'], data['date_time'], exclude_appointment_id=appointment_id):
            raise AlreadyExistsError("Ya existe otro turno para este paciente en la misma fecha y hora.")

        for key, value in data.items():
            setattr(appointment, key, value)  # Actualizar los campos dinámicamente

        try:
            self.db.session.commit()
            return appointment
        except Exception as e:
            self.db.session.rollback()
            if "foreign key" in str(e.orig).lower():  
                raise ForeignKeyError("El paciente especificado no existe") 
            raise e # Relanzo la excepcion para que sea capturada por quien invoque el servicio.
        

    def delete_appointment(self, appointment_id):
        """ Elimina un turno por su ID """
        appointment = self.get_appointment_by_id(appointment_id)

        try:
            self.db.session.delete(appointment)
            self.db.session.commit()
            return appointment
        except Exception as e:
            self.db.session.rollback()
            raise e


    def appointment_exists(self, patient_id, date_time, exclude_appointment_id=None):
        """ Verifica si ya existe un turno para el paciente en la fecha y hora dadas. """
        query = self.db.session.query(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.date_time == date_time
        )
        if exclude_appointment_id:
            query = query.filter(Appointment.id != exclude_appointment_id)

        return query.first() is not None

