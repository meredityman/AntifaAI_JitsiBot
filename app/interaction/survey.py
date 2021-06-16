import json
import numpy as np
from numpy.lib.function_base import select
from .interaction import SingleGeneratorEngine
from ..utils.make_map import draw_map
from ..utils.cuemanager import send_cue
from .prompts import prompt_option

OUTPUT_MAP_PATH  = "app/static/var/map_latest.jpg"

QUESTION_PATH = "app/data/survey/survey.json"


class Survey(SingleGeneratorEngine):

    def _setup(self):
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
        selected, response = prompt_option(self.text, list(range(len(choices))))
        
        if selected:
            if qIndex not in self.responses:
                self.responses[qIndex] = {}

            self.responses[qIndex][self.id] = selected

        return response


    def questionAnswered(self, qIndex):
        if qIndex not in self.responses:
            return False

        yetToAnswer = set(self.ids) - set(self.responses[qIndex].keys())
        print("Yet to answer", yetToAnswer)
        return len(yetToAnswer) == 0

    def finalizeAllQuestions(self):
        route = self.getRoute()
        message = f"{' -> '.join(route)}"

        route.insert(0, "Questionaire")
        draw_map(route, OUTPUT_MAP_PATH)
        return message


    def getRoute(self, number = 4):

        scores = { m["name"] : 0.0 for m in self.metrics }
        for qIndex, response in self.responses.items():
            question = self.questions[qIndex]
            metric   = question['metric']
            print(response)
            score = [question['choices'][r-1]['score'] for r in response.values()]

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

        print(point)

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
        self.questions = survey_def["questions"]
        self.metrics   = survey_def["metrics"]
        self.prompt    = survey_def["prompt"]
        self.stations  = [ s for s in survey_def["stations"] if s["active"] ]


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
                if self.text:
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
