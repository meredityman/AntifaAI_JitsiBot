import time
import json
from flask import request

from .. import socketio, conferenceName, botName

from ..interaction import engine
from ..interaction.constants import *
from app import interaction


interactionEngines = {}
clients = []

def start_conference(message):
    for client_id in clients:
        socketio.emit('start_conference', json.dumps(message), json=True, room=client_id)
        print('Starting Conference "{}" to client "{}".'.format(message, client_id))

def send_message(message):
    for client_id in clients:
        socketio.emit('send_message', message, room=client_id)
        print('sending message "{}" to client "{}".'.format(message, client_id))


def send_private_message(id, message):
    for client_id in clients:
        print(f'sending private message "{message}" to user {id} on client "{client_id}".')
        socketio.emit('send_private_message', { 'id' : id, 'message' : message}, room=client_id)



def send_date_time():
    date = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    send_message(date)


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)

    start_conference({
        'displayName'        : botName,
        'conference'         : conferenceName,
        'default-engine-config': DEFAULT_ENGINE_CONFIG,
        'interaction-types'  : {
            'public' : INTERACTION_TYPES_PUBLIC,
            'private' : INTERACTION_TYPES_PRIVATE
        }
    })

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)

@socketio.on('received_private_message')
def received_private_message(message):
    id = message['id']
    text = message['text']
    client = request.sid
    print('received_private_message', client, id, text)

    response = engine.getPrivateResponse(client, id, text)
    if response:
        send_private_message(id, response)

@socketio.on('received_message')
def received_message(message):
    id = message['id']
    text = message['text']
    client = request.sid
    print('received_message', client, id, text)

    response = engine.getPublicResponse(client, id, text)
    if response:
        send_message(response)


@socketio.on('set_interaction_engine')
def set_interaction_engine(config):
    print('set_interaction_engine', config)
    engine.setup( config )
    