import os
from flask import render_template, send_from_directory
from . import main
from pathlib import Path
import json

MAP_DATA_PATH  = "app/data/incidents"



@main.route('/')
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