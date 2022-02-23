from app.interaction.constants import *
from .interaction import *
from .constants import *

# class Engine():

#     def __init__(self):
#         self.interactionEngine = None
#         self.interactionType   = None
#         self.setup(DEFAULT_ENGINE_CONFIG)
    
#     def get_commands(self):
#         if(self.interactionEngine):
#             return self.interactionEngine.commands
#         else:
#             return []

#     def set_ids(self, args):
#         self.ids = args['ids']   

#         if self.interactionEngine:
#             self.interactionEngine.setIds(self.ids)

#     def setup(self, args, publicSendCallback = None, privateSendCallback = None):
#         print(args)

#         requestedType  = args['type']
#         self.ids = args['ids']

#         print(f"Requesting public {requestedType}")

#         if requestedType:
#             if requestedType in interactionTypes:
#                 if self.interactionType == requestedType:
#                     print(f"Reseting Private Engine - {requestedType}")
#                     if self.interactionEngine is not None:
#                         self.interactionEngine.reset()
#                 else:
#                     print(f"Creating private Engine - {requestedType}")
#                     c = interactionTypes[requestedType]
#                     if c:
#                         self.interactionEngine = c(callback = privateSendCallback,  broadcastCallback = publicSendCallback, ids = self.ids)
#                     else:
#                         self.interactionEngine = None

#                 self.interactionType = requestedType

#             else:
#                 print(f"Interaction type '{requestedType}' not recognized")



#     def feedEnginePublic(self, id, text):
#         if self.interactionEngine is not None:
#             self.interactionEngine.getResponsePublic(id, text)
#         else:
#             print(f"No engine for public message from {id}")


#     def feedEnginePrivate(self, id, text):
#         if self.interactionEngine is not None:
#             print(f"Feeding engine {id} <- {text}")
#             self.interactionEngine.getResponsePrivate(id, text)
#         else:
#             print(f"No engine for private message from {id}")

# engine = Engine()