from config import *
from utils import *
from irc import *
import re

def Interjection(parsed):
    if parsed['event'] == 'PRIVMSG':
        if re.search('\slinux(?!\w)', parsed['event_msg'], re.IGNORECASE):
            sendMessage(CHANNEL, "I would just like to interject for a moment, what you know as Linux is in fact, GNU/Linux or as I have taken to calling it, Unity.")
