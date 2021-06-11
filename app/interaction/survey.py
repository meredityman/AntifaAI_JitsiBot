import json
import numpy as np
from .interaction import SingleGeneratorEngine
from ..horror import  draw_map
#from ..horror import send_data
        
OUTPUT_MAP_PATH  = "app/static/map_latest.jpg"

QUESTION_PATH = "app/interaction/survey.json"




class Survey(SingleGeneratorEngine):

    def _setup(self):
        pass

    def _reset(self):
        self.loadQuestions()
        self.responses = {}
        self.iterateGenerator()

    def _generator(self):
        self.sendBroadcastMessage(self.intro)

        for qIndex in range(len(self.questions)):

            self.sendQuestion(qIndex)
            yield

            while True:
                self.parseResponse(qIndex)

                if self.questionAnswered(qIndex):
                    break
                else:
                    yield

            self.finalizeQuestion()

        self.finalizeAllQuestions()


    def getQuestionText(self, qIndex):
        question = self.questions[qIndex]

        choices = question["choices"]
        prompt  = question["prompt"]

        text = f"{prompt}"

        for i, c in enumerate(choices):#here abcd instead of 0 to 3
            text += f"\t{i+1}. {c['option']}"

        return text


    def sendQuestion(self, qIndex):
        text =  self.getQuestionText(qIndex)
        for id in self.ids:
            self.sendMessage(id,text)

    def parseResponse(self, qIndex):
        if self.id not in self.ids:
            self.sendMessage(self.id, "You are not in the survey")

        try:
            selected = int(self.text) - 1
        except ValueError:
            self.sendMessage(self.id, "Response not recognized!")
            return

        question = self.questions[qIndex]
        choices = question["choices"]

        if( selected >= len(choices) or selected < 0 ):
            self.sendMessage(self.id, "Response not recognized!")
            return

        if qIndex not in self.responses:
            self.responses[qIndex] = {}

        self.responses[qIndex][self.id] = selected


    def questionAnswered(self, qIndex):
        if qIndex not in self.responses:
            return False
        try:
            return set(self.ids) <= set(self.responses[qIndex].keys())
        except IndexError:
            return False

    def finalizeQuestion(self):
        pass

    def finalizeAllQuestions(self):
        route = self.getRoute()
        message = f"{' -> '.join(route)}"
        # send_data("map-decision", message)
        self.sendBroadcastMessage(message)

        route.insert(0, "Questionaire")
        print(f"{'->'.join(route)}")
        draw_map(route, OUTPUT_MAP_PATH)




    def getRoute(self, number = 4):

        scores = { m["name"] : 0.0 for m in self.metrics }
        for qIndex, response in self.responses.items():
            question = self.questions[qIndex]
            metric   = question['metric']

            score = [question['choices'][r] ['score'] for r in response.values()]

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
        self.questions = survey_def["questions"]
        self.metrics   = survey_def["metrics"]
        self.stations  = [ s for s in survey_def["stations"] if s["active"] ]


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
