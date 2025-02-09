class PatientAlreadyExistsError(Exception):
    def __init__(self, message="Ya existe un paciente con ese correo electrónico"):
        self.message = message
        super().__init__(self.message)

class NotFoundError(Exception):
    pass