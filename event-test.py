from asyncio import run, sleep
from concurrent.futures import ThreadPoolExecutor
from xbot.events.keyboard import press_key
from xbot.events.mouse import MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, mouseClick, mouseMoveSmooth, mousePos


async def test():
    executor = ThreadPoolExecutor()
    
    await sleep(5)
    await press_key(executor, 'f5')

    await sleep(1)
    await press_key(executor, 'f6')

    # await send_key_string(executor, 'eELoO')
    # print(mousePos())

    # mouseClick(MOUSEEVENTF_RIGHTDOWN)
    # await sleep(1)
    # # mouseMove(100, 100)
    # await mouseMoveSmooth(executor, 100, 100)
    # await sleep(1)
    # mouseClick(MOUSEEVENTF_RIGHTUP)


run(test())
