from .interaction import InteractionEngine

class Echo(InteractionEngine):
    def _getResponse(self, id, text, isPublic):
        if isPublic:
            self.broadcastCallback(text)
        else:
            self.callback(text)

    def _reset():
        pass

    def _setup(self):
        pass

