"""
importamos  datetime para poder realizar
la validacion de la fecha de nacimeinto
"""
from datetime import datetime
#importamos re para poder realizar la validacion
#los nombres que se ingresen
import re

"""
Funcion para realizar la validacion de la fecha
requiere de un parametro que es recibido de app,py
"""
def valida_fecha(fecha):
    """
    Valida si la fecha ingresada coincide con el 
    formato especificado
    %d = Day/Dia = dd
    %m = Month/Mes = mm
    %Y = Year/Año = yyyy
    Regresa un parametro True que permite el seguimiento
    de la funcion de  app.py
    """
    if datetime.strptime(fecha, '%d/%m/%Y'):
        return True
    else:
        return False

"""
Funcion para realizar la validacion de los nombres
requiere de un parametro recibido de app.py
"""
def valida_Nombre(text):
    """
    Valida que mientras 'text' no coincida con los 
    parametros especificados en la cadena y no mayor a 25 
    caracteres no podra continuar
    De lo contrario envia un True y continua con el proceso
    """
    while (not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{1,25}", text)):
        return False
    else:
        return True
        