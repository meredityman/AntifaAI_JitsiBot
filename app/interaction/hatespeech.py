from typing import Text
from .interaction import MultiGeneratorEngine
import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
import json
import random
from collections import defaultdict

MODEL = "deepset/bert-base-german-cased-hatespeech-GermEval18Coarse"
LABELS = ['Other', 'Offense']

class HateSpeech(MultiGeneratorEngine):

    def _setup(self):
        self.tokenizer = BertTokenizer.from_pretrained(MODEL)
        self.model = BertForSequenceClassification.from_pretrained(MODEL)

    def _reset(self):
        self.data = json.load(open("app/data/hatespeech/hatespeech.json", 'r'))

        self.prompts = self.data['prompts']
        self.commands = self.data['commands']
        self.final_prompt = self.data['final-prompt']

        self.prompts_seen = defaultdict(list)

        for line in self.data['introduction']:
            self.sendMessageAll(line)

    def forward(self, message):
        inputs  = self.tokenizer(message, return_tensors="pt")
        labels  = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        loss    = outputs.loss
        logits  = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1).cpu().detach().numpy()
        return loss, probabilities

    def parsePrompt(self):
        if self.text in self.commands['prompt']:
            return True
        else:
            return False

    def getPrompt(self):
        prompts_available = set(range(len(self.prompts))).difference( self.prompts_seen[self.id])

        if( len(prompts_available) ==  0):
            self.sendMessage(self.id, self.final_prompt)
        else:
            prompt_i = random.choice(list(prompts_available))
            prompt = self.prompts[prompt_i]
            self.prompts_seen[self.id].append(prompt_i)
            self.sendMessage(self.id, prompt)

    def _generator(self):
        while True:
            if self.parsePrompt():
                self.sendMessage(self.id, self.getPrompt())
            else:
                self.getPrediction()
            yield

    def getPrediction(self):
        loss, probabilities = self.forward(self.text)

        prediction = LABELS[np.argmax(probabilities)]
        certainty = np.max(probabilities)

        response = f"Classified as: {prediction} ({certainty:.0%})"

        self.sendMessage(self.id, response)