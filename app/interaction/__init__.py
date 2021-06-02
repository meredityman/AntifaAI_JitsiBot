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
        ids = args['ids']

        if requestedPrivateType:
            if requestedPrivateType in interactionTypesPrivate:
                if self.privateInteractionType == requestedPrivateType:
                    print(f"Reseting Private Engine - {requestedPrivateType}")
                    if self.privateInteractionEngine:
                        self.privateInteractionEngine.reset()
                    else:
                        print("errrorrrr")
                else:
                    print(f"Creating private Engine - {requestedPrivateType}")
                    c = interactionTypesPrivate[requestedPrivateType]
                    if c:
                        self.privateInteractionEngine = c()
                    else:
                        print("errrorrrr")

                self.privateInteractionType = requestedPrivateType

        if requestedPublicType:
            if requestedPublicType in interactionTypesPublic:
                if self.publicInteractionType == requestedPublicType:
                    print(f"Reseting Public Engine - {requestedPublicType}")
                    if self.privateInteractionEngine:
                        self.publicInteractionEngine.reset()
                    else:
                        print("errrorrrr")
                else:
                    print(f"Creating public Engine - {requestedPublicType}")
                    c = interactionTypesPublic[requestedPublicType]
                    if c:
                        self.publicInteractionEngine  = c()
                    else:
                        print("errrorrrr")
                self.publicInteractionType = requestedPublicType


    def getPrivateResponse(self, client, id, text):
        if self.privateInteractionEngine is None:
            return None

        if( id not in self.ids ):
            return None

        return self.privateInteractionEngine.getResponse(id, text)


    def getPublicResponse(self, client, id, text):
        if self.privateInteractionEngine:
            return self.privateInteractionEngine.getResponse(id, text)
        else:
            print("No public engine")
            return None


engine = Engine()