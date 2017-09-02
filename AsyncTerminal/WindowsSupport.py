"""
Extends GenericSupport with the calls that assume a Windows environment
"""

import ctypes
from ctypes import wintypes
import msvcrt
import sys

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
        cls.__sendEnter()

    @classmethod
    def getChar(cls):
        # See docs at https://docs.python.org/3.6/library/msvcrt.html
        byteIn = msvcrt.getch()

        if byteIn == b'\x03':
            # Handle catching ctrl+C on windows
            sys.exit(1)
        else:
            return byteIn.decode("utf8")

    @classmethod
    def __sendEnter(cls):
        """
        Simulates a the enter key being pressed
            Used by close() to get the terminal to show a prompt on program exit (stupid wumbows)

        How this works:
            https://stackoverflow.com/questions/13564851/how-to-generate-keyboard-events-in-python
            https://msdn.microsoft.com/en-us/library/dd375731
        """

        user32 = ctypes.WinDLL('user32', use_last_error=True)

        INPUT_KEYBOARD = 1
        KEYEVENTF_KEYUP = 0x0002
        KEYEVENTF_UNICODE = 0x0004
        MAPVK_VK_TO_VSC = 0

        # C struct definitions

        wintypes.ULONG_PTR = wintypes.WPARAM

        class MOUSEINPUT(ctypes.Structure):
            _fields_ = (("dx", wintypes.LONG),
                        ("dy", wintypes.LONG),
                        ("mouseData", wintypes.DWORD),
                        ("dwFlags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", wintypes.ULONG_PTR))

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = (("wVk", wintypes.WORD),
                        ("wScan", wintypes.WORD),
                        ("dwFlags", wintypes.DWORD),
                        ("time", wintypes.DWORD),
                        ("dwExtraInfo", wintypes.ULONG_PTR))

            def __init__(self, *args, **kwds):
                super(KEYBDINPUT, self).__init__(*args, **kwds)
                # some programs use the scan code even if KEYEVENTF_SCANCODE
                # isn't set in dwFflags, so attempt to map the correct code.
                if not self.dwFlags & KEYEVENTF_UNICODE:
                    self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                         MAPVK_VK_TO_VSC, 0)

        class HARDWAREINPUT(ctypes.Structure):
            _fields_ = (("uMsg", wintypes.DWORD),
                        ("wParamL", wintypes.WORD),
                        ("wParamH", wintypes.WORD))

        class INPUT(ctypes.Structure):
            class _INPUT(ctypes.Union):
                _fields_ = (("ki", KEYBDINPUT),
                            ("mi", MOUSEINPUT),
                            ("hi", HARDWAREINPUT))

            _anonymous_ = ("_input",)
            _fields_ = (("type", wintypes.DWORD),
                        ("_input", _INPUT))

        LPINPUT = ctypes.POINTER(INPUT)

        def _check_count(result, func, args):
            if result == 0:
                raise ctypes.WinError(ctypes.get_last_error())
            return args

        user32.SendInput.errcheck = _check_count
        user32.SendInput.argtypes = (wintypes.UINT,  # nInputs
                                     LPINPUT,  # pInputs
                                     ctypes.c_int)  # cbSize

        # Send the key press

        ENTER_KEY = 13

        keydown = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=ENTER_KEY))
        user32.SendInput(1, ctypes.byref(keydown), ctypes.sizeof(keydown))

        keyup = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=ENTER_KEY, dwFlags=KEYEVENTF_KEYUP))
        user32.SendInput(1, ctypes.byref(keyup), ctypes.sizeof(keyup))