from ..models import Patient  
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from ..exceptions.servicesExceptions import AlreadyExistsError,NotFoundError

class PatientService:
    
    def __init__(self, db):
        self.db = db  
    
    
    def get_all_patients(self):
        patients = self.db.session.query(Patient).all()
        return patients
    
    def get_patient_by_id(self, patient_id):
        patient = self.db.session.get(Patient, patient_id)
        if not patient:
            raise NotFoundError(f"No se encontró el paciente con ID {patient_id}")
        return patient
    
    

    def create_patient(self, name, last_name, email, dni ,birthdate=None, phone_number=None):
        # Verificar si ya existe un paciente con el mismo correo electrónico
        existing_patient = self.db.session.query(Patient).filter(
            or_(
                Patient.email == email,  # Buscar por email
                Patient.dni == dni       # Buscar por dni
            )
        ).first()
        
        if existing_patient:
            raise AlreadyExistsError('El email o usuario ya existen')
        
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
        try:
            patient = self.get_patient_by_id(patient_id)
            self.db.session.delete(patient)
            self.db.session.commit()
            return patient
        except Exception as e:
            self.db.session.rollback()
            raise e


