import json
import numpy as np
from .interaction import MultiGeneratorEngine
from ..horror import  draw_map
from validator_collection import validators
from pathlib import PurePath
import time
import json
import googlemaps
from pyproj import Transformer

#from ..horror import send_data
        
OUTPUT_PATH  = "app/data/incidents"
API_KEY = "AIzaSyAQZQllaEBGRi42pB0YU7nX9hsf_wArSJI"

questions = [
    {
        'text'           : 'What year did the incident happen?',
        'hint'           : 'Enter the years as a number, e.g. 1997',
        'compulsory'     : True,
        'field'          : 'year',
        'validator'      : validators.integer,
        'validator-args' : { 'minimum' : 1900, 'maximum' : 2021 }
    },
    {
        'text'           : 'What month did the incident happen?',
        'hint'           : 'Enter the month as a number, e.g. "3" for March',
        'compulsory'     : True,
        'field'          : 'month',
        'validator'      : validators.integer,
        'validator-args' : { 'minimum' : 1, 'maximum' : 12 }
    },
    {
        'text'           : 'What day did the incident happen?',
        'hint'           : 'Enter the day',
        'compulsory'     : False,
        'field'          : 'day',
        'validator'      : validators.integer,
        'validator-args' : { 'minimum' : 0, 'maximum' : 31 }
    },
    {
        'text'           : 'Where did the incident happen?',
        'hint'           : 'Write the address as precisely as you can',
        'compulsory'     : True,
        'field'          : 'location',
        'validator'      : validators.string,
        'validator-args' : { }
    },
    {
        'text'           : 'What happened?',
        'hint'           : 'Write between 50-150 words',
        'compulsory'     : True,
        'field'          : 'description',
        'validator'      : validators.string,
        'validator-args' : {  }
    }
]

class Incidents(MultiGeneratorEngine):

    def _setup(self):
        self.gmaps = googlemaps.Client(key=API_KEY )

    def _reset(self):
        self.responses = {}
        self.iterateAllGenerators()

    def _generator(self):
        for question in questions:
            self.sendMessage(self.id, question['text'])
            self.sendMessage(self.id, question['hint'])
            yield

            validator = question['validator']
            args = question['validator-args']

            while True:
                try:
                    response = validator(self.text, **args, allow_empty = (not question['compulsory']))
                    break
                except (ValueError, TypeError) as e:
                    self.sendMessage(self.id, str(e))
                    self.sendMessage(self.id, question['hint'])
                    yield

            if self.id not in self.responses:
                self.responses[self.id] = {}

            self.responses[self.id][question['field']] = response
        
        self.sendMessage(self.id, "Thank you we adding your response to out database.")
        self.saveEntry(self.id, self.responses[self.id])

    def saveEntry(self, id, entry):

        location = entry.pop('location')

        geocode_result = self.gmaps.geocode(location)

        print(geocode_result)

        if geocode_result:
            address_components = geocode_result[0]['address_components']

            def get_feature(name):
                for feat in address_components:
                    if name in feat['types']:
                        return feat['long_name']
                return ""

            coords = geocode_result[0]['geometry']['location']

            entry['city']        = get_feature("locality")
            entry['postal_code'] = get_feature("postal_code")

            entry['address']     = geocode_result[0]['formatted_address']


            # inProj  = Proj("EPSG:3857")
            # outProj = Proj('PROJCS["unnamed",GEOGCS["Bessel 1841",DATUM["unknown",SPHEROID["bessel",6377397.155,299.1528128]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",3],PARAMETER["scale_factor",1],PARAMETER["false_easting",1500000],PARAMETER["false_northing",0],UNIT["Meter",1]]')

            entry['latitude']    = coords['lat']
            entry['longitude']   = coords['lng']


            transformer = Transformer.from_crs('epsg:3857', 'epsg:31491') 
            entry['coordinates'] = transform.itransform([(coords['lng'], coords['lat'])])[0]


        filename = f"{id}-{time.strftime('%Y%m%d-%H%M%S')}.json"
        path = PurePath(OUTPUT_PATH, filename )
        json.dump(entry, open(path, 'w'))
        
            
            