from flask import Flask, g
from flask_socketio import SocketIO
from flask import render_template
import atexit

socketio = SocketIO()

def create_app(args):
    app = Flask( __name__ )
    app.debug = args.debug

    socketio.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
