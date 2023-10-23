#!/usr/bin/env python3
# TWMApp is written by Roberto Rodriguez Jr <hardkorebob@gmail.com> in 2023
# TinyWM is written by Nick Welch <nick@incise.org> in 2005 & 2011.
# This software is in the public domain and is provided AS IS, with NO WARRANTY.

import tkinter as tk
import threading

from Xlib.display import Display
from Xlib import X, XK

class TWMApp:

    # [hardkorebob]
    def __init__(self, root):
        self.tinywm = TinyWM()
        self.tinywm_thread = threading.Thread(target=self.tinywm.run)
        self.tinywm_thread.daemon = True
        self.tinywm_thread.start()

class TinyWM:

    def __init__(self):
        self.dpy = Display()
        self.start = None

    # [hardkorebob] (Tab and Mod4)
    def run(self):
        self.dpy.screen().root.grab_key(self.dpy.keysym_to_keycode(XK.string_to_keysym("Tab")), X.Mod4Mask, 1, X.GrabModeAsync, X.GrabModeAsync)
        self.dpy.screen().root.grab_button(1, X.Mod4Mask, 1, X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask, X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE)
        self.dpy.screen().root.grab_button(3, X.Mod4Mask, 1, X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask, X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE)

        while True:
            ev = self.dpy.next_event()
            if ev.type == X.KeyPress and ev.child != X.NONE:
                ev.child.configure(stack_mode=X.Above)
            elif ev.type == X.ButtonPress and ev.child != X.NONE:
                attr = ev.child.get_geometry()
                self.start = ev
            elif ev.type == X.MotionNotify and self.start:
                xdiff = ev.root_x - self.start.root_x
                ydiff = ev.root_y - self.start.root_y
                self.start.child.configure(
                    x=attr.x + (self.start.detail == 1 and xdiff or 0),
                    y=attr.y + (self.start.detail == 1 and ydiff or 0),
                    width=max(1, attr.width + (self.start.detail == 3 and xdiff or 0)),
                    height=max(1, attr.height + (self.start.detail == 3 and ydiff or 0)))
            elif ev.type == X.ButtonRelease:
                self.start = None
            
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background="#000")
    app = TWMApp(root)
    root.mainloop()



