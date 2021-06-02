from .interaction import InteractionEngine


class GPT2(InteractionEngine):

    def setup(self):
        from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline

        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/german-gpt2")
        self.model = AutoModelWithLMHead.from_pretrained("dbmdz/german-gpt2")

        self.pipe = pipeline('text-generation', model="dbmdz/german-gpt2",
                 tokenizer="dbmdz/german-gpt2")

    def getResponse(self, id, text, callback, broadcastCallback = None, selected_ids = []):
        response = self.pipe(text, max_length=100)[0]["generated_text"]
        callback(response)