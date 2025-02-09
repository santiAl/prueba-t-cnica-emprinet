from datetime import datetime
from src import db

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)  
    state = db.Column(db.String(50), default="pendiente")   

    # Relación con Paciente
    patient = db.relationship("Patient", back_populates="appointments")

    def __repr__(self):
        return f"<Turno {self.id} - {self.fecha_hora} - {self.estado}>"
