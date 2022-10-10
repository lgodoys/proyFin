import sys
import os
from functools import partial
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.Exceptions import *
from utils.util import *
from registros.registroEspacios import *

class Espacios(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("300x400")
        self.title("Registro Espacios")
        self.configure(background = "#404041")
        
        ttk.Style().map("C.TButton", foreground=[('!active','#404041'),('pressed','#404041'),('active','#404041')], background=[('!active','#FAAD3F'),('pressed','!disabled','#FAAD3F'),('active','#F48120')])
        ttk.Style().configure("TLabel", background = "#404041", foreground = "#F48120")

        ttk.Label(self,text = "SGE 1.0 - Módulo de registro Espacios").place(x = 10, y = 10)

        idespacio = tk.IntVar(self)
        direccion = tk.StringVar(self)

        ttk.Label(self,text="Indique el ID del espacio\n(número de estacionamiento)").place(x=20,y=80)
        idespacio_entry = ttk.Entry(self,textvariable=idespacio)
        idespacio_entry.place(x=20,y=120)
     
        ttk.Label(self,text="Indique la direccion del edificio").place(x=20,y=220)
        direccion_entry = ttk.Entry(self,textvariable=direccion)
        direccion_entry.place(x=20, y=250)
        
        espacio = partial(self.RegistroEspacio, idespacio,direccion)

        b1=ttk.Button(self, text = "Registrar", command = espacio, style="C.TButton")
        b1.place(x = 60, y = 300)

    def RegistroEspacio(self,idespacio,direccion):
        respuestaMySQL, estado, errorMySQL = registroEspacio(idespacio.get(),direccion.get())
        ask = messagebox.askquestion("Resultado de ejecución",respuestaMySQL)
        if ask == 'yes':
            self.destroy()