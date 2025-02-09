from flask import Flask, request, jsonify
from flask import Blueprint
from ..services.appointmentService import AppointmentService
from .. import db
from ..schemas.appointmentSchema import appointments_schema, appointment_schema
from marshmallow import ValidationError
from ..exceptions.servicesExceptions import NotFoundError, AlreadyExistsError,ForeignKeyError

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/', methods=['GET'])
def get_all_appointments():
    try:
        appointment_service = AppointmentService(db)
        # Usar el servicio para obtener todos los pacientes
        appointments = appointment_service.get_all_appointments()
        
        appointment_list = appointments_schema.dump(appointments)

        return jsonify({
            'status':'success',
            'data': appointment_list
            }),200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred",
            "details": {"message": str(e)}  
        }), 500


@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    try:
        data = request.get_json()

        # Validación con Marshmallow
        validated_data = appointment_schema.load(data)

        appointment_service = AppointmentService(db)
        new_appointment = appointment_service.create_appointment(validated_data)

        return jsonify({
            'status': 'success',
            'data': appointment_schema.dump(new_appointment)
        }), 201

    except ValidationError as err:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "details": err.messages  # Los detalles del error de Marshmallow
        }), 400
    except ForeignKeyError as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  
        }), 500  
    

@appointment_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    try:
        appointment_service = AppointmentService(db)
        appointment = appointment_service.get_appointment_by_id(appointment_id)
        
        return jsonify({
            'status': 'success',
            'data': appointment_schema.dump(appointment)
        }), 200

    except NotFoundError as e:
        return jsonify({
                "status": "error",
                "message": "No se pudo encontrar un paciente con ese ID",
                "details": {"message": str(e)}  
            }), 404
    except Exception as e:  
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  
        }), 500  



@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        appointment_service = AppointmentService(db)
        data = request.get_json()
        appointment_data = appointment_schema.load(data, partial=True)  # Permitir actualización parcial
        updated_appointment = appointment_service.update_appointment(appointment_id, appointment_data)
        
        return jsonify({
            'status': 'success',
            'data': appointment_schema.dump(updated_appointment)
        }), 200
        

    except ValidationError as err:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "details": err.messages  # Los detalles del error de Marshmallow
        }), 400
    except NotFoundError as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  
        }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  
        }), 500  
    

@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment_service = AppointmentService(db)
    try:
        appointment = appointment_service.delete_appointment(appointment_id)

        if appointment:  # Si la eliminación fue exitosa
            return jsonify({"message": f"El turno {appointment.id} fue eliminado correctamente"}), 200

    except NotFoundError as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  
        }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  
        }), 500  
