from decouple import config
import datetime
import pytz
import jwt


class Security():
    """
    Clase encargada de la gestion de tokens JWT para la proteccion de rutas.
    Atributos:
    - **tz**: Zona horaria. Buenos Aires (Argentina).
    - **secret**: Secret Key para la firma de los tokens, obtenida de .env o del docker-compose.yml.
    Métodos:
    - **generate_token(authenticated_user)**: Genera un token JWT para un usuario autenticado.
    - **verify_token(headers)**: Verifica la validez de un token JWT enviado en los headers de la solicitud.
    """


    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    secret = config('JWT_KEY')



    @classmethod
    def generate_token(self,authenticated_user):
        """
        Genera un token JWT para un usuario autenticado.
        - **Parametros**: 
            - authenticated_user: Objeto que representa al usuario autenticado. Debe tener el atributo username.
        - **Retorno**: Token JWT codificado con el algoritmo 'HS256', con un tiempo de expiración de 10 minutos.
        """

        payload={
            'iat': datetime.datetime.now(tz=self.tz),
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=10),   # Aca se puede cambiar el tiempo de expiracion del toquen
            'username': authenticated_user.username
        }
        return jwt.encode(payload,self.secret,algorithm="HS256")
    



    @classmethod
    def verify_token(self,headers):
        """
        Verifica la validez de un token JWT proporcionado en los headers de la solicitud.
        - **Parametros**:
            - headers: Diccionario de los encabezados HTTP de la solicitud, que debe incluir un campo 'Authorization'.
        - **Retorno**: 
            - **True**: Si el token es valido y no expiro.
            - **False**: Si el token es invalido, expiro o no esta presente en los headers.
        - **Errores posibles**: 
            - **ExpiredSignatureError**: El token expiro.
            - **DecodeError**: El token no pudo ser decodificado correctamente.
        """

        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            try:
                # Intenta decodificar el token
                payload = jwt.decode(encoded_token,self.secret,algorithms=["HS256"])
                return True
            except(jwt.ExpiredSignatureError,jwt.DecodeError):
                return False


        return False