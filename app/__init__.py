from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routes import bp as main_bp, schedule_update

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()  # Create tables if they do not exist
        schedule_update(app)

    return app