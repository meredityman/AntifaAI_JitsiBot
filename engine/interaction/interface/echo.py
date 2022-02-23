# from .interaction import InteractionEngine

# class Echo(InteractionEngine):
#     def _getResponse(self, id, text, isPublic):
#         if isPublic:
#             self.broadcastCallback(text)
#         else:
#             self.callback(text)

#     def _reset():
#         pass

#     def _setup(self):
#         pass
from .interface import Interface

class Echo(Interface) :

    def __init__(self, users = []):
        super().__init__()

    def message(self, user : str, data : dict) -> list:
        channel = data["channel"]
        message = data["message"]

        return [
            {
                "channel" : channel,
                "message" : f"{user}:{channel} -> '{message}'"
            }
        ]