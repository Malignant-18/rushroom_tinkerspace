# init
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/rushroom'
    db.init_app(app)
#---------------------------------------------------------------------------------------------
        # Initialize the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"  # Redirect to auth.login if not logged in
    login_manager.init_app(app)  # Attach it to the app

    from .models import User, Post, Booking

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app  # Return the app instance

def create_database(app):
    with app.app_context():
        db.create_all()  # Create all tables
        print("Created database tables if they did not exist!")
