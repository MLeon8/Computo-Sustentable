import math
#import shutil

import pandas as pd
from scipy import integrate
from sympy import Integral
from sympy import Symbol

def rombergMethod(values, dx=1):
        """
        Aplicacion del metodo de Romberg a partir de una muestra

        :param values: valores a evaluar
        :param dx: espaciado
        :return: Float
        """
        return integrate.romb(y=values, dx=dx)


def calculateIntegral(x, fx, lower_limit, upper_limit):
        """
        Funcion para el calculo de la integral de cualquier funcion

        :param x: valor en el cual evaluar la funcion
        :param fx: funcion a evaluar
        :param lower_limit: limite inferior
        :param upper_limit: limite superior
        :return: Float
        """
        # Se define la integral
        dx = Integral(fx, (x, lower_limit, upper_limit)).doit()
        return dx

def getEnergyProportionality(data):
        """
        Calculo de la metrica EP
        :param data: consumo de watts del servidor de 0% al 100% de carga de trabajo
        :return: Integer
        """
        peak=data[-1]
        return 2 - areaUnderCurve(values=data, dx=0.1) / integralProportionalServer(peak=peak)


def areaUnderCurve(values, dx=1):
        """
                :param values: consumo de watts del servidor de 100% al 0% de carga de trabajo
        :param dx: margen de separacion
        :return: Integer
        """
        subarray1 = values[0:9]
        subarray2 = values[8:11]
        return rombergMethod(subarray1, dx) + \
               rombergMethod(subarray2, dx)

def integralProportionalServer(peak):
        """
        Area bajo la curva de un servidor proporcionalmente energetico

        :param peak: consumo de watts del servidor al 100% de carga de trabajo
        :return: Integer
        """
        # Creando el simbolo x.
        x = Symbol('x')
        # Pe(l)=P(1)*l
        pe = peak * x
        return calculateIntegral(x, pe, 0, 1)




def metrics(file):
        result=[]
        
        for row in file:
                tmp=[]        
                ssjops=row[0:9]
                wattConsume=row[10:]
                watts_consumption_list=wattConsume.tolist()
                watts_consumption_list.reverse()
                tmp.append(getEnergyProportionality(watts_consumption_list))
                tmp.append(getPowerEfficiency(ssjops,watts_consumption_list))
                result.append(tmp)
        return result




def getPowerEfficiency(ssjops,wattConsume):
        sumaPerf=0
        sumaPower=0
        powerEficciency=0;
        for x in ssjops:
                sumaPerf+=x
        for y in wattConsume:
                sumaPower+=y

        powerEficciency=sumaPerf/sumaPower
        return powerEficciency


results=[]
file_path="SpecPower.xlsx"
metrics_file_path="Results.xlsx"

fileX=pd.read_excel(file_path)
columns=fileX.columns.tolist()
start_index=columns.index('ssj_ops @ 100% of target load\t')
end_index=columns.index('Average watts @ active idle\t')
selected_data = fileX.iloc[:, start_index:end_index]
values = selected_data.values
results=metrics(values)
fileY=pd.read_excel(metrics_file_path)
columna=['PE','EP']
fileY[columna]=results
fileY.to_excel(metrics_file_path, index=False)
"""
Power Efficiency=(Suma_k=1 to n performance_k)/(Suma_k=1 to n power_k)
"""
