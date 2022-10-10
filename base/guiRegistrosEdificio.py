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
from registros.registroEdificios import *

class Edificios(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("300x400")
        self.title("Registro Edificios")
        self.configure(background = "#404041")
        
        ttk.Style().map("C.TButton", foreground=[('!active','#404041'),('pressed','#404041'),('active','#404041')], background=[('!active','#FAAD3F'),('pressed','!disabled','#FAAD3F'),('active','#F48120')])
        ttk.Style().configure("TLabel", background = "#404041", foreground = "#F48120")

        ttk.Label(self,text = "SGE 1.0 - Módulo de registro Edificios").place(x = 10, y = 10)

        direccion = tk.StringVar(self)
        contacto = tk.StringVar(self)
        telefono = tk.StringVar(self)

        ttk.Label(self,text="Indique la dirección del edificio").place(x=20,y=80)
        direccion_entry = ttk.Entry(self,textvariable=direccion)
        direccion_entry.place(x=20,y=100)

        ttk.Label(self,text="Indique el nombre del contacto\n(nombre y apellido)").place(x=20,y=140)             
        contacto_entry= ttk.Entry(self,textvariable=contacto)
        contacto_entry.place(x=20, y=180)
        
        ttk.Label(self,text="Indique el telefono del contacto\n(en formato 321234567)").place(x=20,y=220)
        telefono_entry = ttk.Entry(self,textvariable=telefono)
        telefono_entry.place(x=20, y=260)
        
        repVehiculo = partial(self.RegistroEdificio, direccion,contacto,telefono)

        b1=ttk.Button(self, text = "Reporte por Vehiculo", command = repVehiculo, style="C.TButton")
        b1.place(x = 60, y = 300)

    def RegistroEdificio(self,dir,cont,tel):
        respuestaMySQL, estado, errorMySQL = registroEdificio(dir.get(),cont.get(),tel.get())
        ask = messagebox.askquestion("Resultado de ejecución",respuestaMySQL)
        if ask == 'yes':
            self.destroy()