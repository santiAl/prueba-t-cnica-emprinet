from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..services.authService import AuthService
from ..exceptions.servicesExceptions import NotFoundError
from ..schemas.userSchema import UserSchema
from .. import db
from ..utils.security import Security

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['POST'])
def login_user():
    """
    Autentica a un usuario con su username y contraseña.
    - **Metodo**: POST
    - **Parametros**: Nombre de usuario y contraseña (en el body de la solicitud)
    - **Respuesta exitosa**: Codigo 200, token JWT generado
    - **Errores posibles**: Codigo 400, error de validacion de los datos de entrada. Codigo 404, el usuario no fue encontrado . Codigo 500, error inesperado en el servidor.
    """

    try:
        data = request.get_json() 
        schema = UserSchema()
        user_data = schema.load(data)  
        
        # Se crea una instancia del servicio de autenticacion para autenticar a usuario
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(user_data['username'], user_data['password_hash'])

        if(user != None):
            # Genera el JWT. Si las credenciales son correctas
            encoded_token = Security.generate_token(user)
            return jsonify({'status': 'success','data': encoded_token}), 200
        else:
            return jsonify({"status": "failure","message": "Credenciales invalidas"}), 400

    except ValidationError as err:
        # Si los datos no son válidos, Marshmallow lanzara un ValidationError
        return jsonify({"status": "error","message": "Validation failed","details": err.messages }), 400
    except NotFoundError as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 404
    except Exception as e:
        return jsonify({"status": "error","message": "Ha ocurrido un error inesperado","details": {"message": str(e)}  }), 500 
