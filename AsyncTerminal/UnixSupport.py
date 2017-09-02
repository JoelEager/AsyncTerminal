"""
Extends GenericSupport with the calls that assume a Linux or Mac environment

How this works:
    http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
"""

import sys
import termios
import tty
import select
import asyncio

from .GenericSupport import GenericSupport

class UnixSupport(GenericSupport):
    """
    See docs in GenericSupport.py
    """
    OSEnvironment = "Linux/Mac"
    __oldSettings = None

    @classmethod
    def setup(cls):
        stdinFile = sys.stdin.fileno()
        cls.__oldSettings = termios.tcgetattr(stdinFile)
        tty.setraw(stdinFile)

        return cls

    @classmethod
    def cleanup(cls):
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, cls.__oldSettings)
        print("Unix exit")

    @classmethod
    async def getChar(cls):
        while True:
            stdinFile = select.select([sys.stdin], [], [], 0.0)[0]

            # Make sure key is pressed before reading it
            if stdinFile:
                return stdinFile[0].buffer.read(1).decode("utf8")
            else:
                await asyncio.sleep(0.1)

    @classmethod
    def print(cls, message):
        sys.stdout.write(message)

        if message.endswith("\n"):
            # Return the cursor to the left side of the screen
            sys.stdout.write(u"\u001b[1000D")