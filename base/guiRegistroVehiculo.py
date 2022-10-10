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
from registros.registroVehiculo import *
from registros.registroDuenos import *


class Vehiculos(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("350x500")
        self.title("Registro Vehiculos")
        self.configure(background = "#404041")
        
        ttk.Style().map("C.TButton", foreground=[('!active','#404041'),('pressed','#404041'),('active','#404041')], background=[('!active','#FAAD3F'),('pressed','!disabled','#FAAD3F'),('active','#F48120')])
        ttk.Style().configure("TLabel", background = "#404041", foreground = "#F48120")

        ttk.Label(self,text = "SGE 1.0 - Módulo de registro Vehiculos").place(x = 10, y = 10)

        rut = tk.StringVar(self)
        nombre = tk.StringVar(self)
        apellido = tk.StringVar(self)
        placa = tk.StringVar(self)
        direccion = tk.StringVar(self)

        ttk.Label(self,text="Indique el RUT del dueño\nen formato '12345678-9'").place(x=20,y=80)
        rut_entry = ttk.Entry(self,textvariable=rut)
        rut_entry.place(x=20,y=120)

        ttk.Label(self,text="Indique el nombre del dueño, solo nombre").place(x=20,y=160)         
        nombre_entry = ttk.Entry(self,textvariable=nombre)
        nombre_entry.place(x=20, y=180)
        
        ttk.Label(self,text="Indique el apellido del dueño, solo apellido").place(x=20,y=220)
        apellido_entry = ttk.Entry(self,textvariable=apellido)
        apellido_entry.place(x=20, y=240)

        ttk.Label(self,text="Indique la placa patente del vehículo").place(x=20,y=280)      
        placa_entry = ttk.Entry(self,textvariable=placa)
        placa_entry.place(x=20, y=300)

        ttk.Label(self,text="Indique la dirección del edificio").place(x=20,y=340)
        direccion_entry = ttk.Entry(self,textvariable=direccion)
        direccion_entry.place(x=20,y=360)
       
        repVehiculo = partial(self.RegistroVehiculo,rut,nombre,apellido,placa,direccion)

        b1=ttk.Button(self, text = "Registro de vehículo", command = repVehiculo, style="C.TButton")
        b1.place(x = 60, y = 420)

    def RegistroVehiculo(self,rut,nombre,apellido,placa,direccion):
        respuestaMySQL, estado, errorMySQL = registroAuto(direccion.get(),placa.get())
        print(respuestaMySQL)
        respuestaMySQL, estado, errorMySQL = registroDueno(rut.get(), nombre.get(), apellido.get(), placa.get())
        print(respuestaMySQL)
        ask = messagebox.askquestion("Resultado de ejecución",respuestaMySQL)
        if ask == 'yes':
            self.destroy()