import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import cv2 as cv
import regex
import serial
import random
import time


from xbot.vision.ocr import detect_text_in_boxes, find_im_boxes, get_ocr_reader, merge_boxes
from xbot.vision.preprocess import match_color
from xbot.events.keyboard import press_key, press_multiple_keys
from xbot.events.mouse import  mouseSmoothTo
from xbot.vision.screen import get_monitor_config, grab_frame


# Globals
image_queue = asyncio.Queue(maxsize=1)

# Run buffs
async def set_buf_skills(executor):
    # Zsiądź z konia ctr+g
    time.sleep(random.uniform(1.5,2))
    await press_multiple_keys(executor, ["ctrl", "g"])

    # Skill f1
    time.sleep(random.uniform(0.2,0.5))
    await press_key(executor, 'f1')

    # Skill f2
    time.sleep(random.uniform(2,3))
    await press_key(executor, 'f2')

    # Wsiądź na konia
    time.sleep(random.uniform(0.5,2))
    await press_multiple_keys(executor, ["ctrl", "g"])
    

# Screen
async def take_photo(executor):
    cfg = get_monitor_config()
    im = await grab_frame(executor, cfg)
    return im


# Find position of object
def position(detections, pattern):
    position=[] 
    pattern = pattern.lower()
    for box, text, score in detections:
        matches = regex.findall(f"({pattern}){{e<=2}}", text.lower())
        print(matches)
        if matches:
            x,y = np.mean(box, axis=0)
            position.append((float(x),float(y)))
    return position
 
    
# UART controlled eMouse
class ESPMouseController:
    def __init__(self, port="COM7", baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
    
    def send_command(self, command: str):
        if not command.endswith("\n"):
            command += "\n"
        self.ser.write(command.encode("utf-8"))
        
    def move(self, x:int, y:int):
        self.send_command(f"MOUSEMOVE({x},{y})")
        
    def left_click(self):
        self.send_command("LEFTCLICK")
    
    def right_click(self):
        self.send_command("RIGHTCLICK")
        
    def close(self):
        self.ser.close()
    

# Detect object
async def monster_detection(executor, mouse, reader, im_orig):
    im = match_color(im_orig[..., ::-1], [255,255,255])
    boxes = find_im_boxes(im, 10)
    boxes = merge_boxes(boxes, 15)

    start = time.perf_counter()
    positionXY = position(detect_text_in_boxes(reader, im, boxes), "Metin")
    end = time.perf_counter()

    print(f"Time: {end-start:.2f}s")

    if not positionXY:
        directions = ['w', 'a', 's', 'd']
        direction = random.choice(directions)
        duration = random.uniform(0.3, 0.7)
        await press_key(executor, direction, duration)
        return

    if positionXY:
        h, w = im.shape[:2]
        center = (w // 2, h // 2)

        # Wybierz punkt najbliżej środka
        closest = min(positionXY, key=lambda pt: (pt[0] - center[0])**2 + (pt[1] - center[1])**2)

        x, y = closest
        await mouseSmoothTo(executor, int(x), int(y)+10)
        mouse.left_click()  
    
    await asyncio.sleep(random.uniform(0.5,1)) 
        
        
# Main "z" key task executor for items        
async def click_loop(executor):
    while True:
        await press_key(executor, 'z')
        await asyncio.sleep(random.uniform(0.3,1))


# Main take photo loop
async def photo_loop(executor):
    while True:
        im = await take_photo(executor)
         
        if image_queue.full():
            try:
                _ = image_queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            
        await image_queue.put(im) 


# Main monster detection task executor
async def monster_detection_loop(executor, mouse, mouse_lock):
    reader = get_ocr_reader()

    while True:
        im = await image_queue.get()
        async with mouse_lock:
            await monster_detection(executor, mouse, reader, im)
        
   
# Auxiliary skills 
async def run_inventory_and_skills(executor, mouse, mouse_lock): 
    while True:
        async with mouse_lock:
            await set_buf_skills(executor)
            
            time.sleep(random.uniform(0.5,1))
            
            await press_key(executor, 'f4')        
            await mouseSmoothTo(executor, 1000,320)
            mouse.left_click()    
            time.sleep(random.uniform(0.8,1))
            mouse.left_click()
            time.sleep(random.uniform(0.5,1))
            await press_key(executor, 'f4')
            
            time.sleep(random.uniform(0.3,0.4))
            await press_key(executor, 'i') 
        
        await asyncio.sleep(random.uniform(180,360)) 


# Beginning of code
async def main():
    print("Start!")
    
    executor = ThreadPoolExecutor()
    mouse = ESPMouseController(port="COM7")
    mouse_lock = asyncio.Lock()
    
    tasks = [
        asyncio.create_task(run_inventory_and_skills(executor, mouse, mouse_lock)),
        asyncio.create_task(photo_loop(executor)),
        asyncio.create_task(click_loop(executor)),
        asyncio.create_task(monster_detection_loop(executor, mouse, mouse_lock))
    ]
    
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Cancelled")
    finally:
        executor.shutdown()
      
      
# RUN
if __name__ == '__main__':    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user!")
        sys.exit(0)

