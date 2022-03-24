import os
from flask import render_template, send_from_directory
from . import main
from pathlib import Path
import json
import requests

from bot import conferenceName, operatorName

MAP_DATA_PATH  = "app/data/incidents"


def getLink(link):
    return 

@main.route('/')
def index():

    params={
        "userInfo.displayName" : operatorName,
        "config.startWithAudioMuted" : "true",
        "config.disableAP" : "false",
        "config.disableAEC": "false",
        "config.disableNS" : "true",
        "config.disableAGC": "true",
        "config.disableHPF": "true",
        "config.stereo"    : "true",
        "resolution"       : "1280"
    }
    params = [ f'{k}="{v}"' for k, v in params.items()]
    params = "&".join(params)

    audienceUrl      = f"http://show.cobratheatercobra.com/?meeting={conferenceName}"
    scribeUrl        = f"display?meeting={conferenceName}"
    audienceUrlLocal = f"file://{Path('./viewer').absolute()}/index.html/?meeting={conferenceName}"
    operator_link    = f"https://meet.cobratheatercobra.com/{conferenceName}#{params}"
    link             = f"https://meet.cobratheatercobra.com/{conferenceName}"

    links = [
        {'href' : "bot"           , 'text' : '🤖 Bot'             },
        {'href' : "avatar"        , 'text' : '📹 Avatar'          },
        {'href' : scribeUrl       , 'text' : '🖥️ Display Chat'    },
        {'href' : audienceUrl     , 'text' : '🧝🏻‍♀️ Audience'        },
        {'href' : audienceUrlLocal, 'text' : '🧝🏻‍♀️ Audience (local)'}, 
        {'href' : link            , 'text' : '🍿 Remote Audience' }, 
        {'href' : operator_link   , 'text' : '🎬 Operator'        },
    ]


    root = "http://127.0.0.1:5001"

    embed = [
        {'href' : f"{root}/telegram.html" , 'text' : 'Telegram', 'w' : 720 , 'h' : 720     },
        {'href' : f"{root}/twitter.html"  , 'text' : 'Twitter' , 'w' : 720 , 'h' : 720     },
        {'href' : f"{root}/map.jpg"       , 'text' : 'Map'     , 'w' : 1280, 'h' : 720    },
        {'href' : f"./qrcode"       , 'text' : 'Map'  , 'w' : 450 , 'h' : 450     },
    ]

    return render_template('index.html', links = links, embed=embed)

# @main.route('/cue', methods=['POST'])
# def cue():a
#     if requests.method == 'POST':
#         return send_cue('name', data)


@main.route('/bot')
def bot():
    return render_template('bot.html')

@main.route('/display')
def display():
    return render_template('display.html')

@main.route('/avatar')
def avatar():
    return render_template('avatar.html')

@main.route('/resources/<path:name>')
def get_asset(name):
    return send_from_directory('../resources', name)

@main.route('/meetings')
def get_meetings():
    return render_template('meetings.html')


@main.route('/qrcode')
def get_qr():
    return send_from_directory('static/var', 'qr.png')

# @main.route('/map.jpg')
# def get_route():
#     return send_from_directory('static/var', 'map_latest.jpg')


# @main.route('/telegram.html')
# def get_telegram():
#     return send_from_directory('static/var', 'TelegramRatingScatter.html')


# @main.route('/twitter.html')
# def get_twitter():
#     return send_from_directory('static/var', 'NaziTwitterBubble.html')

# @main.route('/map-data.json')
# def get_map_data():
#     data = {}
#     data['type'] = "FeatureCollection"
#     data['features'] = []
#     data["crs"] = {
#         "type": "name",
#         "properties": {
#             "name": ""
#         }
#     }

#     for path in Path(MAP_DATA_PATH).glob('*.json'):
#         with open(path, 'r') as p:
#             properties = json.load(p)

#         if 'coordinates' in properties:
#             coordinates = properties.pop('coordinates')

#             data['features'].append(
#                 {
#                     "type": "Feature",
#                     "properties": properties,
#                     "geometry": {
#                         "type": "Point",
#                         "coordinates": coordinates
#                     }
#                 }
#             )

#     return data