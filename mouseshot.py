from pynput import mouse
import pyscreenshot as screen
from  subprocess import PIPE,Popen
import os, threading, time, datetime, sys
from Xlib import display


if sys.platform == 'wind32':
    slash = "\\"
else:
    slash = "/"

# Database [folder address]
Database = f".{slash}example-output"
rect_Height = 500 # height of rectangle (should be even), set to zero for screen height
rect_Width = 500 # width of rectangle (should be even), set to zero for screen width

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
        screen = display.Display().screen()
        screen_y_height = screen.height_in_pixels
        screen_x_width = screen.width_in_pixels
    else:       
        print("Wrong platform!!")
        sys.exit(1)
    return (screen_x_width, screen_y_height)

[screen_x_width, screen_y_height] = get_screen_resolution()

def main(x, y):
    print(f"Mouse clicked at ({x}, {y})")
    print("mouse is clicked!")
    # to capture a rectangle within the screen 
    x_mouse, y_mouse = x, y
    [ x_mouse, y_mouse ] = fix_rect_and_screen_near_edges(x_mouse, y_mouse, rect_Width, rect_Height)
    output_address = f"{Database}{slash}{datetime.datetime.now().date()}"
    if not os.path.isdir(output_address) :
        os.makedirs(output_address)
    image = screen.grab(bbox=(  
        x_mouse-rect_Width //2  if rect_Width  != 0 else 0,
        y_mouse-rect_Height//2  if rect_Height != 0 else 0, 
        x_mouse+rect_Width //2  if rect_Width  != 0 else screen_x_width, 
        y_mouse+rect_Height//2  if rect_Height != 0 else screen_y_height))
    image = image.convert("RGB")
    image.save(f"{output_address}{slash}{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")

def on_click(x, y, button, pressed):
    if pressed:
        main(x, y)

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
