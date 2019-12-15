from io import BytesIO
from reportlab.pdfgen import canvas
from bottle import response

def convertHtmlToPdf(pdf):
    response.headers['Content-Type'] = 'application/pdf; charset=UTF-8'
    response.headers['Content-Disposition'] = 'attachment; filename="test.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100,100, pdf)
    p.showPage()
    p.save()
    buffer.close()

    return buffer.getvalue()