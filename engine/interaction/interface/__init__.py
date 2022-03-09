from .echo       import Echo
from .survey     import Survey
from .hatespeech import Hatespeech
from .telegram   import Telegram
from .telegram   import LTelegram
from .twitter    import Twitter
from .twitter    import LTwitter
from .incidents  import Incidents


INTERFACES = {
    "Echo"              : Echo,
    "Survey"            : Survey,
    "Hatespeech"        : Hatespeech,
    "Telegram"          : Telegram,
    "Telegram Rating"   : LTelegram,
    "Twitter"           : Twitter,
    "Twitter Rating"    : LTwitter,
    "Incidents"         : Incidents,
}
