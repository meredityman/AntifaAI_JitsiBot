
class InteractionEngine:
    def __init__(self, callback = None, broadcastCallback = None, ids = []):
        self.callback = callback
        self.broadcastCallback = broadcastCallback
        self.ids = ids
        self.setup()

    def sendBroadcastMessage(self, message):
        if self.broadcastCallback:
            print(f"Sending broadcase message to {id}/n'{message}'")
            self.broadcastCallback(message)
        else:
            print("No broadcast callback set")

    def sendMessage(self, id, message):
        if self.callback:
            print(f"Sending message to {id}/n'{message}'")
            self.callback(id, message)
        else:
            print("No callback set")

    def reset(self):
        pass

    def setup(self):
        pass

    def getResponse(self, id, text):
        raise NotImplementedError()


class Echo(InteractionEngine):
    def getResponse(self, id, text):
        self.callback(text)
