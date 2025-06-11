from asyncio import run, sleep
from concurrent.futures import ThreadPoolExecutor
from xbot.events.keyboard import press_key, press_multiple_keys
from xbot.events.mouse import MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, mouseClick, mouseMoveSmooth, mousePos
from xbot.game.game import set_buf_skills, do_metin


async def test():
    executor = ThreadPoolExecutor()

    # await set_buf_skills(executor)
    await do_metin(executor)

run(test())
