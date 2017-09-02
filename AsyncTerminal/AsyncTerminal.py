"""
Provides the nice, application-facing terminal IO calls with support for use in asyncio loops
"""

import asyncio
import atexit

from .GenericSupport import GenericSupport

# Internal state data
class __terminalState:
    inputBuffer = ""
    osSupport = GenericSupport()

async def __bufferedReader():
    """
    Async task used to read and buffer input from the osSupport class
    """
    while True:
        # Get char and then append to prevent a race condition caused by the async await
        charIn = await __terminalState.osSupport.getInputChar()
        __terminalState.inputBuffer += charIn

def readInput():
    """
    :return: A string containing all waiting input
    """
    chars = __terminalState.inputBuffer
    __terminalState.inputBuffer = ""
    return chars

def isInputWaiting():
    """
    :return: True input is waiting in the buffer, False if not
    """
    return __terminalState.inputBuffer != ""

def writeln(message):
    """
    Writes the given message to the terminal and advances to the next line
    """
    write(message + "\n")

def write(message):
    """
    Writes the given message to the terminal
    """
    __terminalState.osSupport.print(message)

def endTasks():
    """
    Ends any asyncio tasks spawned by AsyncTerminal
        Call before ending the asyncio loop to ensure a clean exit
    """
    __terminalState.bufferedReaderTask.cancel()

# AsyncTerminal setup logic
try:
    # Attempt to instantiate UnixSupport
    from .UnixSupport import UnixSupport
    __terminalState.osSupport = UnixSupport.setup()
except ImportError:
    # That doesn't work so assume windows
    from .WindowsSupport import WindowsSupport
    __terminalState.osSupport = WindowsSupport.setup()

# Register bufferedReaderTask with asyncio
__terminalState.bufferedReaderTask = asyncio.get_event_loop().create_task(__bufferedReader())

# Register the cleanup function to be called on program end to make sure the terminal is left in an usable state
atexit.register(__terminalState.osSupport.cleanup)