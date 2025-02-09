from datetime import datetime
from src import db

class Appointment(db.Model):
    """
    Modelo que representa un turno en la base de datos.

    Cada turno está asociado a un paciente y contiene información sobre la 
    fecha, el motivo de la consulta y su estado.

    Atributos:
        id (int): Identificador único del turno.
        patient_id (int): Clave foránea que referencia al paciente asociado.
        date_time (datetime): Fecha y hora del turno en formato 'YYYY-MM-DD HH:MM'.
        reason (str, opcional): Motivo de la consulta, limitado a 255 caracteres.
        state (str, opcional): Estado del turno (por defecto, "pendiente").
    """

    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)  
    state = db.Column(db.String(50), default="pendiente")   

    # Relacion con paciente. Esta relacion sirve para el manejo de SqlAlchemy 
    patient = db.relationship("Patient", back_populates="appointments")

    def __repr__(self):
        return f"<Appointment {self.id} - {self.date_time} - {self.state}>"
