# services/users/project/__init__.py

import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt # new
from flask_mail import Mail
from flask_bootstrap import Bootstrap

# instantiate the db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
bootstrap = Bootstrap()

def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)
    from project.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')


    if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='ingme Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
