
from flask import Flask, request, jsonify
from flask import Blueprint
from ..services.patientService import PatientService
from sqlalchemy.exc import IntegrityError
from .. import db
from marshmallow import ValidationError
from ..schemas.patientSchema import PatientSchema
from ..schemas.patientSchema import patient_schema , patients_schema
from ..exceptions.servicesExceptions import PatientAlreadyExistsError,NotFoundError

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/', methods=['GET'])
def get_all_patients():
    patient_service = PatientService(db)
    # Usar el servicio para obtener todos los pacientes
    try:
        patients = patient_service.get_all_patients()
        
        # Convertir la lista de pacientes en una lista de diccionarios para JSON
        patients_list = patients_schema.dump(patients)
        
        return jsonify({
            'status':'success',
            'data': patients_list
            }),200
    except Exception as e:
        return jsonify({
            "status": "error",
            "data": None,
            "errors": {"general": str(e)}
        }), 400

@patient_bp.route('/', methods=['POST'])
def create_patient():
    try:
        # Obtener los datos de la solicitud POST
        data = request.get_json()

        patient_data = patient_schema.load(data)


        # Crear un nuevo paciente usando el servicio
        patient_service = PatientService(db)
        patient = patient_service.create_patient(
            patient_data['name'], patient_data['last_name'], patient_data['email'], patient_data['birthdate'], patient_data['phone_number']
        )

        return jsonify({
            'status': 'success',
            'data': patient_schema.dump(patient)
        }), 201

    except ValidationError as err:
        # Si los datos no son válidos, Marshmallow lanzará un ValidationError
        return jsonify({
            "status": "error",
            "data": None,
            "errors": {
                "validation": err.messages
            }
        }), 400

    except IntegrityError as e:
        return jsonify({
            "status": "error",
            "data": None,
            "errors": {"general": str(e)}
        }), 400

    except Exception as e:
        # Capturar cualquier otro tipo de error y devolverlo
        return jsonify({
            'status': 'error',
            'data': None,
            "errors": {"general": str(e)}
        }), 400




@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """ Obtener un paciente por ID """
    patient_service = PatientService(db)
    try:
        patient = patient_service.get_patient_by_id(patient_id)
        return jsonify({
            'status': 'success',
            'data': patient_schema.dump(patient)
        }), 201
    except NotFoundError as e:
        return jsonify({
            'status': 'error',
            'data': None,
            "errors": {"general": str(e)}
        }), 400


@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """ Actualizar un paciente """
    patient_service = PatientService(db)
    try:
        data = request.get_json()
        patient_data = patient_schema.load(data, partial=True)  # Permitir actualización parcial
        patient = patient_service.update_patient(patient_id, patient_data)
        return jsonify({
            'status': 'success',
            'data': patient_schema.dump(patient)
        }), 201
    except ValidationError as err:
        return jsonify({
            "status": "error",
            "data": None,
            "errors": {
                "validation": err.messages
            }
        }), 400
    except PatientAlreadyExistsError as e:
        return jsonify({
            'status': 'error',
            'data': None,
            "errors": {"general": str(e)}
        }), 400
    except NotFoundError as e:
        return jsonify({
            'status': 'error',
            'data': None,
            "errors": {"general": str(e)}
        }), 404

@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """ Eliminar un paciente """
    patient_service = PatientService(db)
    try:
        patient = patient_service.delete_patient(patient_id)
        return jsonify({
            'status': 'success',
            'data': patient_schema.dump(patient)
        }), 200
    except NotFoundError as e:
        return jsonify({
            'status': 'error',
            'data': None,
            "errors": {"general": str(e)}
        }), 404

