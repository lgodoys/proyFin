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
from reportes.reporteAnio import *
from reportes.reporteMes import *
from reportes.reporteDia import *
from reportes.reporteEstadia import *
from reportes.reporteAuto import *

class Reportes(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.geometry("380x400")
        self.title("Reportes")
        self.configure(background = "#404041")
        
        ttk.Style().map("C.TButton", foreground=[('!active','#404041'),('pressed','#404041'),('active','#404041')], background=[('!active','#FAAD3F'),('pressed','!disabled','#FAAD3F'),('active','#F48120')])
        ttk.Style().configure("TLabel", background = "#404041", foreground = "#F48120")

        ttk.Label(self,text = "SGE 1.0 - Módulo de Reportes").place(x = 10, y = 10)

        patente = tk.StringVar(self,name="PPU")
        anio = tk.IntVar(self)
        mes = tk.IntVar(self)
        dia = tk.IntVar(self)

        ttk.Label(self,text="Indique la placa patente del vehículo").place(x=20,y=80)
        placa_entry = ttk.Entry(self,textvariable=patente)
        placa_entry.place(x=20,y=100)

        ttk.Label(self,text="Indique el día a consultar").place(x=20,y=200)             
        dia_entry = ttk.Entry(self,textvariable=dia)
        dia_entry.place(x=20, y=220)
        
        ttk.Label(self,text="Indique el mes a consultar").place(x=20,y=260)             
        mes_entry = ttk.Entry(self,textvariable=mes)
        mes_entry.place(x=20, y=280)

        ttk.Label(self,text="Indique el año a consultar").place(x=20,y=320)             
        anio_entry = ttk.Entry(self,textvariable=anio)
        anio_entry.place(x=20, y=340)
        
        repVehiculo = partial(self.ReporteVehiculo, patente)
        repDia = partial(self.ReporteDiario,dia)
        repMes = partial(self.ReporteMensual,mes)
        repAnio = partial(self.ReporteAnual, anio)

        b1=ttk.Button(self, text = "Reporte por Vehiculo", command = repVehiculo, style="C.TButton")
        b1.place(x = 200, y = 100)
        b2=ttk.Button(self, text = "Reporte de Estadía", command = self.ReporteEstadia, style="C.TButton")
        b2.place(x = 200, y = 160)
        b3=ttk.Button(self, text = "Reporte por Dia", command = repDia, style="C.TButton")
        b3.place(x = 200, y = 220)
        b4=ttk.Button(self, text = "Reporte por Mes", command = repMes, style="C.TButton")
        b4.place(x = 200, y = 280)
        b5=ttk.Button(self, text = "Reporte por Año", command = repAnio, style="C.TButton")
        b5.place(x = 200, y = 340)

    def ReporteVehiculo(self,ppu):
        errorMySQL, datosEntregadosMySQL = reportePorVehiculo(ppu.get())
        manejador = ManejoDeArchivos()
        formato=["Tiempo Estadía en Horas","ID Vehiculo"]
        if errorMySQL is None:
            manejador.guardarExcel(datosEntregadosMySQL,formato,"../data/reporteVehiculo.xlsx")
            ask = messagebox.askquestion("Resultado de ejecución","Se ha generado el reporte exitosamente. Puede encontrarlo almacenado en la ruta de informes.")
            if ask == 'yes':
                self.destroy()

    def ReporteEstadia(self):
        errorMySQL, datosEntregadosMySQL = reporteEstadia()
        manejador = ManejoDeArchivos()
        formato=["Tiempo Estadía en Horas","ID Vehiculo"]
        if errorMySQL is None:
            manejador.guardarExcel(datosEntregadosMySQL,formato,"../data/reporteEstadia.xlsx")
            ask = messagebox.askquestion("Resultado de ejecución","Se ha generado el reporte exitosamente. Puede encontrarlo almacenado en la ruta de informes.")
            if ask == 'yes':
                self.destroy()


    def ReporteDiario(self,day):
        errorMySQL, datosEntregadosMySQL = reporteDiario(day.get())
        manejador = ManejoDeArchivos()
        formato=["Total","DIA"]
        if errorMySQL is None:
            manejador.guardarExcel(datosEntregadosMySQL,formato,"../data/reporteDiario.xlsx")
            ask = messagebox.askquestion("Resultado de ejecución","Se ha generado el reporte exitosamente. Puede encontrarlo almacenado en la ruta de informes.")
            if ask == 'yes':
                self.destroy()


    def ReporteMensual(self,month):
        errorMySQL, datosEntregadosMySQL = reporteMensual(month.get())
        manejador = ManejoDeArchivos()
        formato=["Total","MES"]
        if errorMySQL is None:
            manejador.guardarExcel(datosEntregadosMySQL,formato,"../data/reporteMensual.xlsx")
            ask = messagebox.askquestion("Resultado de ejecución","Se ha generado el reporte exitosamente. Puede encontrarlo almacenado en la ruta de informes.")
            if ask == 'yes':
                self.destroy()


    def ReporteAnual(self,year):
        errorMySQL, datosEntregadosMySQL = reporteAnual(year.get())
        manejador = ManejoDeArchivos()
        formato=["Total","AÑO"]
        if errorMySQL is None:
            manejador.guardarExcel(datosEntregadosMySQL,formato,"../data/reporteAnual.xlsx")
            ask = messagebox.askquestion("Resultado de ejecución","Se ha generado el reporte exitosamente. Puede encontrarlo almacenado en la ruta de informes.")
            if ask == 'yes':
                self.destroy()