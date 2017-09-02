import atexit

from .AsyncTerminal import *

# Register bufferedReaderTask with asyncio
asyncio.get_event_loop().create_task(bufferedReaderTask())

# Register the cleanup function to get called on exit of the program
atexit.register(osSupport.cleanup)