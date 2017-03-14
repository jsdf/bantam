#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

import os
import platform
import time
import sys

class BantamRenderer(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''') 
        
        self.parent = parent

        self.keysdown = dict()

    def key(self, event):
        print "pressed", repr(event.char)

        self.keysdown[event.char] = True
        print "keys", repr(self.keysdown)
    def keyrelease(self, event):
        self.keysdown[event.char] = False

    def start(self):
        print "start"
        self.parent.title("Bantam")
        self.pack(fill=tk.BOTH, expand=1)
        
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        def key(event):
            print "pressed", repr(event.char)

        self.canvas.bind("<Key>", key)
        self.bind("<KeyRelease>", self.keyrelease)
        
        self.cur_frame_time = time.time()
        self.prev_frame_time = time.time()

    def update(self):
        time.sleep(0.005)
        try:
            self.parent.update_idletasks()
            self.parent.update()
        except:
            sys.exit(0)

        self.canvas.delete(tk.ALL)
        self.prev_frame_time = self.cur_frame_time
        self.cur_frame_time = time.time()
        dt = self.cur_frame_time - self.prev_frame_time
        return dt

    def draw_image(self, image, x, y):
        self.canvas.create_image(x, y, image=image)

def bantam_internal_init():
    global bantam_renderer
    app = tk.Tk()
    bantam_renderer = BantamRenderer(app)
    app.geometry("800x600+300+300")

    bantam_internal_center(app)

    bantam_renderer.start()
    
    def keyup(e):
        print 'up', e.char
    def keydown(e):
        print 'down', e.char
    bantam_renderer.bind("<KeyPress>", keydown)
    bantam_renderer.bind("<KeyRelease>", keyup)

def bantam_update():
    global bantam_renderer
    return bantam_renderer.update()

def bantam_freeze():
    while True:
        bantam_update()

def bantam_internal_center(app):
    app.update_idletasks()
    w = app.winfo_screenwidth()
    h = app.winfo_screenheight()
    size = tuple(int(_) for _ in app.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    app.geometry("%dx%d+%d+%d" % (size + (x, y)))

def image_from_file(file):
    return tk.PhotoImage(file = file)

def draw_image(image, x, y):
    global bantam_renderer
    bantam_renderer.draw_image(image, x, y)

bantam_internal_init()

