import sys
import os
import tkinter as tk
from functools import partial


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from environment import app_config
from utils.Exceptions import *
from utils.util import *
from reportes.reporteEspacios import *
from gui.guiIngresos import *
from gui.guiRegistrosEdificio import *
from gui.guiRegistroEspacios import *
from gui.guiRegistroVehiculo import *
from gui.guiReportes import *
from gui.guiSalida import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("550x300")
        self.title("Sistema de Gestión de Estacionamientos 1.0")
        self.configure(background="#404041")
    
        menubar = tk.Menu(self)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=fileMenu)
        self.config(menu=menubar)

        repLibres = self.reporteLibres()
        repOcupados= self.reporteOcupados()


        ttk.Label(self,text="Espacios disponibles: "+ str(repLibres)).place(x=12, y=2)
        ttk.Label(self,text="Espacios ocupados: "+ str(repOcupados)).place(x=240, y=2)


        ttk.Style().map("C.TButton", foreground=[('!active','#404041'),('pressed','#404041'),('active','#404041')], background=[('!active','#FAAD3F'),('pressed','!disabled','#FAAD3F'),('active','#F48120')])
        ttk.Style().configure("TLabel", background="#404041", foreground="#F48120")

        ttk.Label(self,text="SGE 1.0", font=("Arial",24,"bold")).place(x=230, y=30)

        ttk.Button(self, text="Ingresos", command=self.ingresos, style="C.TButton").place(x=75, y=80)
        ttk.Button(self, text="Salidas", command=self.salidas, style="C.TButton").place(x=237, y=80)
        ttk.Button(self, text="Reportes", command=self.reportes, style="C.TButton").place(x=399, y=80)
        ttk.Button(self, text="Registro Vehiculos", command=self.registroVehiculos, style="C.TButton").place(x=50, y=200)
        ttk.Button(self, text="Registro Edificios", command=self.registroEdificio, style="C.TButton").place(x=220, y=200)
        ttk.Button(self, text="Registro Espacios", command=self.registroEspacios, style="C.TButton").place(x=380, y=200)

        ttk.Button(self, text="Cerrar", command=self.quit, style="C.TButton").place(x=420, y=250)

    
    def reportes(self):
        window=Reportes(self)
        window.grab_set()

    def registroEdificio(self):
        window=Edificios(self)
        window.grab_set()

    def registroEspacios(self):
        window=Espacios(self)
        window.grab_set()

    def registroVehiculos(self):
        window=Vehiculos(self)
        window.grab_set()

    def ingresos(self):
        window=Ingresos(self)
        window.grab_set()

    def salidas(self):
        window=Cobros(self)
        window.grab_set()

    def reporteLibres(self):
        errorMySQL, datosEntregadosMySQL = reporteEspacioLibre()
        if errorMySQL is None:
            libres = datosEntregadosMySQL[0][0]
            return libres
            
    
    def reporteOcupados(self):
        errorMySQL, datosEntregadosMySQL = reporteEspacioOcupado()
        if errorMySQL is None:
            ocupados = datosEntregadosMySQL[0][0]
            return ocupados
            

if __name__ == "__main__":
    app = App()
    app.mainloop()