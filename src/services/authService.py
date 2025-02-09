from werkzeug.security import check_password_hash
from ..models.user import User
from ..exceptions.servicesExceptions import NotFoundError

class AuthService:

    def __init__(self, db):
        self.db = db

    def authenticate_user(self, username, password):
        """
        Autentica un usuario a partir de su nombre de usuario y contraseña.
        - **Parametros**:
            - username (str): Nombre de usuario.
            - password (str): Contraseña en texto plano.
        - **Retorna**:
            - Objeto User si las credenciales son validas.
            - None si la autenticacion falla.
        - **Errores posibles**:
            - **NotFoundError**: Si el username no existe en la base de datos.
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            raise NotFoundError(f"No se encontró el usuario con Username {username}")

        if user and check_password_hash(user.password_hash, password):
            return user
        else:
            return None
