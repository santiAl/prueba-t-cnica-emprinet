from werkzeug.security import generate_password_hash
from ..models.user import User
from ..exceptions.servicesExceptions import AlreadyExistsError
from ..schemas.userSchema import users_schema

class UserService:
    
    def __init__(self, db):
        self.db = db


    def get_all_users(self):
        """
        Obtiene todos los usuarios registrados en la base de datos.
        - **Parametros**: Ninguno.
        - **Retorna**: Lista de Users.
        """
        users = User.query.all()
        return users




    def create_user(self, username, password):
        """
        Crea un nuevo usuario en la base de datos.
        - **Parametros**:
            - username (str): Nombre de usuario unico.
            - password (str): Contraseña en texto plano que sera hasheada.
        - **Retorna**: Objeto User.
        - **Errores posibles**:
            - **AlreadyExistsError**: Si el usuario ya existe en la db.
            - **Excepcion generica**: Si ocurre un error inesperado durante la transaccion.
        """

        # Verifica si ya existe el usuario con el mismo username
        existing_user = User.query.filter((User.username == username)).first()
        if existing_user:
            raise AlreadyExistsError("El usuario ya está registrado.")
        
        # Crea un nuevo usuario
        user = User(username=username)
        user.password_hash = generate_password_hash(password)
        
        try:
            # Guardar en la base de datos
            self.db.session.add(user)
            self.db.session.commit()
            return user
        except Exception as e:
            self.db.session.rollback()  # Deshacer cualquier cambio si ocurre un error
            raise e  # Relanzo la excepcion para que sea capturada por quien invoque el servicio.


