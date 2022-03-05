from .interface import Interface


class Echo(Interface) :

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def message(self, user : str, data : dict) -> list:
        channel = data["channel"]
        message = data["message"]

        return [{
                "channel" : channel,
                "message" : message,
                "user"    : user
        }]
