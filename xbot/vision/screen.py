from asyncio import get_running_loop
import numpy as np
from mss import mss

    
def get_monitor_config(monitor=1):
    with mss() as sct:
        mon = sct.monitors[monitor]
        return {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor,
        }


async def grab_frame(executor, cfg):
    loop = get_running_loop()

    def capture():
        with mss() as sct:
            return np.array(sct.grab(cfg))

    return await loop.run_in_executor(executor, capture)
