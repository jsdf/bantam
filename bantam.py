#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

import os
import platform
import time
import sys
import subprocess

class BantamRenderer(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''') 
        
        self.parent = parent

        self.keysdown = dict()


    def initialize(self):
        bantam_internal_debug("initialize")

        self.exiting = False

        self.pack(fill=tk.BOTH, expand=1)
        
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        
        self.frame_start_time = bantam_internal_get_current_time()
        self.last_frame_delta_time = 16 # seems legit
        self.initialized = True

    def manual_update(self):
        if self.exiting:
            bantam_app.quit()
            bantam_app.destroy()
            sys.exit(bantam_exit_code)

        time.sleep(0.005)
        try:
            self.parent.update_idletasks()
            self.parent.update()
        except:
            sys.exit(bantam_exit_code)

        return self.start_frame()

    def start_frame(self):
        bantam_internal_debug_rendering("start frame")
        self.reset_screen()
        cur_time = bantam_internal_get_current_time()
        self.last_frame_delta_time = cur_time - self.frame_start_time
        self.frame_start_time = cur_time
        return self.last_frame_delta_time

    def reset_screen(self):
        self.canvas.delete(tk.ALL)
        self.canvas.configure(background=self.background_color)

    def do_frame_if_due_then_enqueue(self, world, update, enqueue_frame):
        if self.exiting:
            sys.exit(bantam_exit_code)

        cur_time = bantam_internal_get_current_time()
        since_last_frame = cur_time - self.frame_start_time
        bantam_internal_debug_rendering("since_last_frame: %d" % (since_last_frame))
        if since_last_frame > 16:
            bantam_internal_debug_rendering("rendered frame")
            update(world, self.start_frame())
        bantam_internal_debug_rendering("enqueue frame")
        enqueue_frame(5)

    def mainloop(self, world, update):
        after_handler = None
        enqueue_frame = lambda delay: self.parent.after(delay, after_handler)

        after_handler = lambda: self.do_frame_if_due_then_enqueue(world, update, enqueue_frame)
        if self.exiting:
            sys.exit(bantam_exit_code)

        enqueue_frame(5)

        self.parent.mainloop()

    def draw_image(self, image, x, y):
        self.canvas.create_image(x, y, image=image)

    def set_background_color(self, color):
        self.background_color = color
        self.configure(background=self.background_color)
        self.canvas.configure(background=self.background_color)

bantam_renderer = None
bantam_debug_rendering_enable = False
bantam_debug_enable = False
bantam_key_states = {}
bantam_app = None
bantam_game_file = ("%s/game.py" % (os.path.dirname(os.path.realpath(__file__))))
bantam_exit_code = 0

def bantam_internal_init(title):
    global bantam_renderer
    global bantam_app

    if bantam_renderer and bantam_renderer.initialized:
        bantam_internal_debug('bantam_internal_init called again')
        return
    bantam_app = tk.Tk()

    bantam_app.title(title)
    bantam_renderer = BantamRenderer(bantam_app)
    bantam_app.geometry("800x600+300+300")

    bantam_internal_center_window(bantam_app)

    bantam_renderer.initialize()

    def window_close_handler():
        bantam_renderer.exiting = True
        bantam_internal_debug('WM_DELETE_WINDOW bantam_internal_init')
    bantam_app.protocol("WM_DELETE_WINDOW", window_close_handler)
    
    def keyup(e):
        global bantam_key_states
        bantam_key_states[e.keysym] = False
        bantam_internal_debug('up %s  %s %d' % (e.char, e.keysym, e.keycode))
    def keydown(e):
        global bantam_key_states
        bantam_key_states[e.keysym] = True
        bantam_internal_debug('down %s  %s %d' % (e.char, e.keysym, e.keycode))

    def reload_app(event):
        global bantam_exit_code
        print "reloading game"
        bantam_exit_code = 99
        bantam_renderer.exiting = True
        bantam_app.quit()
        sys.exit(bantam_exit_code)

    bantam_app.bind('<Control-r>', reload_app) 
    bantam_app.bind("<KeyPress>", keydown)
    bantam_app.bind("<KeyRelease>", keyup)

class World():
    def __init__(self):
        pass

def get_last_frame_duration():
    global bantam_renderer
    bantam_renderer.last_frame_delta_time

def bantam_internal_get_current_time():
    return time.time() * 1000

def bantam_next_frame():
    global bantam_renderer
    return bantam_renderer.manual_update()

def bantam_run(world, update):
    global bantam_renderer
    return bantam_renderer.mainloop(world, update)

def bantam_internal_debug_rendering(message):
    if bantam_debug_rendering_enable:
        print message

def bantam_internal_debug(message):
    if bantam_debug_enable:
        print message

def bantam_internal_enable_reloading():
    if len(sys.argv) < 2 or sys.argv[1] != 'with-reloading':
        bantam_internal_debug("starting reloader")
        code = 99
        while code != 0:
            print "loading %s\n" % bantam_game_file
            code = subprocess.call([sys.executable, bantam_game_file, 'with-reloading'])
            bantam_internal_debug("got exit code %d\n" % code)

            if code != 99 and code != 0:
                raw_input("""
Looks like there was an error in your code.
Please fix it, then click this window and press Enter to try loading it again.
""")
        sys.exit(code)

def bantam_internal_center_window(app):
    app.update_idletasks()
    w = app.winfo_screenwidth()
    h = app.winfo_screenheight()
    size = tuple(int(_) for _ in app.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    app.geometry("%dx%d+%d+%d" % (size + (x, y)))

def bantam_create_world():
    return World()

def image_from_file(file):
    return tk.PhotoImage(file = file)

def draw_image(image, x, y):
    global bantam_renderer
    bantam_renderer.draw_image(image, x, y)

def is_key_pressed(keysym):
    if keysym in bantam_key_states:
        return bantam_key_states[keysym]
    else:
        return False

def freeze_game_window():
    global bantam_app

    def window_close_handler():
        bantam_internal_debug('WM_DELETE_WINDOW freeze_game_window')
        sys.exit(bantam_exit_code)

    bantam_app.protocol("WM_DELETE_WINDOW", window_close_handler)
    bantam_app.mainloop()

def open_game_window(title='Bantam'):
    bantam_internal_init(title)

def set_background_color(color):
    global bantam_renderer
    bantam_renderer.set_background_color(color)

bantam_internal_enable_reloading()
