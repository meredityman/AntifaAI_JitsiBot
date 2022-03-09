import json
import numpy as np
from numpy.lib.function_base import select
from .utils.make_map import draw_map
from .utils.cuemanager import send_cue
from .utils.prompts import prompt_option

from .interface import MultiUserGenerator


OUTPUT_MAP_PATH  = "engine/static/var/map_latest.jpg"

QUESTION_PATH = "engine/config/survey/survey.json"


class Survey(MultiUserGenerator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.commands = {
            "ESCAPE"
        }

    def start(self) -> list:
        self.loadQuestions()
        self.responses = {}
        self.replies   = [ {"message" : self.intro, "user" : None, "channel" : "public" } ]
        return super().start()


    def generatorFunc(self):
        for qIndex in range(len(self.questions)):

            qtext =  self.getQuestionText(qIndex)
            self.replies  += [ {"message" : qtext, "user" : self.last_user, "channel" : "public" } ]
            self.replies  += [ {"message" : self.prompt, "user" : user, "channel" : "private" } for user in self.users]
            yield


            while True:
                if self.last_data == None:
                    yield
                    continue
                
                user_message = self.last_data["message"]
                isPublic = self.last_data["channel"] == "public"

                if  isPublic:
                    if( user_message == "ESCAPE"):
                        break
                    else:
                        yield
                else:
                    responce = self.parseResponse(qIndex, user_message)
                    if responce:
                        self.replies  += [ {"message" : responce, "user" : self.last_user, "channel" : "private" } ]
                    if self.questionAnswered(qIndex):
                        break
                    else:
                        yield

        message = self.finalizeAllQuestions()
        
        send_cue("map-decision", message)

        self.replies  += [ {"message" : message, "user" : self.last_user, "channel" : "public" } ]
        self.replies  += [ {"message" : self.outro, "user" : user, "channel" : "private" } for user in self.users]


    def getQuestionText(self, qIndex):
        question = self.questions[qIndex]

        choices = question["choices"]
        prompt  = question["prompt"]

        text = f"{prompt}"

        for i, c in enumerate(choices):#here abcd instead of 0 to 3
            text += f"\n{i+1}. {c['option']}"

        return text


    def parseResponse(self, qIndex, user_message):

        choices = self.questions[qIndex]["choices"]
        options = [ c['option'] for c in choices]
        selected, response = prompt_option(user_message, options)
        
        if selected:
            if qIndex not in self.responses:
                self.responses[qIndex] = {}

            score = 0
            for c in choices:
                if c['option'] == selected:
                    score = c['score']
            self.responses[qIndex][self.last_user] = score

        return response


    def questionAnswered(self, qIndex):
        if qIndex not in self.responses:
            return False

        yetToAnswer = set(self.users) - set(self.responses[qIndex].keys())
        if len(yetToAnswer) != 0:
            message = self.pyta.format(pyta=len(yetToAnswer))

            self.replies  += [ {"message" : message, "user" : self.last_user, "channel" : "public" } ]
        return len(yetToAnswer) == 0

    def finalizeAllQuestions(self):
        # Dirty deceitful hack
        #route = self.getRoute()
        route = [
            "Drum",
            "Map",
            "Garage"
        ]


        message = "🗺️" * 8 + "\n"        
        message += "{:_^12}".format("ROUTE") + "\n"
        message += "🗺️" * 8 + "\n\n"

        message += '\n ⬇️\n'.join(route)

        message += "\n\n" + ("🗺️" * 8) + "\n\n"

        route.insert(0, "Questionaire")
        route.append("Inflatable")
        draw_map(route, OUTPUT_MAP_PATH)
        return message


    def getRoute(self, number = 6):

        scores = { m["name"] : 0.0 for m in self.metrics }
        for qIndex, response in self.responses.items():
            question = self.questions[qIndex]
            metric   = question['metric']
            score = list(response.values())

            score = sum(score) / len(score)
            scores[metric] += score

        route = None

        point = [ ]
        for m in self.metrics:
            metric = m["name"]
            try:
                point.append(scores[metric])
            except:
                point.append(0.0) 
        point = 0.5 * (np.asarray(point) + 0.5)         
        point = point/np.linalg.norm(point)

        distances = {}
        for station in self.stations:
            target = np.asarray(station["score"])

            target  = target/np.linalg.norm(target)
            dist = np.linalg.norm(point - target)
            distances[station["name"]] = dist
        route = sorted(distances, key=distances.get, reverse=True)[:number]
        return route


    def loadQuestions(self):
        survey_def = json.load(open(QUESTION_PATH, "r"))

        self.intro     = survey_def["intro"]
        self.outro     = survey_def["outro"]
        self.questions = [q for q in survey_def["questions"] if q["active"]]
        self.metrics   = survey_def["metrics"]
        self.prompt    = survey_def["prompt"]
        self.stations  = [ s for s in survey_def["stations"] if s["active"] ]
        self.pyta      = survey_def["pyta"]



# def runSurvey(survey_def):

#     questions = survey_def["questions"]
#     metrics   = survey_def["metrics"]
#     stations  = [ s for s in survey_def["stations"] if s["active"] ]

#     scores = { m["name"] : 0.0 for m in metrics }
    
#     for i, question in enumerate(questions):
#         print(f"QUESTION {i+1}/{len(questions)}")
#         metric, score = ask_question(question)

#         if metric:
#             scores[metric] += score
#         print("\n")

#     route = get_route(scores, stations, metrics)

#     random.shuffle(route)
    
#     message = f"{' -> '.join(route)}"
#     print(message)

#     send_data("map-decision", message)

#     printMap(route)
