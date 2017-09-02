"""
Extends GenericSupport with the calls that assume a Windows environment
"""

import ctypes
from ctypes import wintypes
import msvcrt
import sys
import asyncio

from .GenericSupport import GenericSupport

class WindowsSupport(GenericSupport):
    """
    See docs in GenericSupport.py
    """
    OSEnvironment = "Windows"

    @classmethod
    def setup(cls):
        return cls

    @classmethod
    def cleanup(cls):
        print("Windows exit")

    @classmethod
    async def getChar(cls):
        # See docs at https://docs.python.org/3.6/library/msvcrt.html

        while True:
            # Make sure key is pressed before reading it
            if msvcrt.kbhit():
                byteIn = msvcrt.getch()
                return byteIn.decode("utf8")
            else:
                await asyncio.sleep(0.1)

    @classmethod
    def print(cls, message):
        print(message, end="")