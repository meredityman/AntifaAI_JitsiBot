from flask import Flask
from .interaction import Engine


engine = Engine()

def create_app(args):
    app = Flask( __name__ )
    app.debug = args.debug
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
