from werkzeug.security import generate_password_hash
from ..models.user import User
from ..exceptions.servicesExceptions import PatientAlreadyExistsError
from ..schemas.userSchema import users_schema

class UserService:
    
    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        """ Obtiene todos los usuarios """
        users = User.query.all()
        return users

    def create_user(self, username, email, password):
        """ Crea un nuevo usuario """
        # Verificar si ya existe el usuario con el mismo nombre o email
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            raise PatientAlreadyExistsError("El usuario o el correo electrónico ya están registrados.")
        
        # Crear un nuevo usuario
        user = User(username=username, email=email)
        user.password_hash = generate_password_hash(password)
        
        # Guardar en la base de datos
        self.db.session.add(user)
        self.db.session.commit()

        return user
