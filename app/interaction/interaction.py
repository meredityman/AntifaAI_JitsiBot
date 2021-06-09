
class InteractionEngine:
    def __init__(self, callback = None, broadcastCallback = None, ids = []):
        self.callback = callback
        self.broadcastCallback = broadcastCallback
        self.ids = ids
        self.setup()

    def sendBroadcastMessage(self, message):
        if self.broadcastCallback:
            print(f"Sending broadcase message/n'{message}'")
            self.broadcastCallback(message)
        else:
            print("No broadcast callback set")

    def sendMessage(self, id, message):
        if self.callback:
            print(f"Sending message to {id}/n'{message}'")
            self.callback(id, message)
        else:
            print("No callback set")


    def getResponse(self, id, text):
        return self._getResponse(id, text)

    def reset(self):
        self._reset()

    def setup(self):
        self._setup()

    def _reset():
        raise NotImplementedError()

    def _setup(self):
        raise NotImplementedError()

    def _getResponse(self, id, text):
        raise NotImplementedError()


class SingleGeneratorEngine(InteractionEngine):
    def reset(self):
        self.generator = self._generator()
        self._reset()


    def setup(self):
        self.reset()
        self._setup()

    def iterateGenerator(self):
        try:
            next(self.generator)
        except StopIteration:
            print("Generator Complete")   


    def _generator(self):
        yield
        raise NotImplementedError()

    def _getResponse(self, id, text):
        self.id   = id
        self.text = text
        self.iterateGenerator()



class MultiGeneratorEngine(InteractionEngine):


    def reset(self):
        self.generators = {}
        for id in self.ids:
            self.generators[id] = self._generator()
        self._reset()

    def setup(self):
        self.reset()
        self._setup()

    def iterateAllGenerators(self):
        for id in self.ids:
            try:
                self.id = id
                next(self.generators[id])
            except StopIteration:
                print(f"Generator {id} Complete")   

    def iterateGenerator(self):
        try:
            next(self.generators[self.id])
        except StopIteration:
            print("Generator Complete")   
        except NameError:
            print("No id set")  


    def _generator(self):
        yield
        raise NotImplementedError()

    def _getResponse(self, id, text):
        self.id   = id
        self.text = text
        self.iterateGenerator()



class Echo(InteractionEngine):
    def getResponse(self, id, text):
        self.callback(text)
