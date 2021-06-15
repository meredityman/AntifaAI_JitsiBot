from app.interaction.hatespeech import HateSpeech
from .gpt2 import GPT2
from .survey import Survey
from .incidents import Incidents
from .hatespeech import HateSpeech
from .telegram import Telegram
from .twitter import Twitter
from .echo import Echo

interactionTypes = {
    'none'      : None,
    # 'echo'      : Echo,
    # 'gpt2'      : GPT2,
    'survey'    : Survey,
    'incidents' : Incidents,
    'hatespeech': HateSpeech,
    'telegram'  : Telegram,
    'twitter'   : Twitter
}



INTERACTION_TYPES = list(interactionTypes.keys())

DEFAULT_ENGINE_CONFIG = {
    'ids' : [],
    'type': 'none',
}

