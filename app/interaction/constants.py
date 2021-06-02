from .interaction import Echo, Survey, StatsBot

interactionTypesPrivate = {
    'none'  : None,
    'echo'  : Echo,
    'survey': Survey
}

interactionTypesPublic = {
    'none'  : None,
    'echo'  : Echo,
    'stats' : StatsBot,
}

INTERACTION_TYPES_PUBLIC  = list(interactionTypesPublic.keys())
INTERACTION_TYPES_PRIVATE = list(interactionTypesPrivate.keys())

DEFAULT_ENGINE_CONFIG = {
    'ids' : [],
    'private-type': 'none',
    'public-type': 'none'
}

