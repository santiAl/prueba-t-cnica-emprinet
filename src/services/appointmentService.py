from ..models import Appointment  
from ..exceptions.servicesExceptions import AlreadyExistsError,NotFoundError,ForeignKeyError

class AppointmentService:
    
    def __init__(self, db):
        self.db = db  

    def get_all_appointments(self):
        """
        Obtiene todos los turnos de la base de datos.
        Retorna:
            list: Una lista de objetos Appointment que representan todos los turnos almacenados.
        """

        patients = self.db.session.query(Appointment).all()
        return patients
    

    def get_appointment_by_id(self, appointment_id):
        """
        Obtiene un turno por su ID.
        Args:
            appointment_id (int): El ID del turno a recuperar.
        Raises:
            NotFoundError: Si no se encuentra un turno con el ID.
        Retorna:
            Appointment: Un objeto Appointment que representa el turno encontrado.
        """

        appointment = self.db.session.query(Appointment).filter_by(id=appointment_id).first()
        if not appointment:
            raise NotFoundError(f"No se encontró el turno con ID {appointment_id}")
        return appointment



    def create_appointment(self, data):
        """
        Crea un nuevo turno en la base de datos.
        Args:
            data (dict): Un diccionario con la informacion del turno.
        Raises:
            AlreadyExistsError: Si el paciente ya tiene un turno en la fecha y hora solicitada.
            ForeignKeyError: Si el paciente no existe en la base de datos.
        Retorna:
            Appointment: El objeto Appointment creado.
        """


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
            # Si surgio un error, volvemos atras
            self.db.session.rollback()
            # Verifica si el error es por clave foránea
            if "foreign key" in str(e.orig).lower():  
                raise ForeignKeyError("El paciente especificado no existe")  
            raise e  # Relanza la excepción si es otro error de integridad
    



    def update_appointment(self, appointment_id, data):
        """
        Actualiza un turno existente en la base de datos.
        Args:
            appointment_id (int): El ID del turno que se va a actualizar.
            data (dict): Un diccionario con los nuevos datos para el turno.
        Raises:
            NotFoundError: Si no se encuentra un turno con el ID proporcionado.
            AlreadyExistsError: Si ya existe un turno para el paciente en la misma fecha y hora.
            ForeignKeyError: Si el paciente especificado no existe.
        Retorna:
            Appointment: El objeto Appointment actualizado.
        """

        # Aca si no encuentra, el servicio invocado se encarga de lanzar la excepcion
        appointment = self.get_appointment_by_id(appointment_id)

        if self.appointment_exists(data['patient_id'], data['date_time'], exclude_appointment_id=appointment_id):
            raise AlreadyExistsError("Ya existe otro turno para este paciente en la misma fecha y hora.")

        # Actualizacion de los campos
        for key, value in data.items():
            setattr(appointment, key, value)  

        try:
            self.db.session.commit()
            return appointment
        except Exception as e:
            # Si surgio un error, volvemos atras
            self.db.session.rollback()
            if "foreign key" in str(e.orig).lower():  
                raise ForeignKeyError("El paciente especificado no existe") 
            raise e # Relanzo la excepcion para que sea capturada por quien invoque el servicio.
        




    def delete_appointment(self, appointment_id):
        """
        Elimina un turno por su ID.
        Args:
            appointment_id (int): El ID del turno que se va a eliminar.
        Raises:
            Exception: Si ocurre algun error al eliminar el turno.
        Retorna:
            Appointment: El objeto Appointment que se elimino.
        """

        # Aca si no encuentra, el servicio invocado se encarga de lanzar la excepcion
        appointment = self.get_appointment_by_id(appointment_id)

        try:
            self.db.session.delete(appointment)
            self.db.session.commit()
            return appointment
        except Exception as e:
            # Si surgio un error, volvemos atras
            self.db.session.rollback()
            raise e




    def appointment_exists(self, patient_id, date_time, exclude_appointment_id=None):
        """
        Verifica si ya existe un turno para el paciente en la fecha y hora dadas.
        Args:
            patient_id (int): El ID del paciente.
            date_time (datetime): La fecha y hora del turno.
            exclude_appointment_id (int, opcional): En el caso de el update se pasaria para que no compare con el resgistro que estamos actializando.
        Retorna:
            bool: True si ya existe un turno para el paciente en la fecha y hora dadas, de lo contrario False.
        """

        query = self.db.session.query(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.date_time == date_time
        )
        if exclude_appointment_id:
            query = query.filter(Appointment.id != exclude_appointment_id)

        return query.first() is not None

