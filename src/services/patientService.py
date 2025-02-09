from ..models import Patient  
from sqlalchemy.exc import IntegrityError
from ..exceptions.servicesExceptions import PatientAlreadyExistsError,NotFoundError

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
    
    

    def create_patient(self, name, last_name, email, birthdate=None, phone_number=None):
        # Verificar si ya existe un paciente con el mismo correo electrónico
        existing_patient = self.db.session.query(Patient).filter_by(email=email).first()
        
        if existing_patient:
            raise PatientAlreadyExistsError()
        
        # Crear un nuevo paciente
        new_patient = Patient(
            name=name,
            last_name=last_name,
            email=email,
            birthdate=birthdate,
            phone_number=phone_number
        )
        
        # Agregar el nuevo paciente a la base de datos
        try:
            self.db.session.add(new_patient)
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()  # Deshacer cualquier cambio si ocurre un error
            return {'message': 'Error al crear el paciente. Posiblemente un campo duplicado o inválido.'}, 400
        
        # Devolver el paciente creado con su ID
        return new_patient  # Ahora devuelves el objeto Patient completo


    def update_patient(self, patient_id, data):
        patient = self.get_patient_by_id(patient_id)
            
        for key, value in data.items():
            setattr(patient, key, value)  # Actualizar los campos dinámicamente

        try:
            self.db.session.commit()
            return patient
        except IntegrityError:
            self.db.session.rollback()
            raise PatientAlreadyExistsError("El correo electrónico ya está registrado.")
        

    def delete_patient(self, patient_id):
        patient = self.get_patient_by_id(patient_id)
        self.db.session.delete(patient)
        self.db.session.commit()
        return patient


