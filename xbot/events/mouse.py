import ctypes
from random import uniform
from asyncio import get_running_loop, sleep

from .sys_struct import GetCursorPos, Input, Input_I, MouseInput, SendInput, POINT


# Mouse Scan Code Mappings
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_LEFTCLICK = MOUSEEVENTF_LEFTDOWN + MOUSEEVENTF_LEFTUP
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_RIGHTCLICK = MOUSEEVENTF_RIGHTDOWN + MOUSEEVENTF_RIGHTUP
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_MIDDLECLICK = MOUSEEVENTF_MIDDLEDOWN + MOUSEEVENTF_MIDDLEUP


def mouseMove(dx, dy):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


async def mouseMoveSmooth(ev_executor, dx, dy, n=8, move_delay=0.025, delay_rand=0.025):
    loop = get_running_loop()
    scale = 1. / n
    for it in range(n):
        await loop.run_in_executor(ev_executor, mouseMove, int(dx*scale), int(dy*scale))
        await sleep(uniform(move_delay, move_delay + delay_rand))


async def mouseSmoothTo(ev_executor, x, y, a=.55, move_delay=0.025, delay_rand=0.025):
    loop = get_running_loop()
    n = 32
    while n:
        n -= 1

        cur_x, cur_y = mousePos()
        dx = x - cur_x
        dy = y - cur_y
        if max(abs(dx), abs(dy)) < 4:
            return

        await loop.run_in_executor(ev_executor, mouseMove, int(dx*uniform(a * .5, a * 1.2)), int(dy*uniform(a * .5, a * 1.2)))
        await sleep(uniform(move_delay, move_delay + delay_rand))


def mousePos():
    cursor = POINT()
    GetCursorPos(ctypes.byref(cursor))
    return cursor.x, cursor.y


def mouseClick(ev):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, ev , 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    
def mouseClick2(x,y):
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, 0,0,0,0)

