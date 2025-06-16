from asyncio import gather, get_running_loop, run, sleep
import asyncio
from concurrent.futures import ThreadPoolExecutor
from random import uniform
import numpy as np
import cv2 as cv
import torch
import regex

from xbot.vision.ocr import detect_text, detect_text_in_boxes, find_im_boxes, get_ocr_reader, merge_boxes
from xbot.vision.preprocess import match_color
from xbot.events.keyboard import press_key, press_multiple_keys
from xbot.events.mouse import mousePos, mouseSmoothTo, mouseClick, MOUSEEVENTF_LEFTCLICK, MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
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


# Take photo of game screen
async def take_photo(executor):
    sct = await init_capture(executor)
    cfg = get_monitor_config(sct)
    reader = get_ocr_reader()
    
    await set_buf_skills(executor)

    await sleep(5)
    print("Take photo")

    im = await grab_frame(executor, sct, cfg)
    cv.imwrite('screens/test.png', im)


# Find position of object
def position(detections, pattern):
    position=[] 
    pattern = pattern.lower()
    for box, text, score in detections:
        matches = regex.findall(f"({pattern}){{e<=2}}", text.lower())
        print(matches)
        if matches:
            # print(np.mean(box, axis=0))
            x,y = np.mean(box, axis=0)
            position.append((float(x),float(y)))
    return position


async def test_mouse():
    await sleep(3)
    mouseClick(MOUSEEVENTF_LEFTDOWN)
    await sleep(1)
    mouseClick(MOUSEEVENTF_LEFTUP)


# Detect object
async def test_monster_detection(executor):
    reader = get_ocr_reader()
    print('initialized')

    im_orig = cv.imread('screens/test.png')
    im = match_color(im_orig[..., ::-1], [255,255,255])
    cv.imwrite('screens/test2.png', im)
    boxes = find_im_boxes(im, 10)
    boxes = merge_boxes(boxes, 15)
    print(boxes)

    # Draw boxes
    im_out = im_orig.copy()
    for x1, y1, x2, y2 in boxes:
        cv.rectangle(im_out, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv.imwrite('screens/test3.png', im_out)
    
    positionXY = position(detect_text_in_boxes(reader, im, boxes), "Metin")

    for x,y in positionXY:
        cv.circle(im_out, (int(x), int(y)+60), 3, (0, 0, 255), -1)
        await mouseSmoothTo(executor, int(x), int(y)+60)

    
    cv.imwrite('screens/test4.png', im_out)


if __name__ == '__main__':
    executor = ThreadPoolExecutor()
    
    print("Start!")
    print(torch.cuda.is_available())
    # asyncio.run(take_photo(executor))
    # asyncio.run(test_monster_detection(executor))
    asyncio.run(test_mouse())
