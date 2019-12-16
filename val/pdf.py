#importamos BytesIO para la conversion a bytes y string
from io import BytesIO
#importamos Canvas para poder escribir el formato HTML en el pdf
from reportlab.pdfgen import canvas
#importamos response para obtener los parametros headers
from bottle import response

"""
funcion para convertir de html a pdf
recibe un parametro obtenido de app.py
"""
def convertHtmlToPdf(pdf):
    """
    Especificacmos que sera tipo pdf, especificando UTF-8 
    para la escritura
    al igual que el nombre con el que se descargara el pdf
    """
    response.headers['Content-Type'] = 'application/pdf; charset=UTF-8'
    response.headers['Content-Disposition'] = 'attachment; filename="usuario.pdf"'

    #Guardamos a BytesIO dentro de una variable para la obtencion de los parametros
    buffer = BytesIO()
    #utiliamos canvas para preparar el archivo y lo guardamos en una variable
    p = canvas.Canvas(buffer)
    #Escribimos dentro del archivo que sera el pdf
    #especificando x,y como posicion y pdf como los datos que escribira
    p.drawString(100,100, pdf)
    #Guardamos el archivo en formato pdf
    p.save()
    
    #retornamos a buffer, para realizar la descarga.
    return buffer.getvalue()