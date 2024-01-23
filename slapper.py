try:
    import weechat
    IMPORT_OK = True
except ImportError:
    print('This script must be run under the instance of WeeChat.')
    print('Get WeeChat now at: https://weechat.org/')
    IMPORT_OK = False
import random
from collections import deque

SCRIPT_NAME = "Slapper"
SCRIPT_AUTHOR = "ComputerTech"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Provides a /slap command for WeeChat with non-repeating, customizable parts"

# Define the parts of the slap messages
VERBS = ["slaps", "whacks", "beats", "uses", "pokes", "smacks", "thumps", "bops", "wallops", "swats"]
PHRASES = ["around a bit", "something else here", "with all their might", "like a ragdoll", "gently", "furiously", "in jest", "for fun", "without mercy", "playfully"]
CONNECTORS = ["with a", "using a", "holding a", "armed with a", "brandishing a", "wielding a", "sporting a", "flaunting a", "equipped with a", "clutching a"]
ITEMS = ["large trout", "rubber chicken", "foam sword", "wet noodle", "giant flyswatter", "rolled-up newspaper", "plastic bat", "feather duster", "stuffed animal", "balloon animal"]

# Initialize queues for recently used parts
RECENT_VERBS = deque(maxlen=5)
RECENT_PHRASES = deque(maxlen=5)
RECENT_CONNECTORS = deque(maxlen=5)
RECENT_ITEMS = deque(maxlen=5)

def get_unique_part(part_list, recent_parts):
    part = random.choice(part_list)
    while part in recent_parts:
        part = random.choice(part_list)
    recent_parts.append(part)
    return part

def slap_cb(data, buffer, args):
    argv = args.strip().split(" ")
    if len(argv) < 1 or argv[0] == "":
        weechat.command(buffer, "/help slap")
        return weechat.WEECHAT_RC_OK

    nick = argv[0]
    amount = 1
    if len(argv) > 2 and argv[1] == "-a":
        try:
            amount = int(argv[2])
        except ValueError:
            weechat.prnt(buffer, "Invalid amount specified.")
            return weechat.WEECHAT_RC_OK

    for i in range(amount):
        verb = get_unique_part(VERBS, RECENT_VERBS)
        phrase = get_unique_part(PHRASES, RECENT_PHRASES)
        connector = get_unique_part(CONNECTORS, RECENT_CONNECTORS)
        item = get_unique_part(ITEMS, RECENT_ITEMS)
        message = f"/me {verb} {nick} {phrase} {connector} {item}"
        weechat.command(buffer, message)

    return weechat.WEECHAT_RC_OK

if __name__ == "__main__":
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        weechat.hook_command("slap", "Slap someone with a random object", "<nick> [-a <amount>]", "nick: nickname of the person to slap\n-a, --amount: the number of times to slap the person\n", "", "slap_cb", "")
