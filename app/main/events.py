from app.main.routes import bot
import time
import json
from flask import request

from .. import socketio, conferenceName, botName, avatarName

from ..interaction import engine
from ..interaction.constants import *
from app import interaction, operatorName


avatar_client = None
bot_client    = None

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

    if bot_client != None and client != bot_client:
        print("Disconnect old client")
        socketio.emit('disconnect_now', {'id' : bot_client }, namespace='/bot')
        

    bot_client = client      
    message = {
        'displayName'        : botName,
        'conference'         : conferenceName,
        'default-engine-config': DEFAULT_ENGINE_CONFIG,
        'types'  :  INTERACTION_TYPES
    }

    print('Starting Conference "{}"'.format(message))
    socketio.emit('start_conference', json.dumps(message), namespace='/bot', json=True)


@socketio.on('disconnect', namespace='/bot')
def handle_disconnect():
    global bot_client

    print('Client disconnected')
    client = request.sid
    if client == bot_client:
        bot_client = None

@socketio.on('received_message', namespace='/bot')
def received_message(message):
    global bot_client
    id = message['uid']
    text = message['text']
    client = request.sid
    if client == bot_client:
        print('received_message', client, id, text)
        engine.feedEnginePublic(id, text)

@socketio.on('received_private_message', namespace='/bot')
def received_private_message(message):
    global bot_client
    id   = message['uid']
    text = message['text']
    client = request.sid
    if client == bot_client:
        print('received_private_message', client, id, text)
        engine.feedEnginePrivate(id, text)



# Avatar
@socketio.on('connect', namespace='/avatar')
def handle_avatar_connect():
    global avatar_client

    print('Client connected')

    client = request.sid

    if avatar_client != None and client != avatar_client:
        print("Disconnect old client")
        socketio.emit('disconnect_now', {'id' : avatar_client }, namespace='/avatar')
        

    avatar_client = client      
    message = {
        'displayName'        : avatarName,
        'conference'         : conferenceName,
        'operatorName'       : operatorName,
        'default-engine-config': DEFAULT_ENGINE_CONFIG,
        'types'  :  INTERACTION_TYPES
    }

    print('Starting Conference "{}"'.format(message))
    socketio.emit('start_conference', json.dumps(message), namespace='/avatar', json=True)


@socketio.on('disconnect', namespace='/avatar')
def handle_disconnect():
    global avatar_client

    print('Client disconnected')
    client = request.sid
    if client == avatar_client:
        avatar_client = None

#Engine
@socketio.on('connect', namespace='/engine')
def handle_engine_connect():
    pass

@socketio.on('disconnect', namespace='/engine')
def handle_engine_disconnect():
    pass


@socketio.on('received_command', namespace='/engine')
def received_command(command):
    engine.feedEnginePublic(None, command)

@socketio.on('set_interaction_engine', namespace='/engine')
def set_interaction_engine(config):
    print('set_interaction_engine', config)
    engine.setup(config, send_message, send_private_message)

    config["commands"] = list(engine.get_commands())
    print("Here!")
    socketio.emit('interaction_engine_changed', config, namespace="/bot")

@socketio.on('set_interaction_engine_ids', namespace='/engine')
def set_interaction_engine_ids(config):
    print('set_interaction_engines_ids', config)
    engine.set_ids(config)
    socketio.emit('interaction_engine_changed', config, namespace="/bot")