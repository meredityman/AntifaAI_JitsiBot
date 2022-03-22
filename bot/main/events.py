from bot.main.routes import bot
import time
import json
from flask import request
import qrcode 

from .. import socketio, conferenceName, botName, avatarName, operatorName

avatar_client = None
bot_client    = None

# def send_message(message):
#     socketio.emit('send_message', message, namespace='/bot')
#     print('sending message "{}"'.format(message))

# def send_private_message(id, message):
#     print(f'sending private message "{message}" to user {id}".')
#     socketio.emit('send_private_message', { 'id' : id, 'message' : message}, namespace='/bot')


# def send_date_time():
#     date = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
#     send_message(date)


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
    }

    webRoot = "file:///media/hdrive/data/work/production/AntifAI-German-Horror-Show/Code/AntifaAI_JitsiBot/viewer"
    audienceUrl = f"{webRoot}/index.html?meeting={conferenceName}"
    img = qrcode.make(audienceUrl)
    img.save(f"bot/static/var/qr.png")

    print('Starting Conference "{}"'.format(message))
    socketio.emit('start_conference', json.dumps(message), namespace='/bot', json=True)


@socketio.on('disconnect', namespace='/bot')
def handle_disconnect():
    global bot_client

    print('Client disconnected')
    client = request.sid
    if client == bot_client:
        bot_client = None

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
