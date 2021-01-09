from IRCMessage import IRCMessage

# ----------------------------------------------------------------------- #
# https://github.com/aidenwallis/irc-message-ts/blob/master/src/parser.ts
# translated to python


# added this because in js when you try to get something from an array,
# it doesnt throw an error for out of index, but in python it does
def getLetterAtIndexWithoutError(string, index: int, alt=None):
    try:
        return string[index]
    except IndexError:
        return alt

def parseIRC(line: str) -> IRCMessage or None:
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
            message.tags[pair[0]] = getLetterAtIndexWithoutError(pair, 1, alt="")

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
            message.params.append(line[position + 1: -1] + line[-1])
            break
    
        # If we still have some whitespace...
        if nextspace != -1:
            # Push whatever's between the current position and the next
            # space to the params array.
            message.params.append(line[position: nextspace])
            position = nextspace + 1

            # Skip any trailing whitespace and continue looping.
            while line[position] == " ": 
                position += 1
            continue

        # If we don't have any more whitespace and the param isn't trailing,
        # push everything remaining to the params array.
        if nextspace == -1:
            message.params.append(line[position: -1] + line[-1])
            break

    # Add the param property
    if len(message.params) > 0:
        message.param = message.params[0]

        # Add the trailing param
        if len(message.params) > 1:
            message.trailing = message.params[len(message.params) - 1]
    
    return message
