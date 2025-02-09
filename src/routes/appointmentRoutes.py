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
    """
    Obtiene todos los turnos.
    - **Metodo**: GET
    - **Parametros**: Ninguno
    - **Respuesta exitosa**: Codigo 200, lista de turnos
    - **Errores posibles**: Codigo 500, error inesperado
    """

    try:
        # Se usa el servicio para obtener la info correspondiente
        appointment_service = AppointmentService(db)
        appointments = appointment_service.get_all_appointments()
        
        appointment_list = appointments_schema.dump(appointments)

        return jsonify({'status':'success','data': appointment_list}),200

    except Exception as e:
        return jsonify({"status": "error","message": "An unexpected error occurred","details": {"message": str(e)}  }), 500





@appointment_bp.route('/', methods=['POST'])
def create_appointment():
    """
    Crea un nuevo turno.
    - **Metodo**: POST
    - **Parámetros**: JSON con los datos del turno
    - **Respuesta exitosa**: Codigo 201, turno creado
    - **Errores posibles**: Codigo 400, error de validación o clave foránea. Codigo 500, error inesperado
    """
    
    try:
        data = request.get_json()

        # Aqui se realiza la validacion de los datos
        validated_data = appointment_schema.load(data)

        appointment_service = AppointmentService(db)
        new_appointment = appointment_service.create_appointment(validated_data)

        return jsonify({'status': 'success','data': appointment_schema.dump(new_appointment)}), 201

    except ValidationError as err:
        # Si los datos no son válidos, Marshmallow lanzara un ValidationError
        return jsonify({"status": "error","message": "Validation failed","details": err.messages}), 400
    except ForeignKeyError as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 400
    except Exception as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 500  
    



@appointment_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """
    Obtiene un turno por ID.
    - **Metodo**: GET
    - **Parametros**: ID del turno
    - **Respuesta exitosa**: Codigo 200, turno encontrado
    - **Errores posibles**: Codigo 404, turno no encontrado. Codigo 500, error inesperado
    """

    try:
        appointment_service = AppointmentService(db)
        appointment = appointment_service.get_appointment_by_id(appointment_id)
        
        return jsonify({'status': 'success','data': appointment_schema.dump(appointment)}), 200

    except NotFoundError as e:
        return jsonify({"status": "error","message": "No se pudo encontrar un paciente con ese ID","details": {"message": str(e)}  }), 404
    except Exception as e:  
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 500  





@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """
    Actualiza un turno por ID.
    - **Metodo**: PUT
    - **Parametros**: ID del turno y datos del turno (parciales)
    - **Respuesta exitosa**: Codigo 200, turno actualizado
    - **Errores posibles**: Codigo 400: error de validación. Codigo 404: turno no encontrado. Codigo 500: error inesperado
    """

    try:
        appointment_service = AppointmentService(db)
        data = request.get_json()
        # Aqui se realiza la validacion de los datos
        appointment_data = appointment_schema.load(data, partial=True)
        updated_appointment = appointment_service.update_appointment(appointment_id, appointment_data)
        
        return jsonify({'status': 'success','data': appointment_schema.dump(updated_appointment)}), 200
        
    except ValidationError as err:
        # Si los datos no son válidos, Marshmallow lanzara un ValidationError
        return jsonify({"status": "error","message": "Validation failed","details": err.messages }), 400
    except NotFoundError as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 404
    except Exception as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 500  
    





@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """
    Elimina un turno por ID.
    - **Metodo**: DELETE
    - **Parametros**: ID del turno
    - **Respuesta exitosa**: Codigo 200, turno eliminado
    - **Errores posibles**: Codigo 404, turno no encontrado. Codigo 500, error inesperado
    """

    appointment_service = AppointmentService(db)
    try:
        appointment = appointment_service.delete_appointment(appointment_id)

        if appointment:  # Si la eliminación fue exitosa
            return jsonify({"message": f"El turno {appointment.id} fue eliminado correctamente"}), 200

    except NotFoundError as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)} }), 404
    except Exception as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)} }), 500  
