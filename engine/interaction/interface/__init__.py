from .echo import Echo
from .survey import Survey
from .hatespeech import Hatespeech
from .telegram import Telegram
from .twitter import Twitter


INTERFACES = {
    "Echo" : Echo,
    "Survey" : Survey,
    "Hatespeech" : Hatespeech,
    "Telegram" : Telegram,
    "Twitter" : Twitter,
}
