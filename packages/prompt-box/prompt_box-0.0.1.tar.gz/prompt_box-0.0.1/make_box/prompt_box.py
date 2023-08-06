import ctypes
from ctypes.wintypes import HWND, LPWSTR, UINT

_user32 = ctypes.WinDLL('user32', use_last_error=True)

_MessageBoxW = _user32.MessageBoxW
_MessageBoxW.restype = UINT 
_MessageBoxW.argtypes = (HWND, LPWSTR, LPWSTR, UINT)


def MessageBoxW(hwnd, text, caption, utype):
    result = _MessageBoxW(hwnd, text, caption, utype)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return result


def message(text, title, yes, no, cancel, error):
    MB_YESNOCANCEL = 3

    IDCANCEL = 2
    IDYES = 6
    IDNO = 7
    
    result = MessageBoxW(None, text, title, MB_YESNOCANCEL)

    if result == IDYES:
        print(yes)
    elif result == IDNO:
        print(no)
    elif result == IDCANCEL:
        print(cancel)
    else:
        print(error)
        
"""
Example use of message:
    
import window

window.message('Hello', 'Neutrino', 'Yes clicked', 'No clicked', 'Cancel clicked', 'Error')

"""

def alert(text):
    MessageBoxW(None, text, 'Alert', 0)




