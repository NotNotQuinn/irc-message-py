# https://github.com/aidenwallis/irc-message-ts/blob/master/src/types.ts
# translated to python

class IRCMessage:
    def __init__(self, command: str or None, prefix: str or None, tags: dict, params: list, raw: str, param: str, trailing: str):
        """A class to store"""
        self.command = command
        self.prefix = prefix
        self.tags = tags
        self.params = params
        self.raw = raw
        self.param = param
        self.trailing = trailing

    # I added this for conveinece
    @staticmethod
    def empty():
        """All defalt peramiters"""
        return IRCMessage(command=None, prefix=None, tags={}, params=[], raw="", param="", trailing="")
