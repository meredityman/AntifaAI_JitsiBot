from app.main.routes import bot
import time
import json
from flask import request

from .. import socketio, conferenceName, botName

from ..interaction import engine
from ..interaction.constants import *
from app import interaction


avatar_client = None
bot_client   = None

def send_message(message):
    socketio.emit('send_message', message, namespace='/bot')
    print('sending message "{}"'.format(message))

def send_private_message(id, message):
    print(f'sending private message "{message}" to user {id}".')
    socketio.emit('send_private_message', { 'id' : id, 'message' : message}, namespace='/bot')


def send_date_time():
    date = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    send_message(date)


# Bot
@socketio.on('connect', namespace='/bot')
def handle_bot_connect():
    global bot_client

    print('Client connected')

    client = request.sid
    if client != bot_client:

        bot_client = client

        message = {
            'displayName'        : botName,
            'conference'         : conferenceName,
            'default-engine-config': DEFAULT_ENGINE_CONFIG,
            'interaction-types'  : {
                'public'  : INTERACTION_TYPES_PUBLIC,
                'private' : INTERACTION_TYPES_PRIVATE
            }
        }
        print('Starting Conference "{}"'.format(message))
        socketio.emit('start_conference', json.dumps(message), namespace='/bot', json=True)



@socketio.on('disconnect', namespace='/bot')
def handle_disconnect():
    print('Client disconnected')
    bot_client = None

@socketio.on('received_message', namespace='/bot')
def received_message(message):
    id = message['id']
    text = message['text']
    client = request.sid
    print('received_message', client, id, text)

    engine.feedEnginePublic(client, id, text)

@socketio.on('received_private_message', namespace='/bot')
def received_private_message(message):
    id   = message['id']
    text = message['text']
    ids  = message['ids']
    client = request.sid
    print('received_private_message', client, id, text)

    engine.feedEnginePrivate(client, id, text)


#Engine
@socketio.on('connect', namespace='/engine')
def handle_engine_connect():
    pass

@socketio.on('disconnect', namespace='/engine')
def handle_engine_disconnect():
    pass
@socketio.on('set_interaction_engine', namespace='/engine')
def set_interaction_engine(config):
    print('set_interaction_engine', config)
    engine.setup(config, send_message, send_private_message)
    