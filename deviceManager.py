import win32gui
import win32api
import win32con
import time
VK_CODE = {
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87, }





def mE_click(x, y):


    win32api.SetCursorPos((x, y))


    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

    time.sleep(.05)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def mE_flick(x, y):

    #save postition

    buffer = get_mouse_position()

    win32api.SetCursorPos((x, y))

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

    time.sleep(.05)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    mE_click(buffer[0], buffer[1])


def mE_rightclick(x, y):


    win32api.SetCursorPos((x, y))


    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)

    time.sleep(.05)

    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def mE_rightflick(x, y):

    #save postition

    buffer = get_mouse_position()

    win32api.SetCursorPos((x, y))


    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)

    time.sleep(.05)

    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

    mE_click(buffer[0], buffer[1])


def get_mouse_position():


    return win32gui.GetCursorPos()


def keyboard_event(user_input):

    user_input = user_input.lower()

    #print("lower",user_input)


    #check if keybind in list VK_CODE

    key = VK_CODE.get(user_input)

    #print("key:",key)

    if key == None:

        return None


    win32api.keybd_event(key, 0, 0, 0)

    time.sleep(.05)

    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

    return "printed key:", key
