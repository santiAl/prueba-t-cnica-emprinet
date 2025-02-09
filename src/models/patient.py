from .. import db


class Patient(db.Model):
    """
    Modelo que representa a los pacientes en la base de datos.

    Este modelo se utiliza para almacenar información sobre los pacientes, 
    incluyendo su nombre, apellido, dni, correo electrónico, fecha de nacimiento y teléfono.

    Atributos:
        id (int): Identificador único del paciente.
        name (str): Nombre del paciente, no puede ser nulo.
        last_name (str): Apellido del paciente, no puede ser nulo.
        dni (str): Documento Nacional de Identidad (DNI) del paciente, único y no nulo.
        email (str): Correo electrónico del paciente, único y no nulo.
        birthdate (date, opcional): Fecha de nacimiento del paciente, en formato 'YYYY-MM-DD'.
        phone_number (str, opcional): Número de teléfono del paciente.
    """

    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    
    # Relacion con appointments. Esta relacion sirve para el manejo de SqlAlchemy
    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.last_name}>"
    