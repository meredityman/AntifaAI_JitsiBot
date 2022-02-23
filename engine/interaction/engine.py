# from .interaction import *
# from .constants import *
from ast import In
import uuid


from .interface import INTERFACES

class Engine():

    def __init__(self):
        self.interfaces = { }

    def get_types(self) -> list:
        return list(INTERFACES.keys())

    def get_interfaces(self) -> list:
        return [{ 'interface_id' : n, 'type' : str(type(i)) } for n, i in  self.interfaces.items()]

    def start(self, interface_type, data):
        if interface_type in INTERFACES:
            new_id = str(uuid.uuid1())
            self.interfaces[new_id] = INTERFACES[interface_type](data)

            msgs = self.interfaces[new_id].start()

            return { 'success' : True, 'interface_id'  : new_id,  'messages' : msgs }
        else:
            return { 'success' : False, 'error'  : f"'{interface_type}' not available!" }


    def stop(self, interface_id, data):
        print(self.interfaces)
        if interface_id not in self.interfaces:
           return { 'success' : False, 'error'  : f"Interface does not exist '{interface_id}'" }

        msgs = self.interfaces[interface_id].stop()

        self.interfaces.pop(interface_id)
        return { 'success' : True, 'interface_id'  : interface_id,  'messages' : msgs }



    def message(self, interface_id, data):
        
        if interface_id not in self.interfaces:
           return { 'success' : False, 'error'  : f"Interface does not exist '{interface_id}'" }

        user = data["user"]
        if user == "":
           return { 'success' : False, 'error'  : f"Invalid user '{user}'" }

        interface = self.interfaces[interface_id]
        msgs = interface.message(user, data)

        return {
            'success' : True,
            'messages'  : msgs
        }

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