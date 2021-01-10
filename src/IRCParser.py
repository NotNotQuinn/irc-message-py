
"""
Copyright (c) 2013-2015, Fionn Kelleher
All rights reserved.
Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright 
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above 
copyright notice, this list of conditions and the following 
disclaimer in the documentation and/or other materials provided 
with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN 
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


# ---------------------------------------------------------------------- #
# https://github.com/aidenwallis/irc-message-ts/blob/master/src/types.ts
# translated to python


class IRCMessage:
    def __init__(self, 
                 command: str, 
                 prefix: str, 
                 tags: dict, 
                 params: list, 
                 raw: str, 
                 param: str, 
                 trailing: str):
        """A class to store a parsed IRC message"""
        self.command = command
        self.prefix = prefix
        self.tags = tags
        self.params = params
        self.raw = raw
        self.param = param
        self.trailing = trailing

    def __str__(self):
        # yes, I know, I know
        out = ""
        out += ("{\n")
        out += (f'    "command":  "{self.command}"\n')
        out += (f'    "param":    "{self.param}"\n')
        out += (f'    "params":   {self.params}\n')
        out += (f'    "prefix":   "{self.prefix}"\n')
        out += (f'    "raw":      "{self.raw}"\n')
        out += (f'    "tags":     {self.tags}\n')
        out += (f'    "trailing": "{self.trailing}"\n')
        out += ('}')

        return out

    # I added this for conveinece
    @staticmethod
    def empty():
        """All defalt peramiters"""
        return IRCMessage(command="", 
                          prefix="", 
                          tags={}, 
                          params=[], 
                          raw="", 
                          param="", 
                          trailing="")


# ----------------------------------------------------------------------- #
# https://github.com/aidenwallis/irc-message-ts/blob/master/src/parser.ts
# translated to python


# added this because in js when you try to get something from an array,
# it doesnt throw an error for out of index, but in python it does
def getLetterAtIndexWithoutError(string, index: int, alt=None):
    try:
        return string[index]
    except (IndexError, KeyError):
        return alt


def parseIRC(line: str) -> IRCMessage or None:
    """Takes in a raw IRC string and breaks it down into its basic components. 
    Returns `None` if there is an invalid IRC message otherwise, returns an 
    `IRCMessage` with the coresponding values
    """
    message = IRCMessage.empty() # all defalt values
    message.raw = line

    # position and nextspace are used by the parser as a reference.
    position = 0
    nextspace = 0

    # The first thing we check for is IRCv3.2 message tags.
    if line.startswith("@"):
        nextspace = line.find(" ")

        if nextspace == -1:
            # malformed IRC message
            return None
        
        # Tags are split by a semi colon.
        rawTags = line[1 : nextspace].split(";")

        i = 0
        while i < len(rawTags):
            # Tags delimited by an equals sign are key=value tags.
            # If there's no equals, we assign the tag a value of true.

            tag = rawTags[i]
            pair = tag.split("=")
            message.tags[pair[0]] = getLetterAtIndexWithoutError(pair, 1, alt=True)

            i += 1
        
        position = nextspace + 1
    
    # Skip any trailing whitespace.
    while getLetterAtIndexWithoutError(line, position) == " ":
        position += 1
    
    # Extract the message's prefix if present. Prefixes are prepended
    # with a colon.
    if getLetterAtIndexWithoutError(line, position) == ":":
        nextspace = line.find(" ", position)

        # If there's nothing after the prefix, deem this message to be
        # malformed.
        if nextspace == -1:
            # Malformed IRC message.
            return None

        message.prefix = line[position + 1: nextspace]
        position = nextspace + 1

        # Skip any trailing whitespace.
        while getLetterAtIndexWithoutError(line, position) == " ":
            position += 1
        
    nextspace = line.find(" ", position)

    # If there's no more whitespace left, extract everything from the
    # current position to the end of the string as the command.
    if nextspace == -1:
        if len(line) > position:
            message.command = line[position:]
            return message
        return None
    

    # Else, the command is the current position up to the next space. After
    # that, we expect some parameters.
    message.command = line[position:nextspace]

    position = nextspace + 1

    # Skip any trailing whitespace.
    while getLetterAtIndexWithoutError(line, position) == " ":
        position += 1
    

    while position < len(line):
        nextspace = line.find(" ", position)

        # If the character is a colon, we've got a trailing parameter.
        # At this point, there are no extra params, so we push everything
        # from after the colon to the end of the string, to the params array
        # and break out of the loop.
        if getLetterAtIndexWithoutError(line, position) == ":":
            message.params.append(line[position + 1:])
            break
    
        # If we still have some whitespace...
        if nextspace != -1:
            # Push whatever's between the current position and the next
            # space to the params array.
            message.params.append(line[position: nextspace])
            position = nextspace + 1

            # Skip any trailing whitespace and continue looping.
            while getLetterAtIndexWithoutError(line, position) == " ": 
                position += 1
            continue

        # If we don't have any more whitespace and the param isn't trailing,
        # push everything remaining to the params array.
        if nextspace == -1:
            message.params.append(line[position:])
            break

    # Add the param property
    if len(message.params) > 0:
        message.param = message.params[0]

        # Add the trailing param
        if len(message.params) > 1:
            message.trailing = message.params[len(message.params) - 1]
    
    return message
