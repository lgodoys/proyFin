import os
from datetime import datetime
import pandas as pd
from pandas import ExcelWriter
import numpy as numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class ManejoDeArchivos:
    def crearDataFrame(self,archivo, col_list):
        error = None
        df = None
        try:
            df = pd.read_csv(archivo,usecols=col_list)
        except Exception as err:
            error = "Error al crear el DataFrame, no se puede leer el archivo: %s"%(err)
        return df, error

    def procesarDataFrame(self,df):
        error = None
        nombre = []
        apellido = []
        rut = []
        direccion = []
        for line in df.itertuples():
            nombre.append(line[2])
            apellido.append(line[3])
            rut.append(line[4])
            direccion.append(line[5])
        return nombre,apellido,rut,direccion, error

    def guardarExcel(self,df,nombreColumnas,writer):
        error = None
        dataFrame = pd.DataFrame(df,columns=nombreColumnas)
        try:
            wr2ter = ExcelWriter(writer)
            dataFrame.to_excel(wr2ter,"Reporte de prueba",index=False, header=True)
            wr2ter.close()
        except Exception as err:
            error = "Error, se produjo un error al intentar guardar el archivo Excel: %s"%(err)
        return error

    def guardarPDF(self,df,nombreColumnas,writer):
        error = None
        dataFrame = pd.DataFrame(df,columns=nombreColumnas)  
        try:
            fig,ax = plt.subplots(figsize=(8.5,11),width_ratios=None)
            plt.title("Reporte PDF")
            ax.axis('off')
            theTable = ax.table(cellText = dataFrame.values, colLabels = dataFrame.columns, loc='upper left', cellLoc='left')
            theTable.auto_set_column_width([0,1,2,3,4])
            theTable.set_fontsize(9)
            pp = PdfPages(writer)
            d = pp.infodict()
            d['Title'] = "Reporte PDF"
            d['Author'] = "Leonardo Godoy S"
            d['Subject'] = "Presentación de un PDF de ejemplo"
            d['Keywords'] = ""
            d['CreationDate'] = datetime.today()
            d['ModDate'] = datetime.today()
            d['Creator'] = "Leonardo Godoy S."
            pp.savefig(fig, orientation='portrait', bbox_inches='tight')
            pp.close()
        except Exception as err:
            error = "Error, se produjo un error al intentar guardar el archivo PDF: %s"%(err)
        return error
