import os
from flask import render_template, send_from_directory
from . import main
from pathlib import Path
import json

MAP_DATA_PATH  = "app/data/incidents"


def getLink(link):
    return 

@main.route('/')
def index():
    links = [
        {'href' : "bot"     , 'text' : 'Bot'   },
        {'href' : "avatar"  , 'text' : 'Avatar'},
        {'href' : "meetings", 'text' : 'MeetingLinks'}
    ]
    return render_template('index.html', links = links)

@main.route('/cue', methods=['POST'])
def cue():
    if request.method == 'POST':
        return send_cue('name', data)


@main.route('/bot')
def bot():
    return render_template('bot.html')

@main.route('/avatar')
def avatar():
    return render_template('avatar.html')

@main.route('/assets/<path:name>')
def get_asset(name):
    return send_from_directory('static', name)

@main.route('/meetings')
def get_meetings():
    return render_template('meetings.html')

@main.route('/map.jpg')
def get_route():
    return send_from_directory('static/var', 'map_latest.jpg')


@main.route('/telegram.html')
def get_telegram():
    return send_from_directory('static/var', 'TelegramRatingScatter.html')


@main.route('/twitter.html')
def get_twitter():
    return send_from_direct
    
    ory('static/var', '')

@main.route('/map-data.json')
def get_map_data():
    data = {}
    data['type'] = "FeatureCollection"
    data['features'] = []
    data["crs"] = {
        "type": "name",
        "properties": {
            "name": ""
        }
    }

    for path in Path(MAP_DATA_PATH).glob('*.json'):
        with open(path, 'r') as p:
            properties = json.load(p)

        if 'coordinates' in properties:
            coordinates = properties.pop('coordinates')

            data['features'].append(
                {
                    "type": "Feature",
                    "properties": properties,
                    "geometry": {
                        "type": "Point",
                        "coordinates": coordinates
                    }
                }
            )

    return data