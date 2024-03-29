
class InteractionEngine:
    def __init__(self, callback = None, broadcastCallback = None, ids = []):
        self.callback = callback
        self.broadcastCallback = broadcastCallback
        self.ids = ids
        self.isPublic = None
        self.commands = {}
        self.setup()


    def setIds(self, ids):
        self.ids = ids
        self._onSetIds()

    def sendBroadcastMessage(self, message):
        if self.broadcastCallback:
            print(f"Sending broadcase message\n'{message}'")
            self.broadcastCallback(message)
        else:
            print("No broadcast callback set")

    def sendMessage(self, id, message):
        if self.callback:
            print(f"Sending message to {id}\n'{message}'")
            self.callback(id, message)
        else:
            print("No callback set")

    def sendMessageAll(self, message):
        if self.callback:
            for id in self.ids:
                print(f"Sending message to {id}\n'{message}'")
                self.callback(id, message)
        else:
            print("No callback set")

    def getResponsePublic(self, id, text):
        self.isPublic = True
        return self._getResponse(id, text, self.isPublic)

    def getResponsePrivate(self, id, text):
        self.isPublic = False
        return self._getResponse(id, text, self.isPublic)

    def reset(self):
        self._reset()

    def setup(self):
        self._setup()

    def _onSetIds(self):
        pass

    def _reset():
        raise NotImplementedError()

    def _setup(self):
        raise NotImplementedError()

    def _getResponse(self, id, text, isPublic):
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



    def _onSetIds(self):
        self.text = None
        self.id = None
        self.iterateGenerator()

    def _generator(self):
        yield
        raise NotImplementedError()

    def _getResponse(self, id, text, isPublic):
        self.isPublic = isPublic
        if id in self.ids or text in self.commands:
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
            except KeyError:
                pass
            except StopIteration:
                print(f"Generator {id} Complete")   

    def iterateGenerator(self):
        try:
            next(self.generators[self.id])
        except StopIteration:
            print("Generator Complete")   
        except NameError:
            print("No id set")  
        except KeyError:
            print("Waaah")


    def _onSetIds(self):
        self.text = None
        self.id = None
        self.iterateAllGenerators()

    def _generator(self):
        yield
        raise NotImplementedError()

    def _getResponse(self, id, text, isPublic):
        self.isPublic = isPublic

        if text in self.commands:
                self.id   = id
                self.text = text
                self.iterateGenerator()
        elif id in self.ids:
            if isPublic:
                print("Skipping Public message")
            else:
                self.id   = id
                self.text = text
                self.iterateGenerator()



