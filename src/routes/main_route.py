# routes/main.py

from flask import Blueprint,request,jsonify
from ..utils.security import Security

# Crear el Blueprint
main_bp = Blueprint('main', __name__)

# Ruta principal
@main_bp.route('/')
def home():
    has_access= Security.verify_token(request.headers)
    if(has_access):
        return "¡Flask está funcionando con Blueprints!"
    else:
        return jsonify({'message': 'Unauthoraized',}), 401