from xbot.events.keyboard import press_key, press_multiple_keys
from asyncio import sleep

async def set_buf_skills(executor):
    # Sekwencja włączania skilli

    # Zsiądź z konia ctr+g
    await sleep(5)
    await press_multiple_keys(executor, ["ctrl", "g"])

    # Skill f1
    await sleep(0.5)
    await press_key(executor, 'f1')

    # Skill f2
    await sleep(2)
    await press_key(executor, 'f2')

    # Wsiądź na konia
    await sleep(2)
    await press_multiple_keys(executor, ["ctrl", "g"])