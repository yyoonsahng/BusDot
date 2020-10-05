# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules import control as con
from modules import hw_init as hw
import buttonClass

#import tts_module as tts
import time
from timeloop import Timeloop
from datetime import timedelta

USER_ID = "root"

if __name__ == "__main__":
    bc = buttonClass.Button(USER_ID)
    con.setup()
    # GPIO 초기화 (GPS,Solenoid, Switch) - 이벤트 핸들러 등록
    hw.init(bc.switch_prev_callback, bc.switch_next_callback,bc.switch_save_callback, bc.switch_done_callback)
    
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        hw.destroy()
        con.destroy()
