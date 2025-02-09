from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..schemas.userSchema import user_schema , users_schema
from ..services.userService import UserService
from ..exceptions.servicesExceptions import PatientAlreadyExistsError
from .. import db

user_bp = Blueprint('user', __name__)



@user_bp.route('/', methods=['GET'])
def get_all_users():
    """ Endpoint para obtener todos los usuarios """
    user_service = UserService(db)
    users = user_service.get_all_users()
    
    user_list = users_schema.dump(users)
        
    return jsonify({
        'status':'success',
        'data': user_list
        }),200
    



@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        # Obtener los datos de la solicitud
        data = request.get_json()
        
        user_data = user_schema.load(data)

        user_service = UserService(db)
        user = user_service.create_user(user_data['username'], user_data['email'], user_data['password_hash'])
        
        # Devolver respuesta
        return jsonify({"message": "Usuario creado exitosamente", "user": user_schema.dump(user)}), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except PatientAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
