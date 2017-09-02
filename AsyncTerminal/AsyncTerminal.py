"""
Provides the nice, application-facing terminal IO calls with support for use in asyncio loops
"""

import asyncio
import atexit

# Configure AsyncTerminal
try:
    # Attempt to instantiate UnixSupport
    from .UnixSupport import UnixSupport
    osSupport = UnixSupport.setup()
except ImportError:
    # That doesn't work so assume windows
    from .WindowsSupport import WindowsSupport
    osSupport = WindowsSupport.setup()

class __data:
    inputBuffer = ""

async def bufferedReaderTask():
    while True:
        # Get char and then append to prevent a race condition caused by the async await
        charIn = await osSupport.getChar()
        __data.inputBuffer += charIn

def readBuffer(clearBuffer=True):
    chars = __data.inputBuffer

    if clearBuffer:
        __data.inputBuffer = ""

    return chars

def isInputWaiting():
    return __data.inputBuffer != ""

def writeln(message):
    write(message + "\n")

def write(message):
    osSupport.print(message)

# Register bufferedReaderTask with asyncio
asyncio.get_event_loop().create_task(bufferedReaderTask())

# Register the cleanup function to get called on exit of the loop
atexit.register(osSupport.cleanup)