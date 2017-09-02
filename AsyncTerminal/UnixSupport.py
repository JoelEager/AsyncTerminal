"""
Extends GenericSupport with the calls that assume a Linux or Mac environment
"""

import sys
import termios
import tty

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

    @classmethod
    def getChar(cls):
        return sys.stdin.read(1)