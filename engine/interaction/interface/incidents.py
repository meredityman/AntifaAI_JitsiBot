import json
import numpy as np
from validator_collection import validators
from pathlib import PurePath
import time
import json
import googlemaps
from pyproj import Transformer
from .utils.prompts import prompt_choice
from .interface import MultiUserGenerator

OUTPUT_PATH  = "engine/data/incidents"
API_KEY = "AIzaSyAQZQllaEBGRi42pB0YU7nX9hsf_wArSJI"


class Incidents(MultiUserGenerator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gmaps = googlemaps.Client(key=API_KEY )

    def start(self) -> list:

        self.responses = {}
        self.config = json.load(open("engine/config/incidents/incidents.json", "r"))
        self.questions = self.config["questions"]
        self.intro     = self.config["intro"]
        self.thankyou  = self.config["thankyou"]
        self.more      = self.config["more"]

        self.replies   = [ {"message" : self.intro, "user" : None, "channel" : "public" } ]

        return super().start()

    def generatorFunc(self):
        while True:
            for question in self.questions:
                self.replies  += [ {"message" : question['text'], "user" : self.last_user, "channel" : "private" } ]
                self.replies  += [ {"message" : question['hint'], "user" : self.last_user, "channel" : "private" } ]
                yield

                validator = eval(question['validator'])
                args = question['validator-args']

                while True:
                    try:
                        response = validator(self.last_data["message"], **args, allow_empty = (not question['compulsory']))
                        break
                    except (ValueError, TypeError) as e:
                        self.replies  += [ {"message" : str(e)          , "user" : self.last_user, "channel" : "private" } ]
                        self.replies  += [ {"message" : question['hint'], "user" : self.last_user, "channel" : "private" } ]
                        yield

                if self.last_user not in self.responses:
                    self.responses[self.last_user] = {}

                self.responses[self.last_user][question['field']] = response
            

            self.replies  += [ {"message" :  self.thankyou, "user" : self.last_user, "channel" : "private" } ]
            self.saveEntry(self.last_user, self.responses[self.last_user])

            while True:
                self.replies  += [ {"message" : self.more , "user" : self.last_user, "channel" : "private" } ]
                yield
                
                selected, response = prompt_choice(self.last_data["message"])

                if response:
                    self.replies  += [ {"message" : response , "user" : self.last_user, "channel" : "private" } ]

                if selected is True:
                    break
                else:
                    yield



    def saveEntry(self, id, entry):

        location = entry.pop('location')

        geocode_result = self.gmaps.geocode(location)

        print("Geocode", geocode_result)

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

            # entry['latitude']    = coords['lat']
            # entry['longitude']   = coords['lng']


            # transformer = Transformer.from_crs('epsg:3857', 'esri:31491') 
       
       

        filename = f"{id}-{time.strftime('%Y%m%d-%H%M%S')}.json"
        path = PurePath(OUTPUT_PATH, filename )
        print(f"Saving {path}")
        json.dump(entry, open(path, 'w'))
        
            
            