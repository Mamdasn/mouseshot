from pynput import mouse
import numpy as np
import pyscreenshot as screen
from  subprocess import PIPE,Popen
import os, threading, time, datetime, sys

# Database [folder address]
Database = "."
if sys.platform == 'wind32':
    slash = "\\"
else:
    slash = "/"

class Mouse:
    def __init__ (self):
        self.x = 0
        self.y = 0
        self.button = 0
        self.pressed = 0
    def get_xy(self):
        return (self.x, self.y)
    def get_pressed(self):
        return self.pressed
    def get_button(self):
        return self.button
    def set_xy(self, x, y, button, pressed):
        self.x = x
        self.y = y
        self.button = button
        self.pressed = pressed


# get monitor resolution
def get_screen_resolution():    
    if sys.platform == 'win32':
        command = 'wmic path Win32_VideoController get VideoModeDescription'
        res = (Popen(command, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True).stdout.read()).decode('utf-8')
        if not res:
            return (False, False)
        screen_y_height = int(res.split('\n')[1].split('x')[1])
        screen_x_width = int(res.split('\n')[1].split('x')[0])
    elif sys.platform == 'linux':
        command = r"xrandr  | grep \* | cut -d' ' -f4"
        res = (Popen(command, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True).stdout.read()).decode('utf-8').strip()
        screen_y_height = int(res.split('x')[1])
        screen_x_width = int(res.split('x')[0])
    else:
        print("Wrong platform!!")
        sys.exit(1)
    return (screen_x_width, screen_y_height)

[screen_x_width, screen_y_height] = get_screen_resolution()
if not screen_x_width:
    print('Add the python code folder to your antivirus Exclusions')
    sys.exit(1)
    
rect_Height = 300 # height of rectangle (should be even)
rect_Width = 300 # width of rectangle (should be even)

def fix_rect_and_screen_near_edges(x_mouse, y_mouse, rect_Width, rect_Height):
    if (x_mouse - rect_Width//2 < 0) : 
        x_mouse =  rect_Width//2
    elif (x_mouse + rect_Width//2 > screen_x_width):
        x_mouse = screen_x_width-rect_Width//2
    if (y_mouse - rect_Height//2 < 0) : 
        y_mouse =  rect_Height//2
    elif (y_mouse + rect_Height//2 > screen_y_height):
        y_mouse = screen_y_height-rect_Height//2
    return (x_mouse, y_mouse)
        
# initializing my_mouse object
my_mouse = Mouse()

def main():
    try:
        while True:
            # if any key on mouse is pressed
            if my_mouse.get_pressed(): 
                [ x_mouse, y_mouse ] = my_mouse.get_xy()
                print("mouse is clicked!")
                # to capture a rectangle within the screen 
                [ x_mouse, y_mouse ] = fix_rect_and_screen_near_edges(x_mouse, y_mouse, rect_Width, rect_Height)
                output_address = f"{Database}{slash}screenshots{slash}{datetime.datetime.now().date()}"
                if not os.path.isdir(output_address) :  
                    os.makedirs(output_address)
                image = screen.grab(bbox=(x_mouse-rect_Width//2, y_mouse-rect_Height//2, x_mouse+rect_Width//2, y_mouse+rect_Height//2))
                image.save(f"{output_address}{slash}{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")
    
                time.sleep(1)
            # to not use up all the cpu
            time.sleep(0.0001)
    except Exception as e:
                # for debugging
                print(e)
                
cThread = threading.Thread(target = main )
cThread.daemon = True
cThread.start()

# Collect events until released 
with mouse.Listener(on_click=my_mouse.set_xy) as listener: 
        listener.join()
listener = mouse.Listener(on_click=my_mouse.set_xy) 
listener.start()

