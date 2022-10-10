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
from registros.cobros import *

class Cobros(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("350x400")
        self.title("Salidas")
        self.configure(background = "#404041")

        menubar = tk.Menu(self)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=fileMenu)
        self.config(menu=menubar)
        
        ttk.Style().map("C.TButton", foreground=[('!active','#404041'),('pressed','#404041'),('active','#404041')], background=[('!active','#FAAD3F'),('pressed','!disabled','#FAAD3F'),('active','#F48120')])
        ttk.Style().configure("TLabel", background = "#404041", foreground = "#F48120")

        ttk.Label(self,text = "SGE 1.0 - Módulo de Cobros").place(x = 10, y = 10)

        patente = tk.StringVar(self,name="PPU")

        ttk.Label(self,text="Indique la placa patente del vehículo").place(x=60,y=80)
        placa_entry = ttk.Entry(self,textvariable=patente)
        placa_entry.place(x=80,y=100)
        
        cobro = partial(self.Cobro, patente)

        b1=ttk.Button(self, text = "Generar cobro", command = cobro, style="C.TButton")
        b1.place(x = 130, y = 150)

    def Cobro(self,ppu):
        datosEntregadosMySQL, errorMySQL = salida(ppu.get())
        idIngreso = datosEntregadosMySQL[0][0]
        horaEntrada = datetime.fromtimestamp(datosEntregadosMySQL[0][1])
        horaSalida = datetime.fromtimestamp(datosEntregadosMySQL[0][2])
        valor = datosEntregadosMySQL[0][3]
        idVehiculo = datosEntregadosMySQL[0][4]
        idEspacio = datosEntregadosMySQL[0][5]
        manejador = ManejoDeArchivos()
        if errorMySQL is None:
            texto="ID Vehiculo: "+str(idVehiculo)+"\nID Ingreso: "+str(idIngreso)+"\nHora de Ingreso: "+str(horaEntrada)+"\nHora de Salida: "+str(horaSalida)+"\nValor: "+str(valor)+"\nID Espacio: "+str(idEspacio)
            manejador.guardarPDF(texto,"../data/cobro"+str(idVehiculo)+".pdf")
            texto="ID Vehiculo: "+str(idVehiculo)+"\nHora de Ingreso: "+str(horaEntrada)+"\nHora de Salida: "+str(horaSalida)+"\nValor: "+str(valor)
            ask = messagebox.askquestion("Resultado de ejecución",texto)
            if ask == 'yes':
                self.destroy()