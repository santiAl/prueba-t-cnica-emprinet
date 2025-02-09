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
    try:
        data = request.get_json()

                
        schema = UserSchema()
        user_data = schema.load(data)  

        auth_service = AuthService(db)
        user = auth_service.authenticate_user(user_data['username'], user_data['password_hash'])

        if(user != None):
            encoded_token = Security.generate_token(user)
            return jsonify({"success": True, "token": encoded_token}), 200
        else:
            return jsonify({"success": False}), 400

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
