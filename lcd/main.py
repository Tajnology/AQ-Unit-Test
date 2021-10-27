#### EXTERNAL MODULE IMPORTS ####
import getopt   # getopt.getopt()
import time
import sys
import os
from threading import Lock
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import base64
from io import BytesIO
from enum import Enum
import ST7735 as ST7735
import threading

#### LOCAL IMPORTS ####
import ipc
import utils

#### LCD HARDWARE DECLARATION ####
disp = ST7735.ST7735(
    port=0,
    cs = ST7735.BG_SPI_CS_FRONT,
    dc = 9,
    backlight = 19,
    rotation = 90,
    spi_speed_hz = 4000000
)

WIDTH = disp.width
HEIGHT = disp.height

TEXT_X = 10
TEXT_Y = 10

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
REFRESH_INTERVAL = 0.5 # seconds
RECEIVE_AQ_DATA = 'air-data'
FONT_SIZE = 20

#### CLASSES ####
class RefObj(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.value = None
    def set(self, temp):
        self.lock.acquire()
        try:
            self.value = temp
        finally:
            self.lock.release()
    def get(self):
        return self.value




#### LOAD FONT ####
font = ImageFont.truetype("Roboto-Medium.ttf",size=15)

render_image = Image.new('RGB',(WIDTH,HEIGHT), color='white') # Create blank image
draw = ImageDraw.Draw(render_image)

#### MAIN PROCEDURE ####
def main(argv):
    disp.begin() # Initialize the LCD.   

    temperature = RefObj()
    cpu = RefObj()


    # Establish Inter-Process Communication
    init_ipc = threading.Thread(target=ipc.init, args=(temperature,cpu,))
    init_ipc.start()
    
    main_loop_thread = threading.Thread(target=main_loop, args=(temperature,cpu,))
    main_loop_thread.start()
    

def main_loop(temperature : RefObj, cpu: RefObj):

    while(True):
        
        draw.rectangle([(0,0),(WIDTH,HEIGHT)],fill="white")
        
        temperature_val = temperature.get()
        cpu_val = cpu.get()
        if temperature_val != None:
            draw.text((TEXT_X,TEXT_Y),"Temp: " + str(round(temperature_val,2)) + "C",font=font,fill=255)
        else:
            draw.text((TEXT_X,TEXT_Y),"No temperature data.",font=font,fill=255)
        
        if cpu_val != None:
            draw.text((TEXT_X,3*TEXT_Y),"CPU Temp: " + cpu.get(),font=font,fill=255)
        disp.display(render_image)

        time.sleep(REFRESH_INTERVAL)



#### ENTRY POINT ####
if __name__ == "__main__":
    main(sys.argv[1:])
