from asyncio import gather, get_running_loop, run, sleep
from concurrent.futures import ThreadPoolExecutor
from random import uniform
import numpy as np
import cv2 as cv

from xbot.events.keyboard import press_key, press_multiple_keys
from xbot.vision.ocr import detect_text, get_ocr_reader
from xbot.vision.preprocess import match_color
from xbot.events.mouse import mousePos, mouseSmoothTo

from xbot.vision.screen import get_monitor_config, grab_frame, init_capture


async def find_text(improc_executor, reader, im_rgb, col_rgb):
    loop = get_running_loop()
    im_det = await loop.run_in_executor(improc_executor, match_color, im_rgb, col_rgb)
    return await loop.run_in_executor(improc_executor, detect_text, reader, im_det)


def find_nearest_monster(found_text, monster_key, player_pos):
    monster_key = monster_key.lower()
    px, py = player_pos
    
    best_score = 1e9
    pos = None
    for coords, text, score in found_text:
        if monster_key in text.lower():
            coords = np.array(coords, dtype=np.float32)
            x, y = np.mean(coords, axis=0)
            s = np.sqrt((px - x)**2 + (py - y)**2) / (score + .1)
            if s < best_score:
                best_score = s
                pos = (float(x), float(y))
    return pos


async def periodic_key(executor, key, delay):
    while True:
        await sleep(uniform(delay * .9, delay * 1.1))
        await press_key(executor, key)


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


async def farm_mobs():
    x = ThreadPoolExecutor()

    await sleep(10)

    await gather(
        periodic_key(x, '1', 20),  # wir
        periodic_key(x, '5', 1),  # atak
        periodic_key(x, 'tab', 7),  # zmiana stworka

        periodic_key(x, '2', 7),  # aura
        periodic_key(x, '3', 10),  # hp
        periodic_key(x, '4', 45),  # mp
        periodic_key(x, '`', .25),  # drop
    )


async def fight():
    x = ThreadPoolExecutor()
    # sct = await init_capture(x)
    # reader = get_ocr_reader()
    # cfg = get_monitor_config(sct)
    # print('initialized')

    await sleep(10)

    await gather(
        periodic_key(x, '1', 20),  # wir
        periodic_key(x, '5', 1),  # atak
        periodic_key(x, 'tab', 7),  # zmiana stworka

        periodic_key(x, '2', 7),  # aura
        periodic_key(x, '3', 10),  # hp
        periodic_key(x, '4', 45),  # mp
        periodic_key(x, '`', .25),  # drop
    )
   
    # await sleep(10)

    # Mouse to monster
    # im = await grab_frame(x, sct, cfg)
    # cv.imwrite('test.png', im)
    # text = await find_text(x, reader, im, [235, 22, 9])
    # p = find_nearest_monster(text, 'dziki', (500, 500))
    # print(p)
    # if p:
    #     await mouseSmoothTo(x, p[0], p[1])


if __name__ == '__main__':
    run(fight())
