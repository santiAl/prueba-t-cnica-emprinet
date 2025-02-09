from ..models import Patient  
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from ..exceptions.servicesExceptions import AlreadyExistsError,NotFoundError

class PatientService:
    
    def __init__(self, db):
        self.db = db  
    
    
    def get_all_patients(self):
        """
        Obtiene todos los pacientes de la base de datos.
        Retorna:
            list: Una lista de objetos Patient representando a todos los pacientes almacenados.
        """
        patients = self.db.session.query(Patient).all()
        return patients
    



    def get_patient_by_id(self, patient_id):
        """
        Obtiene un paciente por su ID.
        Args:
            patient_id (int): El ID del paciente.
        Raises:
            NotFoundError: Si no se encuentra un paciente con el ID.
        Retorna:
            Patient: Un objeto Patient que representa al paciente encontrado.
        """

        patient = self.db.session.get(Patient, patient_id)
        if not patient:
            raise NotFoundError(f"No se encontró el paciente con ID {patient_id}")
        return patient
    
    

    def create_patient(self, name, last_name, email, dni ,birthdate=None, phone_number=None):
        """
        Crea un nuevo paciente en la base de datos.
        Args:
            name (str): Nombre del paciente.
            last_name (str): Apellido del paciente.
            email (str): Email del paciente.
            dni (str): DNI del paciente.
            birthdate (str, opcional): La fecha de nacimiento del paciente en formato 'YYYY-MM-DD'.
            phone_number (str, opcional): Telefono del paciente.
        Raises:
            AlreadyExistsError: Si ya existe un paciente con el mismo correo electrónico o DNI.
        Retorna:
            Patient: El objeto Patient creado.
        """
        
        # Verificar si ya existe un paciente con el mismo correo electrónico
        existing_patient = self.db.session.query(Patient).filter(
            or_(
                Patient.email == email,  # Buscar por email
                Patient.dni == dni       # Buscar por dni
            )
        ).first()
        
        if existing_patient:
            raise AlreadyExistsError('El email o dni ya estan registrados')
        
        # Crear un nuevo paciente
        new_patient = Patient(
            name=name,
            last_name=last_name,
            email=email,
            birthdate=birthdate,
            phone_number=phone_number,
            dni=dni
        )
        
        # Agregar el nuevo paciente a la base de datos
        try:
            self.db.session.add(new_patient)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()  # Deshacer cualquier cambio si ocurre un error
            raise e  # Relanzo la excepcion para que sea capturada por quien invoque el servicio.
        
        # Devolver el paciente creado con su ID
        return new_patient  # Ahora devuelves el objeto Patient completo





    def update_patient(self, patient_id, data):
        """
        Actualiza los datos de un paciente existente en la base de datos.
        Args:
            patient_id (int): El ID del paciente a actualizar.
            data (dict): Un diccionario con los nuevos datos para el paciente.
        Raises:
            NotFoundError: Si no se encuentra un paciente con el ID.
            AlreadyExistsError: Si el email o el DNI ya estan en uso por otro paciente.
        Retorna:
            Patient: El objeto Patient actualizado.
        """

        if 'email' in data or 'dni' in data:
            email = data.get('email')
            dni = data.get('dni')
            # Verificar si ya existe un paciente con el mismo email o dni
            existing_patient = self.db.session.query(Patient).filter(
                or_(
                    Patient.email == email,  # Buscar por email
                    Patient.dni == dni       # Buscar por dni
                )
            ).first()
            if existing_patient and existing_patient.id != patient_id:
                raise AlreadyExistsError('El email o el DNI ya están en uso por otro paciente.')
        
        patient = self.get_patient_by_id(patient_id)
            
        for key, value in data.items():
            setattr(patient, key, value)  # Actualizar los campos dinámicamente

        try:
            self.db.session.commit()
            return patient
        except Exception as e:
            self.db.session.rollback()
            raise e # Relanzo la excepcion para que sea capturada por quien invoque el servicio.
        




    def delete_patient(self, patient_id):
        """
        Elimina un paciente de la base de datos.
        Args:
            patient_id (int): El ID del paciente a eliminar.
        Raises:
            Exception: Si ocurre algun error inesperado.
        Retorna:
            Patient: El objeto Patient eliminado.
        """

        try:
            patient = self.get_patient_by_id(patient_id)
            self.db.session.delete(patient)
            self.db.session.commit()
            return patient
        except Exception as e:
            self.db.session.rollback()
            raise e


