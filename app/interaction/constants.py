from app.interaction.hatespeech import HateSpeech
from .interaction import Echo
from .gpt2 import GPT2
from .survey import Survey
from .incidents import Incidents
from .hatespeech import HateSpeech

interactionTypesPrivate = {
    'none'  : None,
    'echo'  : Echo,
    'gpt2'  : GPT2,
    'survey': Survey,
    'incidents': Incidents,
    'hatespeech': HateSpeech
}

interactionTypesPublic = {
    'none'  : None,
    'echo'  : Echo,
}

INTERACTION_TYPES_PUBLIC  = list(interactionTypesPublic.keys())
INTERACTION_TYPES_PRIVATE = list(interactionTypesPrivate.keys())

DEFAULT_ENGINE_CONFIG = {
    'ids' : [],
    'private-type': 'none',
    'public-type': 'none'
}

