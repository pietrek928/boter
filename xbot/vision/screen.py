from asyncio import get_running_loop
import numpy as np
from mss import mss


async def init_capture(screencap_executor):
    loop = get_running_loop()
    return await loop.run_in_executor(screencap_executor, mss)


def get_monitor_config(sct, monitor=1):
    # Get information of monitor
    mon = sct.monitors[monitor]
    
    # Region to capture (entire monitor)
    return {
        "top": mon["top"],
        "left": mon["left"],
        "width": mon["width"],
        "height": mon["height"],
        "mon": monitor,
    }


async def grab_frame(screencap_executor, sct, cfg):
    loop = get_running_loop()
    sct_im = await loop.run_in_executor(screencap_executor, sct.grab, cfg)
    return np.array(sct_im)
