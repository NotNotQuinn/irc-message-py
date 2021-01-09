# irc-message-py

![](https://cdn.frankerfacez.com/emote/145947/4)

yo, this is only ***partially*** translated to python, I dont understand how all 
that stream stuff works and I didnt bother even looking at it tbh, I'm not intrested.
My idea of what this is is sort of a file you can drop into a folder, and it'll just 
work

If you want to translate that part too, then you can open a pull request & I'll 
merge if it looks like it works.

## How I suggest you use this
Just drop [this file](./src/IRCParser.py) into your project folder and use it as you
wish

## "Example"
This is sort of how I might use this, but I would not try to scale this code up to
more than a few commands, because it will get very hard to debug. What I would 
recommend is to parse the parsed values even more, and give that off to a helper 
function that returns an object with information about how to respond

eg.
  * message
  * channel
  * anything else you can think of
    * whether banphrases are affected by it if there are any
    * whether to send it as an "action" ( /me )
    * I really do mean anything else...

### Example Code
```python
import socket
from IRCparser import parseIRC

# we can connect any way we want, this is an easy way to do it
# I dont know if its secure though
conn = socket.socket()
conn.connect(("irc.chat.twitch.tv", 6667))

# less typing
def sendRaw(data: str):
    conn.send(bytes(data + '\r\n', 'utf-8'))

# login as anon
sendRaw("PASS oauth:x") 
sendRaw("NICK justinfan123")

# request tags
sendRaw("CAP REQ :twitch.tv/tags")

# join any channel, I joined mine
sendRaw("JOIN #quinndt")

# would not recommend putting a loop on global level like this :)
# try putting it in a function
while True:
    rawDataSplit = conn.recv(2048).decode("utf-8").split("\r\n")
    for rawMessage in rawDataSplit:
        user = {}
        msg = parseIRC(rawMessage)
        if not msg: 
            continue  # or break

        # set some useful properties in this user object. aka "parse the parsed values"
        user['username'] = msg.prefix[:msg.prefix.find("!")]

        if msg.command != "PRIVMSG":
            # print the raw so we can see the comunication
            print(msg.raw)
            
        if msg.command == "PRIVMSG":
            # print message
            print(f"[{msg.param}] <{user['username']}>: {msg.trailing}")

            # a basic command
            if msg.trailing.split()[0] == "-ping":

                for i in range(10):
                    # so we can see it worked
                    print("pong!")
                responce = "Pong!"

                # because we are logged in as anon we get no responce from 
                # twitch about this PRIVMSG and it doesnt show up in chat
                sendRaw(f"PRIVMSG :{responce}") 

        if msg.command == "PING": 
            # pings come every 5 mins about
            # if we dont respond we will be disconnected
            sendRaw(f"PONG :{msg.trailing}")
```
### Example Output
```txt
:tmi.twitch.tv 001 justinfan123 :Welcome, GLHF!
:tmi.twitch.tv 002 justinfan123 :Your host is tmi.twitch.tv
:tmi.twitch.tv 003 justinfan123 :This server is rather new
:tmi.twitch.tv 004 justinfan123 :-
:tmi.twitch.tv 375 justinfan123 :-
:tmi.twitch.tv 372 justinfan123 :You are in a maze of twisty passages, all alike.
:tmi.twitch.tv 376 justinfan123 :>
:tmi.twitch.tv CAP * ACK :twitch.tv/tags
:justinfan123!justinfan123@justinfan123.tmi.twitch.tv JOIN #quinndt
:justinfan123.tmi.twitch.tv 353 justinfan123 = #quinndt :justinfan123    
:justinfan123.tmi.twitch.tv 366 justinfan123 #quinndt :End of /NAMES list
[#quinndt] <quinndt>: :) Hello!
[#quinndt] <quinndt>: -ping
pong!
pong!
pong!
pong!
pong!
pong!
pong!
pong!
pong!
pong!

```
## Contributing
If you wish to contribute and change something make sure that when you run [IRCParser.spec.py](./src/IRCParser.spec.py) there are no errrors.
