from glob import glob
from lib2to3.pgen2.tokenize import tokenize
from typing import Text

from numpy.core.numeric import False_
import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
import json
import random
from collections import defaultdict

from .interface import MultiUserGenerator

MODEL = "deepset/bert-base-german-cased-hatespeech-GermEval18Coarse"
LABELS = ['Other', 'Offense']

tokenizer = None
model     = None

class Hatespeech(MultiUserGenerator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        global tokenizer, model

        if tokenizer is None:
            tokenizer = BertTokenizer.from_pretrained(MODEL)

        if model is None:
            model = BertForSequenceClassification.from_pretrained(MODEL)


    def start(self) -> list:
        self.loadData()
        self.prompts_seen = {}
        self.replies  = [ {"message" : s, "user" : None, "channel" : "public" }  for s in self.intro]
        self.replies +=  [ {"message" : self.get_prompt_for_user(user), "user" : user, "channel" : "private" } for user in self.users]
        return super().start()


    def loadData(self):
        self.data = json.load(open("engine/config/hatespeech/hatespeech.json", 'r'))
        self.intro        = self.data['introduction']
        self.prompts      = self.data['prompts']
        self.commands     = self.data['commands']
        self.final_prompt = self.data['final-prompt']
        self.result       = self.data['result']
        self.all_prompts_seen = {}

    def _getResponse(self, id, text, isPublic):
        self.isPublic = isPublic
        self.id   = id
        self.text = text

        self.iterateGenerator()

    def generatorFunc(self):
        running = True
        while running:
            if self.last_data == None:
                yield
                continue

            user_message = self.last_data["message"]
            response = self.getPrediction(user_message)

            isPrivate = self.last_data["channel"] == "private"
            if response:
                self.replies  += [ {"message" : response, "user" : self.last_user, "channel" : self.last_data["channel"] } ]
                if(isPrivate):
                    self.replies  += [ {"message" : self.get_prompt_for_user(self.last_user), "user" : self.last_user, "channel" : "private" } ]
            

            if( len(self.prompts_seen[self.last_user]) ==  len(self.prompts)):
                self.replies  += [ {"message" : "Thank you for participating! ❤️\n[THE END]", "user" : self.last_user, "channel" : "private" } ]
                running = False

            yield

    def getPrediction(self, text):
        try:
            loss, probabilities = self.forward(text)

            prediction = LABELS[np.argmax(probabilities)]
            certainty = np.max(probabilities)

            response = self.result.format(
                prediction = prediction,
                certainty  = certainty
            )

            return response
        except Exception as e:
            print(f"Predictions failed {text}")
            return str(e)

    def forward(self, message):
        global tokenizer, model

        inputs  = tokenizer(message, return_tensors="pt")
        labels  = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = model(**inputs, labels=labels)
        loss    = outputs.loss
        logits  = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1).cpu().detach().numpy()
        return loss, probabilities

    def parsePrompt(self):
        if not self.isPublic:
            if self.text in self.commands['prompt']:
                return True
            else:
                return False
        else: 
            return False

    def get_prompt_for_user(self, user):
        if(user in self.prompts_seen):
            user_prompts_seen = self.prompts_seen[user]

            prompts_available = set(range(len(self.prompts))).difference( user_prompts_seen)

            if( len(prompts_available) ==  0):
                return self.final_prompt
            else:
                prompt_i = random.choice(list(prompts_available))
                prompt = self.prompts[prompt_i]
                self.prompts_seen[user].add(prompt_i)
                return prompt

        else:
            prompt = random.choice(list(self.prompts))
            self.prompts_seen[user] = set([prompt])
            return prompt


