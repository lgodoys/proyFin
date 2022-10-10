import sys
from datetime import *
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
from registros.ingresos import *
from lib.manejo_de_archivos import *

class Ingresos(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("350x300")
        self.title("Ingresos")
        self.configure(background = "#404041")
        
        ttk.Style().map("C.TButton", foreground=[('!active','#404041'),('pressed','#404041'),('active','#404041')], background=[('!active','#FAAD3F'),('pressed','!disabled','#FAAD3F'),('active','#F48120')])
        ttk.Style().configure("TLabel", background = "#404041", foreground = "#F48120")

        ttk.Label(self,text = "SGE 1.0 - Módulo de Ingresos").place(x = 10, y = 10)

        placa = tk.StringVar(self)
        
        ttk.Label(self,text="Indique la placa patente del vehículo").place(x=60,y=80)
        placa_entry = ttk.Entry(self,textvariable=placa)
        placa_entry.place(x=80,y=100)

        ingreso = partial(self.IngresoVehiculo, placa)

        b1=ttk.Button(self, text = "Ingreso", command = ingreso, style="C.TButton")
        b1.place(x = 130, y = 150)

    def IngresoVehiculo(self,ppu):
        datosEntregadosMySQL,errorMySQL = ingresoVehiculos(ppu.get())
        idIngreso = datosEntregadosMySQL[0][0]
        horaEntrada = datetime.fromtimestamp(datosEntregadosMySQL[0][1])
        idVehiculo = datosEntregadosMySQL[0][2]
        idEspacio = datosEntregadosMySQL[0][3]
        manejador = ManejoDeArchivos()
        if errorMySQL is None:
            texto="ID Ingreso: "+str(idIngreso)+"\nID Vehiculo: "+str(idVehiculo)+"\nID Espacio: "+str(idEspacio)+"\nHora de Ingreso: "+str(horaEntrada)
            manejador.guardarPDF(texto,"../data/ingreso"+str(idVehiculo)+".pdf")
            ask = messagebox.askquestion("Resultado de ejecución",texto)
            if ask == 'yes':
                self.destroy()