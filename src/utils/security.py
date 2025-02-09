from decouple import config
import datetime
import pytz
import jwt


class Security():

    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    secret = config('JWT_KEY')

    @classmethod
    def generate_token(self,authenticated_user):
        payload={
            'iat': datetime.datetime.now(tz=self.tz),
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=10),
            'username': authenticated_user.username
        }
        return jwt.encode(payload,self.secret,algorithm="HS256")
    
    @classmethod
    def verify_token(self,headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            try:
                payload = jwt.decode(encoded_token,self.secret,algorithms=["HS256"])
                return True
            except(jwt.ExpiredSignatureError,jwt.DecodeError):
                return False


        return False