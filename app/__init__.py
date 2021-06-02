from flask import Flask, g
from flask_socketio import SocketIO
from flask import render_template
import atexit

socketio = SocketIO()

botName        = ""

def create_app(args):
    global conferenceName, botName
    
    conferenceName = args.uuid
    botName        = args.bname


    app = Flask( __name__ )
    app.debug = args.debug

    socketio.init_app(app)

    # # # Ping
    # if(args.ping):
    #     scheduler = BackgroundScheduler()
    #     scheduler.add_job(func=send_date_time, trigger="interval", seconds=15)
    #     scheduler.start()
    #     atexit.register(lambda: scheduler.shutdown())


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
