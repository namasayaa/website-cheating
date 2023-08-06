from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from os import path
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os


app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dontrepthis@gmail.com'
app.config['MAIL_PASSWORD'] = 'dgiocdhbknjmbotf'
mail=Mail(app)

# DB_NAME = "Tester.db"

def create_app():
    app.config['SECRET_KEY'] = 'INIAdalahSecretKeyKu'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Namasayaari25!@localhost/DB_cheat'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .App import App

    app.register_blueprint(views, name="view", url_prefix='/')
    app.register_blueprint(App, name="app", url_prefix="/" )
    app.register_blueprint(auth, name="auth", url_prefix='/')

    from .model import Using, History

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'view.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Using.query.get(int(id))
    
    return app

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database')