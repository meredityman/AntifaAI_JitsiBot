from typing import Text
from .interaction import InteractionEngine
import torch
import numpy as np

MODEL = "deepset/bert-base-german-cased-hatespeech-GermEval18Coarse"
LABELS = ['Other', 'Offense']
class HateSpeech(InteractionEngine):

    def setup(self):

        from transformers import BertTokenizer, BertForSequenceClassification
        # from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline

        # self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        # self.model = AutoModelWithLMHead.from_pretrained(MODEL)

        # self.pipe = pipeline('text-classification', model=self.model , tokenizer=self.tokenizer)

        self.tokenizer = BertTokenizer.from_pretrained(MODEL)
        self.model = BertForSequenceClassification.from_pretrained(MODEL)


    def forward(self, message):
        inputs  = self.tokenizer(message, return_tensors="pt")
        labels  = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        loss    = outputs.loss
        logits  = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1).cpu().detach().numpy()
        return loss, probabilities


    def _getResponse(self, id, text, isPublic):
        if not isPublic:
            loss, probabilities = self.forward(text)

            prediction = LABELS[np.argmax(probabilities)]
            certainty = np.max(probabilities)
            

            response = f"Classified as: {prediction} ({certainty:.0%})"

            self.sendMessage(id, response)