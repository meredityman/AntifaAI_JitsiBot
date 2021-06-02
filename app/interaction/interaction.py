
class InteractionEngine:
    def __init__(self):

        self.setup()

    def sendPublicMessage(self, id, message):
        if self.publicSendCallback:
            self.publicSendCallback(id, message)

    def sendPrivateMessage(self, id, message):
        if self.privateSendCallback:
            self.privateSendCallback(id, message)

    def reset(self):
        pass

    def setup(self):
        pass

    def getResponse(self, id, text, callback, broadcastCallback = None, selected_ids = []):
        raise NotImplementedError()


class Echo(InteractionEngine):
    def getResponse(self, id, text, callback):
        callback(text)
