
class InteractionEngine:
    def __init__(self):
        pass

    def reset(self):
        pass

    def getResponse(self, id, text):
        raise NotImplementedError()


class Echo(InteractionEngine):
    def getResponse(self, id, text):
        return text

class Survey(InteractionEngine):
    def getResponse(self, id, text):
        return text


class StatsBot(InteractionEngine):
    def getResponse(self, id, text):
        if text == 'marco':
            return 'polo!'
        else:
            return None