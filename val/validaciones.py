from datetime import datetime
import re

def valida_fecha(fecha):
    if datetime.strptime(fecha, '%d/%m/%Y'):
        return True
    else:
        return False

def valida_Nombre(text):
    while (not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{1,20}", text)):
        return False
    else:
        return True
        