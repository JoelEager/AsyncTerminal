# Check Python version
import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    print("Python 3.5 or newer is required to run AsyncTerminal")
    sys.exit(1)
    
from .AsyncTerminal import *