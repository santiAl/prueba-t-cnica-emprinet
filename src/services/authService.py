from werkzeug.security import check_password_hash
from ..models.user import User
from ..exceptions.servicesExceptions import NotFoundError

class AuthService:

    def __init__(self, db):
        self.db = db

    def authenticate_user(self, email, password):
        """ Autentica un usuario a partir de su email y contraseña """
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            return user
        else:
            return None
