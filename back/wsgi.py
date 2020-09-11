# from . import create_app
# app = create_app()


# #from . import routes  # Import routes

# if __name__ == "__main__":
#     app.run()

import os
from flask import Flask
from flask_mail import Mail

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.secret_key = "Blablabla"
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ['FLASK_GMAIL']
    app.config['MAIL_PASSWORD'] = os.environ['FLASK_GMAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    print(os.environ['FLASK_GMAIL'], flush=True)
    if os.environ['FLASK_GMAIL'] is not "":
        mail = Mail(app)
    app.app_context().push() 

    from .routes import routes
    app.register_blueprint(routes)
   
    return app