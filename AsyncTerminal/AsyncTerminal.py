"""
Provides the nice, application-facing terminal IO calls with support for use in asyncio loops
"""

import asyncio

# Configure AsyncTerminal
try:
    # Attempt to instantiate UnixSupport
    from .UnixSupport import UnixSupport
    osSupport = UnixSupport.setup()
except ImportError:
    # That doesn't work so assume windows
    from .WindowsSupport import WindowsSupport
    osSupport = WindowsSupport.setup()

__inputBuffer = ""

async def bufferedReaderTask():
    global __inputBuffer

    try:
        while True:
            __inputBuffer += await asyncio.get_event_loop().run_in_executor(None, osSupport.getChar)
    except asyncio.CancelledError as e:
        # Quit nicely
        raise e

def readBuffer(clearBuffer=True):
    global __inputBuffer

    chars = __inputBuffer

    if clearBuffer:
        __inputBuffer = ""

    return chars

def isInputWaiting():
    return __inputBuffer != ""