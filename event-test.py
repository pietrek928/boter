from asyncio import run, sleep
from concurrent.futures import ThreadPoolExecutor
from xbot.events.keyboard import send_key_string
from xbot.events.mouse import MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, mouseClick, mouseMoveSmooth, mousePos


async def test():
    executor = ThreadPoolExecutor()
    await sleep(5)
    # await send_key_string(executor, 'eELoO')
    # await send_key_string(executor, '2')
    # await send_key_string(executor, ' ')
    # win32api.SetCursorPos((45, 45))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 45, 45, 0, 0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 45, 45, 0, 0)
    # import pydirectinput
    # pydirectinput.press('2')
    print(mousePos())
    mouseClick(MOUSEEVENTF_RIGHTDOWN)
    await sleep(1)
    # mouseMove(100, 100)
    await mouseMoveSmooth(executor, 100, 100)
    await sleep(1)
    mouseClick(MOUSEEVENTF_RIGHTUP)
    await send_key_string(executor, '2')
    print(mousePos())


run(test())
