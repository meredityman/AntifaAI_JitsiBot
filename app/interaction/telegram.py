from numpy.core.fromnumeric import mean
from .interaction import SingleGeneratorEngine
import numpy as np
import random
import json
from .prompts import prompt_rating
from .regex_helper import  is_url
from collections import defaultdict
import holoviews as hv
from holoviews import dim, opts
import json


def plot_telegram():


    print("Plotting...")

    hv.extension('bokeh')

    raw_data = json.load(open("app/data/telegram/telegram_rating_data.json", "r"))


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
    hv.save(overlay, 'app/static/var/TelegramRatingScatter.html')


class Telegram(SingleGeneratorEngine):


    def _setup(self):
        pass

    def _reset(self):
        self.messages = json.load(open("app/config/telegram/channel_telegram_messages.json", 'r'))
        self.ratings  = json.load(open("app/data/telegram/telegram_rating_data.json", 'r'))
        self.metrics  = json.load(open("app/config/telegram/metrics.json"))

        othertext  = json.load(open("app/config/telegram/text.json", 'r'))
        self.intro    = othertext['intro']
        self.thankyou = othertext['thankyou']
        self.outro    = othertext['outro']
        self.line     = othertext['line']
        self.iterateGenerator()

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

            json.dump(self.ratings, open("app/data/telegram/telegram_rating_data.json", 'w'))

        return response


    def _generator(self):
        self.sendBroadcastMessage(self.intro)
        yield
        running = True
        while running:

            while True:
                if  self.isPublic:
                    if( self.text == "CONTINUE" or self.text == "START"):
                        break
                    elif( self.text == "END"): 
                        running = False
                        break
                    else:
                        yield
                else:
                    yield

            message, message_id, channel = self.getRandomMessage()


            message = ("-" * 20) + "\n" + message + "\n" + ("-" * 20)
            self.sendBroadcastMessage(message)

            scores = defaultdict(lambda: defaultdict(list))
            
            for name, metric in self.metrics.items():
                self.sendBroadcastMessage(metric['prompt'])
                self.sendMessageAll(metric['hint'])
                yield
                
                while True:
                    if  self.isPublic:
                        if( self.text == "ESCAPE"):
                            break
                        else:
                            yield
                    else:
                        if self.text is not None:
                            rating, response = prompt_rating(self.text, 0.0, 10.0)

                        if response is not None:
                            self.sendMessage(self.id, response)

                        if rating is not None:
                            scores[name][self.id].append(rating)
                        else:
                            self.sendMessage(self.id, response)
                            self.sendMessage(self.id, metric['hint'])

                        if set(self.ids) <= scores[name].keys():
                            break
                        else:
                            print(scores)
                            yield


            response = self.saveScores(scores, message_id, channel)
            self.sendBroadcastMessage(response)

            try:
                plot_telegram()
            except:
                raise


        self.sendBroadcastMessage(self.outro)

    def getRandomMessage(self):
        message = None

        while message is None or message == "" or is_url(message):
            channel = random.choice(list(self.messages.keys()))
            #print("\n", channel)
            channels_messages = self.messages[channel]

            message_id = random.choice(list(channels_messages.keys()))

            message = channels_messages[message_id ]

        return message, message_id, channel

