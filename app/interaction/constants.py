from .interaction import Echo
from .gpt2 import GPT2
from .survey import Survey

interactionTypesPrivate = {
    'none'  : None,
    'echo'  : Echo,
    'gpt2'  : GPT2,
    'survey': Survey
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

