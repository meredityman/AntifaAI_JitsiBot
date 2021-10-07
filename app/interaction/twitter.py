import re
from numpy.core.fromnumeric import mean
from .interaction import SingleGeneratorEngine
import json
from .regex_helper import  is_url
from collections import defaultdict

import tweepy
import json

from .prompts import prompt_option, prompt_choice


import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from bokeh.sampledata.les_mis import data

import json


def plot_twitter():
    def cn(n):
        #return n.replace("@", "")
        return n

    raw_data = json.load(open("app/data/twitter/twitter-data.json", "r"))

    nodes_data = [ { 'name' : cn(n), 'group' : 0 } for n in raw_data.keys() ]

    index_lookup = { d['name'] : i for i, d in enumerate(nodes_data) }

    links_data = []
    for user, d in raw_data.items():

        user_index = index_lookup[cn(user)]

        links_data.append(
            {
                'source' : user_index,
                'target' : user_index,
                'value'  : 1
            }
        )


        for con, w in d["connections"].items():
            c_user = cn(con)

            if c_user in index_lookup:
                links_data.append(
                    {
                        'source' : user_index,
                        'target' : index_lookup[c_user],
                        'value'  : w
                    }
                )


    hv.extension('bokeh')
    hv.output(size=254)

    links = pd.DataFrame(links_data)
 
    nodes = hv.Dataset(pd.DataFrame(nodes_data), 'index')
    chord = hv.Chord((links, nodes))
    chord.opts(
        opts.Chord(
            cmap='RdGy', 
            edge_cmap='RdGy', 
            edge_color=dim('source').str(), 
            labels='name', 
            node_color=dim('index').str()
            ))

    hv.save(chord, 'app/static/var/NaziTwitterBubble.html')













####input your credentials here
consumer_key        = 'qjBKfredGfs5DeH69SDNLdEXN'
consumer_secret     = 'YoXs5jEOC4EkLKl7MvkNNkpp55L70vqKvmfWofHPVijutnAa5f'
access_token        = '4275253119-VvaVvbgAZRmRQnX8CM4Lr23UVpJeDnfD0Q5f5ys'
access_token_secret = 'py4IZRw0HNdWNCBUmK4WZyvcKvZfoUwq6h7TWOJf79TsX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


## Constants
woeids = {
    "hamburg" : 656958,
    "bochum"  : 639679,
#stuttgart : ,
#halle :
}

def get_trending_hashtags():
    trends = []
    woeid = woeids['hamburg']

    ret = api.get_place_trends(id = woeid)

    for value in ret:
        for trend in value['trends']:
            trends.append(trend['name'])

    return trends
    
def get_users_for_trend(trend):
    users = []

    search = api.search_tweets(q=trend, lang='de')
    for tweet in search: 
        users.append(tweet.user.screen_name)

    return users


class Twitter(SingleGeneratorEngine):

    def _setup(self):
        self.commands = {"END"}

    def _reset(self):
        self.jsonData  = json.load(open("app/data/twitter/twitter-data.json", 'r'))


        othertext  = json.load(open("app/config/twitter/text.json", 'r'))

        self.num_users = othertext ['number-of-users']
        self.intro = othertext ['intro']
        self.outro = othertext ['outro']
        self.question = othertext ['question']
        self.hashtag_question = othertext ['hashtag-question']
        self.users_question   = othertext ['users-question']
        self.is_nazi     = othertext ['is-nazi']
        self.is_not_nazi = othertext ['is-not-nazi']
        self.summary     = othertext ['summary']
        self.picked      = othertext['picked']
        self.calculating = othertext['calculating']
        
        self.iterateGenerator()

    def save_data(self, users):

        for user in users:
            friends = api.friends(user)
            connections = { f.screen_name : 1 for f in friends }

            x = api.get_user(user)

            followers_count = x._json['followers_count']
            self_description= x._json['description']
            location        = x._json['location']   

            if user not in self.jsonData:
                print(f"Saving {user}")
                self.jsonData[user] = {
                    "connections" : connections,
                    "followers"  : followers_count,
                    "location"   : location,
                    "description": self_description,
                }


        json.dump(self.jsonData, open("app/data/twitter/twitter-data.json", "w"), indent=4, sort_keys=True)
 
    def get_user_summmary(self, suspicious_user):
        response= ""

        x = api.get_user(screen_name=suspicious_user)

        followers_count = x._json['followers_count']
        self_description= x._json['description']
        location        = x._json['location']   

        user_title = "@" + suspicious_user.upper()
        response += f"\n{user_title:_^20}\n\n"
        response += self.summary['intro'].format(suspicious_user=suspicious_user, followers_count=followers_count) +"\n"

        response += f"\n{self.summary['description']:_^20}\n\n"
        response += f"{self_description}\n"

        ret = api.user_timeline(screen_name=suspicious_user)

        response += f"\n{self.summary['tweets']:_^20}\n\n"
        for i, r in enumerate(ret):
            if i > 4:
                break

            response += r.text + "\n\n"
            response += ("-" * 20) + "\n"

        return response


    def get_results(self, votes):
        message = ""
        confirmed_users = []
        for user, user_votes in votes.items():

            votes_for = sum(user_votes.values())
            votes_against = len(user_votes) - votes_for
            is_nazi = votes_for > votes_against

            if is_nazi:
                message += self.is_nazi.format(user=user, votes_for=votes_for, votes_against=votes_against) + "\n"
                confirmed_users.append(user)
            else:
                message += self.is_not_nazi.format(user=user, votes_for=votes_for, votes_against=votes_against) + "\n"

        return  message, confirmed_users

    def _generator(self):

        self.sendBroadcastMessage(self.intro)

        running = True
        while running:
        
            # Get a hashtag
            hashtags = get_trending_hashtags()
            message = self.hashtag_question + "\n"
            message += '\n'.join([f"{i+1}). {hashtag}" for i, hashtag in enumerate(hashtags)])
            message += f"\n1-{len(hashtags)}: "
            self.sendBroadcastMessage(message)
            yield

            while True:
                print(self.isPublic)
                if not self.isPublic:
                    # Private messages are ignored
                    yield
                else:
                    if self.text:
                        hashtag, response = prompt_option(self.text, hashtags)
                    
                    if response:#
                        self.sendBroadcastMessage(response)
                        
                    if hashtag:
                        break
                    else:
                        self.sendBroadcastMessage(response)
                        yield


            # Get users
            suspicious_users = set([])
            users = get_users_for_trend(hashtag)
            message  = self.users_question.format(num_users = self.num_users)
            message += "\n"
            message += "\n".join([ f"{i+1}). {user}" for i, user in enumerate(users)])
            message += f"\n\n1-{len(users)}: "
            self.sendBroadcastMessage(message)
            yield

            while True:
                if self.isPublic:
                    if self.text:
                        user, response = prompt_option(self.text, users)

                    if response:#
                        self.sendBroadcastMessage(response)

                    if user:
                        if user in suspicious_users:
                            message = self.picked.format(user = user)
                            self.sendBroadcastMessage(message)
                        else:
                            suspicious_users.add(user)
                            if(len(suspicious_users) >= self.num_users):
                                break
                yield

            # Vote on users
            self.votes = defaultdict(dict)

            for suspicious_user in suspicious_users:
                message = self.get_user_summmary(suspicious_user)
                self.sendBroadcastMessage(message)    
                self.sendMessageAll(self.question )     
                yield
                while True:
                    if  self.isPublic:
                        if( self.text == "ESCAPE"):
                            break
                        else:
                            yield
                    else:
                        if self.text:
                            vote, response = prompt_choice(self.text)

                        if response:
                            self.sendMessage(self.id, response)

                        if vote is not None:
                            self.votes[suspicious_user][self.id] = vote

                        if set(self.ids) <= set(self.votes[suspicious_user].keys()):
                            print(self.ids, self.votes[suspicious_user].keys() )
                            break
     
                        print(self.ids, self.votes[suspicious_user].keys() )
                        yield

            message, confirmed_users = self.get_results(self.votes)
            self.sendBroadcastMessage(message)    
            self.sendBroadcastMessage(self.calculating)  
            running = False

            self.save_data(confirmed_users)
            try:
                plot_twitter()
            except:
                pass
            self.sendBroadcastMessage(self.outro)

# def main_loop():

#     trends = get_trending_hashtags()
#     if len(trends) > 0:
#         selected_trend = prompt_option("Select a trend \n", trends)

#         if selected_trend:
#             users = get_users_for_trend(selected_trend)

#             while True:
#                 suspicous_user = prompt_option("\n Kommt dir ein Name verdächtig vor? Welcher Name kommt dir verdächtig vor \n ", users, nota = True)

#                 if suspicous_user:                
#                     check_user(suspicous_user)

#                 if prompt_continue("\n Select another users?"):
#                     pass
#                 else:
#                     break

        
#     input('\n press Enter to continue')

# def main():

#     # Main program loop
#     while True:
#         try:
#             if prompt_continue('\nThis programm will guide you through! Read carefully. Do you want to start?\n'):
#                 main_loop()
#         except KeyboardInterrupt:
#             break

#     print("Exiting..")

# if __name__ == "__main__":
#     main()




