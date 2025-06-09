from asyncio import run, sleep
from concurrent.futures import ThreadPoolExecutor
from xbot.events.keyboard import press_key, press_multiple_keys
from xbot.events.mouse import MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, mouseClick, mouseMoveSmooth, mousePos
from xbot.game.game import set_buf_skills


async def test():
    executor = ThreadPoolExecutor()

    await set_buf_skills(executor)

    print(mousePos())

    # await send_key_string(executor, 'eELoO')
    # mouseClick(MOUSEEVENTF_RIGHTDOWN)
    # await sleep(1)
    # # mouseMove(100, 100)
    # await mouseMoveSmooth(executor, 100, 100)
    # await sleep(1)
    # mouseClick(MOUSEEVENTF_RIGHTUP)


run(test())
