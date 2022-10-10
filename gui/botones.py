import sys
import os
import tkinter as tk
from tkinter import ttk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

class HoverButton(ttk.Button):
    def __init__(self,master,**kw):
        tk.Button.__init__(self, master = master, **kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self,e):
        self["background"] = self["activebackground"]
        self["foreground"] = self["activeforeground"]

    def on_leave(self,e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground