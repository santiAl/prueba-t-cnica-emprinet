from .. import db



class User(db.Model):
    """
    Modelo que representa a los usuarios del sistema.

    Este modelo se utiliza exclusivamente para la validación de JWT.

    Atributos:
        id (int): Identificador único del usuario.
        username (str): Nombre de usuario, único y no nulo.
        password_hash (str): Contraseña del usuario, almacenada de forma encriptada.
    """
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
