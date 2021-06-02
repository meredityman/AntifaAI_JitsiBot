from app.interaction.constants import *
from .interaction import *
from .constants import *

class Engine():

    def __init__(self):
        self.privateInteractionEngine = None
        self.publicInteractionEngine  = None
        self.privateInteractionType   = None
        self.publicInteractionType    = None
        self.setup(DEFAULT_ENGINE_CONFIG)
    
    def setup(self, args, publicSendCallback = None, privateSendCallback = None):
        print(args)

        self.publicSendCallback  = publicSendCallback  
        self.privateSendCallback = privateSendCallback 

        requestedPublicType  = args['public-type']
        requestedPrivateType = args['private-type']

        print(f"Requesting public {requestedPublicType}")
        print(f"Requesting private {requestedPrivateType}")

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

            else:
                print(f"Interaction type '{requestedPublicType}' not recognized")

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

            else:
                print(f"Interaction type '{requestedPrivateType}' not recognized")



    def feedEnginePublic(self, client, id, text):
        if self.publicInteractionEngine is not None:
            self.publicInteractionEngine.getResponse(id, text, self.publicSendCallback)
        else:
            print(f"No engine for public message from {id}")


    def feedEnginePrivate(self, client, id, selected_ids, text):
        if self.privateInteractionEngine is not None:
            self.privateInteractionEngine.getResponse(id, text, lambda message : self.privateSendCallback(id, message), self.publicSendCallback, selected_ids)
        else:
            print(f"No engine for private message from {id}")

engine = Engine()