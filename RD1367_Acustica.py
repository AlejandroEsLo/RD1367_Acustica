# -*- coding: utf-8 -*-
"""
                 Herramienta de aplicación del RD1367.
      Su ámbito de uso serán los valores de inmisión de actividades.
Arrojará el nivel final de evaluación, Lkeq, T, a comparar con límites normativos.

"""
import sys
from math import log

if __name__ == "__main__":

    try:
        # Introduccion de datos para la realizacion de los calculos.
        LAeq = float(input("Introduzca Valor LAeq: "))
        LCeq = float(input("Introduzca Valor LCeq: "))
        LAIeq = float(input("Introduzca Valor LAIeq: "))
        LAeq_ruido = float(input("Introduzca Valor LAeq_ruido: "))
        LCeq_ruido = float(input("Introduzca Valor LCeq_ruido: "))
        LAIeq_ruido = float(input("Introduzca Valor LAIeq_ruido: "))
        Max_actividad = float(input("Introduzca Valor Maximo de la Actividad: "))
        # Introduccion frecuencias(Frecuencias 1/3 de Octava) y Tonos para calcular las componentes  tonales.
        Freq = float(input("Introduzca Frecuencia: ")) 
        Frecuencias_validas = range(20, 10001)
        
        Tono_emergente = float(input("Introduzca Tono emergente central: ")) 
        Tono_inferior = float(input("Introduzca Tono inferior al Tono emergente central: "))
        Tono_superior = float(input("Introduzca Tono superior al Tono emergente central: "))

        # Comprobacion Frecuencia valida        
        if Freq not in Frecuencias_validas:
            sys.exit("INTRODUZCA UNA FRECUENCIA VALIDA (20HZ - 10000HZ)")
            
    except ValueError:
        sys.exit("Error: No es un valor válido prueba a introducir un valor entero o float correcto")

    print("\nCálculos:")        

    """CALCULAMOS LA CORRECCION POR RUIDO DE FONDO"""
        # Calculamos logaritmo en base 10 => log(x,10)
    LAeq_corregido = 10 * (log(10**(LAeq/10) - 10**(LAeq_ruido/10),10))
    LCeq_corregido = 10 * (log(10**(LCeq/10) - 10**(LCeq_ruido/10),10))
    LAIeq_corregido = 10 * (log(10**(LAIeq/10) - 10**(LAIeq_ruido/10),10))
    
    print("LAeq_corregido = ", LAeq_corregido)
    print("LCeq_corregido = ", LCeq_corregido)
    print("LAIeq_corregido = ", LAIeq_corregido)
    
    """CALCULAMOS LA CORRECCION POR BAJAS FRECUENCIAS PARA SACAR Kf"""
    Lf = LCeq_corregido - LAeq_corregido
    
    print("Lf = ", Lf)
   
    # Comparamos Lf con los valores de la tabla
    if Lf <= 10:
        Kf = 0
    elif Lf > 15:
        Kf = 6
    else:
        Kf = 3
    
    print("Kf = ", Kf)

    """CALCULAMOS LA CORRECCION POR COMPONENTES IMPULSIVAS PARA SACAR Ki"""
    Li = LAIeq_corregido - LAeq_corregido
    
    print("Li = ", Li)
   
    # Comparamos Li con los valores de la tabla
    if Li <= 10:
        Ki = 0
    elif Li > 15:
        Ki = 6
    else:
        Ki = 3
        
    print("Ki = ", Ki)

    """CALCULAMOS LA CORRECCION POR COMPONENTES TONALES PARA SACAR Kt"""
    
    Ls = (Tono_inferior + Tono_superior)/2
    Lt = Tono_emergente - Ls
    
    print("Lt = ", Lt)
   
    # Comparamos la frecuencia introducida para ver en el rango que nos encontramos y calculamos su Kt
    if Freq >= 20 and Freq <= 125:
            
        if Lt < 8:
            Kt = 0
        elif Lt > 12:
            Kt = 6
        else:
            Kt = 3
            
        print("Kt = ", Kt)
         
    elif Freq >= 160 and Freq <= 400:
            
        if Lt < 5:
            Kt = 0
        elif Lt > 8:
            Kt = 6
        else:
            Kt = 3
            
        print("Kt = ", Kt)
        
    elif Freq >= 500 and Freq <= 10000:
            
        if Lt < 3:
            Kt = 0
        elif Lt > 5:
            Kt = 6
        else:
            Kt = 3
            
        print("Kt = ", Kt)

    Suma_corregido = Ki + Kf +Kt
    
    if Suma_corregido > 9:
        Suma_corregido = 9

    print("Ki + Kf + Kt = ", Suma_corregido)
    #CALCULAMOS EL NIVEL DE EVALUACIÓN FINAL
    Lkeq = LAeq_corregido + Suma_corregido + 0.5
    Lkeq = round(Lkeq)  # Redondeamos el resultado para poder manejarlo mejor
    print("\nResultado Final:")
    
    if Lkeq < Max_actividad:
        print ("PARA ESTA ACTIVIDAD SI SE CUMPLE EL RD 1367 YA QUE:" )
        print("LKeq =>", Lkeq, " < ", "Max_actividad =>", Max_actividad)
    elif Lkeq == Max_actividad:
        print ("PARA ESTA ACTIVIDAD SI SE CUMPLE EL RD 1367 YA QUE:" )
        print("LKeq =>", Lkeq, " = ", "Max_actividad =>", Max_actividad)        
    else:
        print ("PARA ESTA ACTIVIDAD NO SE CUMPLE EL RD 1367 YA QUE:")
        print("LKeq =>", Lkeq, " > ", "Max_actividad =>", Max_actividad)        
        