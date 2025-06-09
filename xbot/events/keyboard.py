import ctypes
from random import uniform
from asyncio import get_running_loop, sleep

from .sys_struct import Input, Input_I, KeyBdInput, MapVirtualKey, SendInput


# MapVirtualKey Map Types
MAPVK_VK_TO_CHAR = 2
MAPVK_VK_TO_VSC = 0
MAPVK_VSC_TO_VK = 1
MAPVK_VSC_TO_VK_EX = 3


# KeyBdInput Flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004


# Keyboard Scan Code Mappings
KEYBOARD_SCANCODE_MAPPING = {
    'escape': 0x01,
    'esc': 0x01,
    'f1': 0x3B,
    'f2': 0x3C,
    'f3': 0x3D,
    'f4': 0x3E,
    'f5': 0x3F,
    'f6': 0x40,
    'f7': 0x41,
    'f8': 0x42,
    'f9': 0x43,
    'f10': 0x44,
    'f11': 0x57,
    'f12': 0x58,
    'printscreen': 0xB7,
    'prntscrn': 0xB7,
    'prtsc': 0xB7,
    'prtscr': 0xB7,
    'scrolllock': 0x46,
    'pause': 0xC5,
    '`': 0x29,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    '-': 0x0C,
    '=': 0x0D,
    'backspace': 0x0E,
    'insert': 0xD2 + 1024,
    'home': 0xC7 + 1024,
    'pageup': 0xC9 + 1024,
    'pagedown': 0xD1 + 1024,
    # numpad
    'numlock': 0x45,
    'divide': 0xB5 + 1024,
    'multiply': 0x37,
    'subtract': 0x4A,
    'add': 0x4E,
    'decimal': 0x53,
    # KEY_NUMPAD_ENTER: 0x9C + 1024,
    # KEY_NUMPAD_1: 0x4F,
    # KEY_NUMPAD_2: 0x50,
    # KEY_NUMPAD_3: 0x51,
    # KEY_NUMPAD_4: 0x4B,
    # KEY_NUMPAD_5: 0x4C,
    # KEY_NUMPAD_6: 0x4D,
    # KEY_NUMPAD_7: 0x47,
    # KEY_NUMPAD_8: 0x48,
    # KEY_NUMPAD_9: 0x49,
    # KEY_NUMPAD_0: 0x52,
    # end numpad
    'tab': 0x0F,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    '[': 0x1A,
    ']': 0x1B,
    '\\': 0x2B,
    'del': 0xD3 + 1024,
    'delete': 0xD3 + 1024,
    'end': 0xCF + 1024,
    'capslock': 0x3A,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    ';': 0x27,
    "'": 0x28,
    'enter': 0x1C,
    'return': 0x1C,
    'shift': 0x2A,
    'shiftleft': 0x2A,
    'z': 0x2C,
    'x': 0x2D,
    'c': 0x2E,
    'v': 0x2F,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    ',': 0x33,
    '.': 0x34,
    '/': 0x35,
    'shiftright': 0x36,
    'ctrl': 0x1D,
    'ctrlleft': 0x1D,
    'win': 0xDB + 1024,
    'winleft': 0xDB + 1024,
    'alt': 0x38,
    'altleft': 0x38,
    ' ': 0x39,
    'space': 0x39,
    'altright': 0xB8 + 1024,
    'winright': 0xDC + 1024,
    'apps': 0xDD + 1024,
    'ctrlright': 0x9D + 1024,
    'up': MapVirtualKey(0x26, MAPVK_VK_TO_VSC),
    'left': MapVirtualKey(0x25, MAPVK_VK_TO_VSC),
    'down': MapVirtualKey(0x28, MAPVK_VK_TO_VSC),
    'right': MapVirtualKey(0x27, MAPVK_VK_TO_VSC),
    
}
EXTENDED_KEYS = {
    KEYBOARD_SCANCODE_MAPPING['left'], KEYBOARD_SCANCODE_MAPPING['right'],
    KEYBOARD_SCANCODE_MAPPING['up'], KEYBOARD_SCANCODE_MAPPING['down'],
}

def make_key_map():
    key_map = {}
    for key_code in range(ord('A'), ord('Z') + 1):
        key_map[chr(key_code)] = (KEYBOARD_SCANCODE_MAPPING[chr(key_code).lower()], KEYBOARD_SCANCODE_MAPPING['shift'])
    for key_code in range(ord('A'), ord('Z') + 1):
        key_map[chr(key_code).lower()] = (KEYBOARD_SCANCODE_MAPPING[chr(key_code).lower()],)
    for key_code in range(ord('0'), ord('9') + 1):
        key_map[chr(key_code)] = (KEYBOARD_SCANCODE_MAPPING[chr(key_code)],)
    for it, char in enumerate(')!@#$%^&*('):
        key_map[char] = (KEYBOARD_SCANCODE_MAPPING[chr(ord('0') + it)], KEYBOARD_SCANCODE_MAPPING['shift'])
    for it in range(1,13): #f1-f12
        key_map[f'f{it}'] = (KEYBOARD_SCANCODE_MAPPING[f'f{it}'],)
    # key_map.update({
    #     ' ': (win32con.VK_SPACE,),  # TODO: put rest of keys
    #     'enter': (win32con.VK_RETURN,),
    #     'tab': (win32con.VK_TAB,),
    #     'backspace': (win32con.VK_BACK,),
    #     'delete': (win32con.VK_DELETE,),
    #     'esc': (win32con.VK_ESCAPE,),
    #     'up': (win32con.VK_UP,),
    #     'down': (win32con.VK_DOWN,),
    #     'right': (win32con.VK_RIGHT,),
    #     'left': (win32con.VK_LEFT,),
    #     'f1': (win32con.VK_F1,),
    #     'f2': (win32con.VK_F2,),
    #     'f3': (win32con.VK_F3,),
    #     'f4': (win32con.VK_F4,),
    #     'f5': (win32con.VK_F5,),
    #     'f6': (win32con.VK_F6,),
    #     'f7': (win32con.VK_F7,),
    #     'f8': (win32con.VK_F8,),
    #     'f9': (win32con.VK_F9,)
    # })

    return key_map

KEY_MAP = make_key_map()


def keyDown(hexKeyCode, keybdFlags=KEYEVENTF_SCANCODE):
    if hexKeyCode in EXTENDED_KEYS:
        keybdFlags |= KEYEVENTF_EXTENDEDKEY
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def keyUp(hexKeyCode, keybdFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, keybdFlags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


async def press_key(kbd_executor, key_name, key_delay=0.025, delay_rand=0.025):
    if key_name not in KEY_MAP:
        return

    loop = get_running_loop()
    key_codes = KEY_MAP[key_name]
    for k in key_codes[::-1]:
        await loop.run_in_executor(kbd_executor, keyDown, k)
        await sleep(uniform(key_delay, key_delay + delay_rand))
    for k in key_codes:
        await loop.run_in_executor(kbd_executor, keyUp, k)
        await sleep(uniform(key_delay, key_delay + delay_rand))


async def send_key_string(kbd_executor, s, key_delay=0.025, delay_rand=0.025):
    pressed_keys = set()
    loop = get_running_loop()

    for char in s:
        new_keys = set(KEY_MAP[char])
        for k in pressed_keys - new_keys:
            pressed_keys.remove(k)
            # await loop.run_in_executor(kbd_executor, win32api.keybd_event, k, 0, win32con.KEYEVENTF_KEYUP, 0)
            await loop.run_in_executor(kbd_executor, keyUp, k)
            await sleep(uniform(key_delay, key_delay + delay_rand))

        for k in KEY_MAP[char][::-1]:
            if k not in pressed_keys:
                pressed_keys.add(k)
                # await loop.run_in_executor(kbd_executor, win32api.keybd_event, k, 0, 0, 0)
                await loop.run_in_executor(kbd_executor, keyDown, k)
                await sleep(uniform(key_delay, key_delay + delay_rand))
        
        pressed_keys.remove(KEY_MAP[char][0])
        # await loop.run_in_executor(kbd_executor, win32api.keybd_event, KEY_MAP[char][0], 0, win32con.KEYEVENTF_KEYUP, 0)
        await loop.run_in_executor(kbd_executor, keyUp, KEY_MAP[char][0])
        await sleep(uniform(key_delay, key_delay + delay_rand))

    for k in pressed_keys:
        # await loop.run_in_executor(kbd_executor, win32api.keybd_event, k, 0, win32con.KEYEVENTF_KEYUP, 0)
        await loop.run_in_executor(kbd_executor, keyUp, k)
        await sleep(uniform(key_delay, key_delay + delay_rand))
