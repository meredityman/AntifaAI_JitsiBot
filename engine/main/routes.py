from code import interact
import os
from flask import render_template, jsonify, request, send_from_directory
from . import main
from .. import engine
from pathlib import Path
import json

# MAP_DATA_PATH  = "app/data/incidents"

@main.route('/')
def index():
    return render_template('index.html')

# @main.route('/cue', methods=['POST'])
# def cue():
#     if requests.method == 'POST':
#         return send_cue('name', data)

@main.route('/engine-start/<interface_type>', methods=['POST'])
def engine_start(interface_type):
    if request.method == 'POST':
        ret = engine.start(interface_type, **request.json)
        return ret, 200
    else:
        return { 'success' : False, 'error' : "Not a POST request!"}, 404

@main.route('/engine-message/<interface_id>', methods=['POST'])
def engine_message(interface_id):
    if request.method == 'POST':
        ret = engine.message(interface_id, request.json)
        return ret, 200
    else:
        return { 'success' : False, 'error' : "Not a POST request!"}, 404

@main.route('/engine-stop/<interface_id>', methods=['POST'])
def engine_stop(interface_id):
    if request.method == 'POST':
        ret = engine.stop(interface_id)
        return ret, 200
    else:
        return { 'success' : False, 'error' : "Not a POST request!"}, 404

@main.route('/interface-types', methods=['GET'])
def interface_types():
    if request.method == 'GET':
        interface_types = engine.get_types()
        return { 'success' : True, 'interface-types' : interface_types}, 200
    else:
        return { 'success' : False, 'error' : "Not a GET request!"}, 404

@main.route('/interfaces', methods=['GET'])
def interfaces():
    if request.method == 'GET':
        interfaces = engine.get_interfaces()
        return { 'success' : True, 'interfaces' : interfaces}, 200
    else:
        return { 'success' : False, 'error' : "Not a GET request!"}, 404



@main.route('/map.jpg')
def get_route():
    return send_from_directory('static/var', 'map_latest.jpg')

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