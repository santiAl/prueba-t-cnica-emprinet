from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..schemas.userSchema import user_schema , users_schema
from ..services.userService import UserService
from ..exceptions.servicesExceptions import AlreadyExistsError
from .. import db

user_bp = Blueprint('user', __name__)



@user_bp.route('/', methods=['GET'])
def get_all_users():
    """
    Obtiene la lista de todos los usuarios.
    - **Metodo**: GET
    - **Parametros**: Ninguno
    - **Respuesta exitosa**: Codigo 200, devuelve un JSON con la lista de usuarios.
    - **Errores posibles**: Codigo 500: error inesperado.
    """

    user_service = UserService(db)
    try:
        users = user_service.get_all_users()
        user_list = users_schema.dump(users)
        return jsonify({'status':'success','data': user_list}),200
    except Exception as e:
        return jsonify({"status": "error","message": "An unexpected error occurred","details": {"message": str(e)}  }), 500






@user_bp.route('/', methods=['POST'])
def create_user():
    """
    Crea un nuevo usuario.
    - **Metodo**: POST
    - **Parametros**: Datos del usuario en formato JSON (username y password_hash).
    - **Respuesta exitosa**: Codigo 201, devuelve los datos del usuario creado.
    - **Errores posibles**: Codigo 400, error de validacion o usuario ya existente. Codigo 500, error inesperado.
    """

    try:
        data = request.get_json()
        user_data = user_schema.load(data)
        # Crea una instancia del servicio para crear el usuario.
        user_service = UserService(db)
        user = user_service.create_user(user_data['username'], user_data['password_hash'])
        return jsonify({'status': 'success','data': user_schema.dump(user)}), 201
    
    except ValidationError as err:
        return jsonify({"status": "error","message": "Validation failed","details": err.messages  }), 400
    except AlreadyExistsError as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 400
    except Exception as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)} }), 500
