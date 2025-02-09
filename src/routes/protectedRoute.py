from flask import Blueprint,request,jsonify
from ..utils.security import Security

# Crear el Blueprint
protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/')
def home():
    has_access= Security.verify_token(request.headers)
    if(has_access):
        return "Gracias por probar esta funcionalidad!! Me encanto poder desarrollarla!!"
    else:
        return jsonify({'message': 'Unauthoraized',}), 401