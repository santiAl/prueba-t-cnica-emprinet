from flask import Flask, request, jsonify
from flask import Blueprint
from ..services.appointmentService import AppointmentService
from .. import db
from ..schemas.appointmentSchema import appointments_schema, appointment_schema
from marshmallow import ValidationError
from ..exceptions.servicesExceptions import NotFoundError

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/', methods=['GET'])
def get_all_appointments():
    appointment_service = AppointmentService(db)
    # Usar el servicio para obtener todos los pacientes
    appointments = appointment_service.get_all_appointments()
    
    return jsonify(appointments_schema.dump(appointments)), 200


@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    try:
        data = request.get_json()

        # Validación con Marshmallow
        validated_data = appointment_schema.load(data)

        appointment_service = AppointmentService(db)
        new_appointment = appointment_service.create_appointment(validated_data)

        return jsonify(appointment_schema.dump(new_appointment)), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@appointment_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment_service = AppointmentService(db)
    appointment = appointment_service.get_appointment_by_id(appointment_id)
    
    if not appointment:
        return jsonify({"error": "Turno no encontrado"}), 404

    return jsonify(appointment_schema.dump(appointment)), 200

@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        data = request.get_json()
        appointment_service = AppointmentService(db)
        updated_appointment = appointment_service.update_appointment(appointment_id, data)

        if not updated_appointment:
            return jsonify({"error": "Turno no encontrado"}), 404

        return jsonify(appointment_schema.dump(updated_appointment)), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment_service = AppointmentService(db)
    try:
        appointment = appointment_service.delete_appointment(appointment_id)

        if appointment:  # Si la eliminación fue exitosa
            return jsonify({"message": f"El turno {appointment.id} fue eliminado correctamente"}), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404  # No se encontró el recurso
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Error interno
