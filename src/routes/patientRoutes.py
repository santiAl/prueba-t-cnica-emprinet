
from flask import Flask, request, jsonify
from flask import Blueprint
from ..services.patientService import PatientService
from sqlalchemy.exc import IntegrityError
from .. import db
from marshmallow import ValidationError
from ..schemas.patientSchema import PatientSchema
from ..schemas.patientSchema import patient_schema , patients_schema
from ..exceptions.servicesExceptions import AlreadyExistsError,NotFoundError

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/', methods=['GET'])
def get_all_patients():
    """
    Obtiene todos los pacientes.
    - **Metodo**: GET
    - **Parametros**: Ninguno
    - **Respuesta exitosa**: Codigo 200, lista de pacientes
    - **Errores posibles**: Codigo 500: error inesperado al obtener los pacientes
    """

    patient_service = PatientService(db)
    # Usar el servicio para obtener todos los pacientes
    try:
        patients = patient_service.get_all_patients()
        
        # Convertir la lista de pacientes en una lista de diccionarios para JSON
        patients_list = patients_schema.dump(patients)
        
        return jsonify({'status':'success','data': patients_list}),200
    except Exception as e:
        return jsonify({"status": "error","message": "An unexpected error occurred","details": {"message": str(e)}  }), 500



@patient_bp.route('/', methods=['POST'])
def create_patient():
    """
    Crea un nuevo paciente.
    - **Metodo**: POST
    - **Parametros**: Datos del paciente
    - **Respuesta exitosa**: Codigo 201, paciente creado
    - **Errores posibles**: Codigo 400, error de validación. Codigo 400, paciente ya existe. Codigo 500, error inesperado
    """

    try:
        # Obtener los datos de la solicitud POST
        data = request.get_json()

        patient_data = patient_schema.load(data)

        # Creaa un nuevo paciente usando el servicio
        patient_service = PatientService(db)
        patient = patient_service.create_patient(
            patient_data['name'], patient_data['last_name'],patient_data['email'], patient_data['dni'] , patient_data.get('birthdate'), patient_data.get('phone_number')
        )

        return jsonify({'status': 'success','data': patient_schema.dump(patient)}), 201

    except ValidationError as err:
        # Si los datos no son válidos, Marshmallow lanzará un ValidationError
        return jsonify({"status": "error","message": "Validation failed","details": err.messages }), 400
    except AlreadyExistsError as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)} }), 400
    except Exception as e:
        # Capturar cualquier otro tipo de error y devolverlo
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)} }), 500





@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """
    Obtiene un paciente por ID.
    - **Metodo**: GET
    - **Parametros**: ID del paciente a buscar
    - **Respuesta exitosa**: Codigo 200, paciente encontrado
    - **Errores posibles**: Codigo 404, paciente no encontrado. Codigo 500, error inesperado
    """
    # Se crea el servicio para obtener la info correspondiente
    patient_service = PatientService(db)
    try:
        patient = patient_service.get_patient_by_id(patient_id)
        return jsonify({'status': 'success','data': patient_schema.dump(patient)}), 201
    except NotFoundError as e:
        return jsonify({"status": "error","message": "No se pudo encontrar un paciente con ese ID","details": {"message": str(e)}  }), 404
    except Exception as e:  
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 500  





@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """
    Actualiza los datos de un paciente.
    - **Metodo**: PUT
    - **Parametros**: ID del paciente y datos a actualizar
    - **Respuesta exitosa**: Codigo 200, paciente actualizado
    - **Errores posibles**: Codigo 400, error de validación. Codigo 404, paciente no encontrado. Codigo 500, error inesperado
    """
    # Se inicia el servicio para obtener la info correspondiente
    patient_service = PatientService(db)
    try:
        data = request.get_json()
        # Aqui se realiza la validacion de los datos
        patient_data = patient_schema.load(data, partial=True)
        patient = patient_service.update_patient(patient_id, patient_data)
        return jsonify({'status': 'success','data': patient_schema.dump(patient)}), 200
    
    except ValidationError as err:
        # Si los datos no son válidos, Marshmallow lanzará un ValidationError
        return jsonify({"status": "error","message": "Validation failed","details": err.messages }), 400
    except (AlreadyExistsError,NotFoundError) as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 400
    except Exception as e:  
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 500  





@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """
    Elimina un paciente por ID.
    - **Metodo**: DELETE
    - **Parametros**: ID del paciente a eliminar
    - **Respuesta exitosa**: Codigo 200, paciente eliminado
    - **Errores posibles**: Codigo 404, paciente no encontrado. Codigo 500, error inesperado
    """
    patient_service = PatientService(db)
    try:
        patient = patient_service.delete_patient(patient_id)
        return jsonify({'status': 'success','data': patient_schema.dump(patient)}), 200
    
    except NotFoundError as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 404
    except Exception as e:  
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 500  

