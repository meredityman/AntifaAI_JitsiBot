import json
import numpy as np
from numpy.lib.function_base import select
from .interaction import SingleGeneratorEngine
from ..utils.make_map import draw_map
from ..utils.cuemanager import send_cue
from .prompts import prompt_option

OUTPUT_MAP_PATH  = "app/static/var/map_latest.jpg"

QUESTION_PATH = "app/config/survey/survey.json"


class Survey(SingleGeneratorEngine):

    def _setup(self):
        self.commands = {
            "ESCAPE"
        }
        pass

    def getQuestionText(self, qIndex):
        question = self.questions[qIndex]

        choices = question["choices"]
        prompt  = question["prompt"]

        text = f"{prompt}"

        for i, c in enumerate(choices):#here abcd instead of 0 to 3
            text += f"\n{i+1}. {c['option']}"

        return text


    def parseResponse(self, qIndex):
        if self.id not in self.ids:
            response = None


        choices = self.questions[qIndex]["choices"]
        options = [ c['option'] for c in choices]
        selected, response = prompt_option(self.text, options)
        
        if selected:
            if qIndex not in self.responses:
                self.responses[qIndex] = {}

            score = 0
            for c in choices:
                if c['option'] == selected:
                    score = c['score']
            self.responses[qIndex][self.id] = score

        return response


    def questionAnswered(self, qIndex):
        if qIndex not in self.responses:
            return False

        yetToAnswer = set(self.ids) - set(self.responses[qIndex].keys())
        if len(yetToAnswer) != 0:
            message = self.pyta.format(pyta=len(yetToAnswer))
            self.sendBroadcastMessage( message )
        return len(yetToAnswer) == 0

    def finalizeAllQuestions(self):
        route = self.getRoute()
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


    def _reset(self):
        self.loadQuestions()
        self.responses = {}
        self.iterateGenerator()

    def _generator(self):
        self.sendBroadcastMessage(self.intro)

        for qIndex in range(len(self.questions)):

            text =  self.getQuestionText(qIndex)
            self.sendBroadcastMessage(text)
            self.sendMessageAll(self.prompt)
            yield

            while True:
                if not self.text:
                    yield
                    continue

                if  self.isPublic:
                    if( self.text == "ESCAPE"):
                        break
                    else:
                        yield
                else:
                    responce = self.parseResponse(qIndex)
                    if responce:
                        self.sendMessage(self.id, responce )

                    if self.questionAnswered(qIndex):
                        break
                    else:
                        yield

        message = self.finalizeAllQuestions()
        
        send_cue("map-decision", message)
        self.sendBroadcastMessage(message)
        self.sendBroadcastMessage(self.outro)


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
