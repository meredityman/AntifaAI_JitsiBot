import json
import numpy as np
from .interaction import InteractionEngine

        
# OUTPUT_MAP_PATH  = "output/map_latest.jpg"

QUESTION_PATH = "app/interaction/survey.json"



# def printMap(route):
#     route.insert(0, "Questionaire")

#     print(f"{'->'.join(route)}")

#     draw_map(route, OUTPUT_MAP_PATH)
#     # img = Image.open(OUTPUT_MAP_PATH)
#     # #img.show()


def get_route(scores, stations, metrics, number = 4):
    route = None

    point = [ ]
    for m in metrics:
        metric = m["name"]
        try:
            point.append(scores[metric])
        except:
            point.append(0.0) 
    point = 0.5 * (np.asarray(point) + 0.5)         
    point = point/np.linalg.norm(point)
    distances = {}
    for station in stations:
        target = np.asarray(station["score"])

        target  = target/np.linalg.norm(target)
        dist = np.linalg.norm(point - target)
        distances[station["name"]] = dist
    route = sorted(distances, key=distances.get, reverse=True)[:number]
    return route

class Survey(InteractionEngine):
    def setup(self):
        self.reset()

    def reset(self):
        self.loadQuestions()

        self.responses = {}
        self.generator = self.surveyGenerator()

        self.iterateSurvey()

    def getResponse(self, id, text):
        self.id   = id
        self.text = text
        self.iterateSurvey()

    def iterateSurvey(self):
        try:
            next(self.generator)
        except StopIteration:
            print("Survey Complete")
            self.reset()

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
            print(self.ids)
            print(self.responses[qIndex])
            return set(self.ids) <= set(self.responses[qIndex].keys())
        except IndexError:
            return False

    def finalizeQuestion(self):
        pass

    def finalizeAllQuestions(self):
        route = get_route(self.responses, self.stations, self.metrics)
        message = f"{' -> '.join(route)}"
        self.sendBroadcastMessage(message)



    def surveyGenerator(self):
        self.sendBroadcastMessage(self.intro)

        for qIndex in range(len(self.questions)):
            responses = {}

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
