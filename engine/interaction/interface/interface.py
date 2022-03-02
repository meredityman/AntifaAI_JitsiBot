
class Interface:
    def __init__(self, **kwargs):
        self.users = set([])
        print("interface.__init__", kwargs)
        if "users" in kwargs:
            for user in kwargs["users"]:
                self.users.add(user)
        else:
            raise
                

    def message(self, user : str, data : dict) -> list:
        raise NotImplementedError()

    def start(self) -> list:
        return []

    def stop(self) -> list:
        return []

class MultiUserGenerator(Interface):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_user = None
        self.last_data = None
        self.dirty     = False
        self.replies   = []

    def message(self, user : str, data : dict) -> list:
        self.channel = data["channel"]

        if user not in self.users:
            print(f"User '{user}' not registered! Registering...")
            self.users.add(user)

        self.last_data   = data
        self.last_user   = user
        self.iterateGenerator()

        return self.reply()

    def start(self) -> list:
        self.generator = self.generatorFunc()
        self.iterateGenerator()
        return self.reply()

    def reply(self):
        replies = self.replies
        self.replies = []
        return replies

    def stop(self) -> list:
        self.iterateGenerator()
        return self.reply()

    def iterateGenerator(self):
        try:
            next(self.generator)
        except StopIteration:
            print("Generator Complete")   

    # def _onSetIds(self):
    #     self.text = None
    #     self.id = None
    #     self.iterateGenerator()

    def generatorFunc(self):
        yield
        raise NotImplementedError()



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
