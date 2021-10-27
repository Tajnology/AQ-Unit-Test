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
RECEIVE_IMAGE_EVENT = 'td-image'
RECEIVE_TEMPERATURE_EVENT = 'air-data'
DISPLAY_MODE_FILE = '/home/payload/Code/PayloadSoftware/displaymode/display_mode.txt'
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

#### GLOBAL VARIABLES ####
ip = utils.get_ip()
current_display = 0 # 0 = IP, 1 = Target, 2 = Air

render_image = Image.new('RGB',(WIDTH,HEIGHT), color='white') # Create blank image
draw = ImageDraw.Draw(render_image)

#### MAIN PROCEDURE ####
def main(argv):
    disp.begin() # Initialize the LCD.   

    temperature = RefObj()
    target_image = RefObj()


    # Establish Inter-Process Communication
    init_ipc = threading.Thread(target=ipc.init, args=(temperature,target_image,))
    init_ipc.start()
    
    main_loop_thread = threading.Thread(target=main_loop, args=(temperature,target_image,))
    main_loop_thread.start()
    

def main_loop(temperature : RefObj, target_image: RefObj):
    global current_display
    while(True):
        
        current_display = utils.get_display_mode(DISPLAY_MODE_FILE)
        ip = utils.get_ip()
        draw.rectangle([(0,0),(WIDTH,HEIGHT)],fill="white")
        # Render and display image on LCD
        if(current_display == 0):
            # Draw IP to display
            draw.text((TEXT_X,TEXT_Y),ip,font=font,fill=255)
        elif(current_display == 1):
            target_image_val = target_image.get()
            if(target_image_val != None):
                im = Image.open(BytesIO(base64.b64decode(target_image_val)))
                im.thumbnail((WIDTH,1000),Image.ANTIALIAS)
                render_image.paste(im,None)
            else:
                draw.text((TEXT_X,TEXT_Y),"No video feed.",font=font,fill=255)
                # Draw a 'no image found icon'
        elif current_display == 2:
            temperature_val = temperature.get()
            if temperature_val != None:
                draw.text((TEXT_X,TEXT_Y),"Temp: " + str(round(temperature_val,2)) + "C",font=font,fill=255)
            else:
                draw.text((TEXT_X,TEXT_Y),"No temperature data.",font=font,fill=255)
        disp.display(render_image)

        time.sleep(REFRESH_INTERVAL)



#### ENTRY POINT ####
if __name__ == "__main__":
    main(sys.argv[1:])
