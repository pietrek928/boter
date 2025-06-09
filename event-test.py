from asyncio import run, sleep
from concurrent.futures import ThreadPoolExecutor
from xbot.events.keyboard import press_key, press_multiple_keys
from xbot.events.mouse import MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, mouseClick, mouseMoveSmooth, mousePos


async def test():
    executor = ThreadPoolExecutor()


    # Sekwencja włączania skilli
    #Zsiądź z konia ctr+g
    await sleep(5)
    await press_multiple_keys(executor, ["ctrl", "g"])

    #Skill f1
    await sleep(5)
    await press_key(executor, 'f1')

    #Skill f2
    await sleep(5)
    await press_key(executor, 'f2')

    print(mousePos())

    # await send_key_string(executor, 'eELoO')
    # mouseClick(MOUSEEVENTF_RIGHTDOWN)
    # await sleep(1)
    # # mouseMove(100, 100)
    # await mouseMoveSmooth(executor, 100, 100)
    # await sleep(1)
    # mouseClick(MOUSEEVENTF_RIGHTUP)


run(test())
