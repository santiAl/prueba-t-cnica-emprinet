from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..schemas.userSchema import user_schema , users_schema
from ..services.userService import UserService
from ..exceptions.servicesExceptions import AlreadyExistsError
from .. import db

user_bp = Blueprint('user', __name__)



@user_bp.route('/', methods=['GET'])
def get_all_users():
    """ Endpoint para obtener todos los usuarios """
    user_service = UserService(db)
    try:
        users = user_service.get_all_users()
        user_list = users_schema.dump(users)
        return jsonify({
            'status':'success',
            'data': user_list
            }),200
    except Exception as e:
        return jsonify({
                "status": "error",
                "message": "An unexpected error occurred",
                "details": {"message": str(e)}  
            }), 500



@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()
        user_data = user_schema.load(data)
        user_service = UserService(db)
        user = user_service.create_user(user_data['username'], user_data['password_hash'])
        # Devolver respuesta
        return jsonify({
            'status': 'success',
            'data': user_schema.dump(user)
        }), 201

    except ValidationError as err:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "details": err.messages  # Los detalles del error de Marshmallow
        }), 400
    except AlreadyExistsError as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  # Detalle general como objeto
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Ha ocurrido un error inesperado",
            "details": {"message": str(e)}  # Detalle general como objeto
        }), 500
