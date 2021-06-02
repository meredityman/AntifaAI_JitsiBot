from app.interaction.constants import *
from .interaction import *
from .constants import *

class Engine():

    def __init__(self):
        self.privateInteractionEngine = None
        self.publicInteractionEngine  = None
        self.privateInteractionType   = None
        self.publicInteractionType    = None
        self.ids = []
        self.setup(DEFAULT_ENGINE_CONFIG)
    
    def setup(self, args):
        print(args)
        requestedPublicType  = args['public-type']
        requestedPrivateType = args['private-type']
        self.ids = args['ids']

        if requestedPrivateType:
            if requestedPrivateType in interactionTypesPrivate:
                if self.privateInteractionType == requestedPrivateType:
                    print(f"Reseting Private Engine - {requestedPrivateType}")
                    if self.privateInteractionEngine is not None:
                        self.privateInteractionEngine.reset()
                else:
                    print(f"Creating private Engine - {requestedPrivateType}")
                    c = interactionTypesPrivate[requestedPrivateType]
                    if c:
                        self.privateInteractionEngine = c()

                self.privateInteractionType = requestedPrivateType

        if requestedPublicType:
            if requestedPublicType in interactionTypesPublic:
                if self.publicInteractionType == requestedPublicType:
                    print(f"Reseting Public Engine - {requestedPublicType}")
                    if self.publicInteractionEngine is not None:
                        self.publicInteractionEngine.reset()
                else:
                    print(f"Creating public Engine - {requestedPublicType}")
                    c = interactionTypesPublic[requestedPublicType]
                    if c:
                        self.publicInteractionEngine  = c()
                self.publicInteractionType = requestedPublicType


    def getPrivateResponse(self, client, id, text):
        if self.privateInteractionEngine is None:
            return None

        if( id not in self.ids ):
            print(f"Participant {id} not selected fro private chat")
            return None

        return self.privateInteractionEngine.getResponse(id, text)


    def getPublicResponse(self, client, id, text):
        if self.publicInteractionEngine:
            return self.publicInteractionEngine.getResponse(id, text)
        else:
            print("No public engine")
            return None


engine = Engine()