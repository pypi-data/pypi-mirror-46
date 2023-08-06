#!/usr/bin/python
import Tkinter as tk
from  picamera import PiCamera
from time import sleep, strftime
camera = PiCamera()

def CameraON():
    #camera.preview_fullscreen=False
    #camera.preview_window=(0,0, 80, 60)
    #camera.resolution=(640,480)
    curr_time = strftime("%Y%m%d-%H%M%S")
    camera.capture('/home/pi/Pictures/image_%s.jpg' % curr_time)

def CameraOFF():
    camera.stop_preview()

def EXIT():
    root.destroy
    camera.stop_preview()
    camera.close()
    quit()

camera.start_preview(fullscreen=False,window=(50,50,320,240))
root = tk.Tk()
root.resizable(width=False, height=False)
root.geometry("320x300+89+50")
root.title("Camera Button Test")

root.buttonframe = tk.Frame(root)
root.buttonframe.grid(row=2, column=2, columnspan=2)
tk.Button(root.buttonframe, text='Take Photo', command=CameraON).grid(row=1, column = 1)



root.mainloop()
