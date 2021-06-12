from numpy.core.fromnumeric import mean
from .interaction import SingleGeneratorEngine
import numpy as np
import random
import json
from .prompts import prompt_continue, prompt_rating
from .regex_helper import  is_url
from collections import defaultdict
metrics = json.load(open("app/data/telegram/metrics.json"))


class Telegram(SingleGeneratorEngine):

    def parseHrResponse(self):
        pass
        # if self.id not in self.ids:
        #     self.sendMessage(self.id, "You are not in the survey")

        # try:
        #     selected = int(self.text) - 1
        # except ValueError:
        #     self.sendMessage(self.id, "Response not recognized!")
        #     return

        # question = self.questions[qIndex]
        # choices = question["choices"]

        # if( selected >= len(choices) or selected < 0 ):
        #     self.sendMessage(self.id, "Response not recognized!")
        #     return

        # if qIndex not in self.responses:
        #     self.responses[qIndex] = {}

        # self.responses[qIndex][self.id] = selected

    def _setup(self):
        pass

    def _reset(self):
        self.messages = json.load(open("app/data/telegram/channel_telegram_messages.json", 'r'))
        self.ratings  = json.load(open("app/data/telegram/telegram_rating_data.json", 'r'))
        self.iterateGenerator()

    def saveScores(self, scores, message_id, channel, metrics):
        response = "Thank you for your responses.\nAverage scores:\n"

        for name, newRatings in scores.items():
            print("Ratings", newRatings)
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

            mean = np.mean(np.asarray(self.ratings[key]["hr"]))
            std  = np.std(np.asarray(self.ratings[key]["hr"]))
            self.ratings[key][ name + "-mean"] = mean
            self.ratings[key]["hr-std"] = std 

            response += f"\t'{name}'\tmean: {mean}, std: {std}"

            json.dump(self.ratings, open("app/data/telegram/telegram_rating_data.json", 'w'))

        return response

    def _generator(self):
        while True:

            message, message_id, channel = self.getRandomMessage()

            self.sendBroadcastMessage(message)

            scores = defaultdict(lambda: defaultdict(list))
            
            for name, metric in metrics.items():
                self.sendMessageAll(metric['prompt'])
                self.sendMessageAll(metric['hint'])
                yield
                
                while True:

                    rating, response = prompt_rating(self.text, 0.0, 10.0)

                    if rating:
                        scores[name][self.id].append(rating)
                    else:
                        self.sendMessage(self.id, response)
                        self.sendMessage(self.id, metric['hint'])

                    if set(self.ids) <= scores[name].keys():
                        break
                    else:
                        print(scores)
                        yield

            response = self.saveScores(scores, message_id, channel, metrics)
            self.sendBroadcastMessage(response)

            

    def getRandomMessage(self):
        message = None

        while message is None or message == "" or is_url(message):
            channel = random.choice(list(self.messages.keys()))
            #print("\n", channel)
            channels_messages = self.messages[channel]

            message_id = random.choice(list(channels_messages.keys()))

            message = channels_messages[message_id ]

        return message, message_id, channel

