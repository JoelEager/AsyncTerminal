"""
Provides the nice, application-facing terminal IO calls design for use in asyncio loops
"""

import asyncio
import atexit

from .GenericSupport import GenericSupport

class __terminalState:
    """
    Internal state data
    """
    inputBuffer = ""
    osSupport = GenericSupport()
    inputHandlers = {None: []}

async def __bufferedReader():
    """
    Async task used to read and buffer input from the osSupport class
    """
    while True:
        # Get char and then append to prevent a race condition caused by the async await
        charIn = await __terminalState.osSupport.getInputChar()

        wasHandled = False
        for key, handlers in __terminalState.inputHandlers.items():
            if key is None or charIn in key:
                for handler in handlers:
                    asyncio.get_event_loop().call_soon(handler, charIn)
                    wasHandled = True

        if not wasHandled:
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

def registerInputHandler(callback, filterString=None):
    """
    Registers a callback for handling input
        All input handled by a callback will not be buffered so it won't be read by calls to readInput()
        Note that multiple callbacks can be registered for a given filter
    :param callback: The function to call. Must have one argument which will be the character that was inputed.
    :param filterString: If set the function will only be called if the character inputed is in this string
    """
    if filterString in __terminalState.inputHandlers:
        __terminalState.inputHandlers[filterString].append(callback)
    else:
        __terminalState.inputHandlers[filterString] = [callback]

def unregisterInputHandlers(filterString=None):
    """
    Unregisters all input handlers with the given filter
        If no filter is provided the input handlers without filters will be unregistered
    """
    __terminalState.inputHandlers[filterString] = []

def unregisterAllInputHandlers():
    """
    Unregisters all input handlers regardless of filter
    """
    __terminalState.inputHandlers = {None: []}

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