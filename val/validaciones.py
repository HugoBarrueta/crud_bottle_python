from datetime import datetime

def valida_letras(text):
    if text.isalpha():
        return True
    else:
        return False

def valida_fecha(fecha):
    if datetime.strptime(fecha, '%d/%m/%Y'):
        return True
    else:
        return False