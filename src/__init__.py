from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



# Inicialización de SQLAlchemy
db = SQLAlchemy()

# Inicialización de Flask-Migrate
migrate = Migrate()

app = Flask(__name__)

def init_app(config):
    # Configuracion
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from src.models import user , appointment , patient  

    from .routes import protectedRoute , patientRoutes, appointmentRoutes , userRoutes , authRoutes
    # Blueprints con los prefijos para las rutas
    app.register_blueprint(protectedRoute.protected_bp,url_prefix='/')
    app.register_blueprint(patientRoutes.patient_bp,url_prefix='/patients')
    app.register_blueprint(appointmentRoutes.appointment_bp,url_prefix='/appointments')
    app.register_blueprint(userRoutes.user_bp,url_prefix='/user')
    app.register_blueprint(authRoutes.auth_bp,url_prefix='/auth')

    return app