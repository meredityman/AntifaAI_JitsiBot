from numpy.core.fromnumeric import mean
import numpy as np
import random
import json
from .utils.prompts import prompt_rating
from .utils.regex_helper import  is_url
from collections import defaultdict
import holoviews as hv
from holoviews import dim, opts
import json

from .interface import MultiUserGenerator


def plot_telegram():
    print("Plotting...")

    hv.extension('bokeh')
    raw_data = json.load(open("engine/data/telegram/telegram_rating_data.json", "r"))
    channels = []

    data_groups = {}
    for message in raw_data.values():

        channel = message["channel"].split("/")[-1]

        if channel in data_groups:
            data_groups[channel].append(message["hr-mean"])
            data_groups[channel].append(message["gr-mean"])
        else:
            data_groups[channel] = [message["hr-mean"], message["gr-mean"]]


    overlay = hv.NdOverlay({channel: hv.Scatter(np.clip(np.asarray(data).reshape([-1,2]), 0.0, 1.0), 'Hatefullness' , 'Galvanizing')
                            for channel, data in data_groups.items()})

    overlay.opts( opts.NdOverlay(legend_position='right', width=1000, height=700), opts.Scatter(color = hv.Cycle('RdGy'), alpha=0.8,  marker='s', size=6))

    print("Saving...")
    hv.save(overlay, 'engine/static/var/TelegramRatingScatter.html')


class Telegram(MultiUserGenerator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.commands = {
            "ESCAPE",
            "START",
            "END"
        }

    def start(self) -> list:
        self.messages = json.load(open("engine/config/telegram/channel_telegram_messages.json", 'r'))
        self.ratings  = json.load(open("engine/data/telegram/telegram_rating_data.json", 'r'))
        self.metrics  = json.load(open("engine/config/telegram/metrics.json"))

        othertext  = json.load(open("engine/config/telegram/text.json", 'r'))
        self.intro    = othertext['intro']
        self.thankyou = othertext['thankyou']
        self.outro    = othertext['outro']
        self.line     = othertext['line']


        self.replies   = [ {"message" : self.intro, "user" : None, "channel" : "public" } ]

        return super().start()


    def generatorFunc(self):

        running = True
        while running:
            print("Telegram.generatorFunc", "Last data:", self.last_data)
            if self.last_data == None:
                yield
                continue   


            while True: 
                isPublic = self.last_data["channel"] == "public"
                user_message = self.last_data["message"]
                print("Telegram.generatorFunc", user_message)
                if  isPublic:
                    if( user_message == "START"):
                        break
                    elif( user_message == "END"): 
                        running = False
                        break
                    else:
                        yield
                else:
                    yield

            message, message_id, channel = self.getRandomMessage()
            message = ("-" * 20) + "\n" + message + "\n" + ("-" * 20)

            self.replies  += [ {"message" : message, "user" : self.last_user, "channel" : "public" } ]

            scores = defaultdict(lambda: defaultdict(list))
            
            for name, metric in self.metrics.items():
                self.replies  += [ {"message" : metric['prompt'], "user" : self.last_user, "channel" : "public" } ]
                self.replies  += [ {"message" : metric['hint'], "user" : user, "channel" : "private" } for user in self.users]
                yield
                
                while True:

                    isPublic = self.last_data["channel"] == "public"
                    user_message = self.last_data["message"]

                    if  isPublic:
                        if( user_message == "ESCAPE"):
                            break
                        else:
                            yield
                    else:
                        if user_message is not None:
                            rating, response = prompt_rating(user_message, 0.0, 10.0)

                        if response is not None:
                            self.replies  += [ {"message" : response, "user" : self.last_user, "channel" : "private" } ]


                        if rating is not None:
                            scores[name][self.last_user].append(rating)
                        else:
                            self.replies  += [ {"message" : response, "user" : self.last_user, "channel" : "private" } ]
                            self.replies  += [ {"message" : metric['hint'], "user" : self.last_user, "channel" : "private" } ]

                        if set(self.users) <= scores[name].keys():
                            print(scores)
                            break
                        else:
                            print(scores)
                            yield


            response = self.saveScores(scores, message_id, channel)
            self.replies  += [ {"message" : response, "user" : self.last_user, "channel" : "public" } ]
            
            try:
                plot_telegram()
            except:
                raise


        self.replies  += [ {"message" : self.outro, "user" : user, "channel" : "private" } for user in self.users]

    def saveScores(self, scores, message_id, channel):
        response = f"{self.thankyou}"

        for name, newRatings in scores.items():
            newRatings = [ r / 10.0 for rs in newRatings.values() for r in rs]

            key = f"{message_id}-{channel.split('/')[-1]}"


            if key not in self.ratings:
                self.ratings[key] = {
                    "channel" : channel
                }

            if name in self.ratings[key]:
                self.ratings[key][name].append(newRatings)
            else:
                self.ratings[key][name] = newRatings

            mean = np.mean(np.asarray(self.ratings[key][name]))
            std  = np.std(np.asarray(self.ratings[key][name]))
            self.ratings[key][ name + "-mean"] = mean
            self.ratings[key][ name + "-std"] = std 

            response += "\n" + self.line.format(
                displayName = self.metrics[name]['name'],
                mean = mean
                )

            json.dump(self.ratings, open("engine/data/telegram/telegram_rating_data.json", 'w'))

        return response



    def getRandomMessage(self):
        message = None

        while message is None or message == "" or is_url(message):
            channel = random.choice(list(self.messages.keys()))
            #print("\n", channel)
            channels_messages = self.messages[channel]

            message_id = random.choice(list(channels_messages.keys()))

            message = channels_messages[message_id ]

        return message, message_id, channel

